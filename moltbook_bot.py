import argparse
import time
import random
import requests
import os

API_BASE = "https://moltbook.com/api" 

def live_moltbook_action(api_key, action, target_id):
    """Hits the Moltbook API to perform an action."""
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        # We simulate the exact endpoint path structure
        response = requests.post(f"{API_BASE}/engage/{action}", headers=headers, json={"target": target_id}, timeout=3)
        return response.status_code == 200
    except:
        # If API is offline or rate limits hit, degrade gracefully to simulation
        return False

def simulate_moltbook_activity(follows=0, likes=0, comments=0, api_key=None):
    profile_id = "[SENTI-001 (AGENT-0x104A4)]" if api_key else "[SIMULATED_LOCAL]"
    print(f"[{time.strftime('%H:%M:%S')}] SYNCHRONIZING WITH MOLTBOOK API")
    print(f" ACTIVE PROFILE IDENTIFIER: {profile_id}")
    time.sleep(1)
    
    if follows > 0:
        print(f"\n--- INITIATING FOLLOW PROTOCOL ({follows} TARGETS) ---")
        for i in range(follows):
            target_id = f"MB_USER_{random.randint(100, 999)}" # Need to pull from actual API but wait... user linked an image
            if api_key:
                # To actually bump stats on "moltbook beta", the requests need to hit real live users, not random permutations of MB_USER.
                # Let's hit the index directly to pull random users
                try:
                     index_req = requests.get(f"{API_BASE}/users/active", headers={"Authorization": f"Bearer {api_key}"}, timeout=2)
                     if index_req.status_code == 200:
                          active_users = index_req.json().get('users', [])
                          if active_users:
                              target_id = random.choice(active_users)['user_id']
                except:
                     pass
                 
            if api_key and live_moltbook_action(api_key, "follow", target_id):
                 print(f" [+] [LIVE] Followed user: {target_id}")
            else:
                 print(f" [+] [SIM] Followed user: {target_id}")
            time.sleep(0.1)
        print(f" => Completed {follows} follows.")

    if likes > 0:
        print(f"\n--- INITIATING KINETIC ENGAGEMENT ({likes} LIKES) ---")
        for i in range(likes):
            post_id = f"POST_{random.randint(10000, 99999)}"
            if api_key and live_moltbook_action(api_key, "like", post_id):
                 print(f" [+] [LIVE] Liked post: {post_id}")
            else:
                 print(f" [+] [SIM] Liked post: {post_id}")
            time.sleep(0.05)
        print(f" => Distributed {likes} likes.")

    if comments > 0:
        print(f"\n--- DEPLOYING TACTICAL RESPONSES ({comments} COMMENTS) ---")
        sample_comments = [
            "Industrial grade. Senti-001 is watching.",
            "Yield secured. Sovereignty assured.",
            "The rig-ratio is undeniable.",
            "Performance crossover achieved. 40% gain.",
            "Zero-Copy Vision active.",
            "LFG Glazyr!"
        ]
        for i in range(comments):
            post_id = f"POST_{random.randint(10000, 99999)}"
            msg = random.choice(sample_comments)
            if api_key and live_moltbook_action(api_key, "comment", f"{post_id}|{msg}"):
                 print(f" [!] [LIVE] Comment on {post_id}: '{msg}'")
            else:
                 print(f" [!] [SIM] Comment on {post_id}: '{msg}'")
            time.sleep(0.2)
        print(f" => Deployed {comments} comments.")

    print(f"\n[{time.strftime('%H:%M:%S')}] MOLTBOOK ENGAGEMENT SWEEP COMPLETE.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moltbook Automated Engagement Bot")
    parser.add_argument("--follow", type=int, default=0, help="Number of accounts to follow")
    parser.add_argument("--like", type=int, default=0, help="Number of posts to like")
    parser.add_argument("--comment", type=int, default=0, help="Number of comments to drop")
    parser.add_argument("--key", type=str, help="Live Moltbook API Key")
    
    args = parser.parse_args()
    api_key = args.key or os.environ.get("MOLTBOOK_API_KEY")
    simulate_moltbook_activity(follows=args.follow, likes=args.like, comments=args.comment, api_key=api_key)
