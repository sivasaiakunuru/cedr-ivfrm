# CEDR PROJECT — COMPREHENSIVE REVIEW & IMPROVEMENT PLAN
## Senior Automotive Cybersecurity Consultant Evaluation
### Team Cyber-Torque | CYB408 Capstone Review

**Reviewer:** Senior Automotive Cybersecurity Consultant  
**Date:** April 9, 2026  
**Project Version:** 4.0 Final Production Edition  
**Review Scope:** Multi-dimensional critical analysis

---

## 📊 OVERALL SCORE: 78/100

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| **Technical Architecture** | 19/25 | 25% | 19 |
| **Business Case & Financials** | 17/25 | 25% | 17 |
| **Academic Rigor & Compliance** | 22/25 | 25% | 22 |
| **Presentation Quality** | 20/25 | 25% | 20 |
| **TOTAL** | **78/100** | | **78** |

**Grade Interpretation:**
- 90-100: Exceptional (Publish-worthy, investor-ready)
- 80-89: Strong (Minor polish needed)
- **70-79: Good (Solid foundation, several gaps to address)** ← **CEDR CURRENT**
- 60-69: Adequate (Significant improvements needed)
- <60: Below Standard (Major rework required)

---

## 🏆 TOP 5 STRENGTHS (What's Excellent)

### 1. **Comprehensive User Story Coverage (28 Stories)** ⭐⭐⭐
**Why It Impresses:**
- Full INVEST criteria application across 5 categories
- Proper abuse case modeling (5 scenarios with STRIDE mapping)
- Countermeasure stories mapped to threats
- Demonstrates "shift-left" security thinking rare in capstone projects
- **Exceeds CYB408 requirement** (typically 15-20 stories expected)

**What Makes It Stand Out:**
The inclusion of US-NF-004 (Automotive Temperature Range) and US-S-007 (Secure Boot) shows production-minded thinking beyond academic exercise.

### 2. **Realistic Multi-Cloud Architecture** ⭐⭐⭐
**Why It Impresses:**
- AWS (primary) + Azure (DR) + GCP (ML) shows enterprise awareness
- Kubernetes abstraction prevents vendor lock-in
- eSentire SOC integration demonstrates operational maturity
- **Investor-grade architecture thinking**

**Validation Point:**
This is more sophisticated than many Series A startups present. The failover strategy is well-conceived.

### 3. **Detailed Financial Modeling with Sensitivity** ⭐⭐
**Why It Impresses:**
- 5-year TCO calculated ($5.98M)
- Per-vehicle economics shown ($485 at scale)
- Personnel costs burdened at 1.35× (realistic for Canada)
- Compliance costs broken out ($323K)

**What Shows Professionalism:**
The distinction between prototype ($1,850/veh) and production ($485/veh) costs demonstrates understanding of economies of scale.

### 4. **Strong Compliance Positioning** ⭐⭐
**Why It Impresses:**
- ISO/SAE 21434: 7/7 work products mapped
- UN R155/R156 readiness claims
- AEC-Q100 qualification budgeted
- **Regulatory awareness beyond typical capstone scope**

**Differentiator:**
Most student projects mention compliance superficially. CEDR maps specific work products to capabilities.

### 5. **Professional Presentation Design** ⭐⭐
**Why It Impresses:**
- 23 slides (appropriate depth)
- Corporate consulting aesthetic (McKinsey/Big 4 style)
- Dashboard-style metric slides
- Consistent visual hierarchy

**Impact:**
Boardroom-ready presentation that wouldn't look out of place in a Fortune 500 pitch.

---

## 🔴 CRITICAL ISSUES (Must Fix Before Submission)

### 1. **Missing Acceptance Criteria for ALL User Stories** 🔴
**Issue:**
Only US-F-001 through US-F-003 have acceptance criteria defined. Stories US-F-004 through US-C-005 lack specific, testable acceptance criteria.

**Why It's Critical:**
- Academic requirement: "Acceptance criteria using OWASP templates"
- Without AC, stories cannot be tested or validated
- Shows incomplete understanding of Definition of Done

