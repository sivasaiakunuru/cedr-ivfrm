# CEDR Improvement Plan
## Based on Risk Analysis & Solution Evaluation
### Team Cyber-Torque | CYB408 Capstone

**Version:** 1.0  
**Date:** April 9, 2026  
**Status:** Professional Enhancement Roadmap

---

## EXECUTIVE SUMMARY

Based on comprehensive risk analysis and SWOT evaluation, this document outlines specific, actionable improvements to transform CEDR from a capstone prototype into a production-ready automotive cybersecurity solution.

**Priority Areas:**
1. Hardware Migration (Critical Risk: T-001)
2. Competitive Differentiation (Critical Risk: B-002)
3. Testing Expansion (High Risk: T-002)
4. Operational Scalability (Medium Risk: O-002)

---

## 1. HARDWARE IMPROVEMENTS (Priority: CRITICAL)

### 1.1 Current State (Weakness)
- **Issue:** Raspberry Pi 4 not automotive-grade (-40°C to +85°C requirement)
- **Risk Score:** 21 (Critical)
- **Impact:** System failure in extreme temperatures, evidence loss

### 1.2 Recommended Solution

| Current | Improved | Specification | Cost Impact |
|---------|----------|---------------|-------------|
| Raspberry Pi 4 | **Raspberry Pi CM4 Industrial** | -20°C to +70°C | +$15/unit |
| Consumer CAN HAT | **Waveshare Industrial CAN** | Isolated, 5kV protection | +$25/unit |
| Plastic enclosure | **IP67 Aluminum housing** | Automotive temp | +$35/unit |
| External 4G modem | **Integrated Quectel BG96** | On-board cellular | +$20/unit |

**Total Hardware Upgrade:** +$95/unit ($240 → $335 for pilot)

### 1.3 Alternative: Automotive-Grade MCU

**Recommended:** NXP S32K3 (ASIL-B/D capable)

| Feature | Raspberry Pi CM4 | NXP S32K3 |
|---------|------------------|-----------|
| Temp Range | -20°C to +70°C | -40°C to +125°C |
| ASIL Rating | N/A | ASIL-B/D |
| HSM Support | External | Integrated HSE |
| CAN FD | Via HAT | Native (3× controllers) |
| Cost | $75 | $45 |
| **Recommendation** | **Pilot Phase** | **Production Phase** |

### 1.4 Implementation Plan

**Phase 1: Immediate (Weeks 1-4)**
- Order Raspberry Pi CM4 Industrial (10 units)
- Procure Waveshare Industrial CAN HAT
- Design IP67 aluminum enclosure
- Environmental testing protocol

**Phase 2: Short-term (Months 2-3)**
- Temperature chamber testing (-40°C to +85°C)
- Vibration testing (ISO 16750-3)
- EMC pre-compliance testing
- Design migration path to S32K3

**Phase 3: Production (Months 6-12)**
- S32K3 PCB design
- AEC-Q100 qualification
- Production tooling

---

## 2. SECURITY ARCHITECTURE IMPROVEMENTS (Priority: HIGH)

### 2.1 Hardware Security Module (HSM) Integration

**Current:** Software-based key storage (Risk: Key extraction)
**Improved:** Dedicated secure element

| Component | Function | Cost |
|-----------|----------|------|
| NXP A71CH | Secure key storage, crypto acceleration | $10/unit |
| Infineon OPTIGA TPM | TPM 2.0 compliant, measured boot | $12/unit |
| Microchip ATECC608 | Secure element, ECDSA | $8/unit |

**Recommendation:** NXP A71CH (best integration with S32K3)

### 2.2 Enhanced Cryptography

| Current | Improved | Benefit |
|---------|----------|---------|
| AES-128 (Fernet) | **AES-256-GCM** | Higher security margin |
| SHA-256 | **SHA-3-256** | Quantum-resistant prep |
| RSA-2048 signatures | **ECDSA P-384** | Faster, smaller signatures |
| SW key derivation | **PBKDF2 + HKDF** | Better key separation |

### 2.3 Secure Boot Implementation

```
Boot Flow:
1. ROM verifies bootloader (RSA signature)
2. Bootloader verifies kernel (ECDSA signature)
3. Kernel verifies CEDR application (HMAC)
4. Application verifies config (Hash)
5. Runtime integrity checks (Watchdog)
```

**Implementation:**
- U-Boot with secure boot
- dm-verity for root filesystem
- Signed OTA updates

---

## 3. TESTING & VALIDATION IMPROVEMENTS (Priority: HIGH)

### 3.1 Expand Attack Scenarios (13 → 50+)

