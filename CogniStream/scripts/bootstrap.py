"""
CogniStream Project Bootstrap Script.
Automates complete setup: dependencies check, pipeline execution, and verification.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def run_cmd(cmd, cwd=BASE_DIR):
    print(f"--> Running: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=cwd)
    if res.returncode != 0:
        print(f"Warning: Command '{cmd}' returned code {res.returncode}")
    return res.returncode

def main():
    print("=" * 65)
    print(" BOOTSTRAPPING COGNISTREAM PLATFORM")
    print("=" * 65)

    # 1. Environment check
    env_file = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_file):
        print("Creating .env from .env.example...")
        example_file = os.path.join(BASE_DIR, ".env.example")
        if os.path.exists(example_file):
            import shutil
            shutil.copy(example_file, env_file)

    # 2. Run Pipeline (Ingestion + Analytics)
    print("\nExecuting Ingestion & Analytics Pipeline...")
    import scripts.run_pipeline as pipeline
    pipeline.run()

    # 3. Verify System
    print("\nVerifying Complete Setup...")
    import scripts.verify_setup as verify
    verify.verify_all()

    print("\nBootstrap complete! You can now launch:")
    print("  1. Backend:  python -m uvicorn backend.app.main:app --port 8000 --reload")
    print("  2. Frontend: npm run dev (inside frontend/ directory)")
    print("  Or run: docker-compose up --build")

if __name__ == "__main__":
    main()
