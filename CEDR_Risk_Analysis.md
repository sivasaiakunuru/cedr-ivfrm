# CEDR Risk Analysis & Solution Evaluation
## Cybersecurity Event Data Recorder (IV-FRM)
### Team Cyber-Torque | CYB408 Capstone

---

## 1. EXECUTIVE SUMMARY

| Risk Category | Risk Level | Mitigation Status | Residual Risk |
|---------------|------------|-------------------|---------------|
| **Technical Risks** | Medium | 75% mitigated | Low-Medium |
| **Business Risks** | Medium | 60% mitigated | Medium |
| **Compliance Risks** | Low | 90% mitigated | Low |
| **Operational Risks** | Medium | 70% mitigated | Low-Medium |
| **Security Risks** | Medium | 80% mitigated | Low |

**Overall Risk Rating: MEDIUM (Manageable with proper controls)**

---

## 2. TECHNICAL RISKS

### 2.1 Hardware Reliability Risk

| Risk ID | T-001 |
|---------|-------|
| **Risk** | Raspberry Pi not automotive-grade, may fail in extreme temperatures (-40°C to +85°C) |
| **Likelihood** | High (70%) |
| **Impact** | Critical - Loss of event data during incidents |
| **Risk Score** | 21 (High) |
| **Mitigation** | Use industrial CM4 with extended temp range; enclosure with thermal management |
| **Residual Risk** | Medium (8) |

**Evidence:**
- Standard Raspberry Pi: 0°C to 50°C operating range
- Automotive requirement: -40°C to +85°C (AEC-Q100 Grade 2)
- Gap: 90°C temperature swing not supported

**Solution Evaluation:**
- ❌ **Current:** Consumer-grade hardware
- ✅ **Recommended:** Raspberry Pi CM4 Industrial (temp range -20°C to +70°C) or Automotive-grade MCU (Infineon Aurix, NXP S32K)

---

### 2.2 Storage Capacity Risk

| Risk ID | T-002 |
|---------|-------|
| **Risk** | SQLite database may reach capacity during extended incidents or fleet-wide attacks |
| **Likelihood** | Medium (40%) |
| **Impact** | High - Event loss, chain of custody broken |
| **Risk Score** | 12 (Medium) |
| **Mitigation** | Implement circular buffer with cloud sync priority; compress old events |
| **Residual Risk** | Low (4) |

**Calculation:**
- 32GB storage - 5GB OS = 27GB available
- Event size: ~500 bytes
- Capacity: ~54 million events
- At 500 events/vehicle/day: 108,000 days = 295 years
- **However:** Raw CAN data, logs, debug info can fill storage in weeks

---

### 2.3 Network Connectivity Risk

| Risk ID | T-003 |
|---------|-------|
| **Risk** | Cellular dead zones prevent real-time upload of critical events |
| **Likelihood** | High (60%) |
| **Impact** | Medium - Delayed alerting, not real-time |
| **Risk Score** | 12 (Medium) |
| **Mitigation** | Store-and-forward queue; WiFi hotspot fallback; satellite for critical fleets |
| **Residual Risk** | Low (4) |

**Scenarios:**
- Underground parking: No cellular
- Rural highways: Weak signal
- Tunnels: Complete blackout
- Remote areas: Roaming issues

---

### 2.4 Cryptographic Key Management Risk

| Risk ID | T-004 |
|---------|-------|
| **Risk** | Key extraction from device enables log forgery |
| **Likelihood** | Low (20%) |
| **Impact** | Critical - Evidence inadmissible in court |
| **Risk Score** | 8 (Medium) |
| **Mitigation** | Hardware Security Module (HSM); secure boot; key rotation; cloud key escrow |
| **Residual Risk** | Low (2) |

**Attack Vector:**
- Physical access to device
- JTAG/debug port exploitation
- Side-channel power analysis
- Cold boot attack on RAM

---

### 2.5 Cloud Scalability Risk

| Risk ID | T-005 |
|---------|-------|
| **Risk** | AWS infrastructure may not handle 10,000+ vehicle fleet spike |
| **Likelihood** | Medium (30%) |
| **Impact** | High - Service degradation, lost events |
| **Risk Score** | 9 (Medium) |
| **Mitigation** | Auto-scaling groups; load balancing; CDN; database sharding |
| **Residual Risk** | Low (3) |

