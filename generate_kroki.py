#!/usr/bin/env python3
import os
import base64
import zlib
import requests
import time

UML_DIR = "/home/siva/.openclaw/workspace/uml"
KROKI_URL = "https://kroki.io"

def encode_plantuml(text):
    """Encode PlantUML text using deflate + base64 (Kroki format)"""
    compressed = zlib.compress(text.encode('utf-8'), 9)
    # Kroki uses standard base64 without the zlib header/footer manipulation
    return base64.urlsafe_b64encode(compressed).decode('ascii').rstrip('=')

def generate_png(puml_file):
    """Generate PNG from PlantUML file using Kroki"""
    png_file = puml_file.replace('.puml', '.png')
    puml_path = os.path.join(UML_DIR, puml_file)
    png_path = os.path.join(UML_DIR, png_file)
    
    print(f"Processing {puml_file}...")
    
    with open(puml_path, 'r') as f:
        content = f.read()
    
    encoded = encode_plantuml(content)
    url = f"{KROKI_URL}/plantuml/png/{encoded}"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 1000:
            with open(png_path, 'wb') as f:
                f.write(response.content)
            size = len(response.content)
            print(f"  ✅ {png_file} ({size//1024}KB)")
            return True
        else:
            print(f"  ❌ {png_file} failed (status: {response.status_code}, size: {len(response.content)})")
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
        time.sleep(1)
    
    print(f"\n✅ Generated {success}/{len(puml_files)} PNG images")
    print(f"📁 Location: {UML_DIR}")

if __name__ == "__main__":
    main()
