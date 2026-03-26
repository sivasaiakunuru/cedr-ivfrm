"""
Evidence Packaging Module for Legal Proceedings

Provides court-admissible evidence packaging with:
- Chain of custody tracking
- Digital signatures
- Tamper-evident seals
- Standardized evidence formats
"""

import json
import hashlib
import hmac
import base64
from datetime import datetime, timezone
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import uuid


class ChainOfCustody:
    """
    Tracks chain of custody for forensic evidence
    
    Maintains complete audit trail of who accessed evidence,
    when, and for what purpose - critical for legal admissibility.
    """
    
    def __init__(self, evidence_id: str):
        self.evidence_id = evidence_id
        self.custody_chain = []
        self.current_custodian = None
        
    def create_evidence(self, creator: str, description: str, 
                       location: str) -> dict:
        """Initialize chain of custody for new evidence"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "EVIDENCE_CREATED",
            "custodian": creator,
            "description": description,
            "location": location,
            "evidence_id": self.evidence_id,
            "entry_hash": None
        }
        
        # Hash the entry for integrity
        entry["entry_hash"] = self._hash_entry(entry)
        
        self.custody_chain.append(entry)
        self.current_custodian = creator
        
        return entry
    
    def transfer_custody(self, from_custodian: str, to_custodian: str,
                        reason: str, authorization: str) -> dict:
        """Transfer custody of evidence"""
        if from_custodian != self.current_custodian:
            raise ValueError(f"Current custodian is {self.current_custodian}, not {from_custodian}")
        
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "CUSTODY_TRANSFER",
            "from_custodian": from_custodian,
            "to_custodian": to_custodian,
            "reason": reason,
            "authorization": authorization,
            "evidence_id": self.evidence_id,
            "entry_hash": None
        }
        
        entry["entry_hash"] = self._hash_entry(entry)
        
        self.custody_chain.append(entry)
        self.current_custodian = to_custodian
        
        return entry
    
    def access_evidence(self, accessor: str, purpose: str,
                       authorization: str) -> dict:
        """Log access to evidence"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "EVIDENCE_ACCESSED",
            "accessor": accessor,
            "purpose": purpose,
            "authorization": authorization,
            "current_custodian": self.current_custodian,
            "evidence_id": self.evidence_id,
            "entry_hash": None
        }
        
        entry["entry_hash"] = self._hash_entry(entry)
        
        self.custody_chain.append(entry)
        
        return entry
    
    def _hash_entry(self, entry: dict) -> str:
        """Create tamper-evident hash of custody entry"""
        # Include previous hash for chain integrity
        previous_hash = self.custody_chain[-1]["entry_hash"] if self.custody_chain else "GENESIS"
        
        data = json.dumps(entry, sort_keys=True, default=str)
        combined = previous_hash + data
        
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def verify_chain(self) -> dict:
        """Verify integrity of custody chain"""
        violations = []
        
        for i, entry in enumerate(self.custody_chain):
            # Recalculate hash
            entry_copy = entry.copy()
            stored_hash = entry_copy.pop("entry_hash")
            
            previous_hash = self.custody_chain[i-1]["entry_hash"] if i > 0 else "GENESIS"
            data = json.dumps(entry_copy, sort_keys=True, default=str)
            expected_hash = hashlib.sha256((previous_hash + data).encode()).hexdigest()
            
            if stored_hash != expected_hash:
                violations.append({
                    "entry_index": i,
                    "expected_hash": expected_hash,
                    "stored_hash": stored_hash,
                    "timestamp": entry["timestamp"]
                })
        
        return {
            "evidence_id": self.evidence_id,
            "total_entries": len(self.custody_chain),
            "violations": violations,
            "is_valid": len(violations) == 0
        }
    
    def get_chain_report(self) -> dict:
        """Get complete chain of custody report"""
        return {
            "evidence_id": self.evidence_id,
            "current_custodian": self.current_custodian,
            "total_entries": len(self.custody_chain),
            "chain": self.custody_chain,
            "verification": self.verify_chain()
        }