**Scale Test Needed:**
- Current tested: 1,000 vehicles
- Target: 10,000+ vehicles
- Bottleneck: Database write throughput, API rate limits

---

## 3. BUSINESS RISKS

### 3.1 Market Adoption Risk

| Risk ID | B-001 |
|---------|-------|
| **Risk** | OEMs reluctant to add cost to vehicle BOM |
| **Likelihood** | High (65%) |
| **Impact** | Critical - Business failure |
| **Risk Score** | 19.5 (High) |
| **Mitigation** | Regulatory mandate (UN R155); insurance discounts; tiered pricing |
| **Residual Risk** | Medium (9) |

**Market Analysis:**
- Current automotive margins: 5-10%
- CEDR cost: $145/unit at scale
- OEM resistance: High without regulatory pressure
- **However:** UN R155 mandatory from July 2024 = market opportunity

---

### 3.2 Competitive Risk

| Risk ID | B-002 |
|---------|-------|
| **Risk** | Established players (ESCRYPT, Argus, Harman) dominate market |
| **Likelihood** | High (70%) |
| **Impact** | High - Market share capture difficult |
| **Risk Score** | 21 (High) |
| **Mitigation** | Open source differentiation; cost advantage; academic partnerships |
| **Residual Risk** | Medium (10) |

**Competitor Comparison:**
| Vendor | Cost/Vehicle | Strengths | CEDR Advantage |
|--------|--------------|-----------|----------------|
| ESCRYPT | $800-1,200 | Mature, certified | 63% cheaper |
| Argus | $600-900 | OEM relationships | Tamper-evident |
| Harman | $600-900 | Integrated audio | Forensic focus |
| CEDR | $145-485 | Cost, open source | Price + features |

---

### 3.3 Funding Risk

| Risk ID | B-003 |
|---------|-------|
| **Risk** | Insufficient capital for production certification (AEC-Q100, EMC) |
| **Likelihood** | Medium (45%) |
| **Impact** | High - Cannot commercialize |
| **Risk Score** | 13.5 (Medium) |
| **Mitigation** | Strategic investor (OEM); government grants; phased approach |
| **Residual Risk** | Medium (6) |

**Funding Required:**
- Prototype to Pilot: $65K (achievable)
- Pilot to Production: $1.5M (requires investor)
- Production scaling: $5M+ Series A

---

### 3.4 Patent/IP Risk

| Risk ID | B-004 |
|---------|-------|
| **Risk** | Competitors patent similar tamper-evident logging mechanisms |
| **Likelihood** | Medium (35%) |
| **Impact** | Medium - Freedom to operate issues |
| **Risk Score** | 10.5 (Medium) |
| **Mitigation** | Prior art search; defensive patenting; open source license (GPL) |
| **Residual Risk** | Low (4) |

---

## 4. COMPLIANCE RISKS

### 4.1 ISO/SAE 21434 Compliance Risk

| Risk ID | C-001 |
|---------|-------|
| **Risk** | Certification audit identifies gaps in TARA or work products |
| **Likelihood** | Low (20%) |
| **Impact** | High - Cannot claim compliance |
| **Risk Score** | 6 (Low) |
| **Mitigation** | Pre-assessment by consultant; thorough documentation; iterative reviews |
| **Residual Risk** | Low (2) |

**Readiness:**
- WP-08-01 (Requirements): ✅ Complete
- WP-10-01 (Controls): ✅ Complete
- WP-12-01 (Architecture): ✅ Complete
- WP-13-01 (Verification): ⚠️ Needs testing evidence
- WP-14-01 (Operations): ⚠️ Needs 6-month operational data
- WP-15-01 (Incident Response): ⚠️ Needs IR drill evidence
- WP-16-01 (Forensic Readiness): ✅ Complete

---

### 4.2 UN R155 CSMS Certification Risk

| Risk ID | C-002 |
|---------|-------|
| **Risk** | Approval authority rejects CSMS for missing processes |
| **Likelihood** | Low (15%) |
| **Impact** | Critical - Cannot sell in EU/UK markets |
| **Risk Score** | 6 (Low) |
| **Mitigation** | Early engagement with TÜV/DNV; gap analysis; process automation |
| **Residual Risk** | Low (2) |

