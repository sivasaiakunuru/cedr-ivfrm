#!/usr/bin/env python3
"""
Integrated Attack Simulator with Cloud Upload

Runs attack scenarios and uploads events to CEDR cloud backend
so they appear on the web dashboard in real-time.
"""

import sys
import time
import json
import requests
import random
from datetime import datetime, timezone

# Cloud backend endpoint
CLOUD_URL = "http://localhost:8080"
VEHICLE_ID = "VEH-ATTACK-001"

class DashboardAttackSimulator:
    """
    Attack simulator that sends events to CEDR cloud backend
    for real-time dashboard visualization.
    """
    
    def __init__(self):
        self.vehicle_id = VEHICLE_ID
        self.events_sent = 0
        self.cloud_url = CLOUD_URL
        
    def send_event(self, event_type: str, severity: str, source: str, data: dict):
        """Send event to cloud backend"""
        event = {
            "vehicle_id": self.vehicle_id,
            "event": {
                "timestamp": time.time(),
                "event_type": event_type,
                "severity": severity,
                "source": source,
                "data": json.dumps(data),
                "vehicle_id": self.vehicle_id
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            response = requests.post(
                f"{self.cloud_url}/api/cedr/upload",
                json=event,
                timeout=5
            )
            
            if response.status_code == 200:
                self.events_sent += 1
                print(f"  ✓ Sent: {event_type} ({severity})")
                return True
            else:
                print(f"  ✗ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def simulate_can_flooding(self):
        """CAN Bus Flooding Attack"""
        print("\n🚨 ATTACK: CAN Bus Flooding")
        print("  Description: Flooding CAN bus with high-frequency messages")
        print("  Severity: CRITICAL")
        
        for i in range(5):
            self.send_event(
                "BUS_OVERFLOW",
                "CRITICAL",
                "CAN-GATEWAY",
                {
                    "attack_type": "CAN_FLOODING",
                    "bus_id": "CAN-1",
                    "message_count": 1000 + (i * 500),
                    "bus_load_percent": random.randint(90, 100),
                    "mitre_technique": "T0830"
                }
            )
            time.sleep(0.5)
    
    def simulate_message_injection(self):
        """CAN Message Injection Attack"""
        print("\n🚨 ATTACK: CAN Message Injection")
        print("  Description: Injecting spoofed CAN messages")
        print("  Severity: CRITICAL")
        
        targets = ["BRAKE_CONTROL", "STEERING", "ENGINE"]
        for target in targets:
            self.send_event(
                "INTRUSION_DETECTED",
                "CRITICAL",
                f"CAN-{target}",
                {
                    "attack_type": "MESSAGE_INJECTION",
                    "target_ecu": target,
                    "message_id": f"0x{random.randint(0x100, 0x7FF):03X}",
                    "payload_anomaly": True,
                    "mitre_technique": "T0831"
                }
            )
            time.sleep(0.3)
    
    def simulate_replay_attack(self):
        """CAN Replay Attack"""
        print("\n🚨 ATTACK: CAN Replay Attack")
        print("  Description: Recording and replaying valid CAN messages")
        print("  Severity: HIGH")
        
        self.send_event(
            "REPLAY_ATTACK",
            "HIGH",
            "IDS-GATEWAY",
            {
                "attack_type": "REPLAY",
                "message_id": "0x0C9",
                "original_timestamp": time.time() - 300,
                "timestamp_anomaly": True,
                "mitre_technique": "T0832"
            }
        )
    
    def simulate_cellular_mitm(self):
        """Cellular Man-in-the-Middle"""
        print("\n🚨 ATTACK: Cellular MITM")
        print("  Description: Intercepting cellular communications")
        print("  Severity: CRITICAL")
        
        self.send_event(
            "SUSPICIOUS_BASE_STATION",
            "HIGH",
            "TELEMATICS",
            {
                "attack_type": "CELLULAR_MITM",
                "cell_id": "FAKE-12345",
                "signal_strength": -45,
                "location_mismatch": True,
                "mitre_technique": "T0853"
            }
        )
        
        time.sleep(0.5)
        
        self.send_event(
            "COMMUNICATION_ANOMALY",
            "CRITICAL",
            "TELEMATICS",
            {
                "attack_type": "MITM",
                "latency_ms": 1500,
                "certificate_mismatch": True,
                "session_hijacked": True
            }
        )
    
    def simulate_firmware_tampering(self):
        """Firmware Tampering Attack"""
        print("\n🚨 ATTACK: Firmware Tampering")
        print("  Description: Malicious firmware update")
        print("  Severity: CRITICAL")
        
        self.send_event(
            "FIRMWARE_UPDATE_ATTEMPT",
            "HIGH",
            "ECU-ENGINE",
            {
                "attack_type": "FIRMWARE_TAMPERING",
                "update_source": "unauthorized",
                "signature_valid": False,
                "version": "MALICIOUS-v9.9.9",
                "mitre_technique": "T0842"
            }
        )
        
        time.sleep(0.3)
        
        self.send_event(
            "ECU_BEHAVIOR_ANOMALY",
            "CRITICAL",
            "ECU-ENGINE",
            {
                "attack_type": "FIRMWARE_TAMPERING",
                "unexpected_commands": ["DISABLE_BRAKES", "MAX_THROTTLE"],
                "checksum_mismatch": True,
                "memory_corruption": True
            }
        )
    
    def simulate_key_fob_relay(self):
        """Key Fob Relay Attack"""
        print("\n🚨 ATTACK: Key Fob Relay")
        print("  Description: Relaying key fob signal to steal vehicle")
        print("  Severity: HIGH")
        
        self.send_event(
            "UNAUTHORIZED_ACCESS",
            "HIGH",
            "KEYLESS_ENTRY",
            {
                "attack_type": "KEY_FOB_RELAY",
                "access_method": "relay",
                "fob_distance_km": 2.5,
                "relay_detected": True,
                "mitre_technique": "T0872"
            }
        )
        
        time.sleep(0.3)
        
        self.send_event(
            "IGNITION_ON",
            "HIGH",
            "IMMOBILIZER",
            {
                "attack_type": "KEY_FOB_RELAY",
                "fob_present": False,
                "bypass_method": "relay_attack"
            }
        )
    
    def simulate_bluetooth_exploit(self):
        """Bluetooth Exploitation"""
        print("\n🚨 ATTACK: Bluetooth Exploitation")
        print("  Description: Exploiting Bluetooth stack vulnerabilities")
        print("  Severity: HIGH")
        
        self.send_event(
            "BLUETOOTH_EXPLOIT",
            "HIGH",
            "IVI-SYSTEM",
            {
                "attack_type": "BLUETOOTH_EXPLOIT",
                "exploit_type": "buffer_overflow",
                "device_name": "Malicious_Device",
                "mitre_technique": "T0851"
            }
        )
    
    def run_all_attacks(self):
        """Run complete attack simulation suite"""
        print("=" * 60)
        print("  CEDR INTEGRATED ATTACK SIMULATOR")
        print("  Sending attacks to cloud dashboard...")
        print("=" * 60)
        print(f"\nCloud Backend: {self.cloud_url}")
        print(f"Vehicle ID: {self.vehicle_id}")
        
        attacks = [
            self.simulate_can_flooding,
            self.simulate_message_injection,
            self.simulate_replay_attack,
            self.simulate_cellular_mitm,
            self.simulate_firmware_tampering,
            self.simulate_key_fob_relay,
            self.simulate_bluetooth_exploit
        ]
        
        for attack in attacks:
            attack()
            time.sleep(1)
        
        print("\n" + "=" * 60)
        print(f"  ✓ Attack simulation complete!")
        print(f"  ✓ Total events sent: {self.events_sent}")
        print(f"  ✓ Check dashboard: http://localhost:8080")
        print("=" * 60)


def main():
    """Main entry point"""
    print("\n🔌 Checking cloud backend connection...")
    
    try:
        response = requests.get(f"{CLOUD_URL}/api/dashboard/stats", timeout=3)
        if response.status_code == 200:
            print("✓ Cloud backend is online\n")
        else:
            print("⚠ Cloud backend returned error\n")
    except Exception as e:
        print(f"✗ Cannot connect to cloud backend: {e}")
        print("  Make sure to run: bash start.sh")
        return
    
    # Run attack simulator
    simulator = DashboardAttackSimulator()
    simulator.run_all_attacks()


if __name__ == "__main__":
    main()
