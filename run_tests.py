import subprocess
import time
import sys
import os
import signal

def start_discovery_server():
    print("[+] Starting Discovery Server...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "discovery.main:app", "--host", "0.0.0.0", "--port", "8500"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def wait_for_discovery(timeout=10):
    import httpx

    print("[*] Waiting for Discovery Server to be ready...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = httpx.get("http://localhost:8500/health")
            if r.status_code == 200:
                print("[✓] Discovery Server is up!")
                return True
        except Exception:
            pass
        time.sleep(0.5)
    print("[!] Discovery Server not reachable after waiting.")
    return False

def run_pytest():
    print("[*] Running tests...\n")
    code = subprocess.call(["pytest"])
    return code

def main():
    discovery_proc = start_discovery_server()
    try:
        if not wait_for_discovery():
            print("[X] Discovery Server failed to start.")
            discovery_proc.terminate()
            sys.exit(1)
        
        exit_code = run_pytest()

    finally:
        print("\n[*] Shutting down Discovery Server...")
        if os.name == 'nt':  # Windows
            subprocess.call(["pytest", "--html=report.html"])

        else:
            discovery_proc.terminate()
        print("[✓] Discovery Server stopped.")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
