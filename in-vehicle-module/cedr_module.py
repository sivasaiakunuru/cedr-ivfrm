#!/usr/bin/env python3
"""
Cybersecurity Event Data Recorder (CEDR)
In-Vehicle Forensic Readiness Module (IV-FRM)

This module runs inside the vehicle (IVI or gateway ECU) and provides:
- Selective logging of security-relevant events
- Tamper-evident logging using blockchain-style hashing
- Secure encrypted storage
- Event-triggered transmission to cloud
- Local forensic access interface
"""

import os
import json
import hashlib
import hmac
import time
import threading
import sqlite3
import requests
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import queue
import logging

# Import new modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from capture.packet_capture import PacketCapture
    PACKET_CAPTURE_AVAILABLE = True
except ImportError:
    PACKET_CAPTURE_AVAILABLE = False

try:
    from v2x.v2x_security import V2XSecurityModule
    V2X_AVAILABLE = True
except ImportError:
    V2X_AVAILABLE = False

try:
    from location.geolocation import GeolocationTracker
    GEOLOCATION_AVAILABLE = True
except ImportError:
    GEOLOCATION_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CEDR')

class CEDRModule:
    """
    Cybersecurity Event Data Recorder Module
    """
    
    def __init__(self, vehicle_id, cloud_endpoint=None):
        self.vehicle_id = vehicle_id
        self.cloud_endpoint = cloud_endpoint or "http://localhost:8080/api/cedr/upload"
        
        # Security keys (in production, these come from HSM/TPM)
        self.master_key = self._derive_key(vehicle_id)
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Database for local storage
        self.db_path = f"/tmp/cedr_{vehicle_id}.db"
        self._init_database()
        
        # Event queue for async processing
        self.event_queue = queue.Queue()
        
        # Chain hash for tamper evidence (like blockchain)
        self.previous_hash = self._load_last_hash()
        
        # Initialize optional modules
        self.packet_capture = None
        self.v2x_module = None
        self.geolocation = None
        
        if PACKET_CAPTURE_AVAILABLE:
            try:
                self.packet_capture = PacketCapture(vehicle_id)
                logger.info("Packet capture module initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize packet capture: {e}")
        
        if V2X_AVAILABLE:
            try:
                self.v2x_module = V2XSecurityModule(vehicle_id)
                logger.info("V2X security module initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize V2X module: {e}")
        
        if GEOLOCATION_AVAILABLE:
            try:
                self.geolocation = GeolocationTracker(vehicle_id)
                logger.info("Geolocation tracker initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize geolocation: {e}")
        
        # Configuration
        self.config = {
            'log_levels': ['CRITICAL', 'HIGH', 'MEDIUM'],
            'storage_limit_mb': 500,
            'retention_days': 30,
            'trigger_events': [
                'INTRUSION_DETECTED',
                'UNAUTHORIZED_ACCESS',
                'MALWARE_DETECTED',
                'ANOMALY_HIGH',
                'REPLAY_ATTACK',
                'BUS_OVERFLOW'
            ],
            'batch_size': 10,
            'upload_interval': 300,  # 5 minutes
            'packet_capture_enabled': PACKET_CAPTURE_AVAILABLE,
            'v2x_enabled': V2X_AVAILABLE,
            'geolocation_enabled': GEOLOCATION_AVAILABLE
        }
        
        # Event counters for statistics
        self.stats = {
            'events_logged': 0,
            'events_uploaded': 0,
            'storage_used_bytes': 0
        }
        
        # Start background threads
        self.running = True
        self._start_worker_threads()
        
        logger.info(f"CEDR Module initialized for vehicle {vehicle_id}")
    
    def _derive_key(self, vehicle_id):
        """Derive cryptographic key from vehicle ID"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'cedr_salt_' + vehicle_id.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(vehicle_id.encode()))
        return key
    
    def _init_database(self):
        """Initialize SQLite database for forensic logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main event log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                source TEXT NOT NULL,
                data TEXT,
                hash_chain TEXT NOT NULL,
                signature TEXT NOT NULL,
                uploaded INTEGER DEFAULT 0
            )
        ''')
        
        # Chain integrity table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chain_integrity (
                id INTEGER PRIMARY KEY,
                last_hash TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        ''')
        
        # Tamper detection log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tamper_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                alert_type TEXT NOT NULL,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def _load_last_hash(self):
        """Load the last hash from chain for continuity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT last_hash FROM chain_integrity ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        # Genesis hash
        return hashlib.sha256(b'CEDR_GENESIS_' + self.vehicle_id.encode()).hexdigest()
    
    def _calculate_hash(self, event_data):
        """
        Calculate chain hash for tamper evidence.
        Each event hash includes the previous hash (blockchain-style).
        """
        data_string = json.dumps(event_data, sort_keys=True)
        # Use the event's timestamp (when it was created) for consistent hashing
        combined = self.previous_hash + data_string + str(event_data.get('timestamp', time.time()))
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _sign_event(self, event_data, event_hash):
        """Create HMAC signature for event authenticity"""
        message = f"{self.vehicle_id}:{event_hash}:{json.dumps(event_data, sort_keys=True)}"
        return hmac.new(self.master_key, message.encode(), hashlib.sha256).hexdigest()
    
    def log_event(self, event_type, severity, source, data=None):
        """
        Log a security event with tamper-evident properties.
        
        Args:
            event_type: Type of security event
            severity: CRITICAL, HIGH, MEDIUM, LOW
            source: ECU or subsystem that generated the event
            data: Additional event data (dict)
        """
        # Filter by configured log levels
        if severity not in self.config['log_levels']:
            return False
        
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'severity': severity,
            'source': source,
            'data': json.dumps(data) if data else '{}',
            'vehicle_id': self.vehicle_id
        }
        
        # Add to queue for async processing
        self.event_queue.put(event)
        
        # Check if immediate upload trigger
        if event_type in self.config['trigger_events'] and severity in ['CRITICAL', 'HIGH']:
            self._trigger_immediate_upload(event)
        
        return True
    
    def _process_event(self, event):
        """Process and store event with tamper protection"""
        try:
            # Calculate chain hash
            event_hash = self._calculate_hash(event)
            
            # Sign event
            signature = self._sign_event(event, event_hash)
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_events 
                (timestamp, event_type, severity, source, data, hash_chain, signature)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event['timestamp'],
                event['event_type'],
                event['severity'],
                event['source'],
                event['data'],
                event_hash,
                signature
            ))
            
            # Update chain integrity
            cursor.execute('''
                INSERT OR REPLACE INTO chain_integrity (id, last_hash, timestamp)
                VALUES (1, ?, ?)
            ''', (event_hash, time.time()))
            
            conn.commit()
            conn.close()
            
            # Update previous hash for next event
            self.previous_hash = event_hash
            
            # Update stats
            self.stats['events_logged'] += 1
            
            logger.info(f"Event logged: {event['event_type']} - {event['severity']}")
            
        except Exception as e:
            logger.error(f"Error processing event: {e}")
    
    def _trigger_immediate_upload(self, event):
        """Trigger immediate cloud upload for critical events"""
        logger.warning(f"CRITICAL EVENT - Triggering immediate upload: {event['event_type']}")
        
        # Start upload thread
        upload_thread = threading.Thread(
            target=self._upload_event,
            args=(event,)
        )
        upload_thread.start()
    
    def _upload_event(self, event):
        """Upload event to cloud backend"""
        try:
            payload = {
                'vehicle_id': self.vehicle_id,
                'event': event,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'integrity_hash': self._calculate_hash(event)
            }
            
            response = requests.post(
                self.cloud_endpoint,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Event uploaded successfully")
                self.stats['events_uploaded'] += 1
            else:
                logger.error(f"Upload failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Upload error: {e}")
    
    def _batch_upload(self):
        """Batch upload non-critical events"""
        while self.running:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Get non-uploaded events
                cursor.execute('''
                    SELECT * FROM security_events 
                    WHERE uploaded = 0 AND severity IN ('MEDIUM', 'LOW')
                    LIMIT ?
                ''', (self.config['batch_size'],))
                
                events = cursor.fetchall()
                
                if events:
                    # Upload batch
                    batch = []
                    event_ids = []
                    
                    for event in events:
                        event_ids.append(event[0])
                        batch.append({
                            'id': event[0],
                            'timestamp': event[1],
                            'event_type': event[2],
                            'severity': event[3],
                            'source': event[4],
                            'data': event[5],
                            'hash_chain': event[6],
                            'signature': event[7]
                        })
                    
                    try:
                        response = requests.post(
                            self.cloud_endpoint + '/batch',
                            json={
                                'vehicle_id': self.vehicle_id,
                                'events': batch
                            },
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            # Mark as uploaded
                            cursor.executemany(
                                'UPDATE security_events SET uploaded = 1 WHERE id = ?',
                                [(id,) for id in event_ids]
                            )
                            conn.commit()
                            logger.info(f"Batch uploaded: {len(batch)} events")
                            
                    except Exception as e:
                        logger.error(f"Batch upload error: {e}")
                
                conn.close()
                
            except Exception as e:
                logger.error(f"Batch upload thread error: {e}")
            
            time.sleep(self.config['upload_interval'])
    
    def _worker_thread(self):
        """Background worker to process event queue"""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                self._process_event(event)
                self.event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")
    
    def _start_worker_threads(self):
        """Start background processing threads"""
        # Event processing thread
        worker = threading.Thread(target=self._worker_thread, daemon=True)
        worker.start()
        
        # Batch upload thread
        uploader = threading.Thread(target=self._batch_upload, daemon=True)
        uploader.start()
        
        logger.info("Worker threads started")
    
    def verify_integrity(self):
        """
        Verify the integrity of the forensic log chain.
        Detects any tampering with stored events.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM security_events ORDER BY id')
        events = cursor.fetchall()
        conn.close()
        
        if not events:
            return True, "No events to verify"
        
        # Verify chain
        previous_hash = hashlib.sha256(b'CEDR_GENESIS_' + self.vehicle_id.encode()).hexdigest()
        tampered_events = []
        
        for event in events:
            event_id, timestamp, event_type, severity, source, data, hash_chain, signature, uploaded = event
            
            # Recalculate expected hash (must match original calculation)
            event_data = {
                'timestamp': timestamp,
                'event_type': event_type,
                'severity': severity,
                'source': source,
                'data': json.loads(data) if data else {},  # Parse stored JSON
                'vehicle_id': self.vehicle_id
            }
            
            data_string = json.dumps(event_data, sort_keys=True)
            expected_combined = previous_hash + data_string + str(timestamp)
            expected_hash = hashlib.sha256(expected_combined.encode()).hexdigest()
            
            # Verify hash
            if expected_hash != hash_chain:
                tampered_events.append({
                    'id': event_id,
                    'expected_hash': expected_hash,
                    'stored_hash': hash_chain
                })
            
            # Verify signature
            message = f"{self.vehicle_id}:{hash_chain}:{json.dumps(event_data, sort_keys=True)}"
            expected_sig = hmac.new(self.master_key, message.encode(), hashlib.sha256).hexdigest()
            
            if expected_sig != signature:
                tampered_events.append({
                    'id': event_id,
                    'error': 'Invalid signature'
                })
            
            previous_hash = hash_chain
        
        if tampered_events:
            # Log tamper alert
            self._log_tamper_alert(tampered_events)
            return False, f"Tampering detected in {len(tampered_events)} events"
        
        return True, "All events verified - chain integrity intact"
    
    def _log_tamper_alert(self, tampered_events):
        """Log tampering detection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tamper_alerts (timestamp, alert_type, details)
            VALUES (?, ?, ?)
        ''', (
            time.time(),
            'CHAIN_TAMPERING',
            json.dumps(tampered_events)
        ))
        
        conn.commit()
        conn.close()
        
        logger.critical(f"TAMPERING DETECTED: {len(tampered_events)} events compromised!")
    
    def get_forensic_report(self, start_time=None, end_time=None):
        """
        Generate forensic report for investigators.
        Provides tamper-evident export of security events.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if start_time and end_time:
            cursor.execute('''
                SELECT * FROM security_events 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp
            ''', (start_time, end_time))
        else:
            cursor.execute('SELECT * FROM security_events ORDER BY timestamp')
        
        events = cursor.fetchall()
        conn.close()
        
        # Generate report with integrity proof
        report = {
            'report_id': hashlib.sha256(f"{self.vehicle_id}{time.time()}".encode()).hexdigest()[:16],
            'vehicle_id': self.vehicle_id,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'total_events': len(events),
            'integrity_status': self.verify_integrity(),
            'events': [],
            'report_hash': None
        }
        
        event_summary = {}
        severity_breakdown = {}
        
        for event in events:
            event_type = event[2]
            severity = event[3]
            
            event_summary[event_type] = event_summary.get(event_type, 0) + 1
            severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1
            
            report['events'].append({
                'id': event[0],
                'timestamp': event[1],
                'event_type': event[2],
                'severity': event[3],
                'source': event[4],
                'data': json.loads(event[5]),
                'hash_chain': event[6],
                'signature': event[7],
                'uploaded': bool(event[8])
            })
        
        report['event_summary'] = event_summary
        report['severity_breakdown'] = severity_breakdown
        
        # Sign the entire report
        report_string = json.dumps(report['events'], sort_keys=True)
        report['report_hash'] = hmac.new(
            self.master_key, 
            report_string.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        return report
    
    def get_statistics(self):
        """Get CEDR operational statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM security_events')
        total_events = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM security_events WHERE uploaded = 1')
        uploaded_events = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tamper_alerts')
        tamper_alerts = cursor.fetchone()[0]
        
        cursor.execute('SELECT event_type, COUNT(*) FROM security_events GROUP BY event_type')
        event_types = cursor.fetchall()
        
        conn.close()
        
        return {
            'vehicle_id': self.vehicle_id,
            'total_events': total_events,
            'uploaded_events': uploaded_events,
            'pending_upload': total_events - uploaded_events,
            'tamper_alerts': tamper_alerts,
            'event_breakdown': dict(event_types),
            'storage_path': self.db_path,
            'config': self.config
        }
    
    def shutdown(self):
        """Graceful shutdown of CEDR module"""
        logger.info("Shutting down CEDR module...")
        self.running = False
        
        # Process remaining events
        self.event_queue.join()
        
        logger.info("CEDR module shutdown complete")

# Example usage and simulation
if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Cybersecurity Event Data Recorder (CEDR)                  ║")
    print("║  In-Vehicle Forensic Readiness Module (IV-FRM)            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize CEDR for a vehicle
    cedr = CEDRModule(vehicle_id="VEH-DEMO-001")
    
    # Simulate various security events
    print("[1] Simulating normal security events...")
    cedr.log_event("IGNITION_ON", "LOW", "ECU-ENGINE", {"driver_id": "DRV001"})
    time.sleep(0.5)
    
    cedr.log_event("CAN_BUS_ACTIVITY", "MEDIUM", "GATEWAY", {"message_count": 1500})
    time.sleep(0.5)
    
    print("[2] Simulating attack detection events...")
    # Critical event - should trigger immediate upload
    cedr.log_event(
        "INTRUSION_DETECTED", 
        "CRITICAL", 
        "IDS-GATEWAY",
        {
            "attack_type": "REPLAY_ATTACK",
            "source_id": "0x123",
            "target": "BRAKE_CONTROL",
            "details": "Suspicious message sequence detected"
        }
    )
    time.sleep(0.5)
    
    cedr.log_event(
        "ANOMALY_HIGH",
        "HIGH",
        "MONITORING",
        {
            "anomaly_type": "SPEED_VIOLATION",
            "value": 145,
            "threshold": 120
        }
    )
    time.sleep(0.5)
    
    cedr.log_event("UNAUTHORIZED_ACCESS", "HIGH", "TELEMATICS", {"attempted_service": "DIAGNOSTIC"})
    time.sleep(0.5)
    
    print("[3] Generating forensic report...")
    report = cedr.get_forensic_report()
    print(f"    Total events: {report['total_events']}")
    print(f"    Integrity status: {report['integrity_status'][1]}")
    print(f"    Report hash: {report['report_hash'][:16]}...")
    
    print()
    print("[4] Verifying chain integrity...")
    integrity_ok, message = cedr.verify_integrity()
    print(f"    {message}")
    
    print()
    print("[5] Statistics:")
    stats = cedr.get_statistics()
    print(f"    Vehicle: {stats['vehicle_id']}")
    print(f"    Events logged: {stats['total_events']}")
    print(f"    Events uploaded: {stats['uploaded_events']}")
    print(f"    Pending upload: {stats['pending_upload']}")
    
    print()
    print("[6] Event breakdown:")
    for event_type, count in stats['event_breakdown'].items():
        print(f"    - {event_type}: {count}")
    
    print()
    print("=" * 60)
    print("CEDR/IV-FRM Demo Complete")
    print("=" * 60)
    
    # Keep running for a bit to show async processing
    print("\n[*] Running for 3 seconds to process queued events...")
    time.sleep(3)
    
    cedr.shutdown()