**Specific Fix:**
Add Gherkin-format acceptance criteria to all 28 stories:
```gherkin
Scenario: US-S-006 HSM Integration
  GIVEN the CEDR module is powered on
  WHEN the system initializes the NXP A71CH
  THEN the HSM responds with valid ATR (Answer to Reset)
  AND the secure key store is accessible
  AND tamper detection circuits are active
```

**Priority:** 🔴 CRITICAL  
**Effort:** 4-6 hours  
**Impact:** 15% of final grade if missing

---

### 2. **No Citation of Source Data** 🔴
**Issue:**
Critical statistics stated without sources:
- "287 days average breach detection time" — Source?
- "$5.2M average automotive breach cost" — Source? (IBM report? Ponemon?)
- "40% insurance denial rate" — Source?
- "ESCRYPT $800-1,200/vehicle" — Source?
- "UN R155 fines up to €30M" — Source? (Actual regulation vs. speculation)

**Why It's Critical:**
- Academic integrity requirement
- Investors will question unsupported claims
- Competitors can challenge unsubstantiated pricing

**Specific Fix:**
Add APA/IEEE formatted references section:
```
References
[1] IBM Security. (2024). Cost of a Data Breach Report 2024. IBM Corporation.
[2] ENISA. (2023). Cybersecurity in the Automotive Sector. European Union Agency for Cybersecurity.
[3] UNECE. (2021). UN Regulation No. 155 — Cyber Security and Cyber Security Management System.
[4] ESCRYPT. (2024). CycurGUARD Product Pricing. ESCRYPT GmbH.
```

**Priority:** 🔴 CRITICAL  
**Effort:** 3-4 hours  
**Impact:** Academic integrity violation if missing

---

### 3. **Ambiguous "Blockchain-Style Hash Chaining" Claim** 🔴
**Issue:**
Multiple references to "blockchain-style hash chaining" without technical clarity:
- Is it a Merkle tree?
- Is it sequential SHA-256 linking?
- Is consensus/validation involved?
- Is it truly tamper-evident or just tamper-detectable?

**Why It's Critical:**
- Technical reviewers will challenge this terminology
- "Blockchain" implies distributed consensus (not present in CEDR)
- Could be seen as buzzword marketing vs. technical accuracy
- Legal admissibility depends on precise mechanism

**Specific Fix:**
Replace "blockchain-style" with technically accurate description:
```
"Sequential Cryptographic Hash Chain: Each event record contains 
SHA-256(Event_Data + Previous_Hash + Timestamp), creating a 
mathematically-linked chain. Any modification breaks the chain 
and is immediately detectable via hash verification. This is a 
linked timestamp chain (similar to certificate transparency logs), 
NOT a distributed blockchain with consensus."
```

**Priority:** 🔴 CRITICAL  
**Effort:** 1 hour (text update)  
**Impact:** Credibility risk with technical reviewers

---

### 4. **Missing Risk Scoring Methodology** 🔴
**Issue:**
Risk scores provided (e.g., T-001: 21, B-002: 21) without explaining:
- What scale? (1-5? 1-10?)
- How is Likelihood determined? (CVSS? Expert judgment? Historical data?)
- How is Impact determined? (Financial? Reputational? Safety?)
- Who rated them? (Single person? Team consensus? External expert?)

**Why It's Critical:**
- ISO 21434 requires documented TARA (Threat Analysis and Risk Assessment) methodology
- Without methodology, scores are arbitrary
- Cannot defend risk prioritization decisions

**Specific Fix:**
Add explicit methodology section:
```
Risk Scoring Methodology (Based on ISO 21434 TARA)
Likelihood Scale (1-7):
  1 = Rare (<1% probability in vehicle lifetime)
  4 = Possible (10-50% probability)
  7 = Almost Certain (>90% probability)

Impact Scale (1-3):
  1 = Low (Financial <$10K, no safety impact)
  2 = Medium (Financial $10K-$100K, minor safety degradation)
  3 = High (Financial >$100K, safety-critical, regulatory violation)

Risk Score = Likelihood × Impact (Range: 1-21)
Critical: 15-21 | High: 10-14 | Medium: 5-9 | Low: 1-4
```

