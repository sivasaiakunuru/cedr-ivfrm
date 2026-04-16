#!/usr/bin/env python3
"""
Create professional-looking UML diagrams with better styling
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('/home/siva/.openclaw/workspace/uml', exist_ok=True)

def draw_rounded_rect(draw, xy, radius=10, fill=None, outline=None, width=2):
    """Draw a rectangle with rounded corners"""
    x1, y1, x2, y2 = xy
    r = radius
    
    # Draw main rectangle
    if fill:
        draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
        draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
        draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
        draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
        draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
        draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)
    
    # Draw outline
    if outline:
        draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=width)

def create_component_diagram_professional():
    """Professional component diagram"""
    img = Image.new('RGB', (1400, 1000), color='#FAFAFA')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((450, 20), 'CEDR System Component Diagram', fill='#1a237e', font=font_title)
    draw.text((480, 50), 'Production Version with Professional Improvements', fill='#666666', font=font_normal)
    
    # Vehicle Section - Large rounded rectangle
    draw_rounded_rect(draw, (20, 90, 650, 950), radius=15, fill='#E3F2FD', outline='#1565C0', width=3)
    draw.text((30, 100), '🚗 VEHICLE (In-Vehicle Network)', fill='#1565C0', font=font_header)
    
    # CAN Bus
    draw_rounded_rect(draw, (40, 140, 200, 180), radius=8, fill='#FFEBEE', outline='#C62828', width=2)
    draw.text((55, 152), 'CAN/CAN-FD Bus', fill='#C62828', font=font_normal)
    
    # ECUs
    ecus = ['Engine ECU', 'Brake ECU', 'Infotainment', 'ADAS ECU']
    for i, ecu in enumerate(ecus):
        y = 200 + i * 55
        draw_rounded_rect(draw, (40, y, 200, y+45), radius=8, fill='#E8EAF6', outline='#3949AB', width=2)
        draw.text((50, y+12), ecu, fill='#3949AB', font=font_normal)
        # Connection line
        draw.line([(120, y+45), (120, 550)], fill='#9E9E9E', width=1)
    
    # CEDR Module
    draw_rounded_rect(draw, (230, 140, 630, 550), radius=12, fill='#BBDEFB', outline='#1565C0', width=3)
    draw.text((380, 150), 'CEDR IV-FRM Module', fill='#0D47A1', font=font_header)
    draw.text((410, 170), 'Raspberry Pi CM4 Industrial', fill='#666666', font=font_small)
    
    # Processing components
    components = [
        ('Event Capture', 250, 210, '#FFE0B2'),
        ('Message Validator', 430, 210, '#FFE0B2'),
        ('Hash Generator', 250, 270, '#FFE0B2'),
        ('ML Inference\nTensorFlow Lite', 430, 270, '#C8E6C9'),
        ('Anomaly Detection', 430, 340, '#C8E6C9'),
        ('AES-256-GCM', 250, 340, '#FFE0B2'),
        ('Local Storage', 250, 400, '#FFE0B2'),
        ('Event Queue', 430, 400, '#FFE0B2'),
        ('Upload Manager', 340, 460, '#FFE0B2'),
    ]
    
    for name, x, y, color in components:
        draw_rounded_rect(draw, (x, y, x+160, y+45), radius=8, fill=color, outline='#424242', width=1)
        lines = name.split('\n')
        for i, line in enumerate(lines):
            offset = 12 if len(lines) == 1 else 5 + i*16
            draw.text((x+8, y+offset), line, fill='#212121', font=font_small)
    
    # Security Hardware Section
    draw_rounded_rect(draw, (230, 570, 630, 760), radius=12, fill='#FFF9C4', outline='#F9A825', width=3)
    draw.text((380, 580), '🔒 Security Hardware', fill='#F57F17', font=font_header)
    
    sec_items = [
        ('NXP A71CH HSM\nFIPS 140-2 Level 2', 250, 620),
        ('Secure Boot\nU-Boot + dm-verity', 430, 620),
        ('TPM 2.0\nMeasured Boot', 250, 690),
    ]
    
    for name, x, y in sec_items:
        draw_rounded_rect(draw, (x, y, x+160, y+55), radius=8, fill='#FFF59D', outline='#F9A825', width=2)
        lines = name.split('\n')
        for i, line in enumerate(lines):
            draw.text((x+8, y+8+i*16), line, fill='#E65100', font=font_small)
    
    # Environmental specs
    draw_rounded_rect(draw, (230, 780, 630, 930), radius=12, fill='#FFEBEE', outline='#C62828', width=2)
    draw.text((380, 790), '🌡️ Environmental Specs', fill='#C62828', font=font_header)
    draw.text((250, 820), 'Operating Temperature: -40°C to +85°C', fill='#B71C1C', font=font_normal)
    draw.text((250, 850), 'Enclosure: IP67 (Dust & Water Resistant)', fill='#B71C1C', font=font_normal)
    draw.text((250, 880), 'Certification: AEC-Q100 Qualified', fill='#B71C1C', font=font_normal)
    
    # Cloud Section
    draw_rounded_rect(draw, (680, 90, 1380, 700), radius=15, fill='#E8F5E9', outline='#2E7D32', width=3)
    draw.text((690, 100), '☁️ MULTI-CLOUD BACKEND', fill='#2E7D32', font=font_header)
    
    # AWS
    draw_rounded_rect(draw, (700, 140, 950, 380), radius=10, fill='#FFEBEE', outline='#C62828', width=2)
    draw.text((780, 150), 'AWS (Primary)', fill='#C62828', font=font_header)
    aws_services = [
        'API Gateway (Kong)',
        'Event Processor',
        'PostgreSQL RDS',
        'S3 Object Storage',
        'AWS KMS',
        'GuardDuty'
    ]
    for i, svc in enumerate(aws_services):
        y = 180 + i * 32
        draw_rounded_rect(draw, (720, y, 930, y+28), radius=6, fill='#FFCDD2', outline='#C62828', width=1)
        draw.text((730, y+5), svc, fill='#B71C1C', font=font_small)
    
    # Azure
    draw_rounded_rect(draw, (970, 140, 1190, 300), radius=10, fill='#E3F2FD', outline='#1565C0', width=2)
    draw.text((1020, 150), 'Azure (DR)', fill='#1565C0', font=font_header)
    azure_services = ['API Management', 'Azure SQL', 'Blob Storage', 'Monitor']
    for i, svc in enumerate(azure_services):
        y = 180 + i * 28
        draw_rounded_rect(draw, (990, y, 1170, y+25), radius=6, fill='#BBDEFB', outline='#1565C0', width=1)
        draw.text((1000, y+4), svc, fill='#0D47A1', font=font_small)
    
    # GCP
    draw_rounded_rect(draw, (1210, 140, 1360, 260), radius=10, fill='#E8F5E9', outline='#2E7D32', width=2)
    draw.text((1230, 150), 'GCP (ML)', fill='#2E7D32', font=font_header)
    gcp_services = ['Vertex AI', 'Cloud IoT', 'Cloud Storage']
    for i, svc in enumerate(gcp_services):
        y = 180 + i * 25
        draw_rounded_rect(draw, (1225, y, 1345, y+22), radius=6, fill='#C8E6C9', outline='#2E7D32', width=1)
        draw.text((1230, y+3), svc, fill='#1B5E20', font=font_small)
    
    # Shared Services
    draw_rounded_rect(draw, (700, 400, 1360, 550), radius=10, fill='#F3E5F5', outline='#7B1FA2', width=2)
    draw.text((1000, 410), 'Shared Services', fill='#7B1FA2', font=font_header)
    shared = ['Global Load Balancer', 'Fleet Correlator', 'ML Training Pipeline', 'Audit Logger']
    for i, svc in enumerate(shared):
        x = 720 + (i % 2) * 310
        y = 440 + (i // 2) * 50
        draw_rounded_rect(draw, (x, y, x+290, y+40), radius=8, fill='#E1BEE7', outline='#7B1FA2', width=1)
        draw.text((x+10, y+10), svc, fill='#4A148C', font=font_normal)
    
    # SOC Integration
    draw_rounded_rect(draw, (700, 570, 1360, 680), radius=10, fill='#FFF3E0', outline='#E65100', width=2)
    draw.text((1000, 580), '🔔 SOC Integration', fill='#E65100', font=font_header)
    draw_rounded_rect(draw, (720, 610, 1000, 660), radius=8, fill='#FFE0B2', outline='#E65100', width=1)
    draw.text((740, 620), 'eSentire SOC', fill='#E65100', font=font_normal)
    draw.text((740, 640), '24/7 Monitoring', fill='#BF360C', font=font_small)
    draw_rounded_rect(draw, (1020, 610, 1340, 660), radius=8, fill='#FFE0B2', outline='#E65100', width=1)
    draw.text((1040, 620), 'Threat Intelligence', fill='#E65100', font=font_normal)
    draw.text((1040, 640), 'MISP + Commercial Feeds', fill='#BF360C', font=font_small)
    
    # Investigators
    draw_rounded_rect(draw, (680, 720, 1380, 950), radius=15, fill='#FCE4EC', outline='#C2185B', width=3)
    draw.text((1000, 730), '👤 INVESTIGATOR TOOLS', fill='#C2185B', font=font_header)
    
    tools = [
        ('Web Dashboard', 720, 770, '#F8BBD9'),
        ('Mobile App', 1020, 770, '#F8BBD9'),
        ('Evidence Export', 720, 850, '#F8BBD9'),
        ('API Access', 1020, 850, '#F8BBD9'),
    ]
    
    for name, x, y, color in tools:
        draw_rounded_rect(draw, (x, y, x+270, y+65), radius=10, fill=color, outline='#C2185B', width=2)
        draw.text((x+80, y+20), name, fill='#880E4F', font=font_normal)
    
    # Connection arrows
    draw.line([(630, 470), (680, 470)], fill='#1565C0', width=3)
    draw.polygon([(675, 465), (685, 470), (675, 475)], fill='#1565C0')
    draw.text((640, 450), 'TLS 1.3', fill='#1565C0', font=font_small)
    
    img.save('/home/siva/.openclaw/workspace/uml/component_diagram_professional.png')
    print("✅ Created component_diagram_professional.png")

if __name__ == '__main__':
    create_component_diagram_professional()
