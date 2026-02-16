import requests
import json
import os
from pathlib import Path

# Mission Configuration
# SECRET REDACTED FOR REPO SYNC
API_KEY = os.getenv('XI_API_KEY', 'REDACTED_SECRET')
AGENT_ID = "agent_6101khj3773zesqrh2pwcsenxy59"
PROMPT_PATH = r"C:\Users\senti\.gemini\antigravity\brain\fcfeb178-e57c-4d8e-b60e-09ec2a8ac3b7\SENTI_SYSTEM_PROMPT.md"

def load_prompt():
    if not os.path.exists(PROMPT_PATH):
        print("✗ Prompt file not found.")
        return "", ""

    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract First Message and System Prompt
    first_message = ""
    system_prompt = ""
    
    lines = content.split('\n')
    capture_prompt = False
    for line in lines:
        if '"' in line and "First Message:" in content and not first_message:
            if 'First Message:' in line or (lines.index(line) > 0 and 'First Message:' in lines[lines.index(line)-1]):
                first_message = line.strip().strip('"')
        
        if "# System Prompt" in line:
            capture_prompt = True
            continue
        
        if capture_prompt:
            system_prompt += line + "\n"
            
    return first_message.strip(), system_prompt.strip()

def sync_elevenlabs():
    if API_KEY == 'REDACTED_SECRET':
        print("[WARN] API Key not set. Sync paused.")
        return

    first_msg, sys_prompt = load_prompt()
    
    if not sys_prompt:
        print("✗ Failed to load system prompt from artifact.")
        return

    url = f"https://api.elevenlabs.io/v1/convai/agents/{AGENT_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "conversation_config": {
            "agent": {
                "prompt": {
                    "prompt": sys_prompt
                },
                "first_message": first_msg
            }
        }
    }
    
    print(f">>> Synchronizing Senti to ElevenLabs ({AGENT_ID})...")
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("✓ Synchronization Successful. Senti is now mission-current.")
    else:
        print(f"✗ Sync Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    sync_elevenlabs()
