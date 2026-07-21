#!/usr/bin/env bash
# Starts agent, server, and client together using the shared .venv.
# Run from the repo root: ./run_all.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$ROOT_DIR/.venv/Scripts/python.exe"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

if [ ! -x "$PYTHON" ]; then
    echo "Python venv not found at $PYTHON — create it first (python -m venv .venv)." >&2
    exit 1
fi

PIDS=()

cleanup() {
    echo ""
    echo "Stopping services..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
}
trap cleanup EXIT INT TERM

start_service() {
    local name="$1" dir="$2"
    echo "Starting $name (logs/$name.log)..."
    (cd "$ROOT_DIR/$dir" && "$PYTHON" wsgi.py) > "$LOG_DIR/$name.log" 2>&1 &
    PIDS+=($!)
}

start_service "agent" "agent"
sleep 2
start_service "server" "server"
sleep 1
start_service "client" "client"

echo ""
echo "All services started:"
echo "  agent  -> http://localhost:5001 (logs/agent.log)"
echo "  server -> http://localhost:5000 (logs/server.log)"
echo "  client -> http://localhost:8000 (logs/client.log)"
echo ""
echo "Press Ctrl+C to stop all services."

wait