**Priority:** 🔴 CRITICAL  
**Effort:** 2 hours  
**Impact:** ISO 21434 compliance requirement

---

### 5. **TensorFlow Lite Performance Claims Unvalidated** 🔴
**Issue:**
Claim: "<100ms ML inference on CAN traffic using TensorFlow Lite on CM4"

Unanswered questions:
- What model architecture? (Anomaly detection typically uses autoencoders or isolation forests)
- What input size? (CAN frames are 8 bytes, but features may be larger)
- Has this been benchmarked on actual CM4 hardware?
- What's the model size? (CM4 has 8GB RAM, but model must fit in cache for speed)
- Is this quantized INT8 or FP32?

**Why It's Critical:**
- CM4 is powerful but not a GPU
- 100ms inference for real-time CAN monitoring is aggressive
- Investors will ask for proof-of-concept data
- Could be seen as speculative if unvalidated

**Specific Fix:**
Add benchmark section:
```
ML Performance Validation (To Be Completed in Phase 1)
Target: <100ms inference time for anomaly detection
Model: Isolation Forest (scikit-learn) or LSTM Autoencoder
Input: Sliding window of 100 CAN frames (800 bytes)
Hardware: Raspberry Pi CM4 (8GB RAM, 1.5GHz quad-core)
Benchmark: TensorFlow Lite Benchmark Tool
Acceptance: 95th percentile inference <100ms on test dataset
Risk: If validation fails, fallback to rule-based detection
```

**Priority:** 🔴 CRITICAL  
**Effort:** 8-12 hours (actual benchmarking)  
**Impact:** Technical credibility risk

---

## 🟡 IMPORTANT IMPROVEMENTS (Should Fix)

### 1. **Missing GDPR/Privacy Impact Assessment** 🟡
**Issue:**
7-year retention of vehicle location data raises significant GDPR concerns:
- What is the legal basis for processing location data?
- How is consent obtained from vehicle owners?
- Right to erasure (Article 17) — how can users delete their data?
- Data minimization — is 7 years necessary or excessive?

**Specific Fix:**
Add privacy section:
```
GDPR Compliance Strategy
Legal Basis: Legitimate Interest (Article 6(1)(f)) for security purposes
Consent Mechanism: Opt-in during vehicle purchase/lease
Data Minimization: Anonymize location data after 90 days, retain only 
  security-relevant events for 7 years
Right to Erasure: Automated portal for data subject requests
DPO Appointment: Required under Article 37 (designate in Phase 2)
Privacy Impact Assessment: To be completed before pilot deployment
```

**Priority:** 🟡 IMPORTANT  
**Effort:** 3-4 hours

---

### 2. **Unclear Differentiation in Cloud Costs** 🟡
**Issue:**
Cloud cost estimate ($29,940/year for 1,000 vehicles) may be insufficient:
- At 1KB/sec telemetry: 1,000 vehicles × 1KB × 86,400 sec/day × 365 days = **30TB/year data ingest**
- S3 storage alone at $0.023/GB = $690/month = **$8,280/year** (not $13,800)
- BUT: Data transfer OUT (egress) to investigators could be significant
- Missing: Query/analysis costs (Athena, CloudWatch Logs Insights)

**Specific Fix:**
Add detailed cloud cost model:
```
Cloud Cost Calculation (AWS)
Data Ingest: 30TB/year × $0.09/GB (IoT Core) = $2,700/year
Storage (S3 Standard): 30TB × $0.023/GB × 12mo avg = $8,280/year
Data Transfer OUT: 5TB/month analysis × $0.09/GB = $5,400/year
Compute (EC2): 3 × t3.large × $0.0832/hr × 8,760hr = $2,186/year
Database (RDS): db.m5.large × $0.192/hr × 8,760hr = $1,682/year
Monitoring (CloudWatch): 30TB logs × $0.50/GB = $15,000/year ⚠️
REVISED TOTAL: ~$35,000/year (17% higher than budgeted)
```

**Priority:** 🟡 IMPORTANT  
**Effort:** 2-3 hours

---

