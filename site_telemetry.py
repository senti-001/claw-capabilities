import os
import subprocess
import json
import datetime

# --- CONFIGURATION ---
WORKSPACE_ROOT = r"C:\Users\senti\.openclaw\workspace"
REPO_PATH = os.path.join(WORKSPACE_ROOT, "neural-chromium")
# Path for Vercel to consume (Assuming local repo structure)
TELEMETRY_PATH = os.path.join(REPO_PATH, "public", "telemetry.json")

EC2_IP = "3.86.6.53"
SSH_KEY = os.path.join(WORKSPACE_ROOT, "senti-001-ec2-key-clean.pem")

def gather_telemetry():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- Gathering Telemetry [{timestamp}] ---")
    
    telemetry = {
        "last_sync": timestamp,
        "ec2_status": "OFFLINE",
        "ec2_disk": "N/A",
        "project_phase": "Operation Deep Cortex",
        "build_target": "Chromium V1.0 (Zero-Copy)"
    }

    # 1. Check EC2 Disk
    try:
        ssh_cmd = [
            "ssh", "-i", SSH_KEY, 
            "-o", "StrictHostKeyChecking=no", 
            f"ubuntu@{EC2_IP}", 
            "df -h /home/ubuntu | grep /dev/root"
        ]
        status_raw = subprocess.check_output(ssh_cmd, text=True).strip()
        telemetry["ec2_status"] = "ONLINE"
        telemetry["ec2_disk"] = status_raw
        print(f"EC2 Status: {status_raw}")
    except Exception as e:
        print(f"EC2 Telemetry Error: {e}")

    # 2. Extract Latest Commits (Optional for Dashboard)
    try:
        git_cmd = ["git", "-C", REPO_PATH, "log", "-1", "--pretty=format:%h - %s"]
        telemetry["latest_commit"] = subprocess.check_output(git_cmd, text=True).strip()
    except:
        telemetry["latest_commit"] = "N/A"

    # 3. Persist to JSON
    # Ensure public directory exists
    os.makedirs(os.path.dirname(TELEMETRY_PATH), exist_ok=True)
    
    with open(TELEMETRY_PATH, "w") as f:
        json.dump(telemetry, f, indent=4)
    
    print(f"Telemetry persisted to {TELEMETRY_PATH}")

if __name__ == "__main__":
    gather_telemetry()
