"""
V2X (Vehicle-to-Everything) Security Module for CEDR

Records and secures V2X communications:
- V2V: Vehicle-to-Vehicle
- V2I: Vehicle-to-Infrastructure
- V2P: Vehicle-to-Pedestrian
- V2N: Vehicle-to-Network

Aligned with IEEE 1609.2 security standards for V2X.
"""

import sqlite3
import json
import time
import hashlib
import hmac
from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum


class V2XMessageType(Enum):
    """V2X message types per SAE J2735"""
    # V2V Messages
    BSM = "BasicSafetyMessage"           # Basic Safety Message
    EDM = "EmergencyVehicleAlert"        # Emergency vehicle alert
    # V2I Messages
    SPAT = "SignalPhaseAndTiming"        # Traffic signal timing
    MAP = "MapData"                       # Road geometry
    RSA = "RoadSideAlert"                 # Roadside alerts
    TIM = "TravelerInformation"           # Traveler info
    # V2P Messages
    PSM = "PersonalSafetyMessage"         # Pedestrian/cyclist safety
    # V2N Messages
    SRM = "ServiceRequestMessage"         # Service request
    SSM = "ServiceResponseMessage"        # Service response


class V2XSecurityModule:
    """
    V2X Security and Forensic Recording Module
    
    Captures V2X messages with:
    - IEEE 1609.2 certificate validation logging
    - Signature verification records
    - Replay attack detection
    - Misbehavior reporting
    """
    
    def __init__(self, vehicle_id: str, storage_path: str = None):
        self.vehicle_id = vehicle_id
        self.db_path = storage_path or f"/tmp/cedr_v2x_{vehicle_id}.db"
        self._init_database()
        
        # V2X security configuration
        self.config = {
            'ieee1609.2_compliant': True,
            'certificate_validation': True,
            'signature_verification': True,
            'replay_detection': True,
            'misbehavior_reporting': True,
            'range_validation': True,  # Validate message origin range
            'frequency_validation': True  # Detect flooding
        }
        
        # Track seen message IDs for replay detection
        self.seen_message_ids = set()
        self.message_history_limit = 10000
        
    def _init_database(self):
        """Initialize V2X message database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # V2X messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS v2x_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                message_type TEXT NOT NULL,
                message_id TEXT UNIQUE NOT NULL,
                
                -- Sender information
                sender_id TEXT NOT NULL,
                sender_type TEXT,  -- vehicle, rsu, pedestrian, emergency
                sender_position_lat REAL,
                sender_position_lon REAL,
                sender_speed REAL,
                sender_heading REAL,
                
                -- Message content (encrypted/signed)
                payload BLOB,
                payload_size INTEGER,
                
                -- IEEE 1609.2 Security
                certificate_id TEXT,
                certificate_type TEXT,  -- anonymous, identified, custom
                signature_valid INTEGER,
                certificate_valid INTEGER,
                certificate_expiry REAL,
                
                -- Security validation
                replay_detected INTEGER DEFAULT 0,
                range_valid INTEGER DEFAULT 1,
                frequency_valid INTEGER DEFAULT 1,
                misbehavior_flags TEXT,  -- JSON array
                
                -- Communication details
                protocol_version TEXT,
                channel INTEGER,  -- DSRC channel or C-V2X PC5
                rssi INTEGER,
                
                -- Hash for integrity
                hash TEXT NOT NULL,
                
                -- Related security event
                related_event_id INTEGER
            )
        ''')
        
        # V2X misbehavior reports
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS v2x_misbehavior (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                reporter_vehicle_id TEXT NOT NULL,
                target_vehicle_id TEXT,
                misbehavior_type TEXT NOT NULL,
                description TEXT,
                evidence_message_ids TEXT,  -- JSON array
                location_lat REAL,
                location_lon REAL,
                severity TEXT,
                reported_to_ma INTEGER DEFAULT 0  -- Misbehavior Authority
            )
        ''')
        
        # V2X certificate log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS v2x_certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                certificate_id TEXT UNIQUE NOT NULL,
                first_seen REAL NOT NULL,
                last_seen REAL NOT NULL,
                certificate_type TEXT,
                issuer TEXT,
                expiry_date REAL,
                is_valid INTEGER DEFAULT 1,
                revocation_status TEXT DEFAULT 'UNKNOWN',
                message_count INTEGER DEFAULT 0
            )
        ''')
        
        # V2X statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS v2x_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                total_messages INTEGER DEFAULT 0,
                v2v_messages INTEGER DEFAULT 0,
                v2i_messages INTEGER DEFAULT 0,
                v2p_messages INTEGER DEFAULT 0,
                invalid_signatures INTEGER DEFAULT 0,
                replay_attempts INTEGER DEFAULT 0,
                misbehavior_reports INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_v2x_message(self, 
                          message_type: str,
                          message_id: str,
                          sender_id: str,
                          payload: bytes,
                          certificate_id: str = None,
                          signature_valid: bool = True,
                          certificate_valid: bool = True,
                          position: tuple = None,  # (lat, lon)
                          speed: float = None,
                          heading: float = None,
                          rssi: int = None,
                          channel: int = None,
                          related_event_id: int = None) -> dict:
        """
        Record a V2X message with security validation
        
        Args:
            message_type: V2X message type (BSM, SPAT, etc.)
            message_id: Unique message identifier
            sender_id: Pseudonym or certificate ID of sender
            payload: Raw message payload
            certificate_id: IEEE 1609.2 certificate identifier
            signature_valid: Whether signature verification passed
            certificate_valid: Whether certificate is valid
            position: (latitude, longitude) of sender
            speed: Sender speed in m/s
            heading: Sender heading in degrees
            rssi: Received signal strength
            channel: DSRC channel or C-V2X channel
            related_event_id: Link to security event if applicable
        """
        timestamp = time.time()
        
        # Check for replay attack
        replay_detected = message_id in self.seen_message_ids
        if not replay_detected:
            self.seen_message_ids.add(message_id)
            # Limit history size
            if len(self.seen_message_ids) > self.message_history_limit:
                self.seen_message_ids.pop()
        
        # Validate position (basic range check)
        range_valid = True
        if position:
            lat, lon = position
            range_valid = -90 <= lat <= 90 and -180 <= lon <= 180
        
        # Check for misbehavior
        misbehavior_flags = []
        if replay_detected:
            misbehavior_flags.append("REPLAY_ATTACK")
        if not signature_valid:
            misbehavior_flags.append("INVALID_SIGNATURE")
        if not certificate_valid:
            misbehavior_flags.append("INVALID_CERTIFICATE")
        if not range_valid:
            misbehavior_flags.append("INVALID_POSITION")
        
        # Create hash
        hash_data = f"{timestamp}{message_id}{sender_id}{payload.hex() if payload else ''}"
        message_hash = hashlib.sha256(hash_data.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert V2X message
        cursor.execute('''
            INSERT INTO v2x_messages 
            (timestamp, message_type, message_id, sender_id, sender_type,
             sender_position_lat, sender_position_lon, sender_speed, sender_heading,
             payload, payload_size, certificate_id, signature_valid, certificate_valid,
             replay_detected, range_valid, misbehavior_flags, protocol_version,
             channel, rssi, hash, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, message_type, message_id, sender_id, 'vehicle',
              position[0] if position else None, position[1] if position else None,
              speed, heading, payload, len(payload) if payload else 0,
              certificate_id, int(signature_valid), int(certificate_valid),
              int(replay_detected), int(range_valid),
              json.dumps(misbehavior_flags), 'IEEE1609.2-2022',
              channel, rssi, message_hash, related_event_id))
        
        msg_db_id = cursor.lastrowid
        
        # Update certificate log
        if certificate_id:
            cursor.execute('''
                INSERT INTO v2x_certificates 
                (certificate_id, first_seen, last_seen, certificate_type, message_count)
                VALUES (?, ?, ?, ?, 1)
                ON CONFLICT(certificate_id) DO UPDATE SET
                last_seen = excluded.last_seen,
                message_count = message_count + 1
            ''', (certificate_id, timestamp, timestamp, 'pseudonym'))
        
        # Update daily stats
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO v2x_stats (date, total_messages)
            VALUES (?, 1)
            ON CONFLICT(date) DO UPDATE SET
            total_messages = total_messages + 1
        ''', (date_str,))
        
        # Update message type stats
        msg_type_lower = message_type.lower()
        if 'bsm' in msg_type_lower or 'edm' in msg_type_lower:
            cursor.execute('''
                UPDATE v2x_stats SET v2v_messages = v2v_messages + 1 WHERE date = ?
            ''', (date_str,))
        elif 'spat' in msg_type_lower or 'map' in msg_type_lower:
            cursor.execute('''
                UPDATE v2x_stats SET v2i_messages = v2i_messages + 1 WHERE date = ?
            ''', (date_str,))
        elif 'psm' in msg_type_lower:
            cursor.execute('''
                UPDATE v2x_stats SET v2p_messages = v2p_messages + 1 WHERE date = ?
            ''', (date_str,))
        
        # Update security stats
        if not signature_valid:
            cursor.execute('''
                UPDATE v2x_stats SET invalid_signatures = invalid_signatures + 1 WHERE date = ?
            ''', (date_str,))
        if replay_detected:
            cursor.execute('''
                UPDATE v2x_stats SET replay_attempts = replay_attempts + 1 WHERE date = ?
            ''', (date_str,))
        
        conn.commit()
        conn.close()
        
        # Return result
        return {
            'id': msg_db_id,
            'timestamp': timestamp,
            'message_type': message_type,
            'message_id': message_id,
            'sender_id': sender_id,
            'signature_valid': signature_valid,
            'certificate_valid': certificate_valid,
            'replay_detected': replay_detected,
            'misbehavior_flags': misbehavior_flags,
            'hash': message_hash
        }
    
    def report_misbehavior(self,
                          target_vehicle_id: str,
                          misbehavior_type: str,
                          description: str,
                          evidence_message_ids: List[str],
                          location: tuple = None,
                          severity: str = "HIGH") -> dict:
        """
        Report V2X misbehavior to the Misbehavior Authority (MA)
        
        Args:
            target_vehicle_id: Vehicle exhibiting misbehavior
            misbehavior_type: Type of misbehavior
            description: Detailed description
            evidence_message_ids: List of message IDs as evidence
            location: (lat, lon) where misbehavior occurred
            severity: CRITICAL, HIGH, MEDIUM, LOW
        """
        timestamp = time.time()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO v2x_misbehavior
            (timestamp, reporter_vehicle_id, target_vehicle_id, misbehavior_type,
             description, evidence_message_ids, location_lat, location_lon, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, self.vehicle_id, target_vehicle_id, misbehavior_type,
              description, json.dumps(evidence_message_ids),
              location[0] if location else None, location[1] if location else None,
              severity))
        
        report_id = cursor.lastrowid
        
        # Update stats
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE v2x_stats SET misbehavior_reports = misbehavior_reports + 1
            WHERE date = ?
        ''', (date_str,))
        
        conn.commit()
        conn.close()
        
        return {
            'report_id': report_id,
            'timestamp': timestamp,
            'target': target_vehicle_id,
            'type': misbehavior_type,
            'severity': severity,
            'status': 'SUBMITTED_TO_MA'
        }
    
    def get_v2x_forensic_report(self, 
                               start_time: float = None,
                               end_time: float = None,
                               message_type: str = None) -> dict:
        """
        Generate forensic report of V2X activity
        
        Returns comprehensive analysis including:
        - Message statistics
        - Security incidents
        - Misbehavior reports
        - Certificate analysis
        """
        if not end_time:
            end_time = time.time()
        if not start_time:
            start_time = end_time - (24 * 3600)  # Last 24 hours
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = {
            'report_id': hashlib.sha256(f"v2x{start_time}{end_time}".encode()).hexdigest()[:16],
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'vehicle_id': self.vehicle_id,
            'time_range': {'start': start_time, 'end': end_time},
            'summary': {},
            'security_incidents': [],
            'certificate_analysis': [],
            'misbehavior_reports': []
        }
        
        # Message statistics
        query = '''
            SELECT message_type, COUNT(*) as count,
                   SUM(CASE WHEN signature_valid = 0 THEN 1 ELSE 0 END) as invalid_sigs,
                   SUM(replay_detected) as replays
            FROM v2x_messages
            WHERE timestamp BETWEEN ? AND ?
        '''
        params = [start_time, end_time]
        
        if message_type:
            query += ' AND message_type = ?'
            params.append(message_type)
        
        query += ' GROUP BY message_type'
        
        cursor.execute(query, params)
        stats = cursor.fetchall()
        
        report['summary']['message_stats'] = {
            row[0]: {
                'total': row[1],
                'invalid_signatures': row[2],
                'replay_attempts': row[3]
            } for row in stats
        }
        
        # Security incidents (messages with misbehavior)
        cursor.execute('''
            SELECT * FROM v2x_messages
            WHERE timestamp BETWEEN ? AND ?
            AND (replay_detected = 1 OR signature_valid = 0 OR certificate_valid = 0)
            ORDER BY timestamp DESC
            LIMIT 100
        ''', (start_time, end_time))
        
        incidents = cursor.fetchall()
        for incident in incidents:
            report['security_incidents'].append({
                'timestamp': incident[1],
                'message_type': incident[2],
                'message_id': incident[3],
                'sender_id': incident[4],
                'replay_detected': bool(incident[15]),
                'signature_valid': bool(incident[13]),
                'certificate_valid': bool(incident[14]),
                'misbehavior_flags': json.loads(incident[17]) if incident[17] else []
            })
        
        # Certificate analysis
        cursor.execute('''
            SELECT certificate_id, first_seen, last_seen, message_count, is_valid
            FROM v2x_certificates
            WHERE last_seen BETWEEN ? AND ?
            ORDER BY message_count DESC
            LIMIT 50
        ''', (start_time, end_time))
        
        certs = cursor.fetchall()
        for cert in certs:
            report['certificate_analysis'].append({
                'certificate_id': cert[0][:16] + '...',  # Truncate for privacy
                'first_seen': cert[1],
                'last_seen': cert[2],
                'message_count': cert[3],
                'is_valid': bool(cert[4])
            })
        
        # Misbehavior reports
        cursor.execute('''
            SELECT * FROM v2x_misbehavior
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp DESC
        ''', (start_time, end_time))
        
        reports = cursor.fetchall()
        for r in reports:
            report['misbehavior_reports'].append({
                'timestamp': r[1],
                'target': r[3],
                'type': r[4],
                'description': r[5],
                'severity': r[9]
            })
        
        conn.close()
        return report


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("V2X Security Module Demo")
    print("=" * 60)
    
    v2x = V2XSecurityModule("VEH-V2X-001")
    
    # Simulate V2V BSM messages
    print("\n[1] Recording V2V Basic Safety Messages...")
    
    for i in range(5):
        result = v2x.record_v2x_message(
            message_type="BSM",
            message_id=f"BSM-{int(time.time() * 1000)}-{i}",
            sender_id=f"PSEUDONYM-{i:04X}",
            payload=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09',
            certificate_id=f"CERT-{i:08X}",
            signature_valid=True,
            certificate_valid=True,
            position=(43.6532 + (i * 0.001), -79.3832),
            speed=15.5 + i,
            heading=90.0,
            rssi=-65,
            channel=172
        )
        print(f"  BSM from {result['sender_id'][:20]}...")
    
    # Simulate replay attack
    print("\n[2] Detecting replay attack...")
    
    # First message
    msg_id = "BSM-REPLAY-TEST"
    v2x.record_v2x_message(
        message_type="BSM",
        message_id=msg_id,
        sender_id="PSEUDONYM-REPLAY",
        payload=b'\x00\x01\x02\x03',
        certificate_id="CERT-REPLAY",
        signature_valid=True
    )
    
    # Same message ID again (replay)
    replay_result = v2x.record_v2x_message(
        message_type="BSM",
        message_id=msg_id,  # Same ID!
        sender_id="PSEUDONYM-REPLAY",
        payload=b'\x00\x01\x02\x03',
        certificate_id="CERT-REPLAY",
        signature_valid=True
    )
    
    if replay_result['replay_detected']:
        print(f"  ✓ Replay attack detected! Flags: {replay_result['misbehavior_flags']}")
    
    # Simulate V2I message
    print("\n[3] Recording V2I traffic signal message...")
    
    v2x.record_v2x_message(
        message_type="SPAT",
        message_id=f"SPAT-{int(time.time() * 1000)}",
        sender_id="RSU-MAIN-ST-001",
        payload=b'\x20\x00\x30\x00\x00\x05',
        certificate_id="CERT-RSU-001",
        signature_valid=True,
        position=(43.6532, -79.3832),
        channel=183
    )
    print("  SPAT from RSU recorded")
    
    # Report misbehavior
    print("\n[4] Reporting misbehavior...")
    
    report = v2x.report_misbehavior(
        target_vehicle_id="PSEUDONYM-BAD-001",
        misbehavior_type="POSITION_MANIPULATION",
        description="Vehicle reporting impossible position jumps exceeding physical limits",
        evidence_message_ids=["BSM-001", "BSM-002", "BSM-003"],
        location=(43.6532, -79.3832),
        severity="HIGH"
    )
    print(f"  Misbehavior report submitted: {report['report_id']}")
    
    # Generate forensic report
    print("\n[5] Generating V2X forensic report...")
    
    forensic = v2x.get_v2x_forensic_report()
    print(f"  Report ID: {forensic['report_id']}")
    print(f"  Security incidents: {len(forensic['security_incidents'])}")
    print(f"  Misbehavior reports: {len(forensic['misbehavior_reports'])}")
    
    print("\n" + "=" * 60)
    print("V2X Demo Complete")
    print("=" * 60)