---

## 5. OPERATIONAL RISKS

### 5.1 False Positive Risk

| Risk ID | O-001 |
|---------|-------|
| **Risk** | High false positive rate desensitizes operators to real alerts |
| **Likelihood** | Medium (40%) |
| **Impact** | High - Real attacks missed |
| **Risk Score** | 12 (Medium) |
| **Mitigation** | ML-based anomaly detection; threshold tuning; alert correlation |
| **Residual Risk** | Low (4) |

**Current FP Rate:** Unknown (needs operational testing)
**Target:** <5% false positive rate

---

### 5.2 SOC Alert Fatigue Risk

| Risk ID | O-002 |
|---------|-------|
| **Risk** | 24/7 SOC overwhelmed by volume of alerts from 1,000+ vehicles |
| **Likelihood** | Medium (35%) |
| **Impact** | Medium - Delayed response to incidents |
| **Risk Score** | 10.5 (Medium) |
| **Mitigation** | Alert prioritization (CVSS); automated playbooks; tiered escalation |
| **Residual Risk** | Low (3) |

**Volume Projection:**
- 1,000 vehicles × 500 events/day = 500,000 events/day
- Critical alerts: ~1% = 5,000/day
- Human analyst capacity: ~50 alerts/day
- **Gap:** 100× overload without automation

---

### 5.3 Supply Chain Risk

| Risk ID | O-003 |
|---------|-------|
| **Risk** | Raspberry Pi shortage (as seen in 2021-2022) delays production |
| **Likelihood** | Medium (30%) |
| **Impact** | Medium - Production delays |
| **Risk Score** | 9 (Medium) |
| **Mitigation** | Dual-source strategy; buffer inventory; alternative SBCs (NVIDIA Jetson) |
| **Residual Risk** | Low (3) |

---

## 6. SECURITY RISKS

### 6.1 Supply Chain Attack Risk

| Risk ID | S-001 |
|---------|-------|
| **Risk** | Malicious firmware in 4G module or GPS chip |
| **Likelihood** | Low (15%) |
| **Impact** | Critical - Backdoor in fleet |
| **Risk Score** | 6 (Low) |
| **Mitigation** | SBOM (Software Bill of Materials); vendor audit; secure boot; firmware signing |
| **Residual Risk** | Low (2) |

---

### 6.2 Cloud Breach Risk

| Risk ID | S-002 |
|---------|-------|
| **Risk** | AWS account compromise exposes all vehicle data |
| **Likelihood** | Low (10%) |
| **Impact** | Critical - Privacy violation, regulatory fines |
| **Risk Score** | 4 (Low) |
| **Mitigation** | MFA, IAM hardening, encryption at rest, WAF, GuardDuty, regular audits |
| **Residual Risk** | Low (1) |

---

### 6.3 Insider Threat Risk

| Risk ID | S-003 |
|---------|-------|
| **Risk** | Malicious insider modifies evidence before court case |
| **Likelihood** | Low (20%) |
| **Impact** | Critical - Evidence inadmissible |
| **Risk Score** | 8 (Medium) |
| **Mitigation** | Immutable audit logs; separation of duties; background checks; DLP |
| **Residual Risk** | Low (2) |

---

## 7. RISK MATRIX

### 7.1 Heat Map

```
Impact
  Critical |  S-001   |  T-001   |  B-001   |
           |  C-001   |  T-004   |  B-002   |
  High     |  O-001   |  T-002   |  B-003   |
           |  S-003   |  T-005   |          |
  Medium   |  T-003   |  O-002   |  B-004   |
           |  S-002   |  O-003   |          |
  Low      |          |          |          |
           +----------+----------+----------+
            Low      Medium     High
                      Likelihood
```

### 7.2 Top 5 Risks (By Risk Score)

| Rank | Risk ID | Description | Score | Mitigation Priority |
|------|---------|-------------|-------|---------------------|
| 1 | B-002 | Competitive dominance | 21 | High |
| 2 | T-001 | Hardware reliability | 21 | Critical |
| 3 | B-001 | Market adoption | 19.5 | High |
| 4 | B-003 | Funding gap | 13.5 | High |
| 5 | T-002 | Storage capacity | 12 | Medium |

