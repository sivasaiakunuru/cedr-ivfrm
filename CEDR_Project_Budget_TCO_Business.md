# CEDR Project Budget & Total Cost of Ownership (TCO)
## Cybersecurity Event Data Recorder (IV-FRM)
### Team Cyber-Torque | CYB408 Capstone

**Version 3.0 - Business Implementation (Commercial Pricing)**
**Date:** April 9, 2026

---

## Executive Summary

This document presents a realistic cost model for **commercial deployment** of the CEDR system by an automotive OEM or Tier-1 supplier. All costs reflect market rates for professional services, enterprise software licensing, and production hardware at volume.

| Scenario | CAPEX | OPEX Year 1 | Cost per Vehicle | Timeline |
|----------|-------|-------------|------------------|----------|
| **Prototype** (POC) | $8,500 | $2,000 | $8,500 | 3-6 months |
| **Pilot** (50 vehicles) | $85,000 | $65,000 | $1,700 | 6-12 months |
| **Production** (1,000 vehicles) | $485,000 | $385,000 | $485 | Year 1 |
| **Steady State** (1,000 vehicles) | — | $285,000 | $285/yr | Years 2+ |

**5-Year TCO (1,000 vehicles): $1.89M**

**Payback Period:** 18-24 months (via risk mitigation & insurance savings)

---

## 1. Prototype Phase (Proof of Concept)

### 1.1 Engineering Labor

| Role | Hours | Rate | Total | Notes |
|------|-------|------|-------|-------|
| Security Architect | 80 | $150 | $12,000 | System design, threat modeling |
| Embedded Engineer | 120 | $125 | $15,000 | IV-FRM module development |
| Cloud Engineer | 80 | $130 | $10,400 | Backend infrastructure |
| DevSecOps Engineer | 40 | $140 | $5,600 | CI/CD, security scanning |
| **Labor Subtotal** | **320** | | **$43,000** | |

### 1.2 Hardware BOM (Production-Grade Components)

| Item | Unit Cost | Qty | Total | Source |
|------|-----------|-----|-------|--------|
| Raspberry Pi CM4 (8GB, 32GB eMMC) | $85 | 2 | $170 | Retail pricing |
| Waveshare Industrial CAN HAT | $55 | 2 | $110 | Industrial grade |
| Quectel BG96 4G Module (dev kit) | $95 | 2 | $190 | Development kit |
| u-blox NEO-M8N GPS Module | $28 | 2 | $56 | Professional grade |
| Industrial Enclosure (IP67) | $65 | 2 | $130 | Metal, automotive temp |
| Power Supply (Automotive 12V→5V) | $35 | 2 | $70 | AEC-Q200 qualified |
| Testing Cables & OBD-II | $45 | 1 | $45 | Professional set |
| **Hardware Subtotal** | | | **$771** | |

### 1.3 Software & Tools (Commercial Licenses)

| Item | Annual Cost | Notes |
|------|-------------|-------|
| JetBrains All Products Pack | $780 | Commercial license |
| GitHub Team (10 users) | $480 | Code hosting |
| Snyk Pro (200 tests/month) | $2,400 | Dependency scanning |
| SonarQube Developer | $1,200 | Code quality |
| Draw.io Enterprise | $0 | Free tier sufficient |
| **Software Subtotal** | **$4,860** | |

### 1.4 Testing & Lab Equipment

| Item | Cost | Notes |
|------|------|-------|
| USB-to-CAN Analyzer (Professional) | $350 | Kvaser/PCAN |
| Logic Analyzer (16-channel) | $450 | Saleae Logic Pro |
| Oscilloscope (100MHz) | $1,200 | Rigol/Rohde & Schwarz |
| Automotive Power Supply | $650 | Programmable |
| **Testing Subtotal** | **$2,650** | |

### 1.5 Cloud Services (6-Month POC)

| Service | Monthly | 6-Month | Notes |
|---------|---------|---------|-------|
| AWS EC2 t3.medium | $30 | $180 | Development server |
| AWS RDS PostgreSQL | $65 | $390 | Database |
| S3 Standard (50GB) | $1.15 | $6.90 | Object storage |
| Data Transfer | $8 | $48 | Egress |
| **Cloud Subtotal** | | **$625** | |

### 1.6 Contingency & Miscellaneous

| Item | Cost |
|------|------|
| Shipping & Logistics | $150 |
| Documentation & Technical Writing | $1,200 |
| Legal (IP review, contracts) | $2,500 |
| Contingency (15%) | $7,900 |
| **Misc Subtotal** | **$11,750** | |

### **Prototype Phase Total: $63,656**

*Rounded to **$65,000** for planning purposes*

---

## 2. Pilot Phase (50 Vehicles - Fleet Validation)

### 2.1 Hardware BOM (Low-Volume Production)

| Component | Unit Cost | Qty | Extended | Justification |
|-----------|-----------|-----|----------|---------------|
| Raspberry Pi CM4 (8GB, 32GB eMMC) | $75 | 50 | $3,750 | Small volume discount |
| Custom PCB (6-layer automotive) | $65 | 50 | $3,250 | 6-layer for signal integrity |
| CAN Transceiver (TJA1051T/3) | $4.50 | 50 | $225 | Automotive temp grade |
| 4G Module (Quectel EG25-G) | $58 | 50 | $2,900 | Volume pricing starts |
| GPS Module (NEO-M8N) | $16 | 50 | $800 | Bulk pricing |
| Secure Element (A71CH) | $10 | 50 | $500 | HSM functionality |
| PMIC (Automotive-grade) | $12 | 50 | $600 | TI/Maxim automotive |
| Enclosure (IP67, aluminum) | $45 | 50 | $2,250 | CNC machined |
| Wiring Harness (custom) | $28 | 50 | $1,400 | Automotive grade |
| Assembly (Contract) | $35 | 50 | $1,750 | US-based CM |
| Testing & QC | $15 | 50 | $750 | 100% test coverage |
| **Per Vehicle Cost** | **$290** | | **$14,500** | |

**NRE (Non-Recurring Engineering):**
- PCB Design & Simulation: $18,000 (Altium Designer, signal integrity)
- EMC Pre-compliance Testing: $8,500
- Environmental Testing (Temp/Humidity): $6,500
- Mechanical Design & Tooling: $12,000
- Test Fixture Development: $5,500
- **NRE Total: $50,500**

**Pilot Hardware Total: $65,000**

### 2.2 Engineering Labor (Pilot Phase)

| Role | Hours | Rate | Total |
|------|-------|------|-------|
| Security Architect | 160 | $150 | $24,000 |
| Embedded Engineer | 240 | $125 | $30,000 |
| Cloud Engineer | 160 | $130 | $20,800 |
| DevSecOps Engineer | 120 | $140 | $16,800 |
| QA Engineer | 80 | $110 | $8,800 |
| Project Manager | 80 | $120 | $9,600 |
| **Labor Total** | **840** | | **$110,000** | |

### 2.3 Cloud Infrastructure (50 Vehicles)

| Service | Configuration | Monthly | Annual |
|---------|--------------|---------|--------|
| EC2 (3× t3.medium, HA) | Load balanced | $90 | $1,080 |
| RDS PostgreSQL (Multi-AZ) | db.t3.small | $52 | $624 |
| ElastiCache Redis | cache.t3.micro | $28 | $336 |
| S3 Standard | 10GB + growth | $0.23 | $2.76 |
| CloudWatch Logs | 2GB/day ingestion | $18 | $216 |
| Data Transfer | 20GB/month | $1.80 | $21.60 |
| Route 53 | DNS | $0.50 | $6 |
| **Cloud Total** | | **$191** | **$2,286** | |

### 2.4 Enterprise Software & DevSecOps

| Tool | Annual Cost | Notes |
|------|-------------|-------|
| GitHub Enterprise (25 users) | $6,000 | Advanced security features |
| Snyk Enterprise | $12,000 | Unlimited tests |
| SonarQube Enterprise | $8,000 | 1M lines of code |
| HashiCorp Vault Enterprise | $10,000 | Secrets management |
| Jira + Confluence (25 users) | $3,600 | Project management |
| Datadog APM (50 hosts) | $18,000 | Monitoring & logging |
| **DevSecOps Total** | **$57,600** | |

### 2.5 Compliance & Security Engineering

