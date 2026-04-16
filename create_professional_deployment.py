#!/usr/bin/env python3
"""
Create professional deployment diagram
"""

from PIL import Image, ImageDraw, ImageFont
import os

def draw_rounded_rect(draw, xy, radius=10, fill=None, outline=None, width=2):
    x1, y1, x2, y2 = xy
    r = radius
    if fill:
        draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
        draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
        draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
        draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
        draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
        draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)
    if outline:
        draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=width)

os.makedirs('/home/siva/.openclaw/workspace/uml', exist_ok=True)

img = Image.new('RGB', (1400, 900), color='#FAFAFA')
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
draw.text((450, 15), 'CEDR Deployment Architecture', fill='#1a237e', font=font_title)
draw.text((480, 45), 'Automotive-Grade Production Environment', fill='#666666', font=font_normal)

# Vehicle Node
draw_rounded_rect(draw, (20, 80, 600, 850), radius=15, fill='#E3F2FD', outline='#1565C0', width=3)
draw.text((30, 90), '🚗 VEHICLE ENVIRONMENT', fill='#1565C0', font=font_header)

# In-Vehicle Network
draw_rounded_rect(draw, (40, 130, 580, 200), radius=10, fill='#FFEBEE', outline='#C62828', width=2)
draw.text((250, 140), 'In-Vehicle Network', fill='#C62828', font=font_header)
draw.text((60, 165), 'CAN Bus • CAN-FD • Automotive Ethernet', fill='#B71C1C', font=font_normal)

# CEDR Hardware
draw_rounded_rect(draw, (40, 220, 580, 450), radius=12, fill='#BBDEFB', outline='#1565C0', width=3)
draw.text((220, 230), 'CEDR Hardware (Automotive-Grade)', fill='#0D47A1', font=font_header)

hardware = [
    ('🖥️ Raspberry Pi CM4 Industrial', '8GB RAM, 32GB eMMC, -20°C to +70°C', '#E8F5E9'),
    ('🔌 Industrial CAN HAT', 'Isolated, 5kV protection, AEC-Q100', '#FFF3E0'),
    ('🔐 NXP A71CH HSM', 'FIPS 140-2 Level 2, Secure Key Storage', '#FFF9C4'),
    ('📡 Quectel BG96 4G/LTE', 'LTE Cat-M1/NB-IoT, GPS/GNSS', '#F3E5F5'),
]

for i, (name, desc, color) in enumerate(hardware):
    y = 265 + i * 45
    draw_rounded_rect(draw, (60, y, 560, y+40), radius=8, fill=color, outline='#424242', width=1)
    draw.text((70, y+3), name, fill='#212121', font=font_normal)
    draw.text((70, y+20), desc, fill='#616161', font=font_small)

# Software Stack
draw_rounded_rect(draw, (40, 470, 580, 700), radius=12, fill='#E8F5E9', outline='#2E7D32', width=3)
draw.text((220, 480), 'Secure Software Stack', fill='#1B5E20', font=font_header)

software = [
    ('🔒 Secure Boot (U-Boot)', 'RSA/ECDSA Signature Verification', '#C8E6C9'),
    ('🛡️ Linux Kernel (dm-verity)', 'Verified Boot, Integrity Protection', '#C8E6C9'),
    ('🤖 Python 3.11 + TensorFlow Lite', 'ML Inference on Edge Device', '#C8E6C9'),
    ('💾 SQLite (SQLCipher)', 'AES-256 Database Encryption', '#C8E6C9'),
    ('📤 CEDR Application', 'Event Capture, Processing, Upload', '#C8E6C9'),
]

for i, (name, desc, color) in enumerate(software):
    y = 515 + i * 36
    draw_rounded_rect(draw, (60, y, 560, y+33), radius=6, fill=color, outline='#2E7D32', width=1)
    draw.text((70, y+3), name, fill='#1B5E20', font=font_normal)
    draw.text((70, y+18), desc, fill='#33691E', font=font_small)

# Environmental Specs
draw_rounded_rect(draw, (40, 720, 580, 835), radius=12, fill='#FFEBEE', outline='#C62828', width=3)
draw.text((200, 730), '🌡️ Environmental Specifications', fill='#C62828', font=font_header)
specs = [
    '✓ Operating Temperature: -40°C to +85°C (AEC-Q100 Grade 2)',
    '✓ Enclosure: IP67 Rated (Dust Tight, Immersion 1m)',
    '✓ Vibration: ISO 16750-3 (Vehicle Durability)',
    '✓ EMC: ISO 11452 (Automotive Immunity)',
]
for i, spec in enumerate(specs):
    draw.text((60, 760 + i*18), spec, fill='#B71C1C', font=font_small)

# Cloud Infrastructure
draw_rounded_rect(draw, (620, 80, 1380, 550), radius=15, fill='#E8F5E9', outline='#2E7D32', width=3)
draw.text((950, 90), '☁️ MULTI-CLOUD INFRASTRUCTURE', fill='#2E7D32', font=font_header)

# AWS Primary
draw_rounded_rect(draw, (640, 130, 920, 400), radius=10, fill='#FFEBEE', outline='#C62828', width=2)
draw.text((730, 140), 'AWS (Primary)', fill='#C62828', font=font_header)
aws_items = [
    ('EC2 API Servers', 't3.large × 3, Auto Scaling'),
    ('Application Load Balancer', 'HTTPS/TLS 1.3 Termination'),
    ('PostgreSQL RDS', 'Multi-AZ, Encrypted'),
    ('ElastiCache Redis', 'Session Cache, Rate Limiting'),
    ('S3 Object Storage', 'Versioned, Cross-Region'),
    ('AWS KMS', 'Key Management, HSM Backed'),
    ('GuardDuty', 'Threat Detection'),
    ('WAF', 'DDoS Protection'),
]
for i, (name, desc) in enumerate(aws_items):
    y = 170 + i * 28
    draw_rounded_rect(draw, (655, y, 905, y+26), radius=6, fill='#FFCDD2', outline='#C62828', width=1)
    draw.text((660, y+2), name, fill='#B71C1C', font=font_small)
    draw.text((660, y+14), desc, fill='#8B0000', font=font_small)