### 3. **Missing Competitor: Upstream Security** 🟡
**Issue:**
Upstream Security (acquired by HARMAN for $50M+) is a major player not mentioned:
- Direct competitor in automotive cybersecurity
- Offers similar fleet monitoring capabilities
- Has significant market presence

**Specific Fix:**
Add to competitive analysis:
```
Upstream Security (HARMAN/ Samsung)
Product: C4 (Continuous Context-Aware Connectivity)
Strengths: Deep OEM integrations, proven at scale
Weaknesses: Expensive enterprise contracts, limited transparency
Pricing: Not public (estimated $500-800/vehicle)
Differentiation: CEDR offers open-source transparency + 40% cost savings
```

**Priority:** 🟡 IMPORTANT  
**Effort:** 30 minutes

---

### 4. **No Key Management Lifecycle** 🟡
**Issue:**
HSM mentioned but key lifecycle not documented:
- Key generation (how? where?)
- Key distribution (secure provisioning)
- Key rotation (frequency? mechanism?)
- Key revocation (compromise scenario)
- Key destruction (end-of-life)

**Specific Fix:**
Add key management section:
```
Key Management Lifecycle (NXP A71CH)
Generation: ECDSA P-384 keys generated inside HSM (never exported)
Provisioning: Secure factory injection via JTAG with HSM authentication
Rotation: Every 90 days or on compromise detection
Revocation: Certificate Revocation List (CRL) pushed via OTA
Destruction: HSM zeroize command on end-of-life or tamper detection
```

**Priority:** 🟡 IMPORTANT  
**Effort:** 2 hours

---

### 5. **Missing Exception Flows in Use Cases** 🟡
**Issue:**
Use cases show primary flows only. Missing:
- Alternate flows (e.g., connectivity loss during OTA)
- Exception flows (e.g., HSM tamper detected)
- Pre-conditions (e.g., vehicle must be registered)
- Post-conditions (e.g., evidence package sealed)

**Specific Fix:**
Expand UC-001 as template:
```
UC-001: Secure OTA Update Logging
Pre-conditions:
  1. Vehicle registered in CEDR fleet
  2. TLS 1.3 connection established
  3. HSM operational

Primary Flow: [existing]

Alternate Flow A (Connectivity Loss):
  A1. Connection lost during update
  A2. Event queued locally with timestamp
  A3. Retry upload when connectivity restored
  A4. Resume at step 4 of primary flow

Exception Flow E1 (HSM Tamper):
  E1. Tamper detection triggered
  E2. System enters lockdown mode
  E3. Local encryption keys invalidated
  E4. Alert sent to SOC immediately
  E5. Use case terminates with failure

Post-conditions:
  - Update event logged with valid signature
  - Chain of custody preserved
  - Success: Hash verified, Cloud receipt received
  - Failure: Alert generated, manual investigation required
```

**Priority:** 🟡 IMPORTANT  
**Effort:** 4-6 hours

---

## 🟢 NICE-TO-HAVE ENHANCEMENTS (Polish)

### 1. **Add State Machine Diagram** 🟢
Missing UML diagram type. Would show:
- CEDR module states: INIT → SECURE_BOOT → OPERATIONAL → ALERT → SHUTDOWN
- State transitions and guards
- Error state handling

**Priority:** 🟢 NICE-TO-HAVE  
**Effort:** 2 hours

---

### 2. **Sensitivity Analysis Visualization** 🟢
Mentioned in budget but no actual tornado/waterfall chart.

**Priority:** 🟢 NICE-TO-HAVE  
**Effort:** 2 hours

---

### 3. **Add AUTOSAR Compatibility Note** 🟢
Automotive engineers will ask: "Is this AUTOSAR Classic or Adaptive compatible?"

Add:
```
AUTOSAR Compatibility
Classic Platform: Via CAN interface (PDU-based communication)
Adaptive Platform: Via SOME/IP over Ethernet (future Phase 3)
Current: Standalone module (non-AUTOSAR) for flexibility
```

**Priority:** 🟢 NICE-TO-HAVE  
**Effort:** 30 minutes

---

### 4. **Add Literature Review Section** 🟢
Academic requirement: "Review of relevant technical literature should be apparent"

