#!/bin/bash
# CEDR/IV-FRM Quick Start Script

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Cybersecurity Event Data Recorder (CEDR)                      ║"
echo "║  In-Vehicle Forensic Readiness Module (IV-FRM)                ║"
echo "║  Quick Start Script                                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "[*] Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python 3 found"

# Install dependencies (using --break-system-packages for demo environment)
echo ""
echo "[*] Installing Python dependencies..."

# Check if already installed
if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask already installed"
else
    echo "[*] Installing Flask and dependencies..."
    pip3 install --break-system-packages -q flask flask-cors flask-socketio python-socketio eventlet cryptography requests pyjwt 2>/dev/null || \
    pip3 install --break-system-packages flask flask-cors flask-socketio python-socketio eventlet cryptography requests pyjwt
fi

echo "✅ Dependencies ready"

# Start Cloud Backend
echo ""
echo "[*] Starting Cloud Backend on http://localhost:8080..."
cd /home/siva/openclaw/cedr-ivfrm/cloud-backend

# Create templates directory for Flask
mkdir -p templates
if [ ! -L "templates/investigator_dashboard.html" ]; then
    ln -sf /home/siva/openclaw/cedr-ivfrm/frontend/investigator_dashboard.html templates/investigator_dashboard.html
fi

python3 cloud_server.py &
CLOUD_PID=$!

# Wait for server to start
echo "[*] Waiting for cloud backend to start..."
sleep 5

# Check if server is running
if ! kill -0 $CLOUD_PID 2>/dev/null; then
    echo "❌ Cloud backend failed to start. Check logs above."
    exit 1
fi

echo "✅ Cloud backend running on http://localhost:8080"

# Start In-Vehicle Demo
echo ""
# Check if user wants attack simulation
if [ "$1" == "--attack" ]; then
    echo ""
    echo "[*] Starting Attack Simulation Demo..."
    echo "   (This will simulate various cybersecurity attacks)"
    cd /home/siva/openclaw/cedr-ivfrm
    python3 demo_attack_simulation.py &
    VEHICLE_PID=$!
else
    echo ""
    echo "[*] Starting In-Vehicle Module Demo..."
    echo "   (This will simulate events and upload to cloud)"
    cd /home/siva/openclaw/cedr-ivfrm/in-vehicle-module
    python3 cedr_module.py &
    VEHICLE_PID=$!
fi

sleep 2

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✅ CEDR System Running!                                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Access Points:"
echo "  • Cloud API:    http://localhost:8080"
echo "  • Dashboard:    http://localhost:8080"
echo "  • API Test:     http://localhost:8080/api/dashboard/stats"
echo ""
echo "Demo Credentials:"
echo "  • Investigator: INV001"
echo "  • Badge:        BADGE-001"
echo ""
echo "What you're seeing:"
echo "  1. In-vehicle module capturing security events"
echo "  2. Tamper-evident logging with blockchain-style hashes"
echo "  3. Events uploading to cloud backend"
echo "  4. Real-time alerts for critical events"
echo "  5. Investigator can search, analyze, and generate reports"
echo ""
echo "Press Ctrl+C to stop all components"
echo ""

# Handle Ctrl+C to clean up
cleanup() {
    echo ""
    echo "[*] Shutting down CEDR system..."
    kill $CLOUD_PID $VEHICLE_PID 2>/dev/null
    echo "✅ Shutdown complete"
    exit 0
}
trap cleanup INT

# Keep script running
wait