| Activity | Cost | Provider/Method |
|----------|------|-----------------|
| TARA Workshop (3-day) | $15,000 | External consultant (SynSpace/TÜV) |
| ISO 21434 Gap Assessment | $18,500 | DNV or TÜV SÜD |
| UN R155 CSMS Pre-assessment | $12,000 | Readiness review |
| Penetration Testing (Comprehensive) | $18,000 | CREST-certified firm |
| Security Architecture Review | $8,000 | External security architect |
| Code Audit (Static Analysis) | $6,500 | Specialized firm |
| **Compliance Total** | **$78,000** | |

### 2.6 Operations & Support (Year 1)

| Item | Annual Cost |
|------|-------------|
| 24/7 NOC (Basic) | $36,000 | Outsourced tier-1 |
| Vulnerability Management | $12,000 | Rapid7/Tenable.io |
| Customer Support (Part-time) | $24,000 | Email/ticket support |
| **Operations Total** | **$72,000** | |

### **Pilot Phase Total (50 vehicles, Year 1)**

| Category | Amount |
|----------|--------|
| CAPEX (Hardware + NRE) | $65,000 |
| Engineering Labor | $110,000 |
| Cloud Infrastructure | $2,286 |
| Enterprise Software | $57,600 |
| Compliance & Security | $78,000 |
| Operations | $72,000 |
| **Total Year 1** | **$384,886** |
| **Cost per Vehicle** | **$1,850** |

---

## 3. Production Phase (1,000 Vehicles)

### 3.1 Hardware BOM (Volume Manufacturing)

| Component | Unit Cost (1K) | Volume Discount | Supplier |
|-----------|----------------|-----------------|----------|
| Raspberry Pi CM4 (8GB, 32GB eMMC) | $58 | 32% | Raspberry Pi (bulk) |
| Custom PCB (6-layer, 100mm²) | $12 | Volume 1K+ | JLCPCB/PCBWay |
| CAN Transceiver (TJA1051T/3) | $2.80 | Digi-Key 1K | NXP authorized |
| 4G Module (Quectel EG25-G) | $32 | Volume | Quectel distributor |
| GPS Module (NEO-M8N) | $9 | u-blox volume | Authorized distributor |
| Secure Element (A71CH) | $5.50 | NXP 1K | NXP direct |
| PMIC (Automotive-grade) | $6 | TI volume | TI authorized |
| Enclosure (IP67, die-cast) | $12 | Tooling amortized | Injection mold |
| Wiring Harness | $7 | Contract mfg | Auto wire harness |
| Assembly (China CM) | $9 | Foxconn/Jabil | Turnkey assembly |
| Testing (Automated) | $2.50 | ICT + functional | In-line testing |
| **Hardware per Vehicle** | **$145** | | |

**NRE at Production Scale:**
- PCB Re-spin & Validation: $25,000
- Production Test Fixtures: $15,000
- EMC Full Certification: $35,000 (FCC, CE, IC)
- Automotive Qualification (AEC-Q100): $45,000
- Production Line Setup: $20,000
- **NRE Total: $140,000**

**Production Hardware Total: $285,000 (1,000 × $145 + $140K NRE)**

### 3.2 Engineering Labor (Production Ramp)

| Role | FTE | Annual Salary | Total |
|------|-----|---------------|-------|
| Security Architect | 0.5 | $180,000 | $90,000 |
| Embedded Engineer | 1.0 | $150,000 | $150,000 |
| Cloud Engineer | 1.0 | $160,000 | $160,000 |
| DevSecOps Engineer | 0.5 | $170,000 | $85,000 |
| QA Engineer | 0.5 | $120,000 | $60,000 |
| Product Manager | 0.5 | $140,000 | $70,000 |
| **Labor Total** | **4.0** | | **$615,000** | |

### 3.3 Cloud Infrastructure (1,000 Vehicles)

| Service | Configuration | Monthly | Annual |
|---------|--------------|---------|--------|
| ECS Fargate | Auto-scaling, 10 tasks | $420 | $5,040 |
| RDS PostgreSQL | db.r5.large, Multi-AZ | $285 | $3,420 |
| ElastiCache Redis | 3-node cluster | $145 | $1,740 |
| S3 Standard-IA | 500GB + 15GB/mo | $12 | $144 |
| CloudWatch Logs | 10GB ingestion/day | $68 | $816 |
| CloudFront | Global CDN | $35 | $420 |
| SNS/SQS | High-throughput | $28 | $336 |
| KMS | Key rotation | $15 | $180 |
| **Cloud Total** | | **$1,008** | **$12,096** | |