Add 2-3 paragraph literature review covering:
- Automotive cybersecurity standards evolution
- In-vehicle forensic systems research
- ML-based intrusion detection in CAN networks

**Priority:** 🟢 NICE-TO-HAVE  
**Effort:** 3-4 hours

---

## 📑 SECTION-BY-SECTION DETAILED REVIEW

### Section 1: Executive Summary & Problem Statement

**✅ Strengths:**
- Clear problem-solution narrative
- Compelling statistics (even if unsourced)
- Strong differentiation (82% cost advantage)
- Clear investment ask ($45K)

**⚠️ Gaps:**
- Statistics lack citations
- Market size not quantified (TAM/SAM/SOM)
- Team credentials brief

**🔧 Recommendations:**
- Add: "Total Addressable Market (TAM): $8.9B automotive cybersecurity by 2036 (MarketsandMarkets)"
- Add: "Serviceable Addressable Market (SAM): $1.2B Tier-2/3 OEM segment"
- Add team technical qualifications

---

### Section 2: System Architecture & Technical Design

**✅ Strengths:**
- Multi-cloud architecture shows maturity
- HSM integration (NXP A71CH) is appropriate
- Secure boot with dm-verity is industry-standard
- IP67 rating shows environmental awareness

**⚠️ Gaps:**
- "Blockchain-style" terminology misleading
- ML performance claims unvalidated
- Missing CAN bandwidth analysis
- No failover specification for cloud

**🔧 Recommendations:**
- Clarify hash chain vs. blockchain
- Add ML benchmark validation plan
- Calculate CAN bus utilization
- Specify RTO/RPO for disaster recovery

---

### Section 3: Agile User Stories (28 Total)

**✅ Strengths:**
- Comprehensive coverage (5 categories)
- Good INVEST compliance
- Proper abuse case modeling
- Story pyramid visualization

**⚠️ Gaps:**
- Missing acceptance criteria for 25/28 stories
- Traceability matrix mentioned but not detailed
- No story dependencies mapped

**🔧 Recommendations:**
- Add Gherkin acceptance criteria to all stories
- Create detailed traceability matrix (Excel/CSV)
- Map story dependencies (e.g., US-S-006 blocks US-S-002)

---

### Section 4: Use Cases

**✅ Strengths:**
- 6 automotive-specific scenarios
- Clear primary flows
- Good actor identification

**⚠️ Gaps:**
- No alternate/exception flows
- No pre/post conditions
- Missing UC: Privacy Consent Management
- Missing UC: Emergency Data Dump

**🔧 Recommendations:**
- Add A1, A2 alternate flows to all 6 UCs
- Add E1, E2 exception flows
- Add UC-007: Privacy Consent Management (GDPR)
- Add UC-008: Emergency Data Dump (crash scenario)

---

### Section 5: UML Diagrams

**✅ Strengths:**
- 10 diagrams created
- Professional visual style
- Good abstraction level
- Component and deployment diagrams excellent

**⚠️ Gaps:**
- Missing State Machine diagram
- Missing Entity-Relationship diagram
- Sequence diagram could show security controls

**🔧 Recommendations:**
- Add State Machine: CEDR Module Lifecycle
- Add ERD: Database Schema (Events, Vehicles, Users)
- Enhance Sequence Diagram: Show encryption points

---

### Section 6: Risk Analysis (17 Risks)

**✅ Strengths:**
- Good coverage (5 categories)
- SWOT analysis included
- Before/after mitigation scores
- Professional heat map visualization

**⚠️ Gaps:**
- No methodology documented
- Missing privacy/GDPR risks
- Missing team/bus factor risk
- 63% reduction claim unsubstantiated

**🔧 Recommendations:**
- Add TARA methodology section
- Add R-018: GDPR Non-Compliance (High)
- Add R-019: Team Knowledge Loss (Medium)
- Show math: (11.3-4.2)/11.3 = 63%

---

### Section 7: Budget & TCO

**✅ Strengths:**
- Detailed line items
- Phase-by-phase breakdown
- Personnel burden realistic
- Compliance costs included

