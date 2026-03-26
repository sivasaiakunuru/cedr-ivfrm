#!/usr/bin/env python3
"""
CEDR Attack Simulation Demo

This script simulates various cybersecurity attacks on a vehicle
and demonstrates how CEDR captures, logs, and responds to them.
"""

import sys
import time
import random
import requests
import threading

# Add parent directory to path to import cedr_module
sys.path.insert(0, '/home/siva/openclaw/cedr-ivfrm/in-vehicle-module')
from cedr_module import CEDRModule

class AttackSimulator:
    """Simulates various vehicle cybersecurity attacks"""
    
    def __init__(self, vehicle_id="VEH-ATTACK-001"):
        self.cedr = CEDRModule(vehicle_id=vehicle_id)
        self.vehicle_id = vehicle_id
        self.attack_count = 0
        self.running = True
        
        # Attack scenarios
        self.attack_scenarios = [
            self.replay_attack,
            self.bus_flooding,
            self.diagnostic_intrusion,
            self.speed_manipulation,
            self.unauthorized_remote_access,
            self.malware_injection
        ]
        
    def normal_operation(self, duration=5):
        """Simulate normal vehicle operation"""
        print(f"\n{'='*60}")
        print("[PHASE 1] Normal Vehicle Operation")
        print(f"{'='*60}\n")
        
        for i in range(duration):
            # Normal CAN bus activity
            self.cedr.log_event(
                "CAN_BUS_ACTIVITY",
                "LOW",
                "GATEWAY",
                {"message_count": random.randint(800, 1200), "bus_load": f"{random.randint(20, 40)}%"}
            )
            
            # Normal diagnostic session (authorized)
            if i == 2:
                self.cedr.log_event(
                    "DIAGNOSTIC_SESSION",
                    "LOW",
                    "OBD-II",
                    {"authorized": True, "service": "ROUTINE_CHECK", "workshop_id": "WS-1234"}
                )
            
            time.sleep(1)
            
        print(f"✅ Normal operation logged: {duration} seconds of activity")
    
    def replay_attack(self):
        """
        Simulate a CAN bus replay attack.
        Attacker records valid messages and replays them.
        """
        print(f"\n{'='*60}")
        print("[ATTACK 1] CAN Bus Replay Attack")
        print(f"{'='*60}")
        print("Attacker records brake messages, replays them later...")
        print()
        
        # First, some normal braking
        self.cedr.log_event(
            "BRAKE_APPLICATION",
            "LOW",
            "BRAKE_ECU",
            {"pressure": "45%", "deceleration": "2.5 m/s²"}
        )
        time.sleep(0.5)
        
        # Attack begins - suspicious rapid messages
        for i in range(3):
            self.cedr.log_event(
                "REPLAY_ATTACK",
                "CRITICAL",
                "IDS-GATEWAY",
                {
                    "attack_type": "MESSAGE_REPLAY",
                    "target_bus": "POWERTRAIN_CAN",
                    "suspicious_id": f"0x1{random.randint(10, 99)}",
                    "replay_interval_ms": random.randint(5, 15),  # Too fast!
                    "anomaly_score": 0.95,
                    "mitigation": "BLOCKED"
                }
            )
            time.sleep(0.3)
        
        self.attack_count += 1
        print(f"🚨 CRITICAL: Replay attack detected and blocked!")
        
    def bus_flooding(self):
        """
        Simulate Denial of Service via CAN bus flooding.
        Attacker overwhelms the bus with messages.
        """
        print(f"\n{'='*60}")
        print("[ATTACK 2] CAN Bus Flooding (DoS)")
        print(f"{'='*60}")
        print("Attacker flooding bus with high-priority messages...")
        print()
        
        # Normal bus state
        self.cedr.log_event(
            "CAN_BUS_ACTIVITY",
            "MEDIUM",
            "GATEWAY",
            {"message_count": 5000, "bus_load": "95%", "state": "OVERLOAD"}
        )
        time.sleep(0.5)
        
        # Detect flooding
        self.cedr.log_event(
            "BUS_OVERFLOW",
            "CRITICAL",
            "IDS-GATEWAY",
            {
                "attack_type": "DENIAL_OF_SERVICE",
                "bus_id": "CHASSIS_CAN",
                "message_rate": "15000 msg/sec",  # Way above normal!
                "normal_rate": "500 msg/sec",
                "impact": "LEGITIMATE_MESSAGES_DROPPED",
                "countermeasure": "RATE_LIMITING_ACTIVATED"
            }
        )
        
        self.attack_count += 1
        print(f"🚨 CRITICAL: Bus flooding detected! Rate limiting activated.")
        
    def diagnostic_intrusion(self):
        """
        Simulate unauthorized diagnostic access attempt.
        Attacker tries to access ECU diagnostics without authorization.
        """
        print(f"\n{'='*60}")
        print("[ATTACK 3] Unauthorized Diagnostic Intrusion")
        print(f"{'='*60}")
        print("Attacker attempting to bypass authentication...")
        print()
        
        # Failed auth attempts
        for i in range(3):
            self.cedr.log_event(
                "UNAUTHORIZED_ACCESS",
                "HIGH" if i < 2 else "CRITICAL",
                "TELEMATICS",
                {
                    "attempt": i + 1,
                    "target_service": "ECU_FLASHING",
                    "auth_method": "SEED_KEY",
                    "result": "FAILED",
                    "source_ip": f"192.168.1.{random.randint(10, 99)}",
                    "tool_signature": "J2534_UNKNOWN"
                }
            )
            time.sleep(0.5)
        
        # Account lockout
        self.cedr.log_event(
            "ACCOUNT_LOCKOUT",
            "HIGH",
            "AUTHENTICATION",
            {"reason": "TOO_MANY_FAILED_ATTEMPTS", "lockout_duration": "300s"}
        )
        
        self.attack_count += 1
        print(f"🚨 HIGH: Unauthorized diagnostic access blocked after 3 attempts!")
        
    def speed_manipulation(self):
        """
        Simulate speedometer manipulation attack.
        Attacker tries to spoof speed sensor data.
        """
        print(f"\n{'='*60}")
        print("[ATTACK 4] Speed Sensor Manipulation")
        print(f"{'='*60}")
        print("Attacker injecting false speed data...")
        print()
        
        # GPS shows 60 km/h, but CAN shows 120 km/h (anomaly!)
        self.cedr.log_event(
            "ANOMALY_HIGH",
            "CRITICAL",
            "DATA_FUSION",
            {
                "anomaly_type": "SENSOR_INCONSISTENCY",
                "sensor_can": "120 km/h",
                "sensor_gps": "60 km/h",
                "sensor_imu": "58 km/h",
                "discrepancy": "60 km/h",
                "confidence": "98%",
                "likely_cause": "CAN_INJECTION"
            }
        )
        
        # Secondary effect - adaptive cruise control confused
        self.cedr.log_event(
            "SAFETY_SYSTEM_ALERT",
            "HIGH",
            "ADAS",
            {"system": "ADAPTIVE_CRUISE", "state": "DEGRADED", "reason": "UNRELIABLE_SPEED_DATA"}
        )
        
        self.attack_count += 1
        print(f"🚨 CRITICAL: Speed manipulation detected! ADAS degraded.")
        
    def unauthorized_remote_access(self):
        """
        Simulate remote exploit attempt via telematics.
        """
        print(f"\n{'='*60}")
        print("[ATTACK 5] Remote Exploit Attempt")
        print(f"{'='*60}")
        print("Attacker exploiting telematics unit...")
        print()
        
        # Initial probe
        self.cedr.log_event(
            "INTRUSION_DETECTED",
            "CRITICAL",
            "TELEMATICS",
            {
                "attack_type": "BUFFER_OVERFLOW",
                "target": "TCU_MODEM",
                "vulnerability": "CVE-2024-XXXX",
                "exploit_signature": "KNOWN_MALWARE_FAMILY_X",
                "command_executed": "whoami; cat /etc/passwd",
                "privilege": "ROOT",
                "data_exfiltrated": False
            }
        )
        
        # IDS detects unusual network traffic
        self.cedr.log_event(
            "NETWORK_ANOMALY",
            "HIGH",
            "NETWORK_IDS",
            {
                "connection": "CELLULAR",
                "dest_ip": "185.XXX.XXX.XXX",
                "dest_country": "SUSPICIOUS",
                "data_volume": "15MB",
                "protocol": "HTTPS_TUNNEL",
                "duration": "45s"
            }
        )
        
        self.attack_count += 1
        print(f"🚨 CRITICAL: Remote intrusion detected! TCU compromised.")
        
    def malware_injection(self):
        """
        Simulate malware injection via USB/OBD.
        """
        print(f"\n{'='*60}")
        print("[ATTACK 6] Malware Injection via USB")
        print(f"{'='*60}")
        print("Malicious USB device plugged into infotainment...")
        print()
        
        # USB device detected
        self.cedr.log_event(
            "MALWARE_DETECTED",
            "CRITICAL",
            "IVI_SYSTEM",
            {
                "detection_method": "SIGNATURE_SCAN",
                "malware_family": "RANSOMWARE_CAR",
                "file_name": "update_firmware.exe",
                "hash": "d41d8cd98f00b204e9800998ecf8427e",
                "behavior": "ENCRYPTION_OF_MAP_DATA",
                "quarantine": "SUCCESSFUL"
            }
        )
        
        # System isolation
        self.cedr.log_event(
            "SYSTEM_ISOLATION",
            "HIGH",
            "SECURITY_MANAGER",
            {
                "isolated_systems": ["IVI", "TELEMATICS", "WIFI"],
                "preserved_systems": ["BRAKE", "STEERING", "ENGINE"],
                "mode": "LIMP_HOME"
            }
        )
        
        self.attack_count += 1
        print(f"🚨 CRITICAL: Malware quarantined! Non-critical systems isolated.")
        
    def demonstrate_tamper_detection(self):
        """
        Demonstrate what happens if someone tries to tamper with logs.
        """
        print(f"\n{'='*60}")
        print("[DEMO] Tamper Detection Demonstration")
        print(f"{'='*60}")
        print("Simulating attacker trying to delete evidence...")
        print()
        
        # First, verify integrity
        print("[*] Verifying log integrity before 'attack'...")
        integrity_ok, message = self.cedr.verify_integrity()
        print(f"    Result: {message}")
        
        # Simulate tampering (we'll directly modify the DB for demo)
        print("\n[*] Simulating tampering attempt...")
        import sqlite3
        conn = sqlite3.connect(self.cedr.db_path)
        cursor = conn.cursor()
        
        # Get an event and 'tamper' with it
        cursor.execute('SELECT id, hash_chain FROM security_events LIMIT 1')
        event = cursor.fetchone()
        
        if event:
            event_id, original_hash = event
            print(f"    Event ID: {event_id}")
            print(f"    Original hash: {original_hash[:20]}...")
            
            # Simulate tampering by changing the hash
            fake_hash = "TAMPERED_HASH_12345"
            cursor.execute(
                'UPDATE security_events SET hash_chain = ? WHERE id = ?',
                (fake_hash, event_id)
            )
            conn.commit()
            print(f"    Tampered hash: {fake_hash}")
        
        conn.close()
        
        # Now verify again - should detect tampering!
        print("\n[*] Verifying log integrity after tampering...")
        integrity_ok, message = self.cedr.verify_integrity()
        
        if not integrity_ok:
            print(f"    🚨 TAMPERING DETECTED: {message}")
            print("\n    The hash chain is broken!")
            print("    This proves the forensic evidence is tamper-evident.")
        else:
            print(f"    Result: {message}")
            
    def run_full_simulation(self):
        """Run complete attack simulation"""
        print("\n" + "="*70)
        print("  🔴 CEDR ATTACK SIMULATION DEMO 🔴")
        print("  Demonstrating cybersecurity event capture & forensic readiness")
        print("="*70)
        
        # Phase 1: Normal operation
        self.normal_operation(duration=3)
        
        # Phase 2: Attack sequence
        print(f"\n{'='*60}")
        print("  ⚠️  ATTACK SEQUENCE INITIATED")
        print(f"{'='*60}")
        
        for attack in self.attack_scenarios:
            attack()
            time.sleep(1)
        
        # Phase 3: Tamper detection demo
        self.demonstrate_tamper_detection()
        
        # Phase 4: Generate forensic report
        print(f"\n{'='*60}")
        print("[PHASE 4] Forensic Report Generation")
        print(f"{'='*60}\n")
        
        report = self.cedr.get_forensic_report()
        print(f"Report ID: {report['report_id']}")
        print(f"Total Events: {report['total_events']}")
        print(f"Integrity Status: {report['integrity_status'][1]}")
        print()
        
        # Event breakdown
        print("Event Breakdown:")
        for event_type, count in report['event_summary'].items():
            severity_emoji = "🔴" if "CRITICAL" in str(report.get('severity_breakdown', {})) else "⚠️"
            print(f"  {severity_emoji} {event_type}: {count}")
        
        # Final statistics
        print(f"\n{'='*60}")
        print("[FINAL STATISTICS]")
        print(f"{'='*60}")
        stats = self.cedr.get_statistics()
        print(f"Vehicle ID: {stats['vehicle_id']}")
        print(f"Total Events Logged: {stats['total_events']}")
        print(f"Attacks Simulated: {self.attack_count}")
        print(f"Events Pending Upload: {stats['pending_upload']}")
        print()
        
        # Cloud upload status
        print(f"{'='*60}")
        print("[CLOUD UPLOAD STATUS]")
        print(f"{'='*60}")
        try:
            response = requests.get("http://localhost:8080/api/dashboard/stats", timeout=5)
            if response.status_code == 200:
                cloud_stats = response.json()
                print(f"✅ Cloud connection successful!")
                print(f"   Vehicles in cloud: {cloud_stats.get('total_vehicles', 0)}")
                print(f"   Total events stored: {cloud_stats.get('total_events', 0)}")
                print(f"   Correlations detected: {cloud_stats.get('total_correlations', 0)}")
            else:
                print(f"⚠️  Cloud responded with status: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Cloud not reachable: {e}")
            print("   (Run ./start.sh to start the cloud backend)")
        
        print(f"\n{'='*70}")
        print("  ✅ SIMULATION COMPLETE")
        print("="*70)
        print()
        print("Key Takeaways:")
        print("  1. All attacks were detected and logged")
        print("  2. Critical events triggered immediate alerts")
        print("  3. Tampering was detected via hash chain verification")
        print("  4. Forensic report generated with integrity proof")
        print()
        
        self.cedr.shutdown()

if __name__ == '__main__':
    simulator = AttackSimulator()
    simulator.run_full_simulation()