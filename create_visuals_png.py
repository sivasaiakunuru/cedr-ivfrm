#!/usr/bin/env python3
"""
Create PNG visualizations for user stories and risks using PIL
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
os.makedirs('/home/siva/.openclaw/workspace/visualizations', exist_ok=True)

def create_story_pyramid():
    """Create user story pyramid image"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Colors
    colors = {
        'abuse': '#FF6B6B',
        'counter': '#FFE66D', 
        'security': '#4ECDC4',
        'functional': '#95E1D3',
        'nonfunc': '#F38181'
    }
    
    # Draw pyramid layers (bottom to top)
    # Layer 1: Non-Functional (bottom)
    draw.polygon([(100, 500), (700, 500), (600, 420), (200, 420)], fill=colors['nonfunc'])
    draw.text((320, 450), 'NON-FUNCTIONAL (3)', fill='black')
    draw.text((300, 470), 'System Support', fill='black')
    
    # Layer 2: Functional
    draw.polygon([(200, 420), (600, 420), (520, 340), (280, 340)], fill=colors['functional'])
    draw.text((330, 370), 'FUNCTIONAL (6)', fill='black')
    draw.text((320, 390), 'Core Features', fill='black')
    
    # Layer 3: Security
    draw.polygon([(280, 340), (520, 340), (460, 260), (340, 260)], fill=colors['security'])
    draw.text((330, 290), 'SECURITY (5)', fill='black')
    draw.text((310, 310), 'Implement Controls', fill='black')
    
    # Layer 4: Countermeasure
    draw.polygon([(340, 260), (460, 260), (420, 180), (380, 180)], fill=colors['counter'])
    draw.text((315, 210), 'COUNTERMEASURE (5)', fill='black')
    draw.text((315, 230), 'Prevent Attacks', fill='black')
    
    # Layer 5: Abuse (top)
    draw.polygon([(380, 180), (420, 180), (400, 100)], fill=colors['abuse'])
    draw.text((350, 125), 'ABUSE (5)', fill='white')
    draw.text((330, 145), 'Block Attackers', fill='white')
    
    # Title
    draw.text((250, 30), 'CEDR User Story Pyramid', fill='black')
    draw.text((280, 55), '24 Stories Total', fill='black')
    
    # Legend
    y = 520
    for i, (name, color) in enumerate(colors.items()):
        draw.rectangle([(50 + i*150, y), (80 + i*150, y+20)], fill=color)
    
    img.save('/home/siva/.openclaw/workspace/visualizations/story_pyramid.png')
    print("✅ Created story_pyramid.png")

