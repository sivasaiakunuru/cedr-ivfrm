# Tools

This directory contains utility scripts and tools for the CEDR project.

## Organization

Scripts have been consolidated from the root directory into categorized subdirectories:

```
tools/
├── presentations/     # Presentation generation scripts
├── reports/          # Report generation utilities
├── visualizations/   # Chart and diagram generators
└── deployment/       # Deployment and configuration tools
```

## Available Tools

### Presentation Generation

| Script | Purpose |
|--------|---------|
| `generate_presentation.py` | Master presentation generator |
| `create_professional_presentation.py` | Professional pitch deck |
| `create_final_presentation.py` | Final capstone presentation |

### Report Generation

| Script | Purpose |
|--------|---------|
| `generate_professional_report.py` | Professional report formatter |
| `generate_ota_report.py` | OTA security report generator |
| `generate_condensed_report.py` | Condensed report version |
| `generate_corrected_report.py` | Corrected report with fixes |

### Visualization Tools

| Script | Purpose |
|--------|---------|
| `create_improvement_visuals.py` | Improvement roadmap charts |
| `create_visuals_png.py` | PNG chart generator |
| `generate_images.py` | Image generation utilities |
| `generate_placeholders.py` | Placeholder image generator |

### UML Generation

| Script | Purpose |
|--------|---------|
| `create_professional_uml.py` | Professional UML diagrams |
| `create_updated_uml_pngs.py` | UML PNG exporter |
| `generate_kroki.py` | Kroki diagram generator |
| `generate_uml_images.sh` | Batch UML image generator |

### Deployment Tools

| Script | Purpose |
|--------|---------|
| `create_professional_deployment.py` | Deployment configuration |
| `finalize_presentation.py` | Final presentation builder |

## Usage

### Generate Presentation

```bash
# Generate professional presentation
cd tools/presentations
python create_professional_presentation.py

# Output: CEDR_Professional_Presentation.pptx
```

### Generate Report

```bash
# Generate OTA security report
cd tools/reports
python generate_ota_report.py

# Output: CYB400_OTA_Security_Report.docx
```

### Generate Visualizations

```bash
# Generate all visualizations
cd tools/visualizations
python create_improvement_visuals.py

# Output: visualizations/*.png
```

## Dependencies

Most tools require:

```bash
pip install python-pptx Pillow matplotlib numpy
```

For UML generation:

```bash
pip install plantuml
# Or use Kroki online service
```

## Migration from Root Directory

Scripts have been moved from root to `tools/` subdirectories:

| Old Location | New Location |
|--------------|--------------|
| `create_*.py` | `tools/presentations/` |
| `generate_*.py` | `tools/reports/` or `tools/visualizations/` |
| `update_*.py` | `tools/presentations/` |
| `finalize_*.py` | `tools/deployment/` |

Symlinks remain in root for backward compatibility.
