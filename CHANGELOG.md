# Changelog

All notable changes to the CEDR (Cybersecurity Event Data Recorder) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-04-15

### Added
- Complete CEDR project implementation for CYB408 Capstone
- 28 agile user stories with acceptance criteria
- 17 risk analysis with NIST methodology
- 5-year TCO analysis ($5.98M)
- 4-phase improvement roadmap
- 10 UML diagrams (component, deployment, class, use case, sequence, activity)
- Professional presentations (35 slides)
- ISO 21434 + UN R155/R156 compliance documentation
- Comprehensive project guide (50KB)

### Infrastructure
- CI/CD workflows with GitHub Actions (lint, test, security)
- Dependabot configuration for automated dependency updates
- MIT LICENSE file
- CONTRIBUTING.md with developer guidelines
- SECURITY.md with vulnerability reporting policy
- pyproject.toml for modern Python packaging
- Dockerfile with multi-stage builds
- docker-compose.yml with full stack deployment
- .gitignore for Python/Node artifacts
- Unit tests with pytest coverage
- Usage examples with runnable scripts

### Documentation
- QUICKSTART.md for rapid onboarding
- Directory-specific READMEs (uml/, visualizations/, tests/, examples/, tools/, docs/)
- GitHub issue and PR templates
- GitHub Discussions enabled

### Fixed
- Fixed hardcoded path in run_cedr.py, now uses relative paths
- Consolidated utility scripts into tools/ directory
- Added proper error handling in run_cedr.py

## Project Information

- **Project**: Cybersecurity Event Data Recorder (IV-FRM)
- **Team**: Cyber-Torque
- **Institution**: St. Clair College
- **Course**: CYB408-26W-001 Automobility Cybersecurity CAP
- **Date**: April 15, 2026

[Unreleased]: https://github.com/sivasaiakunuru/cedr-ivfrm/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/sivasaiakunuru/cedr-ivfrm/releases/tag/v1.0.0
