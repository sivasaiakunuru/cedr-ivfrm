#!/usr/bin/env python3
import os
import base64
import zlib
import urllib.request
import time

UML_DIR = "/home/siva/.openclaw/workspace/uml"
PLANTUML_URL = "http://www.plantuml.com/plantuml/png"

def encode_plantuml(text):
    """Encode PlantUML text for URL"""
    zlibbed = zlib.compress(text.encode('utf-8'), 9)
    compressed = zlibbed[2:-4]  # Remove zlib headers
    return base64.urlsafe_b64encode(compressed).decode('ascii').rstrip('=')

def generate_png(puml_file):
    """Generate PNG from PlantUML file"""
    png_file = puml_file.replace('.puml', '.png')
    puml_path = os.path.join(UML_DIR, puml_file)
    png_path = os.path.join(UML_DIR, png_file)
    
    print(f"Processing {puml_file}...")
    
    with open(puml_path, 'r') as f:
        content = f.read()
    
    encoded = encode_plantuml(content)
    url = f"{PLANTUML_URL}/{encoded}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(png_path, 'wb') as f:
                f.write(response.read())
        size = os.path.getsize(png_path)
        if size > 1000:
            print(f"  ✅ {png_file} ({size//1024}KB)")
            return True
        else:
            print(f"  ❌ {png_file} too small ({size} bytes)")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    puml_files = [f for f in os.listdir(UML_DIR) if f.endswith('.puml')]
    
    print(f"Found {len(puml_files)} PlantUML files\n")
    
    success = 0
    for puml_file in sorted(puml_files):
        if generate_png(puml_file):
            success += 1
        time.sleep(1)  # Be nice to the server
    
    print(f"\n✅ Generated {success}/{len(puml_files)} PNG images")
    print(f"📁 Location: {UML_DIR}")

if __name__ == "__main__":
    main()
