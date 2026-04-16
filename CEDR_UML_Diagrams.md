# CEDR UML Diagrams
## Cybersecurity Event Data Recorder (IV-FRM)
### Team Cyber-Torque | CYB408 Capstone

---

## Table of Contents
1. [Use Case Diagram](#1-use-case-diagram)
2. [Sequence Diagrams](#2-sequence-diagrams)
3. [Component Diagram](#3-component-diagram)
4. [Deployment Diagram](#4-deployment-diagram)
5. [Activity Diagram](#5-activity-diagram)
6. [Class Diagram](#6-class-diagram)

---

## 1. Use Case Diagram

### Mermaid Version
```mermaid
graph LR
    subgraph Actors
        Driver((Driver))
        Mechanic((Mechanic))
        Investigator((Forensic Investigator))
        Attacker((Attacker))
        CloudService((Cloud Service))
    end
    
    subgraph CEDR System
        UC1[Authenticate Driver]
        UC2[Monitor CAN Bus]
        UC3[Detect Anomalies]
        UC4[Log Security Events]
        UC5[Upload to Cloud]
        UC6[Generate Alerts]
        UC7[Retrieve Evidence]
        UC8[Verify Integrity]
        UC9[Generate Reports]
        UC10[Secure OTA Update]
    end
    
    Driver --> UC1
    Driver --> UC10
    Mechanic --> UC7
    Investigator --> UC7
    Investigator --> UC8
    Investigator --> UC9
    CloudService --> UC5
    
    Attacker -.->|Attempts| UC11[Inject Malicious Messages]
    Attacker -.->|Attempts| UC12[Modify Event Logs]
    Attacker -.->|Attempts| UC13[Intercept Communications]
    
    UC2 --> UC3
    UC3 --> UC4
    UC4 --> UC5
    UC3 --> UC6
    UC5 --> UC7
    UC4 --> UC8
```

### PlantUML Version
```plantuml
@startuml CEDR_Use_Case_Diagram
left to right direction
skinparam packageStyle rectangle

actor "Driver" as Driver
actor "Mechanic" as Mechanic
actor "Forensic Investigator" as Investigator
actor "Cloud Service" as Cloud
actor "Attacker" as Attacker #Red

rectangle "CEDR System" {
    usecase "Authenticate Driver" as UC1
    usecase "Monitor CAN Bus" as UC2
    usecase "Detect Anomalies" as UC3
    usecase "Log Security Events" as UC4
    usecase "Upload to Cloud" as UC5
    usecase "Generate Alerts" as UC6
    usecase "Retrieve Evidence" as UC7
    usecase "Verify Integrity" as UC8
    usecase "Generate Reports" as UC9
    usecase "Secure OTA Update" as UC10
    
    usecase "Inject Malicious Messages" as UC11 #Pink
    usecase "Modify Event Logs" as UC12 #Pink
    usecase "Intercept Communications" as UC13 #Pink
}

Driver --> UC1
Driver --> UC10
Mechanic --> UC7
Investigator --> UC7
Investigator --> UC8
Investigator --> UC9
Cloud --> UC5

Attacker --> UC11
Attacker --> UC12
Attacker --> UC13

UC2 ..> UC3 : <<include>>
UC3 ..> UC4 : <<include>>
UC4 ..> UC5 : <<include>>
UC3 ..> UC6 : <<include>>

@enduml
```

---

## 2. Sequence Diagrams

### 2.1 Security Event Detection & Logging

```mermaid
sequenceDiagram
    participant CAN as CAN Bus
    participant IV as IV-FRM Module
    participant DB as Local Database
    participant Cloud as Cloud Backend
    participant Dash as Investigator Dashboard
    
    CAN->>IV: Suspicious Message
    activate IV
    IV->>IV: Validate Message
    IV->>IV: Calculate Hash
    IV->>IV: Encrypt Event Data
    IV->>DB: Store Event (SQLite)
    deactivate IV
    
    alt Critical Event
        IV->>Cloud: Immediate Upload
        activate Cloud
        Cloud->>Cloud: Verify HMAC
        Cloud->>Cloud: Decrypt & Store
        Cloud-->>IV: Acknowledge
        Cloud->>Dash: Real-time Alert
        deactivate Cloud
    else Routine Event
        IV->>IV: Queue for Batch Upload
    end
    
    Dash->>Cloud: Request Evidence
    activate Cloud
    Cloud-->>Dash: Return Events + Chain
    deactivate Cloud
```

### 2.2 Tamper Evidence Verification

```mermaid
sequenceDiagram
    participant Inv as Investigator
    participant Dash as Dashboard
    participant Cloud as Cloud Backend
    participant Chain as Hash Chain
    
    Inv->>Dash: Request Event Log
    activate Dash
    Dash->>Cloud: Fetch Events
    activate Cloud
    Cloud-->>Dash: Event Data + Hashes
    deactivate Cloud
    
    Dash->>Chain: Verify Chain Integrity
    activate Chain
    Chain->>Chain: Recalculate Hashes
    Chain->>Chain: Compare with Stored
    
    alt Valid Chain
        Chain-->>Dash: Integrity Verified ✓
        Dash-->>Inv: Display Green Status
    else Tampering Detected
        Chain-->>Dash: Chain Broken! ⚠
        Dash-->>Inv: Display Red Alert
    end
    deactivate Chain
    deactivate Dash
```

### 2.3 Secure OTA Update Logging

```mermaid
sequenceDiagram
    participant OEM as OEM Server
    participant Vehicle as Vehicle ECU
    participant CEDR as CEDR Module
    participant Cloud as Cloud Backend
    
    OEM->>Vehicle: Firmware Update Package
    activate Vehicle
    Vehicle->>Vehicle: Verify Signature
    
    Vehicle->>CEDR: Log Update Start
    activate CEDR
    CEDR->>CEDR: Capture Pre-Version
    CEDR->>CEDR: Hash Update Package
    CEDR->>Cloud: Upload Update Event
    deactivate CEDR
    
    Vehicle->>Vehicle: Apply Update
    
    Vehicle->>CEDR: Log Update Complete
    activate CEDR
    CEDR->>CEDR: Capture Post-Version
    CEDR->>CEDR: Calculate Success/Failure
    CEDR->>Cloud: Upload Result Event
    deactivate Vehicle
    deactivate CEDR
```

---

## 3. Component Diagram

```mermaid
graph TB
    subgraph "Vehicle (In-Vehicle Network)"
        CAN[CAN Bus]
        ECU1[Engine ECU]
        ECU2[Brake ECU]
        ECU3[Infotainment ECU]
        
        subgraph "CEDR IV-FRM Module"
            Capture[Event Capture]
            Validator[Message Validator]
            Hasher[Hash Generator]
            Crypto[AES-256 Encryption]
            Storage[Local Storage SQLite]
            Uploader[Upload Manager]
            Queue[Event Queue]
        end
    end
    
    subgraph "Cloud Backend"
        APIGateway[API Gateway]
        Auth[Authentication Service]
        EventProc[Event Processor]
        Correlator[Fleet Correlator]
        CloudDB[(Cloud Database)]
        Audit[Audit Logger]
        Reporter[Report Generator]
    end
    
    subgraph "Investigator Tools"
        Dashboard[Web Dashboard]
        Mobile[Mobile App]
        Export[Evidence Export]
    end
    
    subgraph "External Systems"
        Telematics[4G/5G/WiFi]
        HSM[Hardware Security Module]
    end
    
    CAN --> Capture
    ECU1 --> CAN
    ECU2 --> CAN
    ECU3 --> CAN
    
    Capture --> Validator
    Validator --> Hasher
    Hasher --> Crypto
    Crypto --> Storage
    Storage --> Queue
    Queue --> Uploader
    
    Uploader --> Telematics
    Telematics --> APIGateway
    
    APIGateway --> Auth
    Auth --> EventProc
    EventProc --> CloudDB
    EventProc --> Correlator
    EventProc --> Audit
    
    CloudDB --> Reporter
    Reporter --> Dashboard
    Reporter --> Mobile
    Reporter --> Export
    
    Crypto -.-> HSM
```

---

## 4. Deployment Diagram

```mermaid
graph TB
    subgraph "Vehicle Environment"
        subgraph "In-Vehicle Network"
            CAN[CAN Bus]
            ETH[Automotive Ethernet]
        end
        
        subgraph "CEDR Hardware"
            RPi[Raspberry Pi 4]
            CANH[CAN HAT]
            4G[4G/5G Modem]
            GPS[GPS Module]
        end
        
 subgraph "Software Stack"
            OS[Raspberry Pi OS]
            Python[Python Runtime]
            SQLite[(SQLite DB)]
            CEDRApp[CEDR Application]
        end
    end
    
    subgraph "Cloud Infrastructure"
        subgraph "Load Balancer"
            LB[AWS ALB / NGINX]
        end
        
        subgraph "Application Tier"
            API1[API Server 1]
            API2[API Server 2]
            WS[WebSocket Server]
        end
        
        subgraph "Data Tier"
            RDS[(PostgreSQL RDS)]
            Redis[(Redis Cache)]
            S3[S3 Object Storage]
        end
        
        subgraph "Security Services"
            KMS[AWS KMS]
            WAF[AWS WAF]
            GuardDuty[Threat Detection]
        end
    end
    
    subgraph "Investigator Workstation"
        Browser[Web Browser]
        Laptop[Laptop/Tablet]
    end
    
    CAN --> CANH
    ETH --> RPi
    CANH --> RPi
    RPi --> 4G
    RPi --> GPS
    
    RPi --> OS
    OS --> Python
    Python --> CEDRApp
    CEDRApp --> SQLite
    
    4G -.->|TLS 1.3| LB
    LB --> WAF
    WAF --> API1
    WAF --> API2
    API1 --> RDS
    API1 --> Redis
    API1 --> S3
    API2 --> RDS
    
    API1 -.-> KMS
    API2 -.-> KMS
    
    RDS -.-> GuardDuty
    
    Browser --> LB
    Browser --> Laptop
```

---

## 5. Activity Diagram

### 5.1 Incident Detection & Response Flow

```mermaid
flowchart TD
    Start([Security Event Detected]) --> Classify{Classify Event}
    
    Classify -->|Normal| LogNormal[Log to Routine Queue]
    Classify -->|Suspicious| Analyze{Detailed Analysis}
    Classify -->|Critical| Immediate[Immediate Response]
    
    LogNormal --> Batch[Batch Upload Schedule]
    Batch --> End1([End])
    
    Analyze -->|Confirmed Threat| Critical[Mark Critical]
    Analyze -->|False Positive| LogNormal
    
    Critical --> Encrypt[Encrypt Event Data]
    Immediate --> Encrypt
    
    Encrypt --> Hash[Calculate Hash Chain]
    Hash --> StoreLocal[Store in Local DB]
    
    StoreLocal --> Upload{Upload Strategy}
    
    Upload -->|Critical| ImmediateUpload[Immediate Cloud Upload]
    Upload -->|High Priority| PriorityQueue[Priority Queue]
    Upload -->|Routine| BatchQueue[Batch Queue]
    
    ImmediateUpload --> Cloud[Cloud Processing]
    PriorityQueue --> Cloud
    BatchQueue --> Scheduled[Scheduled Upload]
    Scheduled --> Cloud
    
    Cloud --> Verify{Verify Integrity}
    
    Verify -->|Valid| Alert[Generate Alert]
    Verify -->|Invalid| Error[Log Error / Retry]
    
    Alert --> Notify[Notify Stakeholders]
    Notify --> Dashboard[Update Dashboard]
    
    Error --> Manual[Manual Review Required]
    
    Dashboard --> End2([End])
    Manual --> End2
```

### 5.2 Evidence Retrieval & Verification

```mermaid
flowchart TD
    Start([Investigator Request]) --> Auth{Authenticate}
    
    Auth -->|Invalid| Deny[Access Denied]
    Auth -->|Valid| Authorize{Authorize Access}
    
    Authorize -->|Unauthorized| Deny
    Authorize -->|Authorized| Search[Search Events]
    
    Search --> Filters[Apply Filters]
    Filters --> Retrieve[Retrieve from Cloud]
    
    Retrieve --> VerifyChain[Verify Hash Chain]
    
    VerifyChain -->|Chain Valid| Package[Package Evidence]
    VerifyChain -->|Chain Broken| Alert[Tampering Alert]
    
    Package --> AddMetadata[Add Metadata]
    AddMetadata --> Sign[Digital Sign]
    
    Sign --> Export{Export Format}
    
    Export -->|PDF| GeneratePDF[Generate PDF Report]
    Export -->|JSON| GenerateJSON[Export JSON Data]
    Export -->|RAW| GenerateRAW[Export Raw Evidence]
    
    GeneratePDF --> Deliver[Deliver to Investigator]
    GenerateJSON --> Deliver
    GenerateRAW --> Deliver
    
    Alert --> Escalate[Escalate to Security Team]
    Escalate --> Forensics[Initiate Forensic Analysis]
    
    Deliver --> Audit[Log Access Audit]
    Forensics --> Audit
    Deny --> Audit
    
    Audit --> End([End])
```

---

## 6. Class Diagram

```mermaid
classDiagram
    class Event {
        +String eventId
        +String vehicleId
        +DateTime timestamp
        +String eventType
        +String severity
        +String description
        +String rawData
        +String hash
        +String previousHash
        +Boolean uploaded
        +encrypt()
        +calculateHash()
        +verifyIntegrity()
    }
    
    class Vehicle {
        +String vehicleId
        +String vin
        +String model
        +DateTime registeredAt
        +String status
        +List~Event~ events
        +register()
        +getEvents()
        +getSecurityScore()
    }
    
    class Investigator {
        +String investigatorId
        +String name
        +String badge
        +String role
        +List~String~ authorizedVehicles
        +authenticate()
        +searchEvents()
        +exportEvidence()
    }
    
    class CloudServer {
        +String serverId
        +String endpoint
        +receiveEvent()
        +verifyHMAC()
        +storeEvent()
        +correlateEvents()
        +generateReport()
    }
    
    class HashChain {
        +String genesisHash
        +List~String~ chain
        +addBlock()
        +verifyChain()
        +detectTampering()
    }
    
    class EncryptionModule {
        +String algorithm
        +String keyId
        +encrypt()
        +decrypt()
        +rotateKey()
    }
    
    class AlertService {
        +sendAlert()
        +escalate()
        +notifyDashboard()
    }
    
    class EvidencePackage {
        +String packageId
        +List~Event~ events
        +DateTime createdAt
        +String digitalSignature
        +String custodian
        +generatePDF()
        +generateJSON()
        +verifySignature()
    }
    
    Vehicle "1" --> "*" Event : generates
    Investigator "1" --> "*" Event : retrieves
    Investigator "1" --> "*" EvidencePackage : creates
    Event "*" --> "1" HashChain : part of
    Event --> EncryptionModule : uses
    CloudServer "1" --> "*" Event : stores
    CloudServer --> AlertService : triggers
    EvidencePackage "1" --> "*" Event : contains
```

---

## PlantUML Source Files

### How to Render

**Option 1: Online Renderer**
- Copy PlantUML code to: https://www.plantuml.com/plantuml

**Option 2: VS Code Extension**
- Install "PlantUML" extension
- Preview diagrams directly in editor

**Option 3: Command Line**
```bash
# Install PlantUML
sudo apt install plantuml

# Generate PNG
plantuml CEDR_UML_Diagrams.puml

# Generate SVG
plantuml -tsvg CEDR_UML_Diagrams.puml
```

---

## Diagram Summary

| Diagram Type | Purpose | Key Elements |
|--------------|---------|--------------|
| **Use Case** | Actor-system interactions | Driver, Investigator, Attacker, 10 use cases |
| **Sequence** | Message flow over time | Event logging, tamper verification, OTA updates |
| **Component** | System structure | IV-FRM, Cloud, Dashboard, 15 components |
| **Deployment** | Physical infrastructure | Vehicle, AWS Cloud, Investigator workstation |
| **Activity** | Business process flow | Incident response, evidence retrieval |
| **Class** | Data model relationships | Event, Vehicle, Investigator, 7 classes |

---

## Compliance Mapping

| UML Diagram | ISO/SAE 21434 Work Product | Purpose |
|-------------|---------------------------|---------|
| Use Case Diagram | WP-08-01: Cybersecurity Requirements | Functional + security requirements |
| Sequence Diagram | WP-10-01: Security Controls | Control implementation flow |
| Component Diagram | WP-12-01: Architecture Design | System architecture documentation |
| Deployment Diagram | WP-13-01: Integration & Verification | Production deployment model |
| Activity Diagram | WP-14-01: Cybersecurity Operations | Incident response procedures |
| Class Diagram | WP-09-01: Design Specification | Data model for forensics |

---

*Document Version: 1.0*  
*Last Updated: April 9, 2026*  
*Team: Cyber-Torque*
