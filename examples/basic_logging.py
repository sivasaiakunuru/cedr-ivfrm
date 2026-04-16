#!/usr/bin/env python3
"""
CEDR Basic Event Logging Example

This example demonstrates how to log security events with
tamper-evident hash chaining.

Usage:
    python basic_logging.py
"""

import json
import hashlib
from datetime import datetime


class HashChain:
    """Simple hash chain implementation for demonstration"""
    
    def __init__(self):
        self.events = []
        self.previous_hash = "0" * 64  # Genesis hash
    
    def add_event(self, event_data):
        """Add event to chain with cryptographic hash"""
        timestamp = datetime.utcnow().isoformat()
        
        # Create hash of event + previous hash
        data_string = json.dumps(event_data, sort_keys=True)
        hash_input = f"{timestamp}{data_string}{self.previous_hash}"
        current_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        event = {
            "timestamp": timestamp,
            "data": event_data,
            "hash": current_hash,
            "previous_hash": self.previous_hash
        }
        
        self.events.append(event)
        self.previous_hash = current_hash
        
        return current_hash
    
    def verify_integrity(self):
        """Verify chain integrity"""
        for i in range(len(self.events)):
            event = self.events[i]
            expected_prev = self.events[i-1]["hash"] if i > 0 else "0" * 64
            
            if event["previous_hash"] != expected_prev:
                return False
            
            # Verify hash calculation
            data_string = json.dumps(event["data"], sort_keys=True)
            hash_input = f"{event['timestamp']}{data_string}{event['previous_hash']}"
            expected_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
            if event["hash"] != expected_hash:
                return False
        
        return True
    
    def export(self):
        """Export chain as JSON"""
        return json.dumps(self.events, indent=2)


def main():
    print("=" * 60)
    print("CEDR Basic Event Logging Example")
    print("=" * 60)
    
    # Initialize hash chain
    chain = HashChain()
    
    # Simulate security events
    events = [
        {
            "vehicle_id": "VEH001",
            "event_type": "SYSTEM_BOOT",
            "severity": "INFO",
            "details": "CEDR module initialized"
        },
        {
            "vehicle_id": "VEH001",
            "event_type": "CAN_MONITORING_START",
            "severity": "INFO",
            "details": "Started monitoring CAN bus"
        },
        {
            "vehicle_id": "VEH001",
            "event_type": "ANOMALY_DETECTED",
            "severity": "HIGH",
            "details": "Unusual CAN traffic pattern detected",
            "can_id": "0x123",
            "confidence": 0.92
        },
        {
            "vehicle_id": "VEH001",
            "event_type": "ALERT_SENT",
            "severity": "HIGH",
            "details": "Alert dispatched to SOC"
        }
    ]
    
    # Add events to chain
    print("\n📋 Logging Events:")
    print("-" * 60)
    
    for event in events:
        hash_value = chain.add_event(event)
        print(f"\n📝 {event['event_type']}")
        print(f"   Vehicle: {event['vehicle_id']}")
        print(f"   Severity: {event['severity']}")
        print(f"   Hash: {hash_value[:16]}...{hash_value[-16:]}")
    
    # Verify integrity
    print("\n" + "=" * 60)
    print("🔍 Chain Integrity Verification")
    print("-" * 60)
    
    if chain.verify_integrity():
        print("✅ Chain integrity verified - No tampering detected")
    else:
        print("❌ Chain integrity compromised!")
    
    # Export chain
    print("\n" + "=" * 60)
    print("📦 Chain Export (JSON)")
    print("-" * 60)
    print(chain.export()[:500] + "...")
    
    # Demonstrate tamper detection
    print("\n" + "=" * 60)
    print("🛡️  Tamper Detection Demo")
    print("-" * 60)
    
    # Simulate tampering
    if chain.events:
        print("\n⚠️  Simulating tampering...")
        original_data = chain.events[2]["data"]["severity"]
        chain.events[2]["data"]["severity"] = "LOW"  # Change severity
        
        if chain.verify_integrity():
            print("❌ Tamper detection failed!")
        else:
            print("✅ Tampering detected successfully!")
            print(f"   Original severity: {original_data}")
            print(f"   Tampered severity: {chain.events[2]['data']['severity']}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
