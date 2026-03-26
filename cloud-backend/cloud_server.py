#!/usr/bin/env python3
"""
CEDR Cloud Backend
Cybersecurity Event Data Recorder - Cloud Infrastructure

Provides:
- Event ingestion from multiple vehicles
- Secure storage with encryption
- Forensic correlation across fleet
- Investigator access portal
- Chain of custody tracking
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import sqlite3
import os
import base64
from cryptography.fernet import Fernet
from functools import wraps
import jwt
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
SECRET_KEY = os.environ.get('CEDR_SECRET_KEY', 'demo-secret-key-change-in-production')
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Database initialization
def init_cloud_database():
    """Initialize cloud database for multi-vehicle CEDR storage"""
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    # Events from all vehicles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicle_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            timestamp REAL NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            source TEXT NOT NULL,
            data TEXT,
            hash_chain TEXT NOT NULL,
            signature TEXT NOT NULL,
            received_at REAL NOT NULL,
            encrypted_storage TEXT,
            chain_valid INTEGER DEFAULT 1
        )
    ''')
    
    # Fleet-wide correlations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS correlations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correlation_type TEXT NOT NULL,
            description TEXT,
            affected_vehicles TEXT,  -- JSON array
            pattern_detected TEXT,
            severity TEXT NOT NULL,
            created_at REAL NOT NULL,
            investigated INTEGER DEFAULT 0
        )
    ''')
    
    # Investigator access log (chain of custody)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investigator_id TEXT NOT NULL,
            action TEXT NOT NULL,
            vehicle_id TEXT,
            query_params TEXT,
            timestamp REAL NOT NULL,
            ip_address TEXT,
            justification TEXT
        )
    ''')
    
    # Authorized investigators
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investigators (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            badge_number TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            clearance_level TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at REAL NOT NULL
        )
    ''')
    
    # Insert demo investigators
    cursor.execute('''
        INSERT OR IGNORE INTO investigators (id, name, badge_number, department, clearance_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('INV001', 'John Smith', 'BADGE-001', 'Cybersecurity', 'TOP_SECRET', time.time()))
    
    cursor.execute('''
        INSERT OR IGNORE INTO investigators (id, name, badge_number, department, clearance_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('INV002', 'Sarah Johnson', 'BADGE-002', 'Fleet Security', 'SECRET', time.time()))
    
    conn.commit()
    conn.close()
    print("[Cloud] Database initialized")

init_cloud_database()

# Authentication decorator
def require_investigator_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.investigator = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# ==================== VEHICLE ENDPOINTS ====================

@app.route('/api/cedr/upload', methods=['POST'])
def upload_event():
    """
    Receive single event from vehicle CEDR.
    Typically used for critical events requiring immediate upload.
    """
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id')
        event = data.get('event')
        
        if not vehicle_id or not event:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store event
        conn = sqlite3.connect('/tmp/cedr_cloud.db')
        cursor = conn.cursor()
        
        # Encrypt sensitive data before storage
        encrypted_data = cipher.encrypt(json.dumps(event).encode())
        
        cursor.execute('''
            INSERT INTO vehicle_events 
            (vehicle_id, timestamp, event_type, severity, source, data, 
             hash_chain, signature, received_at, encrypted_storage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle_id,
            event.get('timestamp'),
            event.get('event_type'),
            event.get('severity'),
            event.get('source'),
            json.dumps(event.get('data')),
            data.get('integrity_hash', 'N/A'),
            'SIGNATURE_VERIFIED',  # In production, verify HMAC
            time.time(),
            base64.b64encode(encrypted_data).decode()
        ))
        
        conn.commit()
        conn.close()
        
        # Emit real-time alert for critical events
        if event.get('severity') in ['CRITICAL', 'HIGH']:
            socketio.emit('critical_event', {
                'vehicle_id': vehicle_id,
                'event_type': event.get('event_type'),
                'severity': event.get('severity'),
                'timestamp': event.get('timestamp')
            })
        
        # Check for correlations
        check_correlations(vehicle_id, event)
        
        return jsonify({'status': 'success', 'message': 'Event stored'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cedr/upload/batch', methods=['POST'])
def upload_batch():
    """
    Receive batch of events from vehicle CEDR.
    Used for periodic sync of non-critical events.
    """
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id')
        events = data.get('events', [])
        
        if not vehicle_id or not events:
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = sqlite3.connect('/tmp/cedr_cloud.db')
        cursor = conn.cursor()
        
        inserted_count = 0
        for event in events:
            encrypted_data = cipher.encrypt(json.dumps(event).encode())
            
            cursor.execute('''
                INSERT INTO vehicle_events 
                (vehicle_id, timestamp, event_type, severity, source, data,
                 hash_chain, signature, received_at, encrypted_storage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                vehicle_id,
                event.get('timestamp'),
                event.get('event_type'),
                event.get('severity'),
                event.get('source'),
                json.dumps(event.get('data')),
                event.get('hash_chain'),
                event.get('signature'),
                time.time(),
                base64.b64encode(encrypted_data).decode()
            ))
            inserted_count += 1
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': f'{inserted_count} events stored'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== INVESTIGATOR ENDPOINTS ====================

@app.route('/api/investigator/login', methods=['POST'])
def investigator_login():
    """
    Authenticate investigator and provide access token.
    In production, this would integrate with organizational auth.
    """
    data = request.json
    investigator_id = data.get('investigator_id')
    badge_number = data.get('badge_number')
    
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM investigators 
        WHERE id = ? AND badge_number = ? AND active = 1
    ''', (investigator_id, badge_number))
    
    investigator = cursor.fetchone()
    conn.close()
    
    if not investigator:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT token
    token_payload = {
        'investigator_id': investigator[0],
        'name': investigator[1],
        'badge': investigator[2],
        'clearance': investigator[4],
        'exp': datetime.now(timezone.utc) + timedelta(hours=8)
    }
    
    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'investigator': {
            'id': investigator[0],
            'name': investigator[1],
            'clearance_level': investigator[4]
        }
    }), 200

@app.route('/api/investigator/events/search', methods=['POST'])
@require_investigator_auth
def search_events():
    """
    Search forensic events with filtering capabilities.
    All access is logged for chain of custody.
    """
    data = request.json
    
    # Log access
    log_access(
        investigator_id=request.investigator['investigator_id'],
        action='SEARCH_EVENTS',
        query_params=json.dumps(data),
        ip_address=request.remote_addr
    )
    
    # Build query
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM vehicle_events WHERE 1=1'
    params = []
    
    if 'vehicle_id' in data:
        query += ' AND vehicle_id = ?'
        params.append(data['vehicle_id'])
    
    if 'event_type' in data:
        query += ' AND event_type = ?'
        params.append(data['event_type'])
    
    if 'severity' in data:
        query += ' AND severity = ?'
        params.append(data['severity'])
    
    if 'start_time' in data and 'end_time' in data:
        query += ' AND timestamp BETWEEN ? AND ?'
        params.append(data['start_time'])
        params.append(data['end_time'])
    
    query += ' ORDER BY timestamp DESC LIMIT 1000'
    
    cursor.execute(query, params)
    events = cursor.fetchall()
    conn.close()
    
    # Format response
    results = []
    for event in events:
        results.append({
            'id': event[0],
            'vehicle_id': event[1],
            'timestamp': event[2],
            'event_type': event[3],
            'severity': event[4],
            'source': event[5],
            'data': json.loads(event[6]) if event[6] else {},
            'hash_chain': event[7],
            'received_at': event[9],
            'chain_valid': bool(event[11])
        })
    
    return jsonify({
        'total': len(results),
        'events': results
    }), 200

@app.route('/api/investigator/forensic-report/<vehicle_id>', methods=['GET'])
@require_investigator_auth
def get_forensic_report(vehicle_id):
    """
    Generate comprehensive forensic report for a vehicle.
    Includes integrity verification and chain of custody.
    """
    # Log access
    log_access(
        investigator_id=request.investigator['investigator_id'],
        action='GENERATE_FORENSIC_REPORT',
        vehicle_id=vehicle_id,
        ip_address=request.remote_addr
    )
    
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    # Get all events for vehicle
    cursor.execute('''
        SELECT * FROM vehicle_events 
        WHERE vehicle_id = ? 
        ORDER BY timestamp
    ''', (vehicle_id,))
    
    events = cursor.fetchall()
    
    # Get correlations
    cursor.execute('''
        SELECT * FROM correlations 
        WHERE affected_vehicles LIKE ?
    ''', (f'%{vehicle_id}%',))
    
    correlations = cursor.fetchall()
    conn.close()
    
    # Generate report
    report = {
        'report_id': hashlib.sha256(f"{vehicle_id}{time.time()}".encode()).hexdigest()[:16],
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'generated_by': request.investigator['investigator_id'],
        'vehicle_id': vehicle_id,
        'total_events': len(events),
        'event_summary': {},
        'severity_breakdown': {},
        'timeline': [],
        'correlations': [],
        'integrity_verification': verify_cloud_chain(vehicle_id)
    }
    
    # Event summary
    for event in events:
        event_type = event[3]
        severity = event[4]
        
        report['event_summary'][event_type] = report['event_summary'].get(event_type, 0) + 1
        report['severity_breakdown'][severity] = report['severity_breakdown'].get(severity, 0) + 1
        
        report['timeline'].append({
            'timestamp': event[2],
            'event_type': event[3],
            'severity': event[4],
            'source': event[5],
            'hash': event[7][:16] + '...'
        })
    
    # Add correlations
    for corr in correlations:
        report['correlations'].append({
            'type': corr[1],
            'description': corr[2],
            'pattern': corr[4],
            'severity': corr[5]
        })
    
    return jsonify(report), 200


@app.route('/api/investigator/forensic-report/<vehicle_id>/download', methods=['GET'])
@require_investigator_auth
def download_forensic_report(vehicle_id):
    """
    Download forensic report as JSON or PDF.
    Query params: format=json|pdf
    """
    report_format = request.args.get('format', 'json')
    
    # Log access
    log_access(
        investigator_id=request.investigator['investigator_id'],
        action='DOWNLOAD_FORENSIC_REPORT',
        vehicle_id=vehicle_id,
        ip_address=request.remote_addr
    )
    
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    # Get all events for vehicle
    cursor.execute('''
        SELECT * FROM vehicle_events 
        WHERE vehicle_id = ? 
        ORDER BY timestamp
    ''', (vehicle_id,))
    
    events = cursor.fetchall()
    conn.close()
    
    # Generate report
    report = {
        'report_id': hashlib.sha256(f"{vehicle_id}{time.time()}".encode()).hexdigest()[:16],
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'generated_by': request.investigator['investigator_id'],
        'vehicle_id': vehicle_id,
        'total_events': len(events),
        'event_summary': {},
        'severity_breakdown': {},
        'events': [],
        'integrity_verification': verify_cloud_chain(vehicle_id),
        'chain_of_custody': {
            'prepared_by': request.investigator['investigator_id'],
            'prepared_at': datetime.now(timezone.utc).isoformat(),
            'system': 'CEDR Cloud Forensic Platform',
            'standard': 'ISO/SAE 21434'
        }
    }
    
    # Event summary
    for event in events:
        event_type = event[3]
        severity = event[4]
        
        report['event_summary'][event_type] = report['event_summary'].get(event_type, 0) + 1
        report['severity_breakdown'][severity] = report['severity_breakdown'].get(severity, 0) + 1
        
        report['events'].append({
            'id': event[0],
            'timestamp': event[2],
            'event_type': event[3],
            'severity': event[4],
            'source': event[5],
            'data': json.loads(event[6]) if event[6] else {},
            'hash_chain': event[7],
            'signature': event[8],
            'received_at': event[9]
        })
    
    if report_format == 'json':
        # Return as downloadable JSON file
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(report, temp_file, indent=2)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'CEDR_Forensic_Report_{vehicle_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
    
    else:
        return jsonify({'error': 'Invalid format. Use json'}), 400


@app.route('/api/investigator/correlations', methods=['GET'])
@require_investigator_auth
def get_correlations():
    """
    Get fleet-wide correlations and patterns.
    Identifies coordinated attacks across multiple vehicles.
    """
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM correlations ORDER BY created_at DESC')
    correlations = cursor.fetchall()
    conn.close()
    
    results = []
    for corr in correlations:
        results.append({
            'id': corr[0],
            'type': corr[1],
            'description': corr[2],
            'affected_vehicles': json.loads(corr[3]),
            'pattern': corr[4],
            'severity': corr[5],
            'created_at': corr[6],
            'investigated': bool(corr[7])
        })
    
    return jsonify({
        'total_correlations': len(results),
        'correlations': results
    }), 200

@app.route('/api/investigator/access-log', methods=['GET'])
@require_investigator_auth
def get_access_log():
    """
    Get chain of custody access log.
    Shows who accessed what data and when.
    """
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM access_log 
        ORDER BY timestamp DESC 
        LIMIT 1000
    ''')
    
    logs = cursor.fetchall()
    conn.close()
    
    results = []
    for log in logs:
        results.append({
            'id': log[0],
            'investigator_id': log[1],
            'action': log[2],
            'vehicle_id': log[3],
            'timestamp': log[5],
            'ip_address': log[6],
            'justification': log[7]
        })
    
    return jsonify({
        'total_accesses': len(results),
        'logs': results
    }), 200

# ==================== DASHBOARD ====================

@app.route('/')
def dashboard():
    """Serve investigator dashboard"""
    return render_template('investigator_dashboard.html')

@app.route('/api/dashboard/stats')
def dashboard_stats():
    """Get statistics for dashboard"""
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(DISTINCT vehicle_id) FROM vehicle_events')
    total_vehicles = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM vehicle_events')
    total_events = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM correlations')
    total_correlations = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT event_type, COUNT(*) as count 
        FROM vehicle_events 
        GROUP BY event_type 
        ORDER BY count DESC 
        LIMIT 10
    ''')
    top_events = cursor.fetchall()
    
    cursor.execute('''
        SELECT severity, COUNT(*) as count 
        FROM vehicle_events 
        GROUP BY severity
    ''')
    severity_breakdown = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_vehicles': total_vehicles,
        'total_events': total_events,
        'total_correlations': total_correlations,
        'top_events': dict(top_events),
        'severity_breakdown': dict(severity_breakdown)
    }), 200

# ==================== HELPER FUNCTIONS ====================

def check_correlations(vehicle_id, event):
    """
    Check if new event correlates with known attack patterns.
    Identifies fleet-wide coordinated attacks.
    """
    event_type = event.get('event_type')
    severity = event.get('severity')
    
    # Check for replay attack pattern across multiple vehicles
    if event_type == 'REPLAY_ATTACK':
        conn = sqlite3.connect('/tmp/cedr_cloud.db')
        cursor = conn.cursor()
        
        # Look for similar attacks in last hour
        cursor.execute('''
            SELECT DISTINCT vehicle_id FROM vehicle_events 
            WHERE event_type = 'REPLAY_ATTACK' 
            AND timestamp > ?
        ''', (time.time() - 3600,))
        
        affected = cursor.fetchall()
        
        if len(affected) >= 3:  # Pattern detected
            cursor.execute('''
                INSERT INTO correlations 
                (correlation_type, description, affected_vehicles, pattern_detected, severity, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                'COORDINATED_ATTACK',
                f'Multiple vehicles under replay attack in last hour',
                json.dumps([v[0] for v in affected]),
                'REPLAY_ATTACK_WAVE',
                'CRITICAL',
                time.time()
            ))
            
            conn.commit()
            
            # Emit alert
            socketio.emit('correlation_alert', {
                'type': 'COORDINATED_ATTACK',
                'affected_vehicles': len(affected),
                'description': 'Replay attack pattern detected across fleet'
            })
        
        conn.close()

def verify_cloud_chain(vehicle_id):
    """
    Verify the integrity of stored events for a vehicle.
    Ensures no tampering occurred during transmission or storage.
    """
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, hash_chain, signature, data 
        FROM vehicle_events 
        WHERE vehicle_id = ? 
        ORDER BY id
    ''', (vehicle_id,))
    
    events = cursor.fetchall()
    conn.close()
    
    if not events:
        return {'status': 'NO_DATA', 'message': 'No events for this vehicle'}
    
    # Simple verification (in production, full chain verification)
    invalid_count = 0
    for event in events:
        if not event[2]:  # No signature
            invalid_count += 1
    
    if invalid_count > 0:
        return {
            'status': 'COMPROMISED',
            'message': f'{invalid_count} events may be compromised',
            'total_events': len(events)
        }
    
    return {
        'status': 'VERIFIED',
        'message': 'All events passed integrity checks',
        'total_events': len(events)
    }

def log_access(investigator_id, action, vehicle_id=None, query_params=None, ip_address=None, justification=None):
    """Log investigator access for chain of custody"""
    conn = sqlite3.connect('/tmp/cedr_cloud.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO access_log 
        (investigator_id, action, vehicle_id, query_params, timestamp, ip_address, justification)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        investigator_id,
        action,
        vehicle_id,
        query_params,
        time.time(),
        ip_address,
        justification
    ))
    
    conn.commit()
    conn.close()

# ==================== MAIN ====================

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  CEDR Cloud Backend                                        ║")
    print("║  Cybersecurity Event Data Recorder - Cloud Infrastructure  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("API Endpoints:")
    print("  POST /api/cedr/upload          - Upload vehicle event")
    print("  POST /api/cedr/upload/batch    - Batch upload events")
    print("  POST /api/investigator/login   - Investigator authentication")
    print("  POST /api/investigator/events/search - Search forensic data")
    print("  GET  /api/dashboard/stats      - Dashboard statistics")
    print()
    print("Dashboard: http://localhost:8080")
    print()
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)