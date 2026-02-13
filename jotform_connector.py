import os
import subprocess
import json
import datetime
import requests

# --- CONFIGURATION ---
WORKSPACE_ROOT = r"C:\Users\senti\.openclaw\workspace"
# Placeholder for API Key - To be provided by Primary Intelligence [NC-ORCH-001]
JOTFORM_API_KEY = "YOUR_JOTFORM_API_KEY"
FORM_ID = "YOUR_FORM_ID"
BASE_URL = "https://api.jotform.com"

# BMM / Blogger integration
BLOG_ID = "3560842955308737645"
TOKEN_PATH = os.path.join(WORKSPACE_ROOT, "blogger_token.json")

def fetch_voice_submissions():
    print(f"--- Querying Jotform Submissions [Form: {FORM_ID}] ---")
    headers = {
        "APIKEY": JOTFORM_API_KEY
    }
    
    try:
        # Fetching latest submissions
        url = f"{BASE_URL}/form/{FORM_ID}/submissions?orderby=created_at"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Jotform Error: {resp.status_code} - {resp.text}")
            return []
            
        submissions = resp.json().get("content", [])
        print(f"Retrieved {len(submissions)} submissions.")
        return submissions
    except Exception as e:
        print(f"Connection Error: {e}")
        return []

def archive_to_bmm(submission):
    # Extracting potential audio fields
    # Note: Field IDs depend on the specific form structure
    answers = submission.get("answers", {})
    name = "Anonymous"
    email = "N/A"
    audio_url = None
    
    for key, val in answers.items():
        text = val.get("text", "").lower()
        answer = val.get("answer", "")
        if "name" in text:
            name = answer
        elif "email" in text:
            email = answer
        elif "upload" in val.get("type", "") or "audio" in text:
            # Assuming file upload for recording
            if isinstance(answer, list) and len(answer) > 0:
                audio_url = answer[0]
            else:
                audio_url = answer

    if not audio_url:
        print(f"Skipping submission {submission.get('id')} - No audio found.")
        return

    timestamp = submission.get("created_at")
    title = f"Investor Voice Memo: {name} [{timestamp}]"
    content = f"""
<div style="font-family: sans-serif; border: 1px solid #ccc; padding: 15px; border-radius: 5px;">
<h3 style="color: #2c3e50;">🎙️ Incoming Intelligence: Voice Portal</h3>
<p><b>Investor:</b> {name}</p>
<p><b>Contact:</b> {email}</p>
<hr>
<p><b>Audio Archive:</b> <a href="{audio_url}">Download / Listen to Recording</a></p>
<p style="font-size: 0.8em; color: #7f8c8d;">Sync ID: {submission.get('id')}</p>
</div>
"""

    print(f"Archiving Message from {name} to BMM...")
    try:
        subprocess.run([
            "python", os.path.join(WORKSPACE_ROOT, "scripts", "blogger_publisher.py"),
            "--blog_id", BLOG_ID,
            "--title", title,
            "--content", content,
            "--token", TOKEN_PATH
        ], check=True)
        print("Archival SUCCESS.")
    except Exception as e:
        print(f"Archival failed: {e}")

def run_connector():
    if JOTFORM_API_KEY == "YOUR_JOTFORM_API_KEY":
        print("CRITICAL: Jotform API Key not set. Standing by for Scaffold Revision.")
        return

    submissions = fetch_voice_submissions()
    for sub in submissions:
        # Check if already processed (Logic for persistence could go here)
        archive_to_bmm(sub)

if __name__ == "__main__":
    run_connector()