**Per-Vehicle Cloud Cost:** $12.10/year = $1.01/month

### 3.4 Enterprise Software (Production Scale)

| Tool | Annual Cost | Users/Scale |
|------|-------------|-------------|
| GitHub Enterprise | $20,000 | 100 users |
| Snyk Enterprise | $36,000 | Unlimited |
| SonarQube Enterprise | $18,000 | 5M LOC |
| HashiCorp Vault Enterprise | $25,000 | Production cluster |
| Jira + Confluence Enterprise | $12,000 | 100 users |
| Datadog Enterprise | $48,000 | 1,000+ hosts |
| PagerDuty | $6,000 | On-call management |
| Okta/Auth0 | $9,000 | Identity management |
| **DevSecOps Total** | **$174,000** | |

### 3.5 Compliance & Certification

| Activity | Cost | Frequency |
|----------|------|-----------|
| ISO 21434 Certification Audit | $35,000 | Initial |
| ISO 21434 Surveillance | $18,000 | Annual |
| UN R155 CSMS Certification | $45,000 | Initial |
| UN R155 Surveillance Audit | $22,000 | Annual |
| UN R156 SUMS Assessment | $15,000 | Initial |
| Penetration Testing (quarterly) | $28,000 | 4 × $7,000 |
| Bug Bounty Program | $24,000 | Annual (HackerOne) |
| Third-Party Code Audit | $15,000 | Annual |
| **Compliance Total** | **$202,000** | |

### 3.6 Security Operations (24/7 SOC)

| Item | Annual Cost | Justification |
|------|-------------|---------------|
| Managed SOC (24/7) | $180,000 | Outsourced to SecureWorks/Mandiant |
| SIEM (Splunk/Sentinel) | $45,000 | 50GB/day ingestion |
| Threat Intelligence | $18,000 | Recorded Future/Mandiant |
| Incident Response Retainer | $36,000 | External IR firm |
| Vulnerability Management | $24,000 | Continuous scanning |
| OTA Update Infrastructure | $18,000 | Signing, hosting, delivery |
| **Operations Total** | **$321,000** | |

### 3.7 Customer Support & Success

| Item | Annual Cost |
|------|-------------|
| Customer Success Manager | $85,000 | 1 FTE |
| Technical Support (Tier 2) | $65,000 | 1 FTE |
| Documentation & Training | $15,000 | Video, guides |
| **Support Total** | **$165,000** | |

### **Production Phase Total (1,000 vehicles)**

| Category | Year 1 | Years 2-3 (each) |
|----------|--------|------------------|
| CAPEX (Hardware + NRE) | $285,000 | $50,000* |
| Engineering Labor | $615,000 | $615,000 |
| Cloud Infrastructure | $12,096 | $13,305 (+10%) |
| Enterprise Software | $174,000 | $191,400 (+10%) |
| Compliance | $202,000 | $75,000 (surveillance only) |
| Security Operations | $321,000 | $353,100 (+10%) |
| Customer Support | $165,000 | $181,500 (+10%) |
| **Total Annual** | **$1,774,096** | **$1,479,305** |
| **Cost per Vehicle** | **$485** | **$405** |

*Year 2+: Hardware refresh (150 units/year replacement)

---

## 4. TCO Summary (5-Year Projection)

### 4.1 5-Year TCO (1,000 Vehicles - Business Implementation)

| Year | Phase | CAPEX | OPEX | Annual Total | Cumulative |
|------|-------|-------|------|--------------|------------|
| 1 | Prototype | $65,000 | $2,000 | $67,000 | $67,000 |
| 2 | Pilot (50) | $65,000 | $319,886 | $384,886 | $451,886 |
| 3 | Production Deploy (1K) | $285,000 | $1,489,096 | $1,774,096 | $2,225,982 |
| 4 | Operations | $50,000 | $1,479,305 | $1,529,305 | $3,755,287 |
| 5 | Operations + Refresh | $50,000 | $1,627,236 | $1,677,236 | $5,432,523 |

