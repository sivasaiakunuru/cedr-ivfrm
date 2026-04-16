#!/usr/bin/env python3
"""
Create visualizations for improvement plan
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('/home/siva/.openclaw/workspace/visualizations', exist_ok=True)

def create_roadmap():
    """Create implementation roadmap"""
    img = Image.new('RGB', (1000, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((350, 20), 'CEDR Improvement Roadmap', fill='black')
    
    # Timeline
    phases = [
        ('Phase 1\nFoundation\n(M1-3)', '$45K', '40% Risk↓', '#4ECDC4'),
        ('Phase 2\nHardening\n(M4-6)', '$120K', '65% Risk↓', '#95E1D3'),
        ('Phase 3\nProduction\n(M7-12)', '$285K', '80% Risk↓', '#FFE66D'),
        ('Phase 4\nScale\n(M13-24)', '$850K', '90% Risk↓', '#FF6B6B'),
    ]
    
    x = 50
    width = 200
    height = 300
    
    for i, (phase, cost, risk, color) in enumerate(phases):
        # Draw box
        draw.rectangle([(x, 100), (x+width, 100+height)], fill=color, outline='black', width=2)
        
        # Text
        lines = phase.split('\n')
        y = 120
        for line in lines:
            draw.text((x+20, y), line, fill='black')
            y += 30
        
        draw.text((x+20, 250), cost, fill='black')
        draw.text((x+20, 280), risk, fill='black')
        
        # Arrow
        if i < len(phases) - 1:
            draw.polygon([(x+width+10, 220), (x+width+30, 210), (x+width+30, 230)], fill='black')
        
        x += width + 40
    
    # Timeline bar
    draw.rectangle([(50, 450), (950, 470)], fill='#E0E0E0')
    
    # Milestones
    milestones = ['M3', 'M6', 'M12', 'M24']
    x_pos = [50, 290, 530, 850]
    for i, (ms, xp) in enumerate(zip(milestones, x_pos)):
        draw.ellipse([(xp-5, 445), (xp+5, 475)], fill='black')
        draw.text((xp-10, 480), ms, fill='black')
    
    img.save('/home/siva/.openclaw/workspace/visualizations/improvement_roadmap.png')
    print("✅ Created improvement_roadmap.png")

def create_before_after():
    """Create before/after comparison"""
    img = Image.new('RGB', (1000, 700), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((350, 20), 'CEDR: Before vs After Improvements', fill='black')
    
    # Headers
    draw.text((150, 60), 'CURRENT (Prototype)', fill='red')
    draw.text((650, 60), 'IMPROVED (Production)', fill='green')
    
    # Comparison items
    items = [
        ('Hardware', 'Raspberry Pi 4', 'Raspberry Pi CM4 Industrial', '#FFE6E6', '#E6FFE6'),
        ('Temp Range', '0°C to 50°C', '-40°C to +85°C', '#FFE6E6', '#E6FFE6'),
        ('Security', 'Software keys', 'Hardware HSM (A71CH)', '#FFE6E6', '#E6FFE6'),
        ('Testing', '13 scenarios', '50+ attack scenarios', '#FFE6E6', '#E6FFE6'),
        ('Detection', 'Rule-based', 'ML anomaly detection', '#FFE6E6', '#E6FFE6'),
        ('Cloud', 'AWS only', 'Multi-cloud + Edge', '#FFE6E6', '#E6FFE6'),
        ('Cost/Vehicle', '$1,850 (pilot)', '$485 (production)', '#FFE6E6', '#E6FFE6'),
        ('Risk Score', 'Medium (21)', 'Low-Medium (8)', '#FFE6E6', '#E6FFE6'),
    ]
    
    y = 100
    for item, current, improved, c_color, i_color in items:
        # Item label
        draw.text((20, y+10), item, fill='black')
        
        # Current
        draw.rectangle([(150, y), (480, y+40)], fill=c_color)
        draw.text((160, y+10), current, fill='black')
        
        # Arrow
        draw.polygon([(500, y+15), (530, y+5), (530, y+25)], fill='black')
        
        # Improved
        draw.rectangle([(540, y), (950, y+40)], fill=i_color)
        draw.text((550, y+10), improved, fill='black')
        
        y += 60
    
    img.save('/home/siva/.openclaw/workspace/visualizations/before_after.png')
    print("✅ Created before_after.png")

def create_risk_reduction():
    """Create risk reduction chart"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((250, 20), 'Risk Reduction by Improvement Phase', fill='black')
    
    # Data
    categories = ['Technical', 'Business', 'Compliance', 'Operational', 'Security']
    before = [21, 21, 6, 12, 8]
    after = [8, 10, 2, 4, 2]
    
    # Draw bars
    bar_width = 80
    gap = 60
    start_x = 100
    max_height = 300
    
    y_base = 450
    
    for i, (cat, bef, aft) in enumerate(zip(categories, before, after)):
        x = start_x + i * (bar_width * 2 + gap)
        
        # Before bar (red)
        h_before = (bef / 25) * max_height
        draw.rectangle([(x, y_base - h_before), (x + bar_width, y_base)], fill='#FF6B6B')
        draw.text((x + 10, y_base - h_before - 20), str(bef), fill='black')
        
        # After bar (green)
        h_after = (aft / 25) * max_height
        draw.rectangle([(x + bar_width + 10, y_base - h_after), (x + bar_width * 2 + 10, y_base)], fill='#6BCB77')
        draw.text((x + bar_width + 15, y_base - h_after - 20), str(aft), fill='black')
        
        # Category label
        draw.text((x, y_base + 10), cat, fill='black')
        
        # Percentage reduction
        reduction = ((bef - aft) / bef) * 100
        draw.text((x, y_base + 30), f'-{int(reduction)}%', fill='black')
    
    # Legend
    draw.rectangle([(550, 100), (600, 130)], fill='#FF6B6B')
    draw.text((610, 105), 'Before', fill='black')
    draw.rectangle([(550, 140), (600, 170)], fill='#6BCB77')
    draw.text((610, 145), 'After', fill='black')
    
    # Y-axis label
    draw.text((30, 250), 'Risk Score', fill='black')
    
    img.save('/home/siva/.openclaw/workspace/visualizations/risk_reduction.png')
    print("✅ Created risk_reduction.png")

