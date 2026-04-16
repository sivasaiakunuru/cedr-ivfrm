# Visualizations

This directory contains data visualizations, charts, and graphical representations for the CEDR project documentation and presentations.

## Available Visualizations

### Project Analytics

| Visualization | File | Description |
|---------------|------|-------------|
| **Risk Heat Map** | `risk_heatmap.png` | 17 risks mapped by likelihood vs impact |
| **Risk Reduction** | `risk_reduction.png` | Before/after mitigation comparison |
| **Investment ROI** | `investment_roi.png` | Return on investment visualization |

### Improvement Metrics

| Visualization | File | Description |
|---------------|------|-------------|
| **Improvement Roadmap** | `improvement_roadmap.png` | 4-phase timeline visualization |
| **Before/After** | `before_after.png` | Project improvements comparison |
| **Story Pyramid** | `story_pyramid.png` | User stories hierarchy |
| **SWOT Diagram** | `swot_diagram.png` | Strategic analysis framework |

### Legacy Formats

| File | Description |
|------|-------------|
| `User_Story_Visuals_ASCII.md` | ASCII art representations of user stories |

## Usage in Presentations

All PNG files in this directory are:
- High resolution (300 DPI minimum)
- Transparent backgrounds where applicable
- Ready for PowerPoint/Keynote import

## Generation Scripts

Visualizations are generated using Python scripts in the `/tools` directory:

```bash
# Generate all visualizations
python tools/generate_visualizations.py

# Generate specific chart
python tools/create_improvement_visuals.py
```
