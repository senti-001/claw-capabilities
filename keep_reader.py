import gkeepapi
import os
import sys
import subprocess
import json

# Tactical Configuration [NC-COMMS-014]
USERNAME = os.getenv('GK_EMAIL')
PASSWORD = os.getenv('GK_APP_PASS')
BLOG_ID = "3560842955308737645"
ARCHIVER_SCRIPT = os.path.expanduser("~/comms/blogger_publisher.py")
TOKEN_PATH = os.path.expanduser("~/comms/blogger_token.json")

def process_notes():
    if not USERNAME or not PASSWORD:
        print("CRITICAL: GK_EMAIL or GK_APP_PASS environment variables not set.")
        sys.exit(1)

    keep = gkeepapi.Keep()
    print(f"--- [NC-COMMS-014] Authenticating Google Keep: {USERNAME} ---")
    
    try:
        # Use authenticate as login is deprecated
        keep.authenticate(USERNAME, PASSWORD)
        
        # Target notes with #NC- tag
        notes = keep.find(query='#NC-')
        note_list = list(notes)
        print(f"Found {len(note_list)} notes with #NC- tag.")
        
        for note in note_list:
            # Archival logic [NC-COMMS-015]
            title = f"Intelligence Note: {note.title or 'Untitled'} [{note.timestamps.created}]"
            content = f"""
<div style="font-family: serif; border: 2px solid #34a853; padding: 15px; background: #fdfdfd; color: #1a1a1a;">
<h3 style="color: #34a853; border-bottom: 2px solid #34a853;">📝 PROJECT INTELLIGENCE: KEEP [NC-COMMS-014]</h3>
<p><b>CONTEXT:</b> Gemini Strategy Note</p>
<p><b>TAGS:</b> {', '.join([l.name for l in note.labels])}</p>
<hr style="border: 0; border-top: 1px dashed #34a853;">
<div style="white-space: pre-wrap; word-wrap: break-word;">{note.text}</div>
<p style="font-size: 0.8em; color: #7f8c8d; margin-top: 10px;">NODE: Senti-001 | SYNC_ID: {note.id}</p>
</div>
"""
            print(f">>> Archiving Note: {note.id} to BMM...")
            try:
                subprocess.run([
                    "python3", ARCHIVER_SCRIPT,
                    "--blog_id", BLOG_ID,
                    "--title", title,
                    "--content", content,
                    "--token", TOKEN_PATH
                ], check=True)
                print("Archival SUCCESS.")
            except Exception as e:
                print(f"Archival failed for {note.id}: {e}")

    except Exception as e:
        print(f"Keep Operation FAILED: {e}")

if __name__ == "__main__":
    process_notes()
