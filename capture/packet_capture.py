"""
Raw Packet Capture Module for CEDR

Stores raw communication data for deep forensic analysis:
- CAN bus frames (ID, payload, timestamp)
- Network packets (cellular, Wi-Fi)
- Bluetooth HCI logs
- Diagnostic session data
"""

import sqlite3
import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, BinaryIO
import struct


class PacketCapture:
    """
    Raw packet capture and storage for forensic analysis.
    
    Captures actual communication data (not just events) for:
    - Deep packet inspection
    - Attack reconstruction
    - Evidence verification
    - Research and analysis
    """
    
    def __init__(self, vehicle_id: str, storage_path: str = None):
        self.vehicle_id = vehicle_id
        self.db_path = storage_path or f"/tmp/cedr_packets_{vehicle_id}.db"
        self._init_database()
        
        # Capture configuration
        self.config = {
            'can_capture_enabled': True,
            'network_capture_enabled': True,
            'bluetooth_capture_enabled': True,
            'max_packet_size': 4096,  # bytes
            'retention_hours': 72,     # Keep raw packets for 72 hours
            'capture_filter': None     # Optional filter rules
        }
        
    def _init_database(self):
        """Initialize packet capture database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # CAN bus packets
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS can_packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                bus_id TEXT NOT NULL,
                message_id TEXT NOT NULL,
                payload BLOB NOT NULL,
                payload_hex TEXT NOT NULL,
                dlc INTEGER NOT NULL,
                is_extended INTEGER DEFAULT 0,
                is_remote INTEGER DEFAULT 0,
                hash TEXT NOT NULL,
                related_event_id INTEGER
            )
        ''')
        
        # Network packets (cellular, Wi-Fi)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                interface TEXT NOT NULL,
                protocol TEXT NOT NULL,
                src_address TEXT,
                dst_address TEXT,
                src_port INTEGER,
                dst_port INTEGER,
                payload BLOB,
                payload_size INTEGER,
                flags TEXT,
                hash TEXT NOT NULL,
                related_event_id INTEGER
            )
        ''')
        
        # Bluetooth HCI logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bluetooth_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                event_type TEXT NOT NULL,
                device_address TEXT,
                device_name TEXT,
                packet_type TEXT,
                payload BLOB,
                payload_hex TEXT,
                rssi INTEGER,
                hash TEXT NOT NULL,
                related_event_id INTEGER
            )
        ''')
        
        # Diagnostic session logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnostic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                session_id TEXT NOT NULL,
                tool_id TEXT,
                protocol TEXT NOT NULL,
                request_data BLOB,
                response_data BLOB,
                ecu_address TEXT,
                service_id TEXT,
                hash TEXT NOT NULL,
                related_event_id INTEGER
            )
        ''')
        
        # Packet capture metadata
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS capture_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                started_at REAL NOT NULL,
                ended_at REAL,
                capture_type TEXT NOT NULL,
                trigger_event TEXT,
                total_packets INTEGER DEFAULT 0,
                storage_size_bytes INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def capture_can_frame(self, bus_id: str, message_id: int, payload: bytes,
                         is_extended: bool = False, is_remote: bool = False,
                         related_event_id: int = None) -> dict:
        """
        Capture a raw CAN bus frame
        
        Args:
            bus_id: CAN bus identifier (e.g., 'CAN-1', 'CAN-2')
            message_id: 11-bit or 29-bit CAN ID
            payload: Up to 8 bytes of data
            is_extended: True for 29-bit extended ID
            is_remote: True for remote frame
            related_event_id: Link to security event if applicable
        """
        timestamp = time.time()
        payload_hex = payload.hex()
        dlc = len(payload)
        
        # Create hash for integrity
        hash_data = f"{timestamp}{bus_id}{message_id}{payload_hex}"
        frame_hash = hashlib.sha256(hash_data.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO can_packets 
            (timestamp, bus_id, message_id, payload, payload_hex, dlc, 
             is_extended, is_remote, hash, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, bus_id, hex(message_id), payload, payload_hex, dlc,
              int(is_extended), int(is_remote), frame_hash, related_event_id))
        
        packet_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': packet_id,
            'timestamp': timestamp,
            'bus_id': bus_id,
            'message_id': hex(message_id),
            'payload_hex': payload_hex,
            'dlc': dlc,
            'hash': frame_hash
        }
    
    def capture_network_packet(self, interface: str, protocol: str,
                              src_addr: str, dst_addr: str,
                              payload: bytes = None,
                              src_port: int = None, dst_port: int = None,
                              flags: str = None,
                              related_event_id: int = None) -> dict:
        """
        Capture network packet (cellular, Wi-Fi, Ethernet)
        
        Args:
            interface: Network interface (e.g., 'cellular', 'wifi', 'eth0')
            protocol: Protocol type (TCP, UDP, ICMP, etc.)
            src_addr: Source IP address
            dst_addr: Destination IP address
            payload: Raw packet payload
            src_port: Source port (for TCP/UDP)
            dst_port: Destination port
            flags: TCP flags or other protocol-specific flags
            related_event_id: Link to security event
        """
        timestamp = time.time()
        payload_size = len(payload) if payload else 0
        payload_hash = hashlib.sha256(payload).hexdigest() if payload else ''
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO network_packets 
            (timestamp, interface, protocol, src_address, dst_address,
             src_port, dst_port, payload, payload_size, flags, hash, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, interface, protocol, src_addr, dst_addr,
              src_port, dst_port, payload, payload_size, flags, payload_hash, 
              related_event_id))
        
        packet_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': packet_id,
            'timestamp': timestamp,
            'interface': interface,
            'protocol': protocol,
            'src': f"{src_addr}:{src_port}" if src_port else src_addr,
            'dst': f"{dst_addr}:{dst_port}" if dst_port else dst_addr,
            'size': payload_size,
            'hash': payload_hash
        }
    
    def capture_bluetooth_event(self, event_type: str, 
                               device_address: str = None,
                               device_name: str = None,
                               packet_type: str = None,
                               payload: bytes = None,
                               rssi: int = None,
                               related_event_id: int = None) -> dict:
        """
        Capture Bluetooth HCI event or packet
        
        Args:
            event_type: Type of Bluetooth event (inquiry, connection, pairing, etc.)
            device_address: BD_ADDR of remote device
            device_name: Human-readable device name
            packet_type: L2CAP, RFCOMM, ATT, etc.
            payload: Raw HCI or L2CAP payload
            rssi: Signal strength
            related_event_id: Link to security event
        """
        timestamp = time.time()
        payload_hex = payload.hex() if payload else ''
        
        # Create hash
        hash_data = f"{timestamp}{event_type}{device_address}{payload_hex}"
        event_hash = hashlib.sha256(hash_data.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bluetooth_logs 
            (timestamp, event_type, device_address, device_name, packet_type,
             payload, payload_hex, rssi, hash, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, event_type, device_address, device_name, packet_type,
              payload, payload_hex, rssi, event_hash, related_event_id))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': log_id,
            'timestamp': timestamp,
            'event_type': event_type,
            'device': device_name or device_address,
            'rssi': rssi,
            'hash': event_hash
        }
    
    def capture_diagnostic_traffic(self, session_id: str, protocol: str,
                                   request_data: bytes, response_data: bytes = None,
                                   tool_id: str = None, ecu_address: str = None,
                                   service_id: str = None,
                                   related_event_id: int = None) -> dict:
        """
        Capture diagnostic session data (OBD-II, UDS, etc.)
        
        Args:
            session_id: Unique diagnostic session identifier
            protocol: Diagnostic protocol (OBD-II, UDS, KWP2000, etc.)
            request_data: Raw request bytes
            response_data: Raw response bytes
            tool_id: Diagnostic tool identifier
            ecu_address: Target ECU address
            service_id: Diagnostic service (e.g., 0x22 for ReadDataByIdentifier)
            related_event_id: Link to security event
        """
        timestamp = time.time()
        
        # Create hash
        hash_data = f"{timestamp}{session_id}{request_data.hex()}{response_data.hex() if response_data else ''}"
        traffic_hash = hashlib.sha256(hash_data.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO diagnostic_logs 
            (timestamp, session_id, tool_id, protocol, request_data, response_data,
             ecu_address, service_id, hash, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, session_id, tool_id, protocol, request_data, response_data,
              ecu_address, service_id, traffic_hash, related_event_id))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': log_id,
            'timestamp': timestamp,
            'session': session_id,
            'protocol': protocol,
            'ecu': ecu_address,
            'service': service_id,
            'hash': traffic_hash
        }
    
    def get_packets_for_event(self, event_id: int, 
                             packet_type: str = 'all') -> dict:
        """
        Retrieve all packet captures related to a security event
        
        Args:
            event_id: The security event ID
            packet_type: 'can', 'network', 'bluetooth', 'diagnostic', or 'all'
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        result = {
            'event_id': event_id,
            'total_packets': 0,
            'packets': {}
        }
        
        if packet_type in ('all', 'can'):
            cursor.execute('''
                SELECT * FROM can_packets WHERE related_event_id = ? ORDER BY timestamp
            ''', (event_id,))
            can_packets = cursor.fetchall()
            result['packets']['can'] = [{
                'id': p[0], 'timestamp': p[1], 'bus_id': p[2],
                'message_id': p[3], 'payload_hex': p[5], 'dlc': p[6]
            } for p in can_packets]
            result['total_packets'] += len(can_packets)
        
        if packet_type in ('all', 'network'):
            cursor.execute('''
                SELECT * FROM network_packets WHERE related_event_id = ? ORDER BY timestamp
            ''', (event_id,))
            net_packets = cursor.fetchall()
            result['packets']['network'] = [{
                'id': p[0], 'timestamp': p[1], 'interface': p[2],
                'protocol': p[3], 'src': p[4], 'dst': p[5], 'size': p[9]
            } for p in net_packets]
            result['total_packets'] += len(net_packets)
        
        if packet_type in ('all', 'bluetooth'):
            cursor.execute('''
                SELECT * FROM bluetooth_logs WHERE related_event_id = ? ORDER BY timestamp
            ''', (event_id,))
            bt_packets = cursor.fetchall()
            result['packets']['bluetooth'] = [{
                'id': p[0], 'timestamp': p[1], 'event_type': p[2],
                'device': p[4] or p[3], 'rssi': p[8]
            } for p in bt_packets]
            result['total_packets'] += len(bt_packets)
        
        conn.close()
        return result
    
    def export_packet_capture(self, start_time: float = None, 
                             end_time: float = None,
                             format: str = 'json') -> dict:
        """
        Export packet capture data for forensic analysis
        
        Supports formats:
        - json: Structured JSON with metadata
        - pcap: Standard PCAP format (for network packets)
        - csv: Spreadsheet format for analysis
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Default to last 24 hours if no range specified
        if not end_time:
            end_time = time.time()
        if not start_time:
            start_time = end_time - (24 * 3600)
        
        export_data = {
            'export_id': hashlib.sha256(f"{start_time}{end_time}".encode()).hexdigest()[:16],
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'vehicle_id': self.vehicle_id,
            'time_range': {'start': start_time, 'end': end_time},
            'packets': {}
        }
        
        # Export CAN packets
        cursor.execute('''
            SELECT * FROM can_packets 
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp
        ''', (start_time, end_time))
        
        can_packets = cursor.fetchall()
        export_data['packets']['can'] = [{
            'timestamp': p[1],
            'bus_id': p[2],
            'message_id': p[3],
            'payload_hex': p[5],
            'dlc': p[6],
            'is_extended': bool(p[7]),
            'is_remote': bool(p[8])
        } for p in can_packets]
        
        # Export network packets
        cursor.execute('''
            SELECT * FROM network_packets 
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp
        ''', (start_time, end_time))
        
        net_packets = cursor.fetchall()
        export_data['packets']['network'] = [{
            'timestamp': p[1],
            'interface': p[2],
            'protocol': p[3],
            'src': f"{p[4]}:{p[6]}" if p[6] else p[4],
            'dst': f"{p[5]}:{p[7]}" if p[7] else p[5],
            'size': p[9],
            'flags': p[10]
        } for p in net_packets]
        
        export_data['summary'] = {
            'total_can_packets': len(can_packets),
            'total_network_packets': len(net_packets),
            'capture_duration_seconds': end_time - start_time
        }
        
        conn.close()
        return export_data
    
    def cleanup_old_packets(self, max_age_hours: int = None):
        """
        Remove old packet captures to manage storage
        
        Args:
            max_age_hours: Delete packets older than this (default: config value)
        """
        if max_age_hours is None:
            max_age_hours = self.config['retention_hours']
        
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old packets from all tables
        cursor.execute('DELETE FROM can_packets WHERE timestamp < ?', (cutoff_time,))
        can_deleted = cursor.rowcount
        
        cursor.execute('DELETE FROM network_packets WHERE timestamp < ?', (cutoff_time,))
        net_deleted = cursor.rowcount
        
        cursor.execute('DELETE FROM bluetooth_logs WHERE timestamp < ?', (cutoff_time,))
        bt_deleted = cursor.rowcount
        
        cursor.execute('DELETE FROM diagnostic_logs WHERE timestamp < ?', (cutoff_time,))
        diag_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return {
            'can_packets_deleted': can_deleted,
            'network_packets_deleted': net_deleted,
            'bluetooth_logs_deleted': bt_deleted,
            'diagnostic_logs_deleted': diag_deleted,
            'cutoff_time': cutoff_time
        }


# Demo and testing
if __name__ == "__main__":
    print("=" * 60)
    print("CEDR Packet Capture Module Demo")
    print("=" * 60)
    
    capture = PacketCapture("VEH-DEMO-001")
    
    # Simulate CAN packet captures
    print("\n[1] Capturing CAN bus frames...")
    
    can_frames = [
        (0x123, b'\x01\x02\x03\x04\x05\x06\x07\x08'),
        (0x456, b'\xFF\xFF\x00\x00'),
        (0x789, b'\xAA\xBB\xCC\xDD'),
    ]
    
    for msg_id, payload in can_frames:
        result = capture.capture_can_frame(
            bus_id="CAN-1",
            message_id=msg_id,
            payload=payload,
            related_event_id=1
        )
        print(f"  Captured: {result['message_id']} - {result['payload_hex']}")
    
    # Simulate network packet capture
    print("\n[2] Capturing network packets...")
    
    net_result = capture.capture_network_packet(
        interface="cellular",
        protocol="TCP",
        src_addr="192.168.1.100",
        dst_addr="10.0.0.50",
        src_port=54321,
        dst_port=443,
        payload=b"GET /api/vehicle/data HTTP/1.1",
        flags="SYN,ACK",
        related_event_id=2
    )
    print(f"  Captured: {net_result['protocol']} {net_result['src']} -> {net_result['dst']}")
    
    # Simulate Bluetooth event
    print("\n[3] Capturing Bluetooth event...")
    
    bt_result = capture.capture_bluetooth_event(
        event_type="PAIRING_REQUEST",
        device_address="AA:BB:CC:DD:EE:FF",
        device_name="Malicious_Device",
        rssi=-45,
        related_event_id=3
    )
    print(f"  Captured: {bt_result['event_type']} from {bt_result['device']}")
    
    # Simulate diagnostic traffic
    print("\n[4] Capturing diagnostic traffic...")
    
    diag_result = capture.capture_diagnostic_traffic(
        session_id="DIAG-001",
        protocol="UDS",
        tool_id="TOOL-ABC123",
        ecu_address="0x7E0",
        service_id="0x22",
        request_data=b'\x22\xF1\x90',  # ReadDataByIdentifier for VIN
        response_data=b'\x62\xF1\x90\x57\x44\x42\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30',
        related_event_id=4
    )
    print(f"  Captured: {diag_result['protocol']} session {diag_result['session']}")
    
    # Export packet capture
    print("\n[5] Exporting packet capture...")
    
    export = capture.export_packet_capture()
    print(f"  Export ID: {export['export_id']}")
    print(f"  CAN packets: {export['summary']['total_can_packets']}")
    print(f"  Network packets: {export['summary']['total_network_packets']}")
    
    # Get packets for specific event
    print("\n[6] Retrieving packets for event #1...")
    
    event_packets = capture.get_packets_for_event(1)
    print(f"  Total packets: {event_packets['total_packets']}")
    
    print("\n" + "=" * 60)
    print("Packet Capture Demo Complete")
    print("=" * 60)
