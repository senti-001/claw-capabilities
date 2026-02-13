import requests
import os
import json
import subprocess
import time

# Tactical Configuration [NC-COMMS-012]
API_KEY = 'e8710b5c30d36ede9673e2dc74f6b441'
FORM_ID = '260428252815153'
BASE_URL = "https://api.jotform.com"
INBOX_DIR = os.path.expanduser("~/inbox")

# BMM Integration [NC-COMMS-013]
BLOG_ID = "3560842955308737645"
PUBLISHER_SCRIPT = os.path.expanduser("~/comms/blogger_publisher.py")
TOKEN_PATH = os.path.expanduser("~/comms/blogger_token.json")

def setup_environment():
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
        print(f">>> Initialized Inbox: {INBOX_DIR}")

def archive_to_bmm(payload):
    """Dispatches submission to Blogger Memory Manager."""
    title = f"Intelligence Bridge: {payload['user']} [{payload['timestamp']}]"
    content = f"""
<div style="font-family: monospace; border: 1px solid #00ff00; padding: 15px; background: #000; color: #00ff00;">
<h3 style="color: #00ff00; border-bottom: 1px solid #00ff00;">📡 INCOMING INTELLIGENCE [NC-COMMS-011]</h3>
<p><b>SOURCE:</b> Senti-001 Intelligence Bridge (Jotform)</p>
<p><b>IDENTITY:</b> {payload['user']}</p>
<p><b>ROUTING:</b> {payload['email']}</p>
<hr style="border: 0; border-top: 1px dashed #00ff00;">
<p><b>TRANSCRIPT SUMMARY:</b></p>
<pre style="white-space: pre-wrap; word-wrap: break-word;">{payload['transcript']}</pre>
<p style="font-size: 0.8em; color: #008800;">SYNC_ID: {payload['id']}</p>
</div>
"""
    print(f"Archiving to BMM: {payload['id']}...")
    try:
        subprocess.run([
            "python3", PUBLISHER_SCRIPT,
            "--blog_id", BLOG_ID,
            "--title", title,
            "--content", content,
            "--token", TOKEN_PATH
        ], check=True)
        print("Archival SUCCESS.")
    except Exception as e:
        print(f"Archival FAILED: {e}")

def fetch_and_buffer():
    print(f"--- [NC-COMMS-012] Polling Jotform API for Submissions ---")
    headers = {"APIKEY": API_KEY}
    url = f"{BASE_URL}/form/{FORM_ID}/submissions?orderby=created_at"
    
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Error: {resp.status_code} - {resp.text}")
            return
            
        submissions = resp.json().get("content", [])
        print(f"Retrieved {len(submissions)} submissions.")
        
        for sub in submissions:
            sub_id = sub.get('id')
            buffer_path = os.path.join(INBOX_DIR, f"inquiry_{sub_id}.json")
            
            if os.path.exists(buffer_path):
                continue # Already processed
                
            # Extract structured data
            answers = sub.get('answers', {})
            name_data = answers.get('2', {}).get('answer', {})
            name = f"{name_data.get('first', '')} {name_data.get('last', '')}".strip() or "Anonymous"
            email = answers.get('3', {}).get('answer', 'N/A')
            transcript = answers.get('4', {}).get('answer', 'Empty Content')
            
            payload = {
                "id": sub_id,
                "timestamp": sub.get('created_at'),
                "user": name,
                "email": email,
                "transcript": transcript,
                "type": "Voice Portal [NC-COMMS-011]"
            }
            
            # 1. Local Persistence
            with open(buffer_path, 'w') as f:
                json.dump(payload, f, indent=4)
            print(f">>> Buffered Submission: {sub_id} from {name}")
            
            # 2. BMM Archival
            archive_to_bmm(payload)
            
    except Exception as e:
        print(f"Ingestion Failed: {e}")

if __name__ == "__main__":
    setup_environment()
    fetch_and_buffer()
