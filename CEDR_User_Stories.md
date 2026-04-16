# CEDR User Stories
## Cybersecurity Event Data Recorder (IV-FRM)
### Team Cyber-Torque | CYB408 Capstone

---

## Table of Contents
1. [Functional User Stories](#1-functional-user-stories) (7 stories)
2. [Non-Functional User Stories](#2-non-functional-user-stories) (4 stories)
3. [Security User Stories](#3-security-user-stories) (7 stories)
4. [Abuse (Evil) User Stories](#4-abuse-evil-user-stories) (5 stories)
5. [Countermeasure User Stories](#5-countermeasure-user-stories) (5 stories)
6. [Traceability Matrix](#6-traceability-matrix)

**Total: 28 User Stories** (Updated with Professional Improvements)

---

## 1. Functional User Stories

### US-F-001: Real-Time Security Alerting
**As a** fleet security manager,  
**I want** to receive immediate alerts when a vehicle detects a cyber attack,  
**So that** I can respond to security incidents within seconds and minimize damage.  

**Acceptance Criteria:**
- Critical events trigger alerts within 2 seconds
- Alerts include vehicle ID, attack type, timestamp, and location
- Alerts delivered via dashboard, email, and SMS
- Alert severity levels: CRITICAL, HIGH, MEDIUM, LOW

**Priority:** HIGH  
**Estimate:** 8 story points

---

### US-F-002: Forensic Evidence Retrieval
**As a** forensic investigator,  
**I want** to search and retrieve complete security event logs from any vehicle,  
**So that** I can reconstruct the timeline of a cyber incident for legal proceedings.

**Acceptance Criteria:**
- Search by vehicle ID, date range, event type, severity
- Export evidence packages in tamper-evident format
- Include chain of custody documentation
- Support PDF and JSON export formats

**Priority:** HIGH  
**Estimate:** 13 story points

---

### US-F-003: Fleet-Wide Attack Correlation
**As a** CISO (Chief Information Security Officer),  
**I want** to identify coordinated attacks across multiple vehicles in my fleet,  
**So that** I can detect and respond to large-scale cyber campaigns.

**Acceptance Criteria:**
- Cross-vehicle event correlation by attack signature
- Timeline visualization of fleet-wide incidents
- Automated correlation scoring (0-100% match confidence)
- Alert when similar attack patterns detected across >2 vehicles

**Priority:** MEDIUM  
**Estimate:** 8 story points

---

### US-F-004: Secure OTA Update Logging
**As an** OEM software engineer,  
**I want** all firmware updates to be cryptographically logged,  
**So that** I can verify no unauthorized modifications occurred during OTA deployment.

**Acceptance Criteria:**
- Log firmware version before and after update
- Capture digital signature of update package
- Record update success/failure status
- Store installer authentication credentials

**Priority:** HIGH  
**Estimate:** 5 story points

---

### US-F-005: Vehicle Health Dashboard
**As a** vehicle owner,  
**I want** to view my vehicle's cybersecurity status on a mobile app,  
**So that** I can stay informed about potential security risks.

**Acceptance Criteria:**
- Display overall security score (0-100)
- Show recent security events (last 30 days)
- Provide recommendations for security improvements
- Option to share data with insurance for discounts

**Priority:** MEDIUM  
**Estimate:** 8 story points

---

### US-F-006: Compliance Reporting
**As a** compliance officer,  
**I want** automated generation of ISO/SAE 21434 compliance reports,  
**So that** I can demonstrate regulatory adherence during audits.

**Acceptance Criteria:**
- Generate reports mapping to ISO 21434 work products
- Include TARA (Threat Analysis and Risk Assessment) summaries
- Evidence of security monitoring and incident response
- Automated quarterly report generation

**Priority:** HIGH  
**Estimate:** 8 story points

---

### US-F-007: ML-Based Anomaly Detection ⭐ NEW
**As a** SOC analyst,  
**I want** machine learning-based anomaly detection with low false positive rates,  
**So that** I can focus on real threats instead of wasting time on false alarms.

**Acceptance Criteria:**
- False positive rate < 5% (vs 20-30% rule-based)
- Detection latency < 500ms for ML inference
- Adaptive thresholds based on vehicle behavior baselines
- Integration with TensorFlow Lite on edge device
- Continuous model updates from cloud
- Explainable AI (XAI) features showing why alert triggered

**Priority:** HIGH  
**Estimate:** 13 story points

---

## 2. Non-Functional User Stories

### US-NF-001: Performance Under Load
**As a** system architect,  
**I want** the CEDR system to handle 1,000 concurrent vehicle connections,  
**So that** the solution scales to enterprise fleet deployments.

**Acceptance Criteria:**
- Event capture latency < 10ms at 1,000 concurrent vehicles
- Database queries complete in < 500ms
- 99.9% uptime during peak hours
- Auto-scaling cloud infrastructure

**Priority:** HIGH  
**Estimate:** 13 story points

---

### US-NF-002: Data Retention Policy
**As a** data protection officer,  
**I want** configurable data retention policies,  
**So that** we comply with GDPR and regional privacy regulations.

**Acceptance Criteria:**
- Configurable retention periods (1-7 years)
- Automated data purging after retention period
- Anonymization options for PII data
- Audit trail of data deletion operations

**Priority:** MEDIUM  
**Estimate:** 5 story points

---

### US-NF-003: Cross-Platform Compatibility
**As an** IT administrator,  
**I want** the investigator dashboard to work on all major browsers,  
**So that** investigators can access evidence from any workstation.

**Acceptance Criteria:**
- Support Chrome, Firefox, Safari, Edge (latest 2 versions)
- Responsive design for tablets
- Offline mode for field investigations
- Mobile app for iOS and Android

**Priority:** MEDIUM  
**Estimate:** 8 story points

---

### US-NF-004: Automotive Temperature Range ⭐ NEW
**As a** vehicle manufacturer,  
**I need** CEDR to operate reliably from -40°C to +85°C,  
**So that** it functions in all automotive environments including extreme climates.

**Acceptance Criteria:**
- Full operational capability at -40°C (cold start in arctic conditions)
- Full operational capability at +85°C (dashboard in desert sun)
- Automatic thermal throttling to prevent damage
- Temperature monitoring with alerts at -35°C and +80°C
- Use of automotive-grade components (AEC-Q100 qualified)
- IP67 enclosure rating for dust/water protection

**Priority:** CRITICAL  
**Estimate:** 21 story points

---

## 3. Security User Stories

### US-S-001: Tamper Evidence Detection
**As a** forensic auditor,  
**I want** cryptographic proof if anyone attempts to modify logged events,  
**So that** evidence integrity is guaranteed for legal proceedings.

**Acceptance Criteria:**
- Blockchain-style hash chaining for all events
- Immediate flagging of hash chain breaks
- Immutable cloud backup prevents local tampering
- Digital signatures verify data authenticity

**Priority:** CRITICAL  
**Estimate:** 13 story points  
**OWASP Reference:** [Security User Stories - Integrity](https://github.com/OWASP/user-security-stories)

---

### US-S-002: Encrypted Data Transmission
**As a** security engineer,  
**I want** all vehicle-to-cloud communications encrypted,  
**So that** attackers cannot intercept sensitive security data in transit.

**Acceptance Criteria:**
- TLS 1.3 for all API communications
- AES-256-GCM for payload encryption
- Perfect forward secrecy (PFS) enabled
- Certificate pinning on vehicle module

**Priority:** CRITICAL  
**Estimate:** 8 story points  
**OWASP Reference:** [ASVS 9.1 - HTTPS](https://owasp-aasvs.readthedocs.io/en/latest/V9.html)

---

### US-S-003: Multi-Factor Authentication
**As a** system administrator,  
**I want** MFA required for all investigator dashboard access,  
**So that** stolen credentials alone cannot compromise forensic evidence.

**Acceptance Criteria:**
- Support TOTP (Google Authenticator, Authy)
- Hardware security key support (FIDO2/WebAuthn)
- Biometric authentication for mobile app
- Session timeout after 15 minutes inactivity

**Priority:** HIGH  
**Estimate:** 8 story points  
**OWASP Reference:** [Security User Stories - Authentication](https://github.com/OWASP/user-security-stories)

---

### US-S-004: Role-Based Access Control
**As a** security officer,  
**I want** granular permissions based on investigator roles,  
**So that** users only access evidence relevant to their authorization level.

**Acceptance Criteria:**
- Roles: Admin, Senior Investigator, Investigator, Auditor, Read-Only
- Vehicle-level access restrictions
- Action-level permissions (view, export, delete)
- Audit log of all access attempts

**Priority:** HIGH  
**Estimate:** 8 story points

---

### US-S-005: Secure Key Management
**As a** cryptography specialist,  
**I want** encryption keys stored in Hardware Security Modules (HSM),  
**So that** keys cannot be extracted even if the server is compromised.

**Acceptance Criteria:**
- Integration with AWS CloudHSM or Azure Dedicated HSM
- Key rotation every 90 days
- Separation of duties for key custodians
- FIPS 140-2 Level 3 compliance

**Priority:** HIGH  
**Estimate:** 13 story points

---

### US-S-006: Hardware Security Module (HSM) Integration ⭐ NEW
**As a** security architect,  
**I want** all cryptographic operations performed in a dedicated secure element (NXP A71CH),  
**So that** private keys never leave hardware protection and are immune to extraction attacks.

**Acceptance Criteria:**
- NXP A71CH secure element integration on vehicle module
- All key generation performed inside HSM
- Private keys non-exportable from secure element
- Hardware acceleration for AES-256 and ECDSA operations
- Secure key injection during manufacturing
- Tamper detection and zeroization on physical attack
- FIPS 140-2 Level 2 (or higher) compliance

**Priority:** CRITICAL  
**Estimate:** 13 story points

---

### US-S-007: Secure Boot with Measured Boot ⭐ NEW
**As a** system architect,  
**I want** cryptographically verified boot sequence for the CEDR module,  
**So that** only authentic firmware can execute and any tampering is detected before runtime.

**Acceptance Criteria:**
- U-Boot with RSA/ECDSA signature verification
- Chain of trust from ROM to kernel to application
- dm-verity for root filesystem integrity
- Measured boot with TPM/TEE attestation
- Signed OTA updates with rollback protection
- Automatic recovery mode on verification failure
- Audit logging of all boot attempts (success and failure)

**Priority:** CRITICAL  
**Estimate:** 13 story points

---

## 4. Abuse (Evil) User Stories

### US-A-001: Log Tampering Attempt
**As an** attacker who has compromised a vehicle,  
**I want** to delete or modify security event logs,  
**So that** I can hide evidence of my attack.

**Abuse Scenario:**
- Attacker gains root access to IV-FRM module
- Attempts to delete SQLite database entries
- Tries to modify existing event records
- Attempts to inject false events to confuse investigators

**Threat Level:** HIGH  
**STRIDE Category:** Tampering, Repudiation

---

### US-A-002: Man-in-the-Middle Attack
**As an** attacker on the cellular network,  
**I want** to intercept and modify vehicle-to-cloud communications,  
**So that** I can steal sensitive data or inject malicious commands.

**Abuse Scenario:**
- Attacker sets up rogue cell tower (IMSI catcher)
- Intercepts 4G/5G traffic from vehicle
- Attempts to decrypt or replay captured packets
- Injects fake events to trigger false alerts

**Threat Level:** CRITICAL  
**STRIDE Category:** Information Disclosure, Tampering

---

### US-A-003: Insider Threat - Data Theft
**As a** malicious insider with dashboard access,  
**I want** to exfiltrate sensitive forensic data,  
**So that** I can sell it to competitors or adversaries.

**Abuse Scenario:**
- Authorized user downloads large volumes of event data
- Attempts to export beyond their vehicle assignment
- Uses screen recording to capture sensitive information
- Shares credentials with unauthorized third parties

**Threat Level:** HIGH  
**STRIDE Category:** Information Disclosure

---

### US-A-004: Replay Attack
**As an** attacker on the CAN bus,  
**I want** to capture and replay legitimate security events,  
**So that** I can overwhelm the system with noise or trigger false responses.

**Abuse Scenario:**
- Attacker records valid CEDR event transmissions
- Replays old events with modified timestamps
- Floods cloud backend with duplicate events
- Attempts to exhaust storage or processing capacity

**Threat Level:** MEDIUM  
**STRIDE Category:** Tampering, Denial of Service

---

### US-A-005: Privilege Escalation
**As an** attacker with limited dashboard access,  
**I want** to escalate my permissions to admin level,  
**So that** I can access all evidence and modify system configurations.

**Abuse Scenario:**
- Attacker exploits vulnerability in access control logic
- Manipulates JWT tokens to add admin privileges
- Exploits SQL injection in search functions
- Uses session fixation to hijack admin sessions

**Threat Level:** CRITICAL  
**STRIDE Category:** Elevation of Privilege

---

## 5. Countermeasure User Stories

### US-C-001: Immutable Audit Trail
**As a** system defender,  
**I want** all access attempts logged to append-only storage,  
**So that** attackers cannot cover their tracks even if they compromise the system.

**Countermeasure For:** US-A-001 (Log Tampering)  
**Acceptance Criteria:**
- Write-once storage (WORM) for audit logs
- Separate infrastructure from main application
- Real-time alerting on unusual access patterns
- Offsite backup to air-gapped system

**Priority:** CRITICAL  
**Estimate:** 8 story points

---

### US-C-002: Certificate Pinning & Mutual TLS
**As a** security architect,  
**I want** mutual authentication between vehicle and cloud,  
**So that** MITM attacks are detected and blocked.

**Countermeasure For:** US-A-002 (MITM Attack)  
**Acceptance Criteria:**
- Client certificates on each vehicle module
- Certificate pinning prevents CA compromise
- mTLS required for all API endpoints
- Automatic certificate revocation on compromise detection

**Priority:** CRITICAL  
**Estimate:** 8 story points

---

### US-C-003: Data Loss Prevention (DLP)
**As a** security operations manager,  
**I want** automated monitoring for data exfiltration,  
**So that** insider threats are detected before significant damage occurs.

**Countermeasure For:** US-A-003 (Insider Threat)  
**Acceptance Criteria:**
- Monitor bulk download activities
- Alert when export thresholds exceeded
- Block transfers to untrusted domains
- Screen capture detection on dashboard

**Priority:** HIGH  
**Estimate:** 8 story points

---

### US-C-004: Replay Attack Detection
**As a** detection engineer,  
**I want** the system to detect and drop replayed events,  
**So that** attackers cannot inject stale or duplicate data.

**Countermeasure For:** US-A-004 (Replay Attack)  
**Acceptance Criteria:**
- Timestamp validation with 30-second window
- Event deduplication using hash of content
- Nonce verification for each transmission
- Rate limiting per vehicle (max 100 events/minute)

**Priority:** MEDIUM  
**Estimate:** 5 story points

---

### US-C-005: Zero-Trust Architecture
**As a** security architect,  
**I want** continuous verification of all access requests,  
**So that** privilege escalation attempts are blocked at multiple layers.

**Countermeasure For:** US-A-005 (Privilege Escalation)  
**Acceptance Criteria:**
- Every request re-validates permissions
- JWT tokens signed with rotating keys
- API Gateway enforces rate limits
- Behavioral analytics detect anomalous access patterns

**Priority:** HIGH  
**Estimate:** 13 story points

---

## 6. Traceability Matrix

| User Story | Type | Requirement | Threat/Abuse | Test Method | Component |
|------------|------|-------------|--------------|-------------|-----------|
| US-F-001 | Functional | Alert Generation | - | Unit Test | Cloud Backend |
| US-F-002 | Functional | Evidence Retrieval | - | Integration Test | Dashboard |
| US-F-003 | Functional | Fleet Analytics | - | System Test | Correlation Engine |
| US-F-004 | Functional | OTA Logging | - | Unit Test | IV-FRM Module |
| US-F-005 | Functional | Health Dashboard | - | UI Test | Dashboard |
| US-F-006 | Functional | Compliance Reports | - | Audit Test | Cloud Backend |
| US-F-007 | Functional | ML Anomaly Detection | - | ML Testing | Edge/Cloud |
| US-NF-001 | Non-Functional | Performance | - | Load Test | Cloud Backend |
| US-NF-002 | Non-Functional | Data Retention | - | Compliance Test | Cloud Backend |
| US-NF-003 | Non-Functional | Cross-Platform | - | Compatibility Test | Dashboard |
| US-NF-004 | Non-Functional | Temperature Range | - | Environmental Test | IV-FRM Module |
| US-S-001 | Security | Tamper Evidence | US-A-001 | Penetration Test | IV-FRM Module |
| US-S-002 | Security | Encryption | US-A-002 | Security Audit | Cloud Backend |
| US-S-003 | Security | MFA | US-A-003 | Security Test | Dashboard |
| US-S-004 | Security | RBAC | US-A-005 | Access Control Test | Dashboard |
| US-S-005 | Security | Key Management | - | Security Audit | Cloud Backend |
| US-S-006 | Security | HSM Integration | - | Hardware Test | IV-FRM Module |
| US-S-007 | Security | Secure Boot | - | Boot Security Test | IV-FRM Module |
| US-A-001 | Abuse | Log Tampering | - | Red Team Exercise | IV-FRM Module |
| US-A-002 | Abuse | MITM | - | Red Team Exercise | Communication Layer |
| US-A-003 | Abuse | Insider Threat | - | Red Team Exercise | Dashboard |
| US-A-004 | Abuse | Replay Attack | - | Red Team Exercise | Communication Layer |
| US-A-005 | Abuse | Privilege Escalation | - | Red Team Exercise | Dashboard |
| US-C-001 | Countermeasure | Immutable Logs | US-A-001 | Security Test | Audit System |
| US-C-002 | Countermeasure | mTLS | US-A-002 | Security Test | Communication Layer |
| US-C-003 | Countermeasure | DLP | US-A-003 | Security Test | Dashboard |
| US-C-004 | Countermeasure | Replay Detection | US-A-004 | Fuzzing Test | Cloud Backend |
| US-C-005 | Countermeasure | Zero-Trust | US-A-005 | Security Test | Dashboard |

---

## Compliance Mapping

### ISO/SAE 21434 Alignment

| ISO 21434 Requirement | User Stories | Evidence |
|-----------------------|--------------|----------|
| RC-01 Governance | US-F-006, US-NF-002 | Compliance reports, audit logs |
| RC-02 Risk Management | US-S-001, US-A series | TARA documentation, abuse cases |
| RC-03 Security by Design | US-S-002, US-S-005 | Encryption implementation |
| RC-04 Validation | US-NF-001, US-C series | Test reports, pen test results |
| RC-05 Operations | US-F-001, US-C-001 | Monitoring dashboards, audit trails |
| RC-06 Incident Response | US-F-001, US-F-003 | Incident response procedures |
| RC-07 Forensic Readiness | US-F-002, US-S-001 | Evidence packaging, chain of custody |

### OWASP Security Story Patterns

Reference: [OWASP User Security Stories](https://github.com/OWASP/user-security-stories)

- **Authentication:** US-S-003 (MFA)
- **Authorization:** US-S-004 (RBAC)
- **Integrity:** US-S-001 (Tamper Evidence)
- **Confidentiality:** US-S-002 (Encryption)
- **Non-Repudiation:** US-C-001 (Immutable Audit)

---

## Acceptance Criteria Templates (OWASP)

### Security Story Template
```
GIVEN [context]
WHEN [action]
THEN [security requirement]
AND [verification method]
```

**Example (US-S-001):**
```
GIVEN an attacker modifies an event log
WHEN the system performs integrity verification
THEN the hash chain validation SHALL fail
AND an immediate alert SHALL be sent to security operations
```

---

## References

1. [Atlassian - User Stories](https://www.atlassian.com/agile/project-management/user-stories)
2. [OWASP Security User Stories](https://github.com/OWASP/user-security-stories)
3. [Integrating Cyber Security in Agile](https://www.linkedin.com/pulse/integrating-cyber-security-agile-organisation-james-howden)
4. [ISO/SAE 21434 Standard](https://www.iso.org/standard/70918.html)
5. [FIDO Automotive Security](https://fidoalliance.org/wp-content/uploads/2025/07/Addressing-Cybersecurity-Challenges-in-the-Automotive-Industry-7-2025-1.pdf)

---

*Document Version: 2.0*  
*Last Updated: April 9, 2026*  
*Team: Cyber-Torque*
*Total User Stories: 28 (7 Functional, 4 Non-Functional, 7 Security, 5 Abuse, 5 Countermeasure)*
