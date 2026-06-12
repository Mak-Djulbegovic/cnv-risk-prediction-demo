#!/bin/bash
# CNV Prediction App Launcher
# ===========================
# Serves the Streamlit demo on the LAN so audience phones on the same wifi
# can open it. SYNTHETIC DATA - educational demonstration only.

set -e
cd "$(dirname "$0")"

PORT="${PORT:-8501}"

# Best-effort LAN IP for the share link
LAN_IP=$(python -c "import cnv_core; print(cnv_core.lan_ip())" 2>/dev/null || echo "127.0.0.1")

echo "Launching CNV Risk Prediction app..."
echo "SYNTHETIC DATA - educational demonstration only. NOT for clinical use."
echo ""
echo "  Local:   http://localhost:${PORT}"
echo "  Network: http://${LAN_IP}:${PORT}   (share this with phones on the same wifi)"
echo ""
echo "Press Ctrl+C to stop."
echo ""

# Bind to all interfaces so other devices can reach it; disable Streamlit's
# CORS/XSRF gate which otherwise blocks LAN clients.
exec streamlit run cnv_prediction_app.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT}" \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --browser.gatherUsageStats false
