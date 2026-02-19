import os
import subprocess
import argparse
import sys

# Mission Configuration
ROOT_DIR = r"C:\Users\senti\OneDrive\Desktop\Claw\claw-capabilities"
TASK_LIST = {
    "Senti-Investor-Audit": {
        "script": "nightly_investor_audit.py",
        "trigger": "Daily at 10:30 AM",
        "desc": "Senti-001 High-Integrity Investor Dashboard Audit"
    },
    "Senti-001-Intelligence-Cycle": {
        "script": "intelligence_cycle.py",
        "args": "--mode full",
        "trigger": "Every 6 Hours",
        "desc": "Senti-001 Strategic Advancement Broadcast"
    }
}

def list_tasks():
    print("\n--- Senti-001 Mission Task Manifest ---")
    print(f"{'Task Name':<30} | {'Status':<10} | {'Last Run':<20}")
    print("-" * 65)
    
    for task in TASK_LIST:
        try:
            output = subprocess.check_output(f'schtasks /query /tn "{task}" /fo CSV', shell=True, text=True, stderr=subprocess.DEVNULL)
            status = "Active"
        except:
            status = "Missing"
        
        print(f"{task:<30} | {status:<10} | N/A")

def deploy_task(name):
    if name not in TASK_LIST:
        print(f"✗ Task {name} not found in mission manifest.")
        return

    task = TASK_LIST[name]
    script_path = os.path.join(ROOT_DIR, task['script'])
    args = task.get('args', '')
    
    cmd = f'powershell -ExecutionPolicy Bypass -Command "Register-ScheduledTask -TaskName \'{name}\' -Action (New-ScheduledTaskAction -Execute \'python.exe\' -Argument \'{script_path} {args}\' -WorkingDirectory \'{ROOT_DIR}\') -Trigger (New-ScheduledTaskTrigger -Daily -At 10:30AM) -Force"'
    
    print(f">>> Deploying {name}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {name} deployed successfully.")
    except Exception as e:
        print(f"✗ Deployment FAILED: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Senti-001 Mission Task Orchestrator")
    parser.add_argument("action", choices=["list", "deploy", "run"], default="list", nargs="?")
    parser.add_argument("--task", help="Specific task name")
    
    args = parser.parse_args()
    
    if args.action == "list":
        list_tasks()
    elif args.action == "deploy":
        if args.task:
            deploy_task(args.task)
        else:
            for t in TASK_LIST: deploy_task(t)
    elif args.action == "run":
        if args.task:
            print(f">>> Triggering {args.task}...")
            subprocess.run(f'schtasks /run /tn "{args.task}"', shell=True)
