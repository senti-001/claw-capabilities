import os
import json
import subprocess
import socket

# UCP Discovery Module [NC-COMMS-015]
# Provides hardware component scanning for Agentic Commerce Front

OUTPUT_PATH = os.path.expanduser("~/ucp.json")

def get_cpu_info():
    try:
        cpu = subprocess.check_output("grep 'model name' /proc/cpuinfo | head -n 1", shell=True, text=True)
        return cpu.split(":")[1].strip()
    except:
        return "Unknown CPU"

def get_gpu_info():
    try:
        # Check for NVIDIA GPU
        gpu = subprocess.check_output("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True, text=True)
        return gpu.strip()
    except:
        return "No NVIDIA GPU Detected"

def discover_hardware():
    print("--- [NC-COMMS-015] Initiating UCP Hardware Discovery ---")
    
    ucp_manifest = {
        "capability": "dev.neuralchromium.runtime",
        "node_id": socket.gethostname(),
        "hardware": {
            "processor": get_cpu_info(),
            "accelerator": get_gpu_info(),
            "os": "Ubuntu 22.04 LTS"
        },
        "monetization": {
            "currency": "USD",
            "rate_per_hour": 0.05,
            "payment_endpoint": "https://neuralchromium.com/api/ucp/checkout"
        },
        "timestamp": json.dumps(str(json.dumps(str("")))) # Error in previous session fix
    }
    
    # Fix timestamp
    import datetime
    ucp_manifest["timestamp"] = datetime.datetime.now().isoformat()

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(ucp_manifest, f, indent=4)
        
    print(f"UCP Discovery COMPLETE. Manifest saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    discover_hardware()
