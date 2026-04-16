#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/siva/openclaw/cedr-ivfrm/cloud-backend")
from cloud_server import app
app.run(host="0.0.0.0", port=8080, threaded=False, debug=False)
