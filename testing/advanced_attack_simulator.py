"""
Advanced Attack Simulation Suite for CEDR

Comprehensive cyberattack scenarios targeting connected vehicles
for testing and validating CEDR forensic capabilities.

Attack Categories:
- Network Layer Attacks (CAN, Ethernet)
- ECU/ Firmware Attacks
- Communication Attacks (V2X, Telematics)
- Physical Access Attacks
"""

import time
import random
import threading
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Callable
import json

class AttackCategory(Enum):
    """Vehicle cyberattack categories"""
    NETWORK = "network"
    ECU_FIRMWARE = "ecu_firmware"
    COMMUNICATION = "communication"
    PHYSICAL = "physical"
    APPLICATION = "application"

class AttackSeverity(Enum):
    """Attack impact severity"""
    CRITICAL = "CRITICAL"    # Safety-critical systems affected
    HIGH = "HIGH"            # Major vehicle functions compromised
    MEDIUM = "MEDIUM"        # Minor functions affected
    LOW = "LOW"              # Information disclosure only

class AttackScenario:
    """
    Represents a specific attack scenario with metadata
    """
    
    def __init__(self, name: str, category: AttackCategory, 
                 severity: AttackSeverity, description: str,
                 attack_vector: str, mitre_technique: str = ""):
        self.name = name
        self.category = category
        self.severity = severity
        self.description = description
        self.attack_vector = attack_vector
        self.mitre_technique = mitre_technique
        self.events_generated = []
        self.detection_time_ms = None
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category.value,
            "severity": self.severity.value,
            "description": self.description,
            "attack_vector": self.attack_vector,
            "mitre_technique": self.mitre_technique,
            "events_count": len(self.events_generated),
            "detection_time_ms": self.detection_time_ms
        }