def create_investment_roi():
    """Create investment vs ROI chart"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((250, 20), 'Investment vs Risk Mitigation Value', fill='black')
    
    # Data
    phases = ['Current', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
    investment = [65, 110, 230, 515, 1365]  # Cumulative in thousands
    risk_value = [0, 1200, 1800, 2400, 3000]  # Cumulative risk mitigation value
    
    # Draw line chart
    x_positions = [100, 250, 400, 550, 700]
    y_base = 500
    max_val = 3000
    scale = 350 / max_val
    
    # Investment line (red)
    for i in range(len(investment) - 1):
        y1 = y_base - investment[i] * scale
        y2 = y_base - investment[i+1] * scale
        draw.line([(x_positions[i], y1), (x_positions[i+1], y2)], fill='#FF6B6B', width=3)
        draw.ellipse([(x_positions[i]-5, y1-5), (x_positions[i]+5, y1+5)], fill='#FF6B6B')
    draw.ellipse([(x_positions[-1]-5, y_base-investment[-1]*scale-5), (x_positions[-1]+5, y_base-investment[-1]*scale+5)], fill='#FF6B6B')
    
    # Value line (green)
    for i in range(len(risk_value) - 1):
        y1 = y_base - risk_value[i] * scale
        y2 = y_base - risk_value[i+1] * scale
        draw.line([(x_positions[i], y1), (x_positions[i+1], y2)], fill='#6BCB77', width=3)
        draw.ellipse([(x_positions[i]-5, y1-5), (x_positions[i]+5, y1+5)], fill='#6BCB77')
    draw.ellipse([(x_positions[-1]-5, y_base-risk_value[-1]*scale-5), (x_positions[-1]+5, y_base-risk_value[-1]*scale+5)], fill='#6BCB77')
    
    # X-axis labels
    for i, phase in enumerate(phases):
        draw.text((x_positions[i]-30, 520), phase, fill='black')
    
    # Legend
    draw.line([(550, 100), (600, 100)], fill='#FF6B6B', width=3)
    draw.text((610, 95), 'Investment ($K)', fill='black')
    draw.line([(550, 130), (600, 130)], fill='#6BCB77', width=3)
    draw.text((610, 125), 'Risk Value ($K)', fill='black')
    
    # ROI annotation
    draw.text((400, 150), 'ROI: 2.2x', fill='green')
    draw.text((350, 170), '(Risk value / Investment)', fill='black')
    
    img.save('/home/siva/.openclaw/workspace/visualizations/investment_roi.png')
    print("✅ Created investment_roi.png")

if __name__ == '__main__':
    create_roadmap()
    create_before_after()
    create_risk_reduction()
    create_investment_roi()
    print("\n✅ All improvement visuals created!")
