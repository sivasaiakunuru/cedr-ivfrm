# Contributing to CEDR

Thank you for your interest in contributing to the Cybersecurity Event Data Recorder (CEDR) project! This document provides guidelines for contributing.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

Before creating a bug report, please:
1. Check if the issue already exists
2. Use the latest version to verify the bug still exists
3. Collect information about the bug (logs, steps to reproduce)

When submitting a bug report, include:
- **Description**: Clear description of the bug
- **Steps to Reproduce**: Numbered steps
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, hardware
- **Logs**: Relevant log output

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating one:
- Use a clear, descriptive title
- Provide a detailed description
- Explain why this enhancement would be useful
- List possible implementation approaches

### Pull Requests

1. **Fork the repository** and create your branch from `master`
2. **Make your changes**: Add features or fix bugs
3. **Add tests**: Ensure your changes are tested
4. **Update documentation**: Update README, docstrings, etc.
5. **Ensure code quality**: Run linters and formatters
6. **Submit PR**: Create a pull request with a clear description

#### Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation with any new API changes
3. Ensure all tests pass
4. Update the CHANGELOG.md with your changes
5. Request review from maintainers
6. Address review feedback
7. Once approved, maintainers will merge

## Development Setup

### Prerequisites

- Python 3.9+
- pip or pipenv
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cedr-ivfrm.git
cd cedr-ivfrm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Run tests to ensure everything works
pytest tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_hash_chain.py

# Run with verbose output
pytest -v
```

### Code Style

We follow PEP 8 with some modifications:
- Line length: 100 characters (not 80)
- Use double quotes for strings
- Use type hints where appropriate

Format code before committing:
```bash
# Format with black
black .

# Sort imports
isort .

# Lint with flake8
flake8 .
```

## Project Structure

```
cedr-ivfrm/
├── docs/               # Documentation
├── examples/           # Example scripts
├── tests/              # Test suite
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
├── tools/              # Utility scripts
├── uml/                # UML diagrams
├── visualizations/     # Charts and graphs
├── .github/            # GitHub configuration
├── README.md           # Main documentation
├── CONTRIBUTING.md     # This file
├── LICENSE             # MIT License
└── requirements.txt    # Dependencies
```

## Commit Messages

Use clear, meaningful commit messages:

```
feat: Add tamper detection for CAN bus events
fix: Resolve hash chain verification failure
 docs: Update API documentation for cloud endpoints
 test: Add unit tests for encryption module
refactor: Simplify event logging logic
style: Fix formatting in presentation scripts
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

## Documentation

- Update docstrings for any modified functions
- Update README.md if adding new features
- Add examples to `examples/` for new functionality
- Update UML diagrams if architecture changes

## Questions?

- Open a GitHub Discussion for general questions
- Join our community chat (if available)
- Contact maintainers directly for sensitive issues

## Recognition

Contributors will be recognized in our README.md and release notes.

Thank you for contributing to automotive cybersecurity!
