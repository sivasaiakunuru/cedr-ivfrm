#!/usr/bin/env python3
"""
CEDR Chain Verification Example

Demonstrates how to verify the integrity of a hash chain
and detect any tampering.

Usage:
    python verify_chain.py <chain_file.json>
"""

import json
import hashlib
import sys
from datetime import datetime


class ChainVerifier:
    """Verify integrity of CEDR hash chain"""
    
    def __init__(self, chain_file=None):
        self.chain = []
        self.issues = []
        
        if chain_file:
            self.load(chain_file)
    
    def load(self, filename):
        """Load chain from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.chain = json.load(f)
            print(f"✅ Loaded {len(self.chain)} events from {filename}")
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format in {filename}")
            sys.exit(1)
    
    def verify(self):
        """Verify entire chain integrity"""
        self.issues = []
        
        if not self.chain:
            self.issues.append("Chain is empty")
            return False
        
        for i, event in enumerate(self.chain):
            # Check required fields
            required = ["timestamp", "data", "hash", "previous_hash"]
            for field in required:
                if field not in event:
                    self.issues.append(f"Event {i}: Missing field '{field}'")
                    continue
            
            # Verify previous hash linkage
            if i == 0:
                expected_prev = "0" * 64
            else:
                expected_prev = self.chain[i-1]["hash"]
            
            if event["previous_hash"] != expected_prev:
                self.issues.append(
                    f"Event {i}: Hash linkage broken. "
                    f"Expected {expected_prev[:16]}..., "
                    f"got {event['previous_hash'][:16]}..."
                )
            
            # Verify hash calculation
            data_string = json.dumps(event["data"], sort_keys=True)
            hash_input = f"{event['timestamp']}{data_string}{event['previous_hash']}"
            expected_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
            if event["hash"] != expected_hash:
                self.issues.append(
                    f"Event {i}: Hash mismatch. "
                    f"Data may have been tampered"
                )
        
        return len(self.issues) == 0
    
    def get_statistics(self):
        """Get chain statistics"""
        if not self.chain:
            return {}
        
        event_types = {}
        severities = {}
        
        for event in self.chain:
            data = event.get("data", {})
            
            # Count event types
            event_type = data.get("event_type", "UNKNOWN")
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Count severities
            severity = data.get("severity", "UNKNOWN")
            severities[severity] = severities.get(severity, 0) + 1
        
        return {
            "total_events": len(self.chain),
            "event_types": event_types,
            "severities": severities,
            "first_event": self.chain[0]["timestamp"],
            "last_event": self.chain[-1]["timestamp"]
        }
    
    def print_report(self):
        """Print verification report"""
        print("\n" + "=" * 60)
        print("CHAIN VERIFICATION REPORT")
        print("=" * 60)
        
        # Verify
        is_valid = self.verify()
        
        if is_valid:
            print("\n✅ Chain integrity: VERIFIED")
            print("   No tampering detected")
        else:
            print("\n❌ Chain integrity: COMPROMISED")
            print(f"   {len(self.issues)} issue(s) found:")
            for issue in self.issues:
                print(f"   - {issue}")
        
        # Statistics
        stats = self.get_statistics()
        if stats:
            print("\n📊 Chain Statistics:")
            print(f"   Total Events: {stats['total_events']}")
            print(f"   First Event: {stats['first_event']}")
            print(f"   Last Event: {stats['last_event']}")
            
            print("\n   Event Types:")
            for event_type, count in sorted(stats['event_types'].items()):
                print(f"      {event_type}: {count}")
            
            print("\n   Severity Distribution:")
            for severity, count in sorted(stats['severities'].items()):
                print(f"      {severity}: {count}")
        
        print("\n" + "=" * 60)


def create_sample_chain():
    """Create a sample chain for testing"""
    chain = []
    previous_hash = "0" * 64
    
    events = [
        {"event_type": "BOOT", "severity": "INFO"},
        {"event_type": "ANOMALY", "severity": "HIGH"},
        {"event_type": "ALERT", "severity": "HIGH"},
    ]
    
    for event in events:
        timestamp = datetime.utcnow().isoformat()
        data_string = json.dumps(event, sort_keys=True)
        hash_input = f"{timestamp}{data_string}{previous_hash}"
        current_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        chain.append({
            "timestamp": timestamp,
            "data": event,
            "hash": current_hash,
            "previous_hash": previous_hash
        })
        previous_hash = current_hash
    
    return chain


def main():
    print("=" * 60)
    print("CEDR Chain Verification Tool")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Verify provided file
        chain_file = sys.argv[1]
        verifier = ChainVerifier(chain_file)
    else:
        # Create and verify sample chain
        print("\nℹ️  No file provided. Creating sample chain...")
        verifier = ChainVerifier()
        verifier.chain = create_sample_chain()
        
        # Save sample
        sample_file = "sample_chain.json"
        with open(sample_file, 'w') as f:
            json.dump(verifier.chain, f, indent=2)
        print(f"✅ Created sample chain: {sample_file}")
    
    verifier.print_report()


if __name__ == "__main__":
    main()
