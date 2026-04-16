# Examples

This directory contains usage examples and quick-start guides for the CEDR project.

## Quick Start

### 1. Basic Event Logging

```python
from cedr import EventLogger, HashChain

# Initialize logger
logger = EventLogger()
chain = HashChain()

# Log a security event
event = {
    "timestamp": "2026-04-15T21:30:00Z",
    "vehicle_id": "VEH001",
    "event_type": "INTRUSION_DETECTED",
    "severity": "HIGH",
    "details": "Anomalous CAN traffic detected"
}

# Add to tamper-evident chain
hash_value = chain.add_event(event)
logger.save(event, hash_value)

print(f"Event logged with hash: {hash_value}")
```

### 2. Verify Chain Integrity

```python
from cedr import HashChain

chain = HashChain()

# Load existing chain
chain.load_from_file("/var/cedr/events.chain")

# Verify integrity
if chain.verify_integrity():
    print("✅ Chain integrity verified")
else:
    print("❌ Tampering detected!")
    corrupted = chain.find_corruption()
    print(f"Corruption at index: {corrupted}")
```

### 3. Real-time CAN Monitoring

```python
from cedr.can import CANInterface
from cedr.detection import AnomalyDetector

# Initialize CAN interface
can = CANInterface(channel="can0")
detector = AnomalyDetector(model_path="models/can_anomaly.tflite")

# Monitor loop
for message in can.listen():
    is_anomaly, confidence = detector.predict(message)
    
    if is_anomaly and confidence > 0.8:
        alert = {
            "type": "ANOMALY_DETECTED",
            "can_id": message.id,
            "confidence": confidence,
            "timestamp": message.timestamp
        }
        # Log to tamper-evident chain
        chain.add_event(alert)
```

### 4. Cloud Upload

```python
from cedr.cloud import CloudUploader

uploader = CloudUploader(
    endpoint="https://api.cedr.cloud/v1",
    api_key="your-api-key"
)

# Upload pending events
pending = chain.get_pending_uploads()
for event in pending:
    success = uploader.upload(event)
    if success:
        chain.mark_uploaded(event.hash)
```

### 5. Forensic Export

```python
from cedr.forensics import EvidenceExporter

exporter = EvidenceExporter()

# Export evidence for investigation
evidence = exporter.generate_package(
    vehicle_id="VEH001",
    start_time="2026-04-01T00:00:00Z",
    end_time="2026-04-15T23:59:59Z"
)

# Save with chain of custody
exporter.save_package(evidence, 
    output_path="/evidence/case_001.cedr",
    investigator="Det. John Smith",
    case_number="CASE-2026-001"
)
```

## Example Scripts

| Script | Description |
|--------|-------------|
| `basic_logging.py` | Simple event logging example |
| `can_monitor.py` | Real-time CAN bus monitoring |
| `verify_chain.py` | Chain integrity verification |
| `export_evidence.py` | Forensic evidence export |
| `cloud_sync.py` | Cloud synchronization |

## Running Examples

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run example
python examples/basic_logging.py
```

## Jupyter Notebooks

Interactive examples are available in the `notebooks/` directory:

- `01_introduction.ipynb` - Project overview
- `02_hash_chain_demo.ipynb` - Hash chain walkthrough
- `03_anomaly_detection.ipynb` - ML detection examples
- `04_forensic_analysis.ipynb` - Forensic investigation workflow

```bash
# Start Jupyter
jupyter notebook notebooks/
```