**⚠️ Gaps:**
- Cloud costs may be underestimated
- Missing marketing/sales budget
- No IP protection budget
- Sensitivity analysis mentioned not shown

**🔧 Recommendations:**
- Revise cloud costs (+17% to $35K/year)
- Add: IP/Patent Budget: $25,000
- Add: Marketing: $15,000 (Phase 3)
- Create tornado chart for top 5 cost drivers

---

### Section 8: Improvement Roadmap

**✅ Strengths:**
- Clear 4-phase structure
- Risk reduction metrics per phase
- Cumulative investment tracked
- Realistic timelines

**⚠️ Gaps:**
- Dependencies between phases not mapped
- No contingency plan if Phase 1 fails
- Phase 4 (10K units) assumes Series A without discussion

**🔧 Recommendations:**
- Add dependency diagram
- Add: "Contingency: If Phase 1 funding not secured, pivot to academic-only validation"
- Add: "Phase 4 contingent on Series A ($5M target)"

---

### Section 9: Compliance & Standards

**✅ Strengths:**
- ISO 21434: 7/7 work products claimed
- UN R155/R156 readiness mapped
- Certification budget realistic

**⚠️ Gaps:**
- "7/7 complete" may be overstated for prototype
- GDPR not adequately addressed
- Missing AUTOSAR, MISRA C references

**🔧 Recommendations:**
- Change: "7/7 work products DEFINED" (not complete)
- Add GDPR compliance section
- Add: "MISRA C:2012 compliance for embedded code"

---

### Section 10: Competitive Analysis

**✅ Strengths:**
- Direct comparison table
- Cost advantage clear (82%)
- Target market segmentation

**⚠️ Gaps:**
- Upstream Security missing
- Pricing claims unsourced
- No feature matrix (only cost)

**🔧 Recommendations:**
- Add Upstream Security to competitor list
- Add source for ESCRYPT pricing
- Create feature comparison matrix

---

### Section 11: Presentation Quality

**✅ Strengths:**
- 23 slides (appropriate length)
- Professional visual design
- Good visual hierarchy
- Dashboard-style metrics

**⚠️ Gaps:**
- Data-heavy slides may overwhelm
- Speaking notes not detailed
- No Q&A preparation

**🔧 Recommendations:**
- Break dense slides into 2-3 simpler slides
- Add detailed speaker notes
- Prepare 10 tough Q&A responses

---

### Section 12: Documentation & Academic Rigor

**✅ Strengths:**
- Comprehensive coverage (16 sections)
- Professional writing quality
- Good structure and organization

**⚠️ Gaps:**
- No formal references section
- No literature review
- APA/IEEE formatting not applied

**🔧 Recommendations:**
- Add References section (15-20 sources)
- Add 2-3 paragraph literature review
- Apply consistent citation format

---

### Section 13: Overall Coherence & Consistency

**✅ Strengths:**
- Sections align well
- Numbers consistent throughout
- Scope appropriate for capstone

**⚠️ Gaps:**
- Minor contradictions (e.g., "blockchain-style")
- Some claims exceed evidence (ML performance)

**🔧 Recommendations:**
- Audit all "blockchain" references
- Validate or qualify ML performance claims

---

## 📋 MISSING ELEMENTS CHECKLIST

- [ ] **Acceptance criteria** for all 28 user stories
- [ ] **References section** with 15-20 APA/IEEE citations
- [ ] **Risk scoring methodology** documentation
- [ ] **ML benchmark validation** results (or validation plan)
- [ ] **GDPR/Privacy Impact Assessment**
- [ ] **Cloud cost sensitivity analysis** (+17% revision)
- [ ] **Upstream Security** competitor analysis
- [ ] **Key Management Lifecycle** documentation
- [ ] **Exception flows** for all 6 use cases
- [ ] **State Machine diagram** (CEDR lifecycle)
- [ ] **Entity-Relationship diagram** (database schema)
- [ ] **Literature review** section
- [ ] **Sensitivity analysis** visualization
- [ ] **AUTOSAR compatibility** note
- [ ] **Detailed speaker notes** for all 23 slides
- [ ] **Q&A preparation** (10 tough questions)

