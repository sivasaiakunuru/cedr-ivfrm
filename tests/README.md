# Tests

This directory contains test suites for the CEDR (Cybersecurity Event Data Recorder) project.

## Test Structure

```
tests/
├── unit/                 # Unit tests for individual components
├── integration/          # Integration tests
├── security/            # Security-specific tests
└── fixtures/            # Test data and fixtures
```

## Running Tests

### Using pytest

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test category
pytest tests/unit/
pytest tests/security/

# Run with verbose output
pytest -v
```

### Using unittest

```bash
# Run all tests
python -m unittest discover tests/

# Run specific module
python -m unittest tests.unit.test_hash_chain
```

## Test Coverage Goals

| Component | Target Coverage |
|-----------|-----------------|
| Hash Chain | 95% |
| Encryption | 95% |
| Event Detection | 90% |
| CAN Interface | 85% |
| Cloud Upload | 80% |

## Writing Tests

### Unit Test Example

```python
import unittest
from cedr.hash_chain import HashChain

class TestHashChain(unittest.TestCase):
    def setUp(self):
        self.chain = HashChain()
    
    def test_initial_hash(self):
        """Test genesis hash creation"""
        genesis = self.chain.create_genesis()
        self.assertIsNotNone(genesis)
        self.assertEqual(len(genesis), 64)  # SHA-256 hex
    
    def test_chain_integrity(self):
        """Test hash chain integrity verification"""
        events = ["event1", "event2", "event3"]
        for event in events:
            self.chain.add_event(event)
        
        self.assertTrue(self.chain.verify_integrity())
```

### Security Test Example

```python
def test_tamper_detection():
    """Verify tampered events are detected"""
    chain = HashChain()
    chain.add_event("original")
    
    # Simulate tampering
    chain.events[0].data = "tampered"
    
    assert not chain.verify_integrity()
```

## Continuous Integration

Tests run automatically on:
- Push to `master`, `main`, or `develop` branches
- Pull request creation
- Release tagging

See `.github/workflows/ci.yml` for CI configuration.
