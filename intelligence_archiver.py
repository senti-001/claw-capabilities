import json
import os
import datetime

# Configuration
WORKSPACE_ROOT = r"C:\Users\senti\OneDrive\Desktop\Claw"
INTEL_FILE = os.path.join(WORKSPACE_ROOT, "mission_intelligence_summary.json")
ARCHIVE_FILE = os.path.join(WORKSPACE_ROOT, "mission_archives.jsonl")

def archive_intelligence():
    print(f"--- STARTING INTELLIGENCE ARCHIVAL [{datetime.datetime.now()}] ---")
    
    if not os.path.exists(INTEL_FILE):
        print("✗ Intelligence file not found.")
        return

    try:
        with open(INTEL_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. Append to JSONL Archive (Permanent Storage)
        with open(ARCHIVE_FILE, 'a', encoding='utf-8') as af:
            af.write(json.dumps(data) + "\n")
        
        # 2. Prune "Hot" Intelligence (Keep last 48 hours / latest 5 entries)
        # For simplicity in this sprint, we'll keep the structure but clear old entries
        # Logic: Move voice_transcripts/sms_inbound to archive if older than 48h
        # (This will be refined in Phase 3 weighted pruning)
        
        print(f"✓ Intelligence snapshot archived to {ARCHIVE_FILE}")
        
    except Exception as e:
        print(f"✗ Archival Error: {e}")

if __name__ == "__main__":
    archive_intelligence()