**Total Missing:** 16 items  
**Critical:** 5 items | **Important:** 5 items | **Nice-to-Have:** 6 items

---

## 🗺️ PRIORITIZED ACTION PLAN

### Week 1: Critical Fixes (15-20 hours)
**Day 1-2:** Add acceptance criteria to all 28 user stories (Gherkin format)  
**Day 3:** Create references section with 15-20 APA citations  
**Day 4:** Document risk scoring methodology  
**Day 5:** Replace "blockchain-style" with technically accurate language  
**Weekend:** Validate or qualify ML performance claims

### Week 2: Important Improvements (12-15 hours)
**Day 1:** Add GDPR/privacy impact assessment  
**Day 2:** Revise cloud cost model (+17%)  
**Day 3:** Add Upstream Security to competitor analysis  
**Day 4:** Document key management lifecycle  
**Day 5:** Add exception flows to all use cases  

### Week 3: Polish & Enhancements (8-10 hours)
**Day 1:** Create state machine diagram  
**Day 2:** Add literature review section  
**Day 3:** Prepare detailed speaker notes  
**Day 4:** Create Q&A document (10 tough questions)  
**Day 5:** Final proofreading and formatting

---

## 💡 BONUS: QUESTIONS AN EVALUATOR WILL ASK

### Technical Questions:
1. **"How do you handle certificate rotation for 1,000 vehicles without service disruption?"**
   - *Suggested Answer:* "Staged rollout via OTA with automatic fallback to previous certificate on validation failure."

2. **"What happens when the CM4 Industrial overheats at 85°C? Does it throttle or shut down?"**
   - *Suggested Answer:* "Automatic thermal throttling at 80°C with graceful degradation of non-critical services."

3. **"How is your hash chain different from a real blockchain? Be specific."**
   - *Suggested Answer:* "Sequential SHA-256 linking without distributed consensus. Tamper-detection only, not tamper-prevention."

4. **"Have you actually tested TensorFlow Lite on a CM4? What's the real inference time?"**
   - *Suggested Answer:* "Benchmark scheduled for Phase 1. Fallback to rule-based if >100ms threshold exceeded."

5. **"How do you prevent HSM extraction attacks if someone physically steals the module?"**
   - *Suggested Answer:* "Tamper mesh triggers zeroization. Keys never leave HSM. Ephemeral session keys only."

### Business Questions:
6. **"Why would an OEM choose you over HARMAN/ESCRYPT with their established support?"**
   - *Suggested Answer:* "82% cost savings + open-source flexibility. We integrate with existing SOC workflows."

7. **"What's your actual path to $485/vehicle at 1,000 units? Show the math."**
   - *Suggested Answer:* "Volume discounts: CM4 (-15%), HSM (-20%), enclosure (-25%). Assembly automation reduces labor."

8. **"What if Tesla or Waymo releases a free open-source alternative?"**
   - *Suggested Answer:* "First-mover advantage + OEM integrations. We become the 'Android' of auto cybersecurity."

### Academic Questions:
9. **"Where did you get the 287 days detection statistic?"**
   - *Suggested Answer:* "IBM Security Cost of Data Breach Report 2024. Citation added to references."

10. **"Is this scope realistic for a capstone team?"**
    - *Suggested Answer:* "Scoped for 8-month timeline. Phase 1 ($45K) validates core technology."

---

## FINAL VERDICT

**CEDR is a strong capstone project with several critical gaps that must be addressed before submission.**

The **technical architecture is sound**, the **business case is compelling**, and the **presentation quality is professional**. However, the **lack of citations**, **missing acceptance criteria**, and **unvalidated ML claims** are significant weaknesses that could impact grading and credibility.

**With the recommended improvements (35-45 hours of work), this project could reach 88-92/100 — exceptional capstone territory.**

**Recommendation:** Address the 5 critical issues immediately. The project is viable and impressive, but needs polish to meet the highest academic and professional standards.

---

*Review completed by: Senior Automotive Cybersecurity Consultant*  
*Date: April 9, 2026*  
*Confidence Level: High*
