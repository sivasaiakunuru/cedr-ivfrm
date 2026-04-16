# CEDR Documentation

This directory contains detailed documentation for the CEDR project.

## Available Documentation

### Getting Started
- [QUICKSTART.md](../QUICKSTART.md) - Get up and running in minutes
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute to the project
- [SECURITY.md](../SECURITY.md) - Security policies and procedures

### Project Documentation
- [CEDR_COMPLETE_PROJECT_GUIDE.md](../CEDR_COMPLETE_PROJECT_GUIDE.md) - Complete project guide
- [CEDR_MASTER_DOCUMENT.md](../CEDR_MASTER_DOCUMENT.md) - Master deliverables document
- [CEDR_FINAL_DOCUMENT_v5.md](../CEDR_FINAL_DOCUMENT_v5.md) - Comprehensive fixed edition
- [CEDR_CRITICAL_REVIEW.md](../CEDR_CRITICAL_REVIEW.md) - Consultant evaluation

### Technical Documentation
- [CEDR_User_Stories.md](../CEDR_User_Stories.md) - 28 agile user stories
- [CEDR_Risk_Analysis.md](../CEDR_Risk_Analysis.md) - Risk assessment
- [CEDR_UML_Diagrams.md](../CEDR_UML_Diagrams.md) - UML specifications
- [CEDR_Project_Budget_TCO.md](../CEDR_Project_Budget_TCO.md) - Budget and TCO analysis
- [CEDR_Improvement_Plan.md](../CEDR_Improvement_Plan.md) - 4-phase roadmap

### API Documentation

#### Cloud Backend Endpoints

```
POST   /api/events              - Upload security events
GET    /api/events/{id}         - Retrieve event details
POST   /api/forensics/verify    - Verify hash chain integrity
GET    /api/health              - Health check endpoint
```

See individual module READMEs for detailed API documentation:
- `cloud-backend/README.md` (if available)
- Code docstrings in Python files

### Module Documentation

| Module | README | Description |
|--------|--------|-------------|
| `examples/` | [examples/README.md](../examples/README.md) | Usage examples and demos |
| `tests/` | [tests/README.md](../tests/README.md) | Testing documentation |
| `tools/` | [tools/README.md](../tools/README.md) | Utility scripts |
| `uml/` | [uml/README.md](../uml/README.md) | UML diagrams |
| `visualizations/` | [visualizations/README.md](../visualizations/README.md) | Charts and graphs |

### Deployment

- [Dockerfile](../Dockerfile) - Container configuration
- [docker-compose.yml](../docker-compose.yml) - Multi-service deployment
- [pyproject.toml](../pyproject.toml) - Package configuration

### Additional Resources

- **Presentations**: See `CEDR_*Presentation*.pptx` files in root directory
- **UML Diagrams**: See `uml/*.png` files
- **Visualizations**: See `visualizations/*.png` files

## Generating Documentation

To build HTML documentation locally:

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## Contributing to Documentation

When adding documentation:
1. Use Markdown format
2. Follow existing structure and style
3. Update table of contents
4. Test code examples
5. Submit PR for review

## License

All documentation is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
