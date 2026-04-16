# UML Diagrams

This directory contains all UML (Unified Modeling Language) diagrams for the CEDR (Cybersecurity Event Data Recorder) project.

## Diagram Inventory

### Structural Diagrams

| Diagram | File | Description |
|---------|------|-------------|
| **Component Diagram** | `component_diagram_professional.png` | High-level system components with ML & HSM integration |
| **Deployment Diagram** | `deployment_diagram_professional.png` | Hardware/software stack deployment architecture |
| **Class Diagram** | `class_diagram_v2.png` | Updated class structure with new features |

### Behavioral Diagrams

| Diagram | File | Description |
|---------|------|-------------|
| **Use Case Diagram** | `use_case_diagram.png` | 6 automotive security scenarios |
| **Sequence Diagram** | `sequence_event_logging.png` | Event logging flow sequence |
| **Activity Diagram** | `activity_incident_response.png` | Incident response workflow |

### Visualization Diagrams

| Diagram | File | Description |
|---------|------|-------------|
| **Story Pyramid** | `story_pyramid.png` | 28 user stories hierarchy visualization |
| **Risk Heat Map** | `risk_heatmap.png` | Risk assessment visualization |
| **SWOT Analysis** | `swot_diagram.png` | Competitive analysis framework |

### Source Files

All diagrams are also available as PlantUML source files (`.puml`) for easy modification:
- Edit `.puml` files using any text editor
- Render using [PlantUML](https://plantuml.com/) or [PlantText](https://www.planttext.com/)

## Quick Reference

```bash
# View all PNG diagrams
ls *.png

# Edit a PlantUML diagram
nano component_diagram.puml

# Generate PNG from PlantUML (requires plantuml installed)
plantuml component_diagram.puml
```

## Diagram Standards

- All diagrams follow UML 2.5 specification
- Color coding:
  - 🔵 Blue: Vehicle Edge Components
  - 🟢 Green: Cloud Infrastructure
  - 🟡 Yellow: Security Components
  - 🔴 Red: Attack Vectors
  - ⚪ Gray: External Systems
