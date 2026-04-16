# CEDR - Cybersecurity Event Data Recorder

> In-Vehicle Forensic Readiness Module for Connected Vehicles

[![Project Status](https://img.shields.io/badge/status-capstone%20project-blue)](https://github.com/sivasaiakunuru/cedr-ivfrm)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Compliance](https://img.shields.io/badge/compliance-ISO%2021434%20%7C%20UN%20R155%2FR156-orange)](docs/compliance.md)

---

## Overview

CEDR (Cybersecurity Event Data Recorder) is an in-vehicle forensic readiness module designed to detect, record, and preserve cybersecurity events in connected vehicles. When cyber attacks occur, CEDR provides tamper-evident evidence for forensic investigation and insurance claims.

### The Problem
- Modern vehicles contain **100+ ECUs** generating terabytes of data
- **No standardized security event logging** exists today
- Average breach detection time: **287 days**
- Insurance claim denial rate: **40%**
- Regulatory fines under UN R155: up to **€30M**

### The Solution
CEDR provides:
- ⚡ **Real-time detection** (<500ms latency)
- 🔐 **Tamper-evident logging** via cryptographic hash chaining
- 🤖 **ML-based anomaly detection** (<5% false positives)
- 📊 **Full compliance** with ISO 21434 + UN R155/R156
- 💰 **82% cost advantage** over competitors ($485 vs $800-1,200/vehicle)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VEHICLE EDGE                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CEDR Module (Raspberry Pi CM4 Industrial)           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │ CAN Bus     │  │ GPS/GNSS    │  │ 4G/LTE      │  │  │
│  │  │ Interface   │  │ Receiver    │  │ Cellular    │  │  │
│  │  └──────┬──────┘  └─────────────┘  └─────────────┘  │  │
│  │         │                                            │  │
│  │  ┌──────▼────────────────────────────────────────┐  │  │
│  │  │  Core Processing                               │  │  │
│  │  │  • Event detection engine                     │  │  │
│  │  │  • ML Inference (TensorFlow Lite)            │  │  │
│  │  │  • Hash chain verification                    │  │  │
│  │  │  • AES-256-GCM encryption                     │  │  │
│  │  └──────┬────────────────────────────────────────┘  │  │
│  │         │                                            │  │
│  │  ┌──────▼──────────────┐  ┌─────────────────────┐  │  │
│  │  │ NXP A71CH HSM       │  │ Tamper Detection    │  │  │
│  │  │ • Secure key storage│  │ • Enclosure breach  │  │  │
│  │  │ • Crypto acceleration│ │ • Temperature       │  │  │
│  │  └─────────────────────┘  └─────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ Encrypted TLS 1.3
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 CLOUD INFRASTRUCTURE                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   AWS    │  │  Azure   │  │   GCP    │                  │
│  │(Primary) │  │ (Backup) │  │  (ML)    │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       └─────────────┼─────────────┘                         │
│                     ▼                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Kubernetes Cluster                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐             │  │
│  │  │ API      │ │ Event    │ │ ML       │             │  │
│  │  │ Gateway  │ │ Processor│ │ Inference│             │  │
│  │  └──────────┘ └──────────┘ └──────────┘             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Documents

### Core Documentation
| Document | Description |
|----------|-------------|
| [CEDR_COMPLETE_PROJECT_GUIDE.md](CEDR_COMPLETE_PROJECT_GUIDE.md) | Master guide with all deliverables |
| [CEDR_FINAL_DOCUMENT_v5.md](CEDR_FINAL_DOCUMENT_v5.md) | Comprehensive fixed edition (32 IEEE refs) |
| [CEDR_MASTER_DOCUMENT.md](CEDR_MASTER_DOCUMENT.md) | Integrated deliverables reference |
| [CEDR_CRITICAL_REVIEW.md](CEDR_CRITICAL_REVIEW.md) | Consultant evaluation (78/100) |

### Technical Specifications
| Document | Description |
|----------|-------------|
| [CEDR_User_Stories.md](CEDR_User_Stories.md) | 28 agile user stories |
| [CEDR_Risk_Analysis.md](CEDR_Risk_Analysis.md) | 17 risks + SWOT analysis |
| [CEDR_Project_Budget_TCO.md](CEDR_Project_Budget_TCO.md) | 5-year TCO analysis ($5.98M) |
| [CEDR_Improvement_Plan.md](CEDR_Improvement_Plan.md) | 4-phase improvement roadmap |
| [CEDR_UML_Diagrams.md](CEDR_UML_Diagrams.md) | UML diagram specifications |

### Presentations
| File | Slides | Description |
|------|--------|-------------|
| [CEDR_Final_Presentation_35_with_Images.pptx](CEDR_Final_Presentation_35_with_Images.pptx) | 35 | Complete presentation with images |
| [CEDR_Professional_Presentation.pptx](CEDR_Professional_Presentation.pptx) | 23 | Professional pitch deck |
| [CEDR_Final_Presentation_35_Complete.pptx](CEDR_Final_Presentation_35_Complete.pptx) | 35 | Full presentation |

---

## Quick Stats

- **28 User Stories** (functional, security, abuse cases, countermeasures)
- **6 Use Cases** covering OTA logging, intrusion detection, forensics
- **10 UML Diagrams** (component, deployment, class, use case, sequence, activity)
- **17 Risk Analysis** with NIST methodology
- **$5.98M 5-Year TCO** for 1,000 vehicles
- **$485/vehicle** at production scale (82% cost advantage)

---

## Project Roadmap

| Phase | Investment | Timeline | Risk Reduction |
|-------|------------|----------|----------------|
| **Phase 1: Foundation** | $45,000 | Months 1-3 | 40% |
| **Phase 2: Hardening** | $120,000 | Months 4-6 | 65% |
| **Phase 3: Production** | $285,000 | Months 7-12 | 80% |
| **Phase 4: Scale** | $850,000 | Months 13-24 | 90% |
| **Total** | **$1.37M** | 24 months | - |

---

## Compliance

- ✅ **ISO/SAE 21434** - Cybersecurity Engineering (7/7 work products)
- ✅ **UN R155** - Cybersecurity Management System (CSMS)
- ✅ **UN R156** - Software Update Management System (SUMS)
- ✅ **AEC-Q100** - Automotive qualification (Phase 3)

---

## Team

**Team Cyber-Torque**
- Course: CYB408-26W-001 Automobility Cybersecurity CAP
- Institution: St. Clair College
- Location: Windsor, ON

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- St. Clair College Cybersecurity Program
- CYB408 Capstone Advisors
- Industry consultants and reviewers

---

**Note:** This is a capstone project. The prototype demonstrates core concepts while the production roadmap outlines path to commercialization.