class AdvancedAttackSimulator:
    """
    Advanced Attack Simulator for CEDR Testing
    
    Simulates realistic vehicle cyberattacks to validate
    forensic logging and detection capabilities.
    """
    
    def __init__(self, cedr_module=None):
        self.cedr = cedr_module
        self.scenarios = self._init_scenarios()
        self.active_attacks = []
        self.attack_history = []
        self.callbacks: List[Callable] = []
        self.running = False
        
    def _init_scenarios(self) -> Dict[str, AttackScenario]:
        """Initialize comprehensive attack scenarios"""
        return {
            # Network Layer Attacks
            "can_bus_flooding": AttackScenario(
                name="CAN Bus Flooding Attack",
                category=AttackCategory.NETWORK,
                severity=AttackSeverity.CRITICAL,
                description="Flooding CAN bus with high-frequency messages causing denial of service",
                attack_vector="OBD-II port or compromised ECU",
                mitre_technique="T0830"
            ),
            "can_message_injection": AttackScenario(
                name="CAN Message Injection",
                category=AttackCategory.NETWORK,
                severity=AttackSeverity.CRITICAL,
                description="Injecting spoofed CAN messages to control vehicle functions",
                attack_vector="Compromised diagnostic tool",
                mitre_technique="T0831"
            ),
            "replay_attack": AttackScenario(
                name="CAN Replay Attack",
                category=AttackCategory.NETWORK,
                severity=AttackSeverity.HIGH,
                description="Recording and replaying valid CAN messages",
                attack_vector="Network sniffing + replay",
                mitre_technique="T0832"
            ),
            "ecu_spoofing": AttackScenario(
                name="ECU Spoofing",
                category=AttackCategory.NETWORK,
                severity=AttackSeverity.HIGH,
                description="Masquerading as legitimate ECU on the network",
                attack_vector="Compromised ECU or external device",
                mitre_technique="T0833"
            ),
            
            # ECU/Firmware Attacks
            "firmware_extraction": AttackScenario(
                name="Firmware Extraction",
                category=AttackCategory.ECU_FIRMWARE,
                severity=AttackSeverity.HIGH,
                description="Extracting firmware from ECU for reverse engineering",
                attack_vector="JTAG/debug interface access",
                mitre_technique="T0841"
            ),
            "firmware_modification": AttackScenario(
                name="Malicious Firmware Update",
                category=AttackCategory.ECU_FIRMWARE,
                severity=AttackSeverity.CRITICAL,
                description="Installing modified firmware to alter ECU behavior",
                attack_vector="Compromised update mechanism",
                mitre_technique="T0842"
            ),
            "ecu_reset_attack": AttackScenario(
                name="ECU Reset Attack",
                category=AttackCategory.ECU_FIRMWARE,
                severity=AttackSeverity.MEDIUM,
                description="Forcing ECU reset to disrupt operations",
                attack_vector="Malformed diagnostic messages",
                mitre_technique="T0843"
            ),
            
            # Communication Attacks
            "bt_exploit": AttackScenario(
                name="Bluetooth Exploitation",
                category=AttackCategory.COMMUNICATION,
                severity=AttackSeverity.HIGH,
                description="Exploiting Bluetooth stack vulnerabilities",
                attack_vector="Paired malicious device",
                mitre_technique="T0851"
            ),
            "wifi_exploit": AttackScenario(
                name="Wi-Fi Hotspot Exploitation",
                category=AttackCategory.COMMUNICATION,
                severity=AttackSeverity.HIGH,
                description="Attacking vehicle Wi-Fi hotspot",
                attack_vector="Unauthorized network access",
                mitre_technique="T0852"
            ),
            "cellular_mitm": AttackScenario(
                name="Cellular Man-in-the-Middle",
                category=AttackCategory.COMMUNICATION,
                severity=AttackSeverity.CRITICAL,
                description="Intercepting cellular communications to backend",
                attack_vector="Fake base station or compromised carrier",
                mitre_technique="T0853"
            ),
            "telematics_bypass": AttackScenario(
                name="Telematics System Bypass",
                category=AttackCategory.COMMUNICATION,
                severity=AttackSeverity.HIGH,
                description="Bypassing telematics authentication",
                attack_vector="Stolen credentials or session hijacking",
                mitre_technique="T0854"
            ),
            
            # Application Attacks
            "infotainment_exploit": AttackScenario(
                name="Infotainment System Exploitation",
                category=AttackCategory.APPLICATION,
                severity=AttackSeverity.MEDIUM,
                description="Exploiting IVI vulnerabilities for lateral movement",
                attack_vector="Malicious media file or app",
                mitre_technique="T0861"
            ),
            "mobile_app_exploit": AttackScenario(
                name="Companion App Exploitation",
                category=AttackCategory.APPLICATION,
                severity=AttackSeverity.HIGH,
                description="Exploiting mobile app to control vehicle",
                attack_vector="Compromised mobile device",
                mitre_technique="T0862"
            ),
            
            # Physical Attacks
            "obd_injection": AttackScenario(
                name="OBD-II Port Injection",
                category=AttackCategory.PHYSICAL,
                severity=AttackSeverity.CRITICAL,
                description="Direct injection via OBD-II diagnostic port",
                attack_vector="Physical access + diagnostic tool",
                mitre_technique="T0871"
            ),
            "key_fob_relay": AttackScenario(
                name="Key Fob Relay Attack",
                category=AttackCategory.PHYSICAL,
                severity=AttackSeverity.HIGH,
                description="Relaying key fob signal to unlock/steal vehicle",
                attack_vector="RF relay equipment",
                mitre_technique="T0872"
            ),
            "tpms_exploit": AttackScenario(
                name="TPMS Exploitation",
                category=AttackCategory.PHYSICAL,
                severity=AttackSeverity.LOW,
                description="Exploiting tire pressure monitoring system",
                attack_vector="Wireless tire sensor spoofing",
                mitre_technique="T0873"
            )
        }
    
    def execute_attack(self, scenario_name: str, duration_seconds: int = 10) -> AttackScenario:
        """
        Execute a specific attack scenario
        
        Args:
            scenario_name: Name of the attack scenario
            duration_seconds: How long to run the attack
            
        Returns:
            AttackScenario with execution results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        scenario = self.scenarios[scenario_name]
        print(f"\n[ATTACK] Executing: {scenario.name}")
        print(f"         Category: {scenario.category.value}")
        print(f"         Severity: {scenario.severity.value}")
        print(f"         Vector: {scenario.attack_vector}")
        
        start_time = time.time()
        
        # Execute attack-specific logic
        attack_method = getattr(self, f"_execute_{scenario_name}", self._execute_generic)
        events = attack_method(scenario, duration_seconds)
        
        scenario.events_generated = events
        scenario.detection_time_ms = int((time.time() - start_time) * 1000)
        
        self.attack_history.append({
            "scenario": scenario.to_dict(),
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": duration_seconds
        })
        
        # Notify callbacks
        for callback in self.callbacks:
            callback(scenario)
        
        # Log to CEDR if available
        if self.cedr:
            self.cedr.log_event(
                "ATTACK_SIMULATION",
                scenario.severity.value,
                "ATTACK_SIMULATOR",
                {
                    "scenario": scenario.name,
                    "category": scenario.category.value,
                    "events_generated": len(events),
                    "detection_time_ms": scenario.detection_time_ms
                }
            )
        
        print(f"[ATTACK] Completed: {len(events)} events generated")
        print(f"         Detection time: {scenario.detection_time_ms}ms")
        
        return scenario
    
    def _execute_can_bus_flooding(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Simulate CAN bus flooding attack"""
        events = []
        end_time = time.time() + duration
        message_count = 0
        
        while time.time() < end_time:
            # Simulate high-frequency CAN messages
            events.append({
                "timestamp": time.time(),
                "event_type": "BUS_OVERFLOW",
                "severity": "CRITICAL",
                "source": "CAN-GATEWAY",
                "data": {
                    "bus_id": "CAN-1",
                    "message_count": message_count,
                    "bus_load_percent": random.randint(85, 100),
                    "attack_type": "FLOODING"
                }
            })
            message_count += random.randint(100, 500)
            time.sleep(0.1)
        
        return events
    
    def _execute_can_message_injection(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Simulate CAN message injection attack"""
        events = []
        target_ecus = ["BRAKE_CONTROL", "STEERING", "ENGINE", "TRANSMISSION"]
        
        for _ in range(duration * 2):  # Multiple injection attempts
            target = random.choice(target_ecus)
            events.append({
                "timestamp": time.time(),
                "event_type": "MESSAGE_INJECTION",
                "severity": "CRITICAL",
                "source": f"CAN-{target}",
                "data": {
                    "target_ecu": target,
                    "message_id": hex(random.randint(0x100, 0x7FF)),
                    "payload_anomaly": True,
                    "authentication_failed": True
                }
            })
            time.sleep(0.5)
        
        return events
    
    def _execute_replay_attack(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Simulate replay attack"""
        events = []
        
        # First, simulate recording phase
        recorded_messages = []
        for i in range(5):
            recorded_messages.append({
                "timestamp": time.time() - 60,  # Recorded earlier
                "message_id": f"0x{200 + i:03X}",
                "payload": f"AABBCC{i:02X}"
            })
        
        # Then, replay phase
        for msg in recorded_messages:
            events.append({
                "timestamp": time.time(),
                "event_type": "REPLAY_ATTACK",
                "severity": "HIGH",
                "source": "IDS-GATEWAY",
                "data": {
                    "original_timestamp": msg["timestamp"],
                    "message_id": msg["message_id"],
                    "payload": msg["payload"],
                    "sequence_anomaly": True,
                    "timestamp_suspicious": True
                }
            })
            time.sleep(0.3)
        
        return events
    
    def _execute_cellular_mitm(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Simulate cellular man-in-the-middle attack"""
        events = []
        
        events.append({
            "timestamp": time.time(),
            "event_type": "SUSPICIOUS_BASE_STATION",
            "severity": "HIGH",
            "source": "TELEMATICS",
            "data": {
                "cell_id": "FAKE-12345",
                "signal_strength": -45,  # Suspiciously strong
                "location_mismatch": True,
                "expected_cell": "HOME-56789"
            }
        })
        
        # Simulate intercepted communications
        for i in range(duration):
            events.append({
                "timestamp": time.time(),
                "event_type": "COMMUNICATION_ANOMALY",
                "severity": "CRITICAL",
                "source": "TELEMATICS",
                "data": {
                    "connection_type": "cellular",
                    "latency_ms": random.randint(500, 2000),  # High latency
                    "certificate_mismatch": True,
                    "session_hijacked": True
                }
            })
            time.sleep(1)
        
        return events
    
    def _execute_firmware_modification(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Simulate malicious firmware update"""
        events = []
        
        # Firmware update attempt
        events.append({
            "timestamp": time.time(),
            "event_type": "FIRMWARE_UPDATE_ATTEMPT",
            "severity": "HIGH",
            "source": "ECU-ENGINE",
            "data": {
                "update_source": "unauthorized",
                "signature_valid": False,
                "version": "MALICIOUS-v9.9.9",
                "rollback_attempt": False
            }
        })
        
        # Post-update anomalies
        events.append({
            "timestamp": time.time() + 2,
            "event_type": "ECU_BEHAVIOR_ANOMALY",
            "severity": "CRITICAL",
            "source": "ECU-ENGINE",
            "data": {
                "unexpected_commands": ["DISABLE_BRAKES", "MAX_THROTTLE"],
                "checksum_mismatch": True,
                "memory_corruption": True
            }
        })
        
        return events
    
    def _execute_key_fob_relay(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Simulate key fob relay attack"""
        events = []
        
        events.append({
            "timestamp": time.time(),
            "event_type": "UNAUTHORIZED_ACCESS",
            "severity": "HIGH",
            "source": "KEYLESS_ENTRY",
            "data": {
                "access_method": "key_fob_relay",
                "fob_distance_km": 2.5,  # Fob is far away
                "unlock_location": "unknown",
                "relay_detected": True,
                "signal_amplification": True
            }
        })
        
        events.append({
            "timestamp": time.time() + 1,
            "event_type": "IGNITION_ON",
            "severity": "HIGH",
            "source": "IMMOBILIZER",
            "data": {
                "fob_present": False,
                "bypass_method": "relay_attack",
                "authentication": "bypassed"
            }
        })
        
        return events
    
    def _execute_generic(self, scenario: AttackScenario, duration: int) -> List[dict]:
        """Generic attack execution for unimplemented scenarios"""
        events = []
        
        for i in range(duration * 2):
            events.append({
                "timestamp": time.time(),
                "event_type": "ATTACK_DETECTED",
                "severity": scenario.severity.value,
                "source": "SECURITY_MONITOR",
                "data": {
                    "attack_name": scenario.name,
                    "category": scenario.category.value,
                    "mitre_technique": scenario.mitre_technique,
                    "simulated": True
                }
            })
            time.sleep(0.5)
        
        return events
    
    def run_full_test_suite(self) -> dict:
        """
        Execute complete attack test suite
        
        Runs all attack scenarios and generates comprehensive report
        """
        print("\n" + "=" * 70)
        print("CEDR ADVANCED ATTACK SIMULATION SUITE")
        print("=" * 70)
        
        results = {
            "test_run_id": f"TEST-{int(time.time())}",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "scenarios_executed": [],
            "total_events": 0,
            "detection_summary": {}
        }
        
        # Execute all scenarios
        for name, scenario in self.scenarios.items():
            try:
                executed = self.execute_attack(name, duration_seconds=3)
                results["scenarios_executed"].append(executed.to_dict())
                results["total_events"] += len(executed.events_generated)
            except Exception as e:
                print(f"[ERROR] Failed to execute {name}: {e}")
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        
        # Generate summary
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        category_counts = {}
        
        for scenario_data in results["scenarios_executed"]:
            severity_counts[scenario_data["severity"]] += 1
            cat = scenario_data["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        results["detection_summary"] = {
            "by_severity": severity_counts,
            "by_category": category_counts,
            "average_detection_time_ms": sum(
                s["detection_time_ms"] for s in results["scenarios_executed"]
            ) / len(results["scenarios_executed"]) if results["scenarios_executed"] else 0
        }
        
        print("\n" + "=" * 70)
        print("TEST SUITE SUMMARY")
        print("=" * 70)
        print(f"Total Scenarios: {len(results['scenarios_executed'])}")
        print(f"Total Events Generated: {results['total_events']}")
        print(f"\nBy Severity:")
        for sev, count in severity_counts.items():
            print(f"  {sev}: {count}")
        print(f"\nBy Category:")
        for cat, count in category_counts.items():
            print(f"  {cat}: {count}")
        print(f"\nAverage Detection Time: {results['detection_summary']['average_detection_time_ms']:.0f}ms")
        print("=" * 70)
        
        return results
    
    def register_callback(self, callback: Callable):
        """Register callback for attack events"""
        self.callbacks.append(callback)
    
    def get_attack_history(self) -> List[dict]:
        """Get history of all executed attacks"""
        return self.attack_history


if __name__ == "__main__":
    # Run standalone attack simulation
    simulator = AdvancedAttackSimulator()
    
    # Run full test suite
    results = simulator.run_full_test_suite()
    
    # Save results
    with open("attack_simulation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to attack_simulation_results.json")
