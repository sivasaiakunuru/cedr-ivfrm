import os
import urllib.request
import matplotlib.pyplot as plt
import urllib.parse

DARK_NAVY = '#0A1628'
ELECTRIC_BLUE = '#00A8E8'
WHITE = '#FFFFFF'
ALERT_RED = '#E53E3E'

os.makedirs('images', exist_ok=True)

prompts = {
    "slide1.jpg": "Slide 1 Image\nModern Car Dealership\nDark Navy Aesthetic",
    "slide2.jpg": "Slide 2 Image\nRoadmap Infographic\nSteps & Timeline",
    "slide4.jpg": "Slide 4 Image\nIncident Timeline\nJune 18 - July 30",
    "slide5.jpg": "Slide 5 Image\nBlackSuit Ransomware\nMITRE ATT&CK",
    "slide6.jpg": "Slide 6 Image\nOperational Impact\nManual Paperwork",
    "slide8.jpg": "Slide 8 Image\nRTO & RPO Timeline\nGap Analysis",
    "slide9.jpg": "Slide 9 Image\nRoot Cause Analysis\nFishbone Diagram",
    "slide10.jpg": "Slide 10 Image\nNIST CSF 2.0\nWheel Diagram",
    "slide11.jpg": "Slide 11 Image\nLegal Compliance\nFTC, PIPEDA, SEC",
    "slide12.jpg": "Slide 12 Image\nEthical Dilemmas\nBalance Scale",
    "slide13.jpg": "Slide 13 Image\nZero Trust Architecture\n3-2-1 Backup",
    "slide14.jpg": "Slide 14 Image\nCase Comparison\nVenn Diagram",
    "slide15.jpg": "Slide 15 Image\nKey Takeaways\nDiscussion Questions",
    "slide16.jpg": "Slide 16 Image\nReferences\nQ&A Session"
}

def download_placeholder(text, filename):
    encoded_text = urllib.parse.quote(text)
    # Using placehold.co to generate an image with text
    url = f"https://placehold.co/800x600/0A1628/FFFFFF/png?text={encoded_text}"
    print(f"Downloading {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response, open(f"images/{filename}", 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

for filename, text in prompts.items():
    download_placeholder(text, filename)

print("All placehold images generated.")