| Category | Current | Target | New Tests |
|----------|---------|--------|-----------|
| Network (CAN) | 4 | 15 | CAN FD fuzzing, error injection |
| ECU/Firmware | 3 | 10 | Rowhammer, voltage glitching |
| Communication | 3 | 12 | Cellular jamming, GPS spoofing |
| Application | 2 | 8 | API fuzzing, auth bypass |
| Physical | 1 | 5 | Side-channel, probe attacks |

### 3.2 Automated Testing Framework

```python
# Recommended test structure
/tests
├── /unit              # Component tests
├── /integration       # System integration
├── /security          # Penetration tests
│   ├── /static      # SAST (Semgrep, Bandit)
│   ├── /dynamic     # DAST (OWASP ZAP)
│   └── /fuzz        # AFL++, libFuzzer
├── /hardware        # HIL testing
└── /compliance      # ISO 21434 validation
```

### 3.3 Hardware-in-Loop (HIL) Testing

**Equipment Needed:**
- Vector CANoe/CANalyzer ($15,000)
- dSPACE HIL simulator ($50,000)
- Rohde & Schwarz CMW500 ($80,000)

**Alternative (Cost-Effective):**
- Open-source CAN tools (SocketCAN, can-utils)
- Raspberry Pi-based HIL rig ($2,000)
- Custom test harness

---

## 4. CLOUD INFRASTRUCTURE IMPROVEMENTS (Priority: MEDIUM)

### 4.1 Multi-Cloud Strategy (Reduce Vendor Lock-in)

| Service | AWS (Current) | Azure (Backup) | GCP (Backup) |
|---------|---------------|----------------|--------------|
| Compute | EC2 | Azure VMs | Compute Engine |
| Database | RDS PostgreSQL | Azure SQL | Cloud SQL |
| Storage | S3 | Blob Storage | Cloud Storage |
| IoT | IoT Core | IoT Hub | Cloud IoT |

**Implementation:**
- Terraform for multi-cloud deployment
- Kubernetes for container orchestration
- Cloud-agnostic APIs

### 4.2 Edge Computing

**Current:** All processing in cloud  
**Improved:** Edge + Cloud hybrid

| Function | Edge (Vehicle) | Cloud |
|----------|---------------|-------|
| Event detection | ✅ Real-time | ❌ Delayed |
| Hash chaining | ✅ Local | ❌ Bandwidth |
| Alert filtering | ✅ Priority queue | ❌ All events |
| ML inference | ✅ Anomaly detection | ❌ Batch |
| Long-term storage | ❌ Limited | ✅ Unlimited |
| Fleet correlation | ❌ Single vehicle | ✅ Cross-vehicle |

**Edge Hardware:** NVIDIA Jetson Nano ($299)

### 4.3 Disaster Recovery

| Component | RTO | RPO | Implementation |
|-----------|-----|-----|----------------|
| Database | 1 hour | 5 min | Multi-AZ + read replicas |
| API | 15 min | 0 | Auto-scaling groups |
| Storage | 4 hours | 0 | Cross-region replication |
| Events | N/A | 0 | Local queue + cloud sync |

---

## 5. OPERATIONAL IMPROVEMENTS (Priority: MEDIUM)

### 5.1 ML-Based Anomaly Detection

**Current:** Rule-based detection (high false positives)
**Improved:** ML-based behavioral analysis

```
ML Pipeline:
1. Data Collection → Feature Engineering
2. Training → Isolation Forest / LSTM
3. Inference → Edge deployment (TensorFlow Lite)
4. Feedback → Continuous learning
```

**Benefits:**
- 80% reduction in false positives
- Detection of zero-day attacks
- Adaptive thresholds

### 5.2 Automated Response Playbooks

| Alert Type | Automated Action | Human Escalation |
|------------|------------------|------------------|
| Critical (CVSS 9+) | Isolate vehicle, notify SOC | Immediate |
| High (CVSS 7-8.9) | Increase monitoring | 15 minutes |
| Medium (CVSS 4-6.9) | Log for analysis | 1 hour |
| Low (CVSS <4) | Batch review | Daily |

### 5.3 SOAR Integration

**Tools:**
- Splunk Phantom
- Palo Alto XSOAR
- Swimlane

**Automated Workflows:**
1. Alert ingestion from CEDR
2. Enrichment (threat intel, asset data)
3. Correlation with other security tools
4. Automated containment (isolate vehicle)
5. Case creation and assignment

---

## 6. COMPETITIVE DIFFERENTIATION (Priority: CRITICAL)

### 6.1 Unique Value Propositions

