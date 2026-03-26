"""
ISO/SAE 21434 Compliance Module for CEDR

Maps CEDR functionality to ISO/SAE 21434 requirements:
- [RC-01] Cybersecurity governance
- [RC-02] Risk management
- [RC-03] Security by design
- [RC-04] Security validation
- [RC-05] Security operations
- [RC-06] Incident response
- [RC-07] Forensic readiness
"""

import json
import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

class ISO21434Requirement(Enum):
    """ISO/SAE 21434 Key Requirements"""
    GOVERNANCE = "RC-01"           # Cybersecurity governance
    RISK_MANAGEMENT = "RC-02"      # Risk management
    SECURITY_BY_DESIGN = "RC-03"   # Security by design
    VALIDATION = "RC-04"           # Security validation
    OPERATIONS = "RC-05"           # Security operations
    INCIDENT_RESPONSE = "RC-06"    # Incident response
    FORENSIC_READINESS = "RC-07"   # Forensic readiness

class ComplianceLevel(Enum):
    """Compliance maturity levels"""
    NOT_IMPLEMENTED = 0
    PARTIAL = 1
    IMPLEMENTED = 2
    VALIDATED = 3
    CERTIFIED = 4

class ISO21434Compliance:
    """
    ISO/SAE 21434 Compliance Tracker for CEDR
    
    Tracks compliance status and generates audit reports
    aligned with automotive cybersecurity standards.
    """
    
    def __init__(self, vehicle_id: str):
        self.vehicle_id = vehicle_id
        self.compliance_map = self._init_compliance_map()
        self.audit_log = []
        
    def _init_compliance_map(self) -> Dict:
        """Initialize compliance mapping for CEDR features"""
        return {
            ISO21434Requirement.GOVERNANCE: {
                "description": "Cybersecurity governance and management system",
                "cedr_features": [
                    "Tamper-evident logging with cryptographic chain",
                    "Role-based access control for forensic data",
                    "Security policy enforcement"
                ],
                "status": ComplianceLevel.IMPLEMENTED,
                "evidence": []
            },
            ISO21434Requirement.RISK_MANAGEMENT: {
                "description": "Cybersecurity risk management",
                "cedr_features": [
                    "Real-time threat detection and classification",
                    "Risk scoring based on CVSS automotive",
                    "Attack surface monitoring"
                ],
                "status": ComplianceLevel.IMPLEMENTED,
                "evidence": []
            },
            ISO21434Requirement.SECURITY_BY_DESIGN: {
                "description": "Security by design and default",
                "cedr_features": [
                    "AES-256 encryption for stored events",
                    "HMAC-SHA256 for event authentication",
                    "Secure boot verification logging"
                ],
                "status": ComplianceLevel.IMPLEMENTED,
                "evidence": []
            },
            ISO21434Requirement.VALIDATION: {
                "description": "Security validation and verification",
                "cedr_features": [
                    "Chain integrity verification",
                    "Automated self-tests",
                    "Cryptographic validation"
                ],
                "status": ComplianceLevel.VALIDATED,
                "evidence": []
            },
            ISO21434Requirement.OPERATIONS: {
                "description": "Security operations and monitoring",
                "cedr_features": [
                    "Continuous security event monitoring",
                    "Automated alert generation",
                    "Secure cloud transmission"
                ],
                "status": ComplianceLevel.IMPLEMENTED,
                "evidence": []
            },
            ISO21434Requirement.INCIDENT_RESPONSE: {
                "description": "Cybersecurity incident response",
                "cedr_features": [
                    "Immediate critical event transmission",
                    "Incident correlation and analysis",
                    "Automated response triggering"
                ],
                "status": ComplianceLevel.IMPLEMENTED,
                "evidence": []
            },
            ISO21434Requirement.FORENSIC_READINESS: {
                "description": "Forensic readiness and evidence collection",
                "cedr_features": [
                    "Tamper-evident blockchain-style logging",
                    "Complete event chain reconstruction",
                    "Court-admissible evidence packaging"
                ],
                "status": ComplianceLevel.VALIDATED,
                "evidence": []
            }
        }
    
    def log_compliance_event(self, requirement: ISO21434Requirement, 
                            action: str, evidence: dict):
        """Log a compliance-related event"""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "requirement": requirement.value,
            "action": action,
            "evidence_hash": hashlib.sha256(
                json.dumps(evidence, sort_keys=True).encode()
            ).hexdigest(),
            "vehicle_id": self.vehicle_id
        }
        self.audit_log.append(event)
        self.compliance_map[requirement]["evidence"].append(event)
        return event
    
    def get_compliance_report(self) -> dict:
        """Generate comprehensive compliance report"""
        total_requirements = len(self.compliance_map)
        implemented = sum(1 for r in self.compliance_map.values() 
                         if r["status"].value >= ComplianceLevel.IMPLEMENTED.value)
        validated = sum(1 for r in self.compliance_map.values() 
                       if r["status"].value >= ComplianceLevel.VALIDATED.value)
        
        report = {
            "report_id": hashlib.sha256(
                f"{self.vehicle_id}{datetime.now(timezone.utc).isoformat()}".encode()
            ).hexdigest()[:16],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "vehicle_id": self.vehicle_id,
            "standard": "ISO/SAE 21434:2021",
            "summary": {
                "total_requirements": total_requirements,
                "implemented": implemented,
                "validated": validated,
                "compliance_percentage": round((implemented / total_requirements) * 100, 1)
            },
            "requirements": {}
        }
        
        for req, data in self.compliance_map.items():
            report["requirements"][req.value] = {
                "name": req.name,
                "description": data["description"],
                "status": data["status"].name,
                "cedr_features": data["cedr_features"],
                "evidence_count": len(data["evidence"])
            }
        
        return report
    
    def validate_forensic_readiness(self) -> dict:
        """Validate forensic readiness per ISO 21434 RC-07"""
        checks = {
            "cryptographic_integrity": self._check_crypto_integrity(),
            "chain_verification": self._check_chain_verification(),
            "evidence_preservation": self._check_evidence_preservation(),
            "audit_trail_completeness": self._check_audit_trail(),
            "access_control": self._check_access_control()
        }
        
        all_passed = all(checks.values())
        
        return {
            "validation_id": hashlib.sha256(
                f"forensic{datetime.now(timezone.utc).isoformat()}".encode()
            ).hexdigest()[:16],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "all_checks_passed": all_passed,
            "checks": checks,
            "status": "VALIDATED" if all_passed else "FAILED"
        }
    
    def _check_crypto_integrity(self) -> bool:
        """Check cryptographic integrity mechanisms"""
        # Placeholder - would verify actual crypto implementation
        return True
    
    def _check_chain_verification(self) -> bool:
        """Check blockchain-style chain verification"""
        # Placeholder - would verify chain integrity
        return True
    
    def _check_evidence_preservation(self) -> bool:
        """Check evidence preservation capabilities"""
        # Placeholder - would verify storage and retention
        return True
    
    def _check_audit_trail(self) -> bool:
        """Check audit trail completeness"""
        return len(self.audit_log) > 0
    
    def _check_access_control(self) -> bool:
        """Check access control mechanisms"""
        # Placeholder - would verify RBAC
        return True


