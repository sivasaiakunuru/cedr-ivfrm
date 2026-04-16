#!/usr/bin/env python3
"""
Create updated UML diagram PNGs with professional improvements
Using PIL since PlantUML may not be available
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('/home/siva/.openclaw/workspace/uml', exist_ok=True)

def create_component_diagram_v2():
    """Updated component diagram with HSM, ML, multi-cloud"""
    img = Image.new('RGB', (1200, 900), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((400, 10), 'CEDR Component Diagram (Production)', fill='black')
    draw.text((450, 35), 'v2.0 - Professional Improvements', fill='gray')
    
    # Vehicle Section (Left)
    draw.rectangle([(20, 70), (580, 880)], outline='#1a237e', width=3)
    draw.text((30, 75), 'Vehicle (In-Vehicle Network)', fill='#1a237e')
    
    # CAN Bus
    draw.rectangle([(40, 110), (200, 150)], fill='#FFE6E6', outline='black')
    draw.text((50, 120), 'CAN/CAN-FD Bus', fill='black')
    
    # ECUs
    for i, name in enumerate(['Engine ECU', 'Brake ECU', 'Infotainment', 'ADAS ECU']):
        y = 170 + i * 60
        draw.rectangle([(40, y), (200, y+40)], fill='#E6E6FF', outline='black')
        draw.text((50, y+10), name, fill='black')
        draw.line([(120, y+40), (120, 500)], fill='black', width=1)
    
    # CEDR Module
    draw.rectangle([(230, 110), (560, 450)], fill='#E6F3FF', outline='#0066CC', width=2)
    draw.text((340, 115), 'CEDR IV-FRM Module', fill='#0066CC')
    draw.text((350, 135), '(CM4 Industrial)', fill='gray')
    
    # CEDR Components
    components = [
        ('Event Capture', 250, 170),
        ('ML Inference', 420, 170),
        ('Hash Generator', 250, 230),
        ('Anomaly Detection', 420, 230),
        ('AES-256-GCM Crypto', 250, 290),
        ('Local Storage', 420, 290),
        ('Upload Manager', 250, 350),
        ('Event Queue', 420, 350),
    ]
    
    for name, x, y in components:
        color = '#90EE90' if 'ML' in name or 'Anomaly' in name else '#FFE6E6'
        draw.rectangle([(x, y), (x+140, y+40)], fill=color, outline='black')
        draw.text((x+5, y+10), name, fill='black')
    
    # Security Hardware
    draw.rectangle([(230, 470), (560, 650)], fill='#FFFFE6', outline='#CC9900', width=2)
    draw.text((350, 475), 'Security Hardware', fill='#CC9900')
    
    sec_components = [
        ('NXP A71CH HSM', 250, 520),
        ('Secure Boot (U-Boot)', 250, 570),
        ('TPM 2.0', 250, 620),
    ]
    
    for name, x, y in sec_components:
        draw.rectangle([(x, y), (x+280, y+35)], fill='#FFFACD', outline='black')
        draw.text((x+10, y+8), name, fill='black')
    
    # Cloud Section (Right)
    draw.rectangle([(620, 70), (1180, 880)], outline='#006600', width=3)
    draw.text((630, 75), 'Multi-Cloud Backend', fill='#006600')
    
    # AWS
    draw.rectangle([(640, 110), (860, 350)], fill='#FFE6E6', outline='#CC0000', width=2)
    draw.text((720, 115), 'AWS (Primary)', fill='#CC0000')
    aws = ['API Gateway', 'Event Processor', 'PostgreSQL RDS', 'S3 Storage', 'KMS']
    for i, name in enumerate(aws):
        y = 150 + i * 40
        draw.rectangle([(660, y), (840, y+30)], fill='#FFCCCC', outline='black')
        draw.text((670, y+5), name, fill='black')
    
    # Azure
    draw.rectangle([(880, 110), (1170, 280)], fill='#E6F2FF', outline='#0066CC', width=2)
    draw.text((990, 115), 'Azure (Backup)', fill='#0066CC')
    azure = ['API Management', 'Azure SQL', 'Blob Storage']
    for i, name in enumerate(azure):
        y = 150 + i * 40
        draw.rectangle([(900, y), (1150, y+30)], fill='#CCE5FF', outline='black')
        draw.text((910, y+5), name, fill='black')
    
    # Shared Services
    draw.rectangle([(640, 370), (1170, 550)], fill='#F0F0F0', outline='black', width=2)
    draw.text((900, 375), 'Shared Services', fill='black')
    shared = ['Global Load Balancer', 'Fleet Correlator', 'ML Training (Cloud)', 'Audit Logger']
    for i, name in enumerate(shared):
        x = 660 + (i % 2) * 260
        y = 410 + (i // 2) * 60
        draw.rectangle([(x, y), (x+240, y+40)], fill='#E6E6E6', outline='black')
        draw.text((x+10, y+10), name, fill='black')
    
    # SOC Integration
    draw.rectangle([(640, 570), (1170, 700)], fill='#FFF4E6', outline='#FF6600', width=2)
    draw.text((900, 575), 'SOC Integration', fill='#FF6600')
    draw.rectangle([(660, 610), (840, 680)], fill='#FFE5CC', outline='black')
    draw.text((680, 625), 'eSentire SOC', fill='black')
    draw.text((680, 650), '24/7 Monitoring', fill='black')
    draw.rectangle([(880, 610), (1150, 680)], fill='#FFE5CC', outline='black')
    draw.text((900, 625), 'Threat Intelligence', fill='black')
    draw.text((900, 650), 'Feeds', fill='black')
    
    # Investigator Tools
    draw.rectangle([(640, 720), (1170, 860)], fill='#FFE6F0', outline='#CC0066', width=2)
    draw.text((900, 725), 'Investigator Tools', fill='#CC0066')
    tools = ['Web Dashboard', 'Mobile App', 'Evidence Export']
    for i, name in enumerate(tools):
        x = 660 + i * 170
        draw.rectangle([(x, 760), (x+150, 840)], fill='#FFCCE5', outline='black')
        draw.text((x+10, 790), name, fill='black')
    
    # Connection lines (simplified)
    # Vehicle to Cloud
    draw.line([(560, 370), (640, 370)], fill='black', width=2)
    draw.text((580, 350), 'TLS 1.3', fill='black')
    
    # HSM to Crypto
    draw.line([(350, 520), (350, 480)], fill='black', width=2)
    
    img.save('/home/siva/.openclaw/workspace/uml/component_diagram_v2.png')
    print("✅ Created component_diagram_v2.png")

def create_deployment_diagram_v2():
    """Updated deployment diagram with automotive hardware"""
    img = Image.new('RGB', (1100, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((350, 10), 'CEDR Deployment Diagram (Production)', fill='black')
    draw.text((400, 35), 'v2.0 - Automotive Grade', fill='gray')
    
    # Vehicle Node
    draw.rectangle([(20, 70), (500, 750)], outline='#1a237e', width=3)
    draw.text((30, 75), 'Vehicle Environment', fill='#1a237e')
    
    # Hardware
    draw.rectangle([(40, 110), (480, 350)], fill='#E6F3FF', outline='#0066CC', width=2)
    draw.text((200, 115), 'CEDR Hardware (Automotive)', fill='#0066CC')
    
    hardware = [
        ('Raspberry Pi CM4 Industrial', 60, 150, '#90EE90'),
        ('Industrial CAN HAT (Isolated)', 60, 200, '#FFE6E6'),
        ('NXP A71CH HSM', 60, 250, '#FFFFE6'),
        ('Quectel BG96 4G/LTE', 60, 300, '#E6F3FF'),
    ]
    
    for name, x, y, color in hardware:
        draw.rectangle([(x, y), (x+400, y+35)], fill=color, outline='black')
        draw.text((x+10, y+8), name, fill='black')
    
    # Software Stack
    draw.rectangle([(40, 370), (480, 620)], fill='#F0F8FF', outline='#0066CC', width=2)
    draw.text((200, 375), 'Software Stack (Secure)', fill='#0066CC')
    
    software = [
        ('Secure Boot (U-Boot + dm-verity)', 60, 410),
        ('Linux Kernel (Verified)', 60, 460),
        ('Python 3.11 + TensorFlow Lite', 60, 510),
        ('SQLite (Encrypted)', 60, 560),
    ]
    
    for name, x, y in software:
        draw.rectangle([(x, y), (x+400, y+35)], fill='#E6F3FF', outline='black')
        draw.text((x+10, y+8), name, fill='black')
    
    # Temp specs
    draw.rectangle([(40, 640), (480, 730)], fill='#FFE6E6', outline='red', width=2)
    draw.text((150, 645), 'Environmental Specs', fill='red')
    draw.text((60, 670), 'Operating: -40°C to +85°C', fill='black')
    draw.text((60, 695), 'Enclosure: IP67 (Dust/Water)', fill='black')
    
    # Cloud Node
    draw.rectangle([(530, 70), (1080, 450)], outline='#006600', width=3)
    draw.text((540, 75), 'Multi-Cloud Infrastructure', fill='#006600')
    
    # AWS
    draw.rectangle([(550, 110), (800, 280)], fill='#FFE6E6', outline='#CC0000', width=2)
    draw.text((640, 115), 'AWS (Primary)', fill='#CC0000')
    aws_items = ['EC2 API Servers', 'RDS PostgreSQL', 'S3 Storage', 'KMS']
    for i, item in enumerate(aws_items):
        y = 145 + i * 32
        draw.rectangle([(570, y), (780, y+28)], fill='#FFCCCC', outline='black')
        draw.text((580, y+5), item, fill='black')
    
    # Azure
    draw.rectangle([(820, 110), (1060, 220)], fill='#E6F2FF', outline='#0066CC', width=2)
    draw.text((880, 115), 'Azure (DR)', fill='#0066CC')
    draw.rectangle([(840, 145), (1040, 175)], fill='#CCE5FF', outline='black')
    draw.text((850, 150), 'Azure SQL + Blob', fill='black')
    draw.rectangle([(840, 185), (1040, 210)], fill='#CCE5FF', outline='black')
    draw.text((850, 190), 'API Management', fill='black')
    
    # K8s
    draw.rectangle([(550, 300), (1060, 430)], fill='#F0F0F0', outline='black', width=2)
    draw.text((750, 305), 'Kubernetes Cluster', fill='black')
    k8s = ['Kong API Gateway', 'Event Processors', 'ML Services']
    for i, item in enumerate(k8s):
        x = 570 + i * 160
        draw.rectangle([(x, 340), (x+150, 410)], fill='#E6E6E6', outline='black')
        draw.text((x+10, 370), item, fill='black')
    
    # SOC
    draw.rectangle([(530, 470), (1080, 600)], fill='#FFF4E6', outline='#FF6600', width=2)
    draw.text((750, 475), 'Security Operations', fill='#FF6600')
    draw.rectangle([(550, 510), (800, 580)], fill='#FFE5CC', outline='black')
    draw.text((570, 525), 'eSentire SOC', fill='black')
    draw.text((570, 550), '24/7 Monitoring', fill='black')
    draw.rectangle([(820, 510), (1060, 580)], fill='#FFE5CC', outline='black')
    draw.text((840, 525), 'Splunk SIEM', fill='black')
    draw.text((840, 550), 'XSOAR Automation', fill='black')
    
    # Workstation
    draw.rectangle([(530, 620), (1080, 750)], fill='#FFE6F0', outline='#CC0066', width=2)
    draw.text((750, 625), 'Investigator Workstation', fill='#CC0066')
    draw.rectangle([(550, 660), (800, 730)], fill='#FFCCE5', outline='black')
    draw.text((600, 685), 'Web Dashboard', fill='black')
    draw.rectangle([(820, 660), (1060, 730)], fill='#FFCCE5', outline='black')
    draw.text((860, 685), 'Mobile App', fill='black')
    
    # Connection
    draw.line([(480, 280), (530, 280)], fill='black', width=2)
    draw.text((490, 260), '4G/LTE', fill='black')
    
    img.save('/home/siva/.openclaw/workspace/uml/deployment_diagram_v2.png')
    print("✅ Created deployment_diagram_v2.png")

def create_class_diagram_v2():
    """Updated class diagram with new classes"""
    img = Image.new('RGB', (1100, 900), color='white')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((400, 10), 'CEDR Class Diagram (Production)', fill='black')
    draw.text((450, 35), 'v2.0 - With ML & Security', fill='gray')
    
    # Event Class
    draw.rectangle([(30, 70), (280, 280)], fill='#E6F3FF', outline='black', width=2)
    draw.text((120, 75), 'Event', fill='black')
    draw.line([(30, 95), (280, 95)], fill='black', width=2)
    
    event_attrs = [
        '+eventId: String',
        '+vehicleId: String',
        '+timestamp: DateTime',
        '+severity: String',
        '+hash: String',
        '+previousHash: String',
        '+anomalyScore: Float',
        '+isAnomalous: Boolean',
    ]
    for i, attr in enumerate(event_attrs):
        draw.text((40, 105 + i*20), attr, fill='black')
    
    draw.line([(30, 260), (280, 260)], fill='black', width=1)
    draw.text((40, 265), '+encrypt()', fill='black')
    draw.text((150, 265), '+verifyIntegrity()', fill='black')
    
    # Vehicle Class
    draw.rectangle([(320, 70), (540, 200)], fill='#E6FFE6', outline='black', width=2)
    draw.text((400, 75), 'Vehicle', fill='black')
    draw.line([(320, 95), (540, 95)], fill='black', width=2)
    draw.text((330, 105), '+vehicleId: String', fill='black')
    draw.text((330, 125), '+vin: String', fill='black')
    draw.text((330, 145), '+securityScore: Float', fill='black')
    draw.line([(320, 165), (540, 165)], fill='black', width=1)
    draw.text((330, 175), '+getSecurityScore()', fill='black')
    
    # MLAnomalyDetector (New)
    draw.rectangle([(30, 320), (280, 480)], fill='#90EE90', outline='black', width=2)
    draw.text((60, 325), 'MLAnomalyDetector ⭐', fill='black')
    draw.line([(30, 345), (280, 345)], fill='black', width=2)
    draw.text((40, 355), '+modelPath: String', fill='black')
    draw.text((40, 375), '+threshold: Float', fill='black')
    draw.text((40, 395), '+modelVersion: String', fill='black')
    draw.line([(30, 415), (280, 415)], fill='black', width=1)
    draw.text((40, 425), '+predict()', fill='black')
    draw.text((40, 445), '+explainPrediction()', fill='black')
    draw.text((40, 465), '+exportModel()', fill='black')
    
    # HSMManager (New)
    draw.rectangle([(320, 230), (540, 400)], fill='#FFFACD', outline='black', width=2)
    draw.text((370, 235), 'HSMManager ⭐', fill='black')
    draw.line([(320, 255), (540, 255)], fill='black', width=2)
    draw.text((330, 265), '+hsmType: String', fill='black')
    draw.text((330, 285), '+isTampered: Boolean', fill='black')
    draw.line([(320, 305), (540, 305)], fill='black', width=1)
    draw.text((330, 315), '+signData()', fill='black')
    draw.text((330, 335), '+verifySignature()', fill='black')
    draw.text((330, 355), '+checkTamper()', fill='black')
    draw.text((330, 375), '+zeroize()', fill='black')
    
    # SecureBootVerifier (New)
    draw.rectangle([(580, 70), (850, 250)], fill='#FFE5CC', outline='black', width=2)
    draw.text((620, 75), 'SecureBootVerifier ⭐', fill='black')
    draw.line([(580, 95), (850, 95)], fill='black', width=2)
    draw.text((590, 105), '+bootloaderHash: String', fill='black')
    draw.text((590, 125), '+kernelHash: String', fill='black')
    draw.text((590, 145), '+verified: Boolean', fill='black')
    draw.line([(580, 165), (850, 165)], fill='black', width=1)
    draw.text((590, 175), '+verifyBootloader()', fill='black')
    draw.text((590, 195), '+verifyKernel()', fill='black')
    draw.text((590, 215), '+measureBoot()', fill='black')
    
    # CloudServer
    draw.rectangle([(580, 280), (850, 420)], fill='#FFE6E6', outline='black', width=2)
    draw.text((660, 285), 'CloudServer', fill='black')
    draw.line([(580, 305), (850, 305)], fill='black', width=2)
    draw.text((590, 315), '+serverId: String', fill='black')
    draw.text((590, 335), '+cloudProvider: String', fill='black')
    draw.line([(580, 355), (850, 355)], fill='black', width=1)
    draw.text((590, 365), '+receiveEvent()', fill='black')
    draw.text((590, 385), '+correlateEvents()', fill='black')
    draw.text((590, 405), '+trainMLModel()', fill='black')
    
    # TemperatureMonitor (New)
    draw.rectangle([(320, 430), (540, 580)], fill='#E6F3FF', outline='black', width=2)
    draw.text((360, 435), 'TemperatureMonitor', fill='black')
    draw.line([(320, 455), (540, 455)], fill='black', width=2)
    draw.text((330, 465), '+currentTemp: Float', fill='black')
    draw.text((330, 485), '+minTemp: -40°C', fill='black')
    draw.text((330, 505), '+maxTemp: +85°C', fill='black')
    draw.line([(320, 525), (540, 525)], fill='black', width=1)
    draw.text((330, 535), '+checkLimits()', fill='black')
    draw.text((330, 555), '+triggerThrottle()', fill='black')
    
    # MultiCloudManager (New)
    draw.rectangle([(580, 450), (850, 600)], fill='#CCE5FF', outline='black', width=2)
    draw.text((630, 455), 'MultiCloudManager ⭐', fill='black')
    draw.line([(580, 475), (850, 475)], fill='black', width=2)
    draw.text((590, 485), '+providers: List', fill='black')
    draw.text((590, 505), '+primaryRegion: String', fill='black')
    draw.line([(580, 525), (850, 525)], fill='black', width=1)
    draw.text((590, 535), '+routeTraffic()', fill='black')
    draw.text((590, 555), '+failover()', fill='black')
    draw.text((590, 575), '+syncData()', fill='black')
    
    # Investigator
    draw.rectangle([(30, 520), (280, 650)], fill='#FFE6F0', outline='black', width=2)
    draw.text((100, 525), 'Investigator', fill='black')
    draw.line([(30, 545), (280, 545)], fill='black', width=2)
    draw.text((40, 555), '+investigatorId: String', fill='black')
    draw.text((40, 575), '+role: String', fill='black')
    draw.text((40, 595), '+mfaToken: String', fill='black')
    draw.line([(30, 615), (280, 615)], fill='black', width=1)
    draw.text((40, 625), '+authenticateMFA()', fill='black')
    
    # EvidencePackage
    draw.rectangle([(320, 610), (540, 750)], fill='#F0E6FF', outline='black', width=2)
    draw.text((360, 615), 'EvidencePackage', fill='black')
    draw.line([(320, 635), (540, 635)], fill='black', width=2)
    draw.text((330, 645), '+packageId: String', fill='black')
    draw.text((330, 665), '+digitalSignature: String', fill='black')
    draw.text((330, 685), '+chainOfCustody: String', fill='black')
    draw.line([(320, 705), (540, 705)], fill='black', width=1)
    draw.text((330, 715), '+verifySignature()', fill='black')
    draw.text((330, 735), '+addCustodyEntry()', fill='black')
    
    # Relationships (lines)
    draw.line([(280, 175), (320, 135)], fill='black', width=1)
    draw.line([(280, 400), (320, 315)], fill='black', width=1)  # Event to HSM
    draw.line([(280, 200), (320, 500)], fill='black', width=1)  # Event to Temp
    draw.line([(540, 330), (580, 350)], fill='black', width=1)  # HSM to Cloud
    draw.line([(540, 145), (580, 150)], fill='black', width=1)  # Vehicle to SecureBoot
    draw.line([(540, 520), (580, 520)], fill='black', width=1)  # Temp to MultiCloud
    
    # Legend
    draw.rectangle([(900, 650), (1070, 880)], fill='white', outline='black')
    draw.text((910, 655), 'Legend:', fill='black')
    draw.rectangle([(910, 680), (950, 710)], fill='#90EE90', outline='black')
    draw.text((960, 688), 'ML/AI', fill='black')
    draw.rectangle([(910, 720), (950, 750)], fill='#FFFACD', outline='black')
    draw.text((960, 728), 'Security HW', fill='black')
    draw.rectangle([(910, 760), (950, 790)], fill='#FFE5CC', outline='black')
    draw.text((960, 768), 'Secure Boot', fill='black')
    draw.rectangle([(910, 800), (950, 830)], fill='#CCE5FF', outline='black')
    draw.text((960, 808), 'Cloud', fill='black')
    draw.text((910, 850), '⭐ = New in v2.0', fill='black')
    
    img.save('/home/siva/.openclaw/workspace/uml/class_diagram_v2.png')
    print("✅ Created class_diagram_v2.png")

if __name__ == '__main__':
    create_component_diagram_v2()
    create_deployment_diagram_v2()
    create_class_diagram_v2()
    print("\n✅ All updated UML diagrams created!")
    print("Files saved to: /home/siva/.openclaw/workspace/uml/")