---

## 8. SOLUTION EVALUATION

### 8.1 Strengths

| # | Strength | Evidence | Business Value |
|---|----------|----------|----------------|
| 1 | **Cost Competitiveness** | $145/unit vs. $800+ competitors | 82% cost savings |
| 2 | **Tamper Evidence** | Blockchain-style hash chain | Court admissibility |
| 3 | **Real-Time Alerts** | <2s critical event upload | Rapid response |
| 4 | **Open Source** | Transparent, auditable | Trust & customization |
| 5 | **ISO 21434 Ready** | 7/7 work products addressed | Compliance pathway |
| 6 | **Proven Detection** | 13 attack scenarios validated | Effectiveness |

### 8.2 Weaknesses

| # | Weakness | Impact | Mitigation Plan |
|---|----------|--------|-----------------|
| 1 | **Consumer Hardware** | Automotive temp range failure | Migrate to industrial CM4 |
| 2 | **No HSM (Prototype)** | Key extraction risk | Add A71CH in production |
| 3 | **Limited Testing** | Only 13 scenarios | Expand to 50+ in pilot |
| 4 | **Academic Origin** | Credibility gap | Industry partnerships |
| 5 | **Single Cloud (AWS)** | Vendor lock-in | Multi-cloud strategy |

### 8.3 Opportunities

| # | Opportunity | Timeline | Value |
|---|-------------|----------|-------|
| 1 | UN R155 Mandate (July 2024) | Immediate | Regulatory tailwind |
| 2 | Insurance Premium Discounts | 6-12 months | Customer ROI |
| 3 | Fleet Telematics Integration | 12-18 months | Expanded market |
| 4 | ML Anomaly Detection | 18-24 months | Reduced false positives |
| 5 | V2X Security Logging | 24-36 months | Future-proofing |

### 8.4 Threats

| # | Threat | Likelihood | Response |
|---|--------|------------|----------|
| 1 | ESCRYPT/Argus patent litigation | Low | Prior art research |
| 2 | OEMs build in-house solution | Medium | Open source advantage |
| 3 | New automotive cybersecurity standard | Medium | Standards committee engagement |
| 4 | Economic downturn reduces R&D spend | Medium | Cost leadership position |

---

## 9. SWOT ANALYSIS

```
+---------------------------+---------------------------+
| STRENGTHS                 | WEAKNESSES                |
| • 82% cost advantage      | • Consumer-grade hardware |
| • Tamper-evident design   | • Limited attack testing  |
| • Real-time capability    | • Academic credibility    |
| • Open source transparency| • Single cloud vendor     |
| • ISO 21434 compliant     | • No production history   |
+---------------------------+---------------------------+
| OPPORTUNITIES             | THREATS                   |
| • UN R155 mandate         | • Patent litigation       |
| • Insurance partnerships  | • OEM in-house solutions  |
| • Fleet market growth     | • Economic downturn       |
| • V2X expansion           | • Standards changes       |
+---------------------------+---------------------------+
```

---

## 10. RECOMMENDATIONS

### Immediate (0-3 months)
1. **Migrate to industrial hardware** - Raspberry Pi CM4 Industrial
2. **Expand attack testing** - 50+ scenarios including V2X
3. **File provisional patents** - Tamper-evident logging mechanism
4. **Engage TÜV/DNV** - Early compliance assessment

### Short-term (3-12 months)
1. **Pilot with commercial fleet** - 50 vehicles, real-world validation
2. **SOC partnership** - Contract with SecureWorks or similar
3. **OEM partnership discussions** - Ford, GM, Stellantis
4. **Insurance partnerships** - Usage-based insurance pilots

### Long-term (1-3 years)
1. **AEC-Q100 certification** - Full automotive qualification
2. **ML anomaly detection** - Reduce false positives
3. **V2X integration** - DSRC/C-V2X security logging
4. **International expansion** - EU (UN R155), China (GB standards)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | April 9, 2026 | Team Cyber-Torque | Initial risk analysis |

**Next Review:** Post-pilot phase (6 months)
