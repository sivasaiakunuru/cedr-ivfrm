#!/usr/bin/env python3
import sys
import os

# Use relative path instead of hardcoded absolute path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "cloud-backend"))

# Fallback: Try to find cloud-backend in parent directories
if not os.path.exists(os.path.join(os.path.dirname(__file__), "cloud-backend")):
    # Check common locations
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "cloud-backend"),
        "/home/siva/openclaw/cedr-ivfrm/cloud-backend",  # Original path as fallback
    ]
    for path in possible_paths:
        if os.path.exists(path):
            sys.path.insert(0, os.path.abspath(path))
            break

try:
    from cloud_server import app
    app.run(host="0.0.0.0", port=8080, threaded=False, debug=False)
except ImportError as e:
    print(f"Error: Could not import cloud_server. {e}")
    print("Make sure the cloud-backend directory exists and contains cloud_server.py")
    sys.exit(1)