# Azure DR
draw_rounded_rect(draw, (940, 130, 1200, 300), radius=10, fill='#E3F2FD', outline='#1565C0', width=2)
draw.text((1000, 140), 'Azure (Disaster Recovery)', fill='#1565C0', font=font_header)
azure_items = [
    ('API Management', 'Backup API Gateway'),
    ('Azure SQL Hyperscale', 'Geo-Replication'),
    ('Blob Storage', 'Cold Archive'),
    ('Azure Monitor', 'Cross-Cloud Metrics'),
]
for i, (name, desc) in enumerate(azure_items):
    y = 170 + i * 32
    draw_rounded_rect(draw, (955, y, 1185, y+28), radius=6, fill='#BBDEFB', outline='#1565C0', width=1)
    draw.text((960, y+2), name, fill='#0D47A1', font=font_small)
    draw.text((960, y+15), desc, fill='#01579B', font=font_small)

# GCP ML
draw_rounded_rect(draw, (1220, 130, 1360, 260), radius=10, fill='#E8F5E9', outline='#2E7D32', width=2)
draw.text((1240, 140), 'GCP (ML)', fill='#2E7D32', font=font_header)
draw_rounded_rect(draw, (1230, 170, 1350, 205), radius=6, fill='#C8E6C9', outline='#2E7D32', width=1)
draw.text((1235, 177), 'Vertex AI', fill='#1B5E20', font=font_small)
draw.text((1235, 192), 'Model Training', fill='#33691E', font=font_small)
draw_rounded_rect(draw, (1230, 215, 1350, 250), radius=6, fill='#C8E6C9', outline='#2E7D32', width=1)
draw.text((1235, 222), 'Cloud IoT Core', fill='#1B5E20', font=font_small)
draw.text((1235, 237), 'Device Mgmt', fill='#33691E', font=font_small)

# Kubernetes
draw_rounded_rect(draw, (640, 420, 1360, 530), radius=10, fill='#F3E5F5', outline='#7B1FA2', width=2)
draw.text((970, 430), 'Kubernetes Cluster (EKS)', fill='#7B1FA2', font=font_header)
k8s_items = ['Kong API Gateway', 'Event Processors', 'ML Inference Services', 'Fleet Correlator']
for i, name in enumerate(k8s_items):
    x = 655 + (i % 2) * 350
    y = 460 + (i // 2) * 35
    draw_rounded_rect(draw, (x, y, x+330, y+30), radius=8, fill='#E1BEE7', outline='#7B1FA2', width=1)
    draw.text((x+100, y+6), name, fill='#4A148C', font=font_normal)

# SOC
draw_rounded_rect(draw, (620, 570, 1380, 700), radius=15, fill='#FFF3E0', outline='#E65100', width=3)
draw.text((970, 580), '🔔 SECURITY OPERATIONS CENTER', fill='#E65100', font=font_header)
draw_rounded_rect(draw, (640, 615, 970, 680), radius=10, fill='#FFE0B2', outline='#E65100', width=2)
draw.text((730, 625), 'eSentire SOC', fill='#E65100', font=font_header)
draw.text((670, 650), '24/7 Monitoring & Incident Response', fill='#BF360C', font=font_normal)
draw_rounded_rect(draw, (990, 615, 1360, 680), radius=10, fill='#FFE0B2', outline='#E65100', width=2)
draw.text((1050, 625), 'Splunk + XSOAR', fill='#E65100', font=font_header)
draw.text((1010, 650), 'SIEM & Automated Response', fill='#BF360C', font=font_normal)

# Investigators
draw_rounded_rect(draw, (620, 720, 1380, 870), radius=15, fill='#FCE4EC', outline='#C2185B', width=3)
draw.text((970, 730), '👤 INVESTIGATOR WORKSTATIONS', fill='#C2185B', font=font_header)
tools = [
    ('Web Dashboard', 'Chrome, Firefox, Safari, Edge'),
    ('Mobile App', 'iOS & Android Native'),
    ('API Access', 'REST API + WebSocket'),
    ('Evidence Export', 'PDF, JSON, Chain of Custody'),
]
for i, (name, desc) in enumerate(tools):
    x = 640 + (i % 2) * 370
    y = 770 + (i // 2) * 45
    draw_rounded_rect(draw, (x, y, x+350, y+40), radius=10, fill='#F8BBD9', outline='#C2185B', width=2)
    draw.text((x+120, y+3), name, fill='#880E4F', font=font_normal)
    draw.text((x+10, y+22), desc, fill='#AD1457', font=font_small)

# Connection
draw.line([(580, 335), (620, 335)], fill='#1565C0', width=3)
draw.polygon([(615, 330), (625, 335), (615, 340)], fill='#1565C0')
draw.text((590, 315), '4G/LTE', fill='#1565C0', font=font_small)
draw.text((585, 345), 'TLS 1.3 + mTLS', fill='#1565C0', font=font_small)

img.save('/home/siva/.openclaw/workspace/uml/deployment_diagram_professional.png')
print("✅ Created deployment_diagram_professional.png")