| Feature | CEDR | ESCRYPT | Argus | Harman |
|---------|------|---------|-------|--------|
| Cost | **$145** | $800-1,200 | $600-900 | $600-900 |
| Tamper Evidence | **✅ Yes** | ❌ No | ❌ No | ❌ No |
| Open Source | **✅ Yes** | ❌ No | ❌ No | ❌ No |
| ISO 21434 | **✅ Yes** | ✅ Yes | ✅ Yes | ✅ Yes |
| ML Anomaly Detection | **✅ Planned** | ✅ Yes | ✅ Yes | ❌ No |
| V2X Support | **✅ Roadmap** | ❌ No | ❌ No | ❌ No |

### 6.2 Go-to-Market Strategy

**Target Markets:**
1. **Tier-2/3 OEMs** - Cost-sensitive (BYD, Geely, Tata)
2. **Commercial Fleets** - Telematics providers (Geotab, Samsara)
3. **Aftermarket** - Classic car electrification
4. **Government** - Military/Defense vehicles

**Pricing Strategy:**
- **Pilot:** $1,850/vehicle (includes setup)
- **Volume (1K+):** $485/vehicle
- **Steady-state:** $285/vehicle/year (SaaS model)

---

## 7. DOCUMENTATION IMPROVEMENTS

### 7.1 Technical Documentation

| Document | Current | Improved |
|----------|---------|----------|
| Architecture | Basic diagram | Full ADR (Architecture Decision Records) |
| API | README | OpenAPI 3.0 specification |
| Deployment | Manual | Terraform + Helm charts |
| Security | Basic | Full threat model (STRIDE) |
| Compliance | Checklist | Complete evidence package |

### 7.2 User Documentation

- Investigator handbook (forensic procedures)
- Fleet manager guide (alert response)
- API developer documentation
- Troubleshooting runbooks

---

## 8. IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Months 1-3)
- [ ] Migrate to CM4 Industrial
- [ ] Implement HSM (A71CH)
- [ ] Expand testing to 25 scenarios
- [ ] Deploy ML anomaly detection (basic)

**Cost:** $45,000  
**Risk Reduction:** 40%

### Phase 2: Hardening (Months 4-6)
- [ ] S32K3 PCB design
- [ ] Secure boot implementation
- [ ] Expand testing to 50 scenarios
- [ ] Multi-cloud deployment

**Cost:** $120,000  
**Risk Reduction:** 65%

### Phase 3: Production (Months 7-12)
- [ ] AEC-Q100 qualification
- [ ] Production tooling
- [ ] SOAR integration
- [ ] V2X support (DSRC/C-V2X)

**Cost:** $285,000  
**Risk Reduction:** 80%

### Phase 4: Scale (Months 13-24)
- [ ] 10,000 vehicle deployment
- [ ] Advanced ML models
- [ ] International expansion (EU, China)
- [ ] Autonomous vehicle integration

**Cost:** $850,000  
**Risk Reduction:** 90%

---

## 9. INVESTMENT SUMMARY

| Phase | Investment | Risk Reduction | Cumulative TCO |
|-------|------------|----------------|----------------|
| Current (Prototype) | $65,000 | Baseline | - |
| Phase 1 | $45,000 | 40% | $110,000 |
| Phase 2 | $120,000 | 65% | $230,000 |
| Phase 3 | $285,000 | 80% | $515,000 |
| Phase 4 | $850,000 | 90% | $1,365,000 |

**ROI:** Risk mitigation value of $3M+ vs. $1.37M investment = **2.2x return**

---

## 10. SUCCESS METRICS

### Technical KPIs
| Metric | Current | Target (12 mo) |
|--------|---------|----------------|
| False Positive Rate | Unknown | <5% |
| Detection Latency | ~2s | <500ms |
| System Uptime | N/A | 99.9% |
| Temperature Range | 0-50°C | -40 to +85°C |
| Attack Coverage | 13 | 50+ |

### Business KPIs
| Metric | Current | Target (12 mo) |
|--------|---------|----------------|
| Pilot Customers | 0 | 3 |
| Vehicles Deployed | 1 | 1,000 |
| Revenue | $0 | $500K |
| Cost per Vehicle | $1,850 | $485 |

---

## CONCLUSION

These improvements address all critical and high-risk items from the risk analysis:

✅ **Hardware reliability** → Industrial-grade components  
✅ **Competitive positioning** → Cost advantage + unique features  
✅ **Testing coverage** → 50+ attack scenarios  
✅ **Operational scale** → ML + automation  

**Result:** CEDR transforms from capstone project to production-ready automotive cybersecurity platform.

---

**Next Steps:**
1. Secure Phase 1 funding ($45,000)
2. Form technical advisory board
3. Engage pilot customers (fleet operators)
4. Begin CM4 Industrial migration

**Document Control:**
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | April 9, 2026 | Team Cyber-Torque | Initial improvement plan |