def create_risk_heatmap():
    """Create risk heat map"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((280, 20), 'Risk Heat Map', fill='black')
    
    # Draw grid
    # Y-axis: Impact (top to bottom: Critical, High, Medium, Low)
    # X-axis: Likelihood (left to right: Low, Medium, High)
    
    cell_w = 200
    cell_h = 120
    start_x = 150
    start_y = 80
    
    # Colors for risk levels
    critical = '#DC143C'  # Red
    high = '#FF6B35'      # Orange
    medium = '#FFD93D'    # Yellow
    low = '#6BCB77'       # Green
    
    # Draw cells
    # Row 0: Critical Impact
    draw.rectangle([(start_x, start_y), (start_x+cell_w, start_y+cell_h)], fill=low)
    draw.rectangle([(start_x+cell_w, start_y), (start_x+cell_w*2, start_y+cell_h)], fill=high)
    draw.rectangle([(start_x+cell_w*2, start_y), (start_x+cell_w*3, start_y+cell_h)], fill=critical)
    
    # Row 1: High Impact
    draw.rectangle([(start_x, start_y+cell_h), (start_x+cell_w, start_y+cell_h*2)], fill=low)
    draw.rectangle([(start_x+cell_w, start_y+cell_h), (start_x+cell_w*2, start_y+cell_h*2)], fill=medium)
    draw.rectangle([(start_x+cell_w*2, start_y+cell_h), (start_x+cell_w*3, start_y+cell_h*2)], fill=high)
    
    # Row 2: Medium Impact
    draw.rectangle([(start_x, start_y+cell_h*2), (start_x+cell_w, start_y+cell_h*3)], fill=low)
    draw.rectangle([(start_x+cell_w, start_y+cell_h*2), (start_x+cell_w*2, start_y+cell_h*3)], fill=medium)
    draw.rectangle([(start_x+cell_w*2, start_y+cell_h*2), (start_x+cell_w*3, start_y+cell_h*3)], fill=medium)
    
    # Row 3: Low Impact
    draw.rectangle([(start_x, start_y+cell_h*3), (start_x+cell_w, start_y+cell_h*4)], fill=low)
    draw.rectangle([(start_x+cell_w, start_y+cell_h*3), (start_x+cell_w*2, start_y+cell_h*4)], fill=low)
    draw.rectangle([(start_x+cell_w*2, start_y+cell_h*3), (start_x+cell_w*3, start_y+cell_h*4)], fill=low)
    
    # Add risk labels
    # Critical row
    draw.text((start_x+cell_w+20, start_y+40), 'T-001', fill='black')
    draw.text((start_x+cell_w*2+20, start_y+20), 'B-002', fill='white')
    draw.text((start_x+cell_w*2+20, start_y+50), 'B-001', fill='white')
    
    # High row
    draw.text((start_x+cell_w+30, start_y+cell_h+40), 'O-001', fill='black')
    draw.text((start_x+cell_w*2+20, start_y+cell_h+40), 'T-002', fill='black')
    
    # Medium row
    draw.text((start_x+cell_w+30, start_y+cell_h*2+40), 'T-003', fill='black')
    draw.text((start_x+cell_w+30, start_y+cell_h*2+70), 'O-002', fill='black')
    
    # Labels
    # Y-axis labels
    draw.text((50, start_y+40), 'Critical', fill='black')
    draw.text((50, start_y+cell_h+40), 'High', fill='black')
    draw.text((50, start_y+cell_h*2+40), 'Medium', fill='black')
    draw.text((50, start_y+cell_h*3+40), 'Low', fill='black')
    
    # X-axis labels
    draw.text((start_x+80, start_y+cell_h*4+10), 'Low', fill='black')
    draw.text((start_x+cell_w+80, start_y+cell_h*4+10), 'Medium', fill='black')
    draw.text((start_x+cell_w*2+80, start_y+cell_h*4+10), 'High', fill='black')
    
    # Axis titles
    draw.text((20, 300), 'I', fill='black')
    draw.text((20, 320), 'M', fill='black')
    draw.text((20, 340), 'P', fill='black')
    draw.text((20, 360), 'A', fill='black')
    draw.text((20, 380), 'C', fill='black')
    draw.text((20, 400), 'T', fill='black')
    
    draw.text((400, 580), 'LIKELIHOOD', fill='black')
    
    img.save('/home/siva/.openclaw/workspace/visualizations/risk_heatmap.png')
    print("✅ Created risk_heatmap.png")

def create_swot_diagram():
    """Create SWOT analysis diagram"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Colors
    strength = '#95E1D3'
    weakness = '#F38181'
    opportunity = '#6BCB77'
    threat = '#FFD93D'
    
    # Draw 4 quadrants
    mid_x = 400
    mid_y = 300
    
    # Strength (top-left)
    draw.rectangle([(20, 80), (mid_x-20, mid_y-20)], fill=strength)
    draw.text((150, 100), 'STRENGTHS', fill='black')
    draw.text((40, 130), '• 82% cost advantage', fill='black')
    draw.text((40, 150), '• Tamper-evident design', fill='black')
    draw.text((40, 170), '• Real-time <2s alerts', fill='black')
    draw.text((40, 190), '• Open source', fill='black')
    draw.text((40, 210), '• ISO 21434 compliant', fill='black')
    
    # Weakness (top-right)
    draw.rectangle([(mid_x+20, 80), (780, mid_y-20)], fill=weakness)
    draw.text((520, 100), 'WEAKNESSES', fill='black')
    draw.text((mid_x+40, 130), '• Consumer hardware', fill='black')
    draw.text((mid_x+40, 150), '• Limited testing (13)', fill='black')
    draw.text((mid_x+40, 170), '• Academic credibility', fill='black')
    draw.text((mid_x+40, 190), '• Single cloud vendor', fill='black')
    draw.text((mid_x+40, 210), '• No production history', fill='black')
    
    # Opportunity (bottom-left)
    draw.rectangle([(20, mid_y+20), (mid_x-20, 550)], fill=opportunity)
    draw.text((130, mid_y+40), 'OPPORTUNITIES', fill='black')
    draw.text((40, mid_y+70), '• UN R155 mandate 2024', fill='black')
    draw.text((40, mid_y+90), '• Insurance discounts', fill='black')
    draw.text((40, mid_y+110), '• $8.9B HSM market', fill='black')
    draw.text((40, mid_y+130), '• V2X expansion', fill='black')
    draw.text((40, mid_y+150), '• ML anomaly detection', fill='black')
    
    # Threat (bottom-right)
    draw.rectangle([(mid_x+20, mid_y+20), (780, 550)], fill=threat)
    draw.text((540, mid_y+40), 'THREATS', fill='black')
    draw.text((mid_x+40, mid_y+70), '• Patent litigation', fill='black')
    draw.text((mid_x+40, mid_y+90), '• OEM in-house solutions', fill='black')
    draw.text((mid_x+40, mid_y+110), '• Economic downturn', fill='black')
    draw.text((mid_x+40, mid_y+130), '• Supply chain issues', fill='black')
    draw.text((mid_x+40, mid_y+150), '• Standards changes', fill='black')
    
    # Title
    draw.text((350, 30), 'SWOT Analysis', fill='black')
    
    img.save('/home/siva/.openclaw/workspace/visualizations/swot_diagram.png')
    print("✅ Created swot_diagram.png")

if __name__ == '__main__':
    create_story_pyramid()
    create_risk_heatmap()
    create_swot_diagram()
    print("\n✅ All visualizations created successfully!")
    print("Location: /home/siva/.openclaw/workspace/visualizations/")