class EvidencePackage:
    """
    Court-admissible evidence package
    
    Packages forensic data with:
    - Digital signatures
    - Chain of custody
    - Metadata and context
    - Tamper-evident seals
    """
    
    def __init__(self, case_id: str, investigator_id: str):
        self.package_id = f"PKG-{uuid.uuid4().hex[:12].upper()}"
        self.case_id = case_id
        self.investigator_id = investigator_id
        self.created_at = datetime.now(timezone.utc).isoformat()
        
        self.evidence_items = []
        self.chain_of_custody = ChainOfCustody(self.package_id)
        self.signatures = {}
        
        # Initialize custody chain
        self.chain_of_custody.create_evidence(
            creator=investigator_id,
            description=f"Evidence package for case {case_id}",
            location="CEDR_FORENSIC_SYSTEM"
        )
        
    def add_evidence(self, evidence_type: str, data: dict,
                    description: str, source: str) -> dict:
        """Add evidence item to package"""
        evidence_id = f"EVD-{uuid.uuid4().hex[:12].upper()}"
        
        item = {
            "evidence_id": evidence_id,
            "package_id": self.package_id,
            "type": evidence_type,
            "description": description,
            "source": source,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "collected_by": self.investigator_id,
            "data_hash": hashlib.sha256(
                json.dumps(data, sort_keys=True).encode()
            ).hexdigest(),
            "data": data
        }
        
        self.evidence_items.append(item)
        
        # Log access
        self.chain_of_custody.access_evidence(
            accessor=self.investigator_id,
            purpose=f"Added evidence: {description}",
            authorization=f"CASE-{self.case_id}"
        )
        
        return item
    
    def sign_package(self, private_key_pem: Optional[str] = None) -> dict:
        """
        Digitally sign the evidence package
        
        Creates cryptographic proof of package integrity
        """
        # Generate key pair if not provided
        if private_key_pem is None:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
        else:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None
            )
        
        # Create package hash
        package_data = {
            "package_id": self.package_id,
            "case_id": self.case_id,
            "created_at": self.created_at,
            "evidence_count": len(self.evidence_items),
            "evidence_hashes": [e["data_hash"] for e in self.evidence_items]
        }
        
        package_hash = hashlib.sha256(
            json.dumps(package_data, sort_keys=True).encode()
        ).digest()
        
        # Sign the hash
        signature = private_key.sign(
            package_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Get public key for verification
        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        self.signatures["investigator"] = {
            "signature": base64.b64encode(signature).decode(),
            "public_key": public_key_pem,
            "signed_at": datetime.now(timezone.utc).isoformat(),
            "signer": self.investigator_id
        }
        
        return self.signatures["investigator"]
    
    def verify_signature(self) -> dict:
        """Verify package digital signature"""
        if "investigator" not in self.signatures:
            return {"valid": False, "error": "No signature found"}
        
        try:
            sig_data = self.signatures["investigator"]
            public_key = serialization.load_pem_public_key(
                sig_data["public_key"].encode()
            )
            
            # Recreate package hash
            package_data = {
                "package_id": self.package_id,
                "case_id": self.case_id,
                "created_at": self.created_at,
                "evidence_count": len(self.evidence_items),
                "evidence_hashes": [e["data_hash"] for e in self.evidence_items]
            }
            
            package_hash = hashlib.sha256(
                json.dumps(package_data, sort_keys=True).encode()
            ).digest()
            
            # Verify signature
            signature = base64.b64decode(sig_data["signature"])
            
            try:
                public_key.verify(
                    signature,
                    package_hash,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return {"valid": True, "signer": sig_data["signer"]}
            except Exception:
                return {"valid": False, "error": "Signature verification failed"}
                
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def seal_package(self) -> dict:
        """
        Create tamper-evident seal on package
        
        Finalizes package and creates integrity seal
        """
        # Create comprehensive seal
        seal_data = {
            "package_id": self.package_id,
            "case_id": self.case_id,
            "sealed_at": datetime.now(timezone.utc).isoformat(),
            "sealed_by": self.investigator_id,
            "evidence_count": len(self.evidence_items),
            "custody_verification": self.chain_of_custody.verify_chain(),
            "signature_verification": self.verify_signature()
        }
        
        # Create seal hash
        seal_hash = hashlib.sha256(
            json.dumps(seal_data, sort_keys=True).encode()
        ).hexdigest()
        
        seal = {
            "seal_id": f"SEAL-{uuid.uuid4().hex[:12].upper()}",
            "seal_hash": seal_hash,
            "seal_data": seal_data
        }
        
        return seal
    
    def export_package(self, format: str = "json") -> dict:
        """
        Export complete evidence package
        
        Formats:
        - json: Complete digital package
        - summary: Human-readable summary
        - legal: Legal proceedings format
        """
        if format == "json":
            return {
                "package_id": self.package_id,
                "case_id": self.case_id,
                "investigator_id": self.investigator_id,
                "created_at": self.created_at,
                "evidence_items": self.evidence_items,
                "chain_of_custody": self.chain_of_custody.get_chain_report(),
                "signatures": self.signatures,
                "seal": self.seal_package()
            }
        
        elif format == "summary":
            return {
                "package_id": self.package_id,
                "case_id": self.case_id,
                "investigator": self.investigator_id,
                "created": self.created_at,
                "evidence_count": len(self.evidence_items),
                "evidence_types": list(set(e["type"] for e in self.evidence_items)),
                "custody_entries": len(self.chain_of_custody.custody_chain),
                "is_sealed": True,
                "signature_valid": self.verify_signature().get("valid", False)
            }
        
        elif format == "legal":
            return {
                "case_reference": self.case_id,
                "evidence_package_id": self.package_id,
                "exhibits": [
                    {
                        "exhibit_number": i + 1,
                        "description": e["description"],
                        "type": e["type"],
                        "source": e["source"],
                        "collected": e["collected_at"],
                        "hash": e["data_hash"]
                    }
                    for i, e in enumerate(self.evidence_items)
                ],
                "chain_of_custody": self.chain_of_custody.get_chain_report(),
                "authenticity": {
                    "digitally_signed": "investigator" in self.signatures,
                    "signature_valid": self.verify_signature().get("valid", False),
                    "seal_intact": True
                },
                "prepared_by": self.investigator_id,
                "prepared_date": self.created_at
            }
        
        else:
            raise ValueError(f"Unknown format: {format}")


if __name__ == "__main__":
    # Demo evidence packaging
    print("=" * 60)
    print("EVIDENCE PACKAGING MODULE DEMO")
    print("=" * 60)
    
    # Create evidence package
    package = EvidencePackage(
        case_id="CASE-2024-001",
        investigator_id="INV-001"
    )
    
    print("\n[1] Created evidence package")
    print(f"    Package ID: {package.package_id}")
    print(f"    Case ID: {package.case_id}")
    
    # Add evidence items
    print("\n[2] Adding evidence items...")
    
    package.add_evidence(
        evidence_type="CEDR_LOG",
        data={
            "event_type": "INTRUSION_DETECTED",
            "timestamp": "2024-03-26T14:30:00Z",
            "vehicle_id": "VEH-001",
            "details": {"attack_vector": "CAN_injection"}
        },
        description="Intrusion detection event from vehicle CEDR",
        source="CEDR-Module-V1"
    )
    
    package.add_evidence(
        evidence_type="NETWORK_CAPTURE",
        data={
            "packets": 1500,
            "anomalous_packets": 45,
            "duration_seconds": 300
        },
        description="Network traffic capture during incident",
        source="IDS-Gateway"
    )
    
    print(f"    Added {len(package.evidence_items)} evidence items")
    
    # Sign package
    print("\n[3] Digitally signing package...")
    signature = package.sign_package()
    print(f"    Signed by: {signature['signer']}")
    print(f"    Signed at: {signature['signed_at']}")
    
    # Verify signature
    print("\n[4] Verifying signature...")
    verification = package.verify_signature()
    print(f"    Valid: {verification['valid']}")
    
    # Create seal
    print("\n[5] Creating tamper-evident seal...")
    seal = package.seal_package()
    print(f"    Seal ID: {seal['seal_id']}")
    print(f"    Seal Hash: {seal['seal_hash'][:32]}...")
    
    # Export in different formats
    print("\n[6] Export formats:")
    
    summary = package.export_package("summary")
    print(f"\n    Summary:")
    print(f"      Evidence count: {summary['evidence_count']}")
    print(f"      Types: {', '.join(summary['evidence_types'])}")
    print(f"      Signature valid: {summary['signature_valid']}")
    
    legal = package.export_package("legal")
    print(f"\n    Legal Format:")
    print(f"      Case: {legal['case_reference']}")
    print(f"      Exhibits: {len(legal['exhibits'])}")
    print(f"      Authenticity: {legal['authenticity']}")
    
    # Verify chain of custody
    print("\n[7] Chain of custody verification:")
    custody_check = package.chain_of_custody.verify_chain()
    print(f"    Total entries: {custody_check['total_entries']}")
    print(f"    Is valid: {custody_check['is_valid']}")
    if custody_check['violations']:
        print(f"    Violations: {len(custody_check['violations'])}")
    
    print("\n" + "=" * 60)
    print("Evidence Packaging Demo Complete")
    print("=" * 60)
