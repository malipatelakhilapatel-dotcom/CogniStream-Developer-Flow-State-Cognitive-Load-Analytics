"""
CogniStream Platform Launcher
Starts both the FastAPI Analytical Backend (port 8000) and the React Dashboard (port 5173).
Compatible with Python 3.11 - 3.15+.
"""

import os
import sys
import time
import signal
import subprocess
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COGNISTREAM_DIR = os.path.join(BASE_DIR, "CogniStream") if os.path.exists(os.path.join(BASE_DIR, "CogniStream")) else BASE_DIR

def main():
    print("=" * 65)
    print(" COGNISTREAM - DEVELOPER FLOW-STATE & COGNITIVE LOAD ANALYTICS")
    print(f" Python Version: {sys.version.split()[0]}")
    print("=" * 65)

    backend_dir = COGNISTREAM_DIR
    frontend_dir = os.path.join(COGNISTREAM_DIR, "frontend")

    # Set environment
    env = os.environ.copy()
    env["PYTHONPATH"] = COGNISTREAM_DIR

    print("\n[1/2] Launching Backend API (FastAPI) on http://127.0.0.1:8000 ...")
    backend_cmd = [
        sys.executable,
        "-m", "uvicorn",
        "backend.app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=backend_dir,
        env=env
    )

    time.sleep(2)

    print("[2/2] Launching Frontend Dashboard (Vite + React) on http://localhost:5173 ...")
    # Check if npm is available
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    # Fallback to tools/node if npm not in PATH
    local_npm = os.path.join(COGNISTREAM_DIR, "tools", "node", "npm.cmd")
    if not subprocess.run(f"where {npm_cmd}", shell=True, capture_output=True).returncode == 0:
        if os.path.exists(local_npm):
            npm_cmd = local_npm

    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"],
        cwd=frontend_dir,
        env=env
    )

    print("\n" + "=" * 65)
    print(" ALL SERVICES ACTIVE AND RUNNING ON LOCALHOST:")
    print("  * Dashboard UI:      http://localhost:5173")
    print("  * Interactive API:    http://127.0.0.1:8000/docs")
    print("  * API Health Status:  http://127.0.0.1:8000/api/health")
    print("  * Overview Analytics: http://127.0.0.1:8000/api/overview")
    print("=" * 65)
    print("Press Ctrl+C to stop all services.\n")

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend process terminated unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("Frontend process terminated unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping CogniStream platform services...")
    finally:
        backend_proc.terminate()
        frontend_proc.terminate()
        try:
            backend_proc.wait(timeout=3)
            frontend_proc.wait(timeout=3)
        except Exception:
            backend_proc.kill()
            frontend_proc.kill()
        print("All services stopped.")

if __name__ == "__main__":
    main()