**Total 5-Year TCO: $5.43M**

### 4.2 Cost Per Vehicle Over Time

| Phase | Vehicles | Cost per Vehicle | Notes |
|-------|----------|------------------|-------|
| Prototype | 1 | $65,000 | Engineering-heavy |
| Pilot | 50 | $1,850 | Low volume premium |
| Production Y1 | 1,000 | $485 | Scale efficiencies |
| Steady State | 1,000 | $405 | Optimized operations |
| **5-Year Average** | 1,000 | **$1,085** | Fully-loaded |

---

## 5. ROI & Business Case

### 5.1 Risk Mitigation Value

| Risk Without CEDR | Probability | Impact | Expected Loss |
|-------------------|-------------|--------|---------------|
| Fleet-wide cyber attack | 5% | $10M | $500,000 |
| Regulatory fines (UN R155) | 10% | $500K | $50,000 |
| Insurance premium increase | 30% | $300K | $90,000 |
| Brand reputation damage | 15% | $2M | $300,000 |
| **Annual Expected Loss** | | | **$940,000** |

### 5.2 ROI Analysis

| Metric | Value |
|--------|-------|
| CEDR Investment (5-year TCO) | $5.43M |
| Risk Reduction (40% of expected loss) | $376,000/year |
| Insurance premium savings | $120,000/year |
| Compliance avoidance (fines) | $50,000/year |
| **Annual Benefit** | **$546,000** |
| **Simple Payback Period** | **9.9 years** |
| **NPV (10% discount, 5 years)** | **-$3.2M** |

**Note:** Direct ROI is negative, but **strategic value includes:**
- Regulatory compliance (mandatory for UN R155)
- Market differentiation (cybersecurity as selling point)
- Insurance eligibility (some carriers require security systems)
- Customer trust & brand protection (intangible)

### 5.3 Competitive Comparison

| Solution | Cost per Vehicle | Notes |
|----------|------------------|-------|
| CEDR (Our Solution) | $485 | Open source, customizable |
| ESCRYPT CycurVAULT | $800-1,200 | Commercial HSM solution |
| Harman SHIELD | $600-900 | Telematics security |
| Argus Connectivity Protection | $500-750 | Aftermarket solution |

**CEDR is cost-competitive vs. commercial alternatives.**

---

## 6. Funding & Partnership Options

### 6.1 Recommended Approach

| Phase | Funding Source | Amount | Timeline |
|-------|---------------|--------|----------|
| Prototype | Internal R&D | $65,000 | Q1-Q2 |
| Pilot | Strategic Investor / Grant | $385,000 | Q3-Q4 |
| Production | OEM Partnership | $1.77M | Year 2+ |

### 6.2 Potential Partners

- **OEMs:** Ford, GM, Stellantis (cybersecurity investment arms)
- **Tier-1s:** Bosch, Continental, Denso (supplier programs)
- **VCs:** Automotive-focused (Fontinalis, Trucks VC)
- **Grants:** NIST, DoE (automotive cybersecurity research)

---

## 7. Assumptions & Constraints

### 7.1 Key Assumptions

| Assumption | Basis |
|------------|-------|
| Labor rates $110-180K | Market rate for cybersecurity engineers (Indeed, Glassdoor) |
| Hardware at volume: $145 | Supplier quotes for 1K+ units |
| Cloud: $12/vehicle/year | AWS pricing validated |
| SOC: $180K/year | SecureWorks/Mandiant managed SOC pricing |
| Compliance: $202K Y1 | TÜV SÜD/DNV certification costs |

### 7.2 Constraints

- All pricing in USD
- North American labor market
- AWS cloud infrastructure
- 1,000 vehicle fleet size (economies of scale apply)
- 5-year hardware refresh cycle

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.0 | April 9, 2026 | Team Cyber-Torque | Business implementation pricing |

**Prepared by:** Team Cyber-Torque  
**Status:** Final for business planning

---

*This budget reflects commercial market rates for professional automotive cybersecurity deployment. All costs are estimates based on industry research and should be validated with actual vendor quotes prior to implementation.*