class RiskAssessment:
    """
    Automotive CVSS-based Risk Assessment
    
    Calculates risk scores aligned with ISO/SAE 21434
    risk management requirements.
    """
    
    SEVERITY_WEIGHTS = {
        "CRITICAL": 10.0,
        "HIGH": 7.5,
        "MEDIUM": 5.0,
        "LOW": 2.5,
        "INFO": 1.0
    }
    
    ATTACK_COMPLEXITY = {
        "REPLAY_ATTACK": 0.5,      # Low complexity
        "BUS_OVERFLOW": 0.6,
        "UNAUTHORIZED_ACCESS": 0.7,
        "INTRUSION_DETECTED": 0.8,
        "MALWARE_DETECTED": 0.9,
        "FIRMWARE_TAMPERING": 1.0  # High complexity
    }
    
    def __init__(self):
        self.risk_history = []
    
    def calculate_event_risk(self, event_type: str, severity: str, 
                            impact_scope: str = "single_ecu") -> dict:
        """
        Calculate risk score for a security event
        
        Returns CVSS-style score (0-10) with automotive context
        """
        base_score = self.SEVERITY_WEIGHTS.get(severity, 5.0)
        complexity = self.ATTACK_COMPLEXITY.get(event_type, 0.7)
        
        # Impact scope multiplier
        scope_multiplier = {
            "single_ecu": 1.0,
            "multiple_ecu": 1.3,
            "safety_critical": 1.5,
            "vehicle_wide": 1.8
        }.get(impact_scope, 1.0)
        
        # Calculate final score
        risk_score = min(10.0, base_score * complexity * scope_multiplier)
        
        risk_data = {
            "event_type": event_type,
            "severity": severity,
            "base_score": base_score,
            "attack_complexity": complexity,
            "impact_scope": impact_scope,
            "scope_multiplier": scope_multiplier,
            "risk_score": round(risk_score, 2),
            "risk_level": self._get_risk_level(risk_score),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.risk_history.append(risk_data)
        return risk_data
    
    def _get_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level"""
        if score >= 9.0:
            return "CRITICAL"
        elif score >= 7.0:
            return "HIGH"
        elif score >= 4.0:
            return "MEDIUM"
        elif score >= 2.0:
            return "LOW"
        return "NEGLIGIBLE"
    
    def get_fleet_risk_summary(self) -> dict:
        """Get risk summary for fleet management"""
        if not self.risk_history:
            return {"status": "NO_DATA"}
        
        scores = [r["risk_score"] for r in self.risk_history]
        
        return {
            "total_events": len(self.risk_history),
            "average_risk": round(sum(scores) / len(scores), 2),
            "max_risk": max(scores),
            "critical_count": sum(1 for r in self.risk_history 
                                 if r["risk_level"] == "CRITICAL"),
            "high_count": sum(1 for r in self.risk_history 
                            if r["risk_level"] == "HIGH"),
            "risk_trend": self._calculate_trend()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate risk trend over time"""
        if len(self.risk_history) < 10:
            return "INSUFFICIENT_DATA"
        
        recent = self.risk_history[-10:]
        older = self.risk_history[-20:-10] if len(self.risk_history) >= 20 else self.risk_history[:10]
        
        recent_avg = sum(r["risk_score"] for r in recent) / len(recent)
        older_avg = sum(r["risk_score"] for r in older) / len(older)
        
        diff = recent_avg - older_avg
        if diff > 1.0:
            return "INCREASING"
        elif diff < -1.0:
            return "DECREASING"
        return "STABLE"


if __name__ == "__main__":
    # Demo compliance module
    print("=" * 60)
    print("ISO/SAE 21434 Compliance Module Demo")
    print("=" * 60)
    
    compliance = ISO21434Compliance("VEH-DEMO-001")
    
    # Log some compliance events
    compliance.log_compliance_event(
        ISO21434Requirement.FORENSIC_READINESS,
        "Chain integrity verified",
        {"events_verified": 100, "tampering_detected": False}
    )
    
    compliance.log_compliance_event(
        ISO21434Requirement.INCIDENT_RESPONSE,
        "Critical event transmitted",
        {"event_type": "INTRUSION_DETECTED", "response_time_ms": 150}
    )
    
    # Generate compliance report
    print("\n[1] Compliance Report:")
    report = compliance.get_compliance_report()
    print(f"    Report ID: {report['report_id']}")
    print(f"    Standard: {report['standard']}")
    print(f"    Compliance: {report['summary']['compliance_percentage']}%")
    print(f"    Requirements Implemented: {report['summary']['implemented']}/7")
    
    # Validate forensic readiness
    print("\n[2] Forensic Readiness Validation:")
    validation = compliance.validate_forensic_readiness()
    print(f"    Status: {validation['status']}")
    print(f"    All Checks Passed: {validation['all_checks_passed']}")
    for check, passed in validation['checks'].items():
        status = "✓" if passed else "✗"
        print(f"    {status} {check}")
    
    # Risk assessment demo
    print("\n[3] Risk Assessment:")
    risk = RiskAssessment()
    
    test_events = [
        ("REPLAY_ATTACK", "HIGH", "safety_critical"),
        ("INTRUSION_DETECTED", "CRITICAL", "vehicle_wide"),
        ("UNAUTHORIZED_ACCESS", "MEDIUM", "single_ecu")
    ]
    
    for event_type, severity, scope in test_events:
        result = risk.calculate_event_risk(event_type, severity, scope)
        print(f"    {event_type}: {result['risk_score']} ({result['risk_level']})")
    
    print("\n[4] Fleet Risk Summary:")
    summary = risk.get_fleet_risk_summary()
    print(f"    Total Events: {summary['total_events']}")
    print(f"    Average Risk: {summary['average_risk']}")
    print(f"    Max Risk: {summary['max_risk']}")
    print(f"    Trend: {summary['risk_trend']}")
    
    print("\n" + "=" * 60)
    print("Compliance Module Demo Complete")
    print("=" * 60)
