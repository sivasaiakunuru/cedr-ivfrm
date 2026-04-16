# CEDR Quick Start Guide

Get up and running with CEDR (Cybersecurity Event Data Recorder) in minutes.

## Prerequisites

- **Python**: 3.9 or higher
- **Git**: For cloning the repository
- **Docker** (optional): For containerized deployment

## Installation

### Option 1: Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/sivasaiakunuru/cedr-ivfrm.git
cd cedr-ivfrm

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python -c "import cryptography; print('CEDR dependencies installed successfully')"
```

### Option 2: Docker Installation

```bash
# 1. Clone the repository
git clone https://github.com/sivasaiakunuru/cedr-ivfrm.git
cd cedr-ivfrm

# 2. Start with Docker Compose
docker-compose up -d

# 3. Check status
docker-compose ps
```

## Running Examples

### Basic Hash Chain Demo

```bash
# Run the basic logging example
python examples/basic_logging.py
```

This demonstrates:
- Creating a tamper-evident event log
- Adding events to the hash chain
- Verifying chain integrity
- Detecting tampering

### Verify Chain Integrity

```bash
# Verify a chain file
python examples/verify_chain.py sample_chain.json
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_hash_chain.py -v
```

## Project Structure

```
cedr-ivfrm/
├── examples/              # Usage examples
│   ├── basic_logging.py   # Hash chain demo
│   └── verify_chain.py    # Chain verification
├── tests/                 # Test suite
├── uml/                   # UML diagrams
├── visualizations/        # Charts and graphs
├── tools/                 # Utility scripts
└── docs/                  # Documentation
```

## Key Components

### 1. Hash Chain (`examples/basic_logging.py`)

The core tamper-evident logging mechanism:

```python
from examples.basic_logging import HashChain

# Create chain
chain = HashChain()

# Add event
event = {
    "vehicle_id": "VEH001",
    "event_type": "INTRUSION_DETECTED",
    "severity": "HIGH"
}
hash_value = chain.add_event(event)

# Verify integrity
is_valid = chain.verify_integrity()
```

### 2. Event Verification (`examples/verify_chain.py`)

Verify the integrity of a hash chain:

```python
from examples.verify_chain import ChainVerifier

verifier = ChainVerifier("chain.json")
is_valid = verifier.verify()
verifier.print_report()
```

## Development Workflow

### Making Changes

```bash
# 1. Create a branch
git checkout -b feature/my-feature

# 2. Make your changes
# ... edit files ...

# 3. Run tests
pytest

# 4. Format code
black .
isort .

# 5. Commit
git add .
git commit -m "feat: Add my feature"

# 6. Push
git push origin feature/my-feature
```

### Code Quality

```bash
# Linting
flake8 .

# Type checking
mypy .

# Security scan
bandit -r .
```

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/cedr

# Cloud
CLOUD_ENDPOINT=https://api.cedr.example.com
CLOUD_API_KEY=your-api-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/cedr/app.log
```

## Deployment

### Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment instructions.

## Troubleshooting

### Import Errors

```bash
# If you see "Module not found"
pip install -r requirements.txt

# Or using the package
pip install -e .
```

### Permission Denied

```bash
# Fix permissions on Linux/Mac
chmod +x examples/*.py
```

### Docker Issues

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Next Steps

1. **Read the Documentation**: Check out [CEDR_COMPLETE_PROJECT_GUIDE.md](CEDR_COMPLETE_PROJECT_GUIDE.md)
2. **Review UML Diagrams**: Explore the `uml/` directory
3. **Run All Examples**: Try each script in `examples/`
4. **Explore Tests**: Review `tests/` for usage patterns
5. **Check Compliance**: Review [CEDR_CRITICAL_REVIEW.md](CEDR_CRITICAL_REVIEW.md)

## Getting Help

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/sivasaiakunuru/cedr-ivfrm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sivasaiakunuru/cedr-ivfrm/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Resources

- **Project Overview**: [CEDR_MASTER_DOCUMENT.md](CEDR_MASTER_DOCUMENT.md)
- **User Stories**: [CEDR_User_Stories.md](CEDR_User_Stories.md)
- **Risk Analysis**: [CEDR_Risk_Analysis.md](CEDR_Risk_Analysis.md)
- **Budget/TCO**: [CEDR_Project_Budget_TCO.md](CEDR_Project_Budget_TCO.md)

---

**Ready to dive deeper?** Start with the [complete project guide](CEDR_COMPLETE_PROJECT_GUIDE.md) or explore the [examples](examples/) directory.
