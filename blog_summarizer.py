import os
import json
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Tactical Configuration [NC-COMMS-015]
BLOG_ID = "3560842955308737645"
TOKEN_PATH = os.path.expanduser("~/comms/blogger_token.json")
MEMORY_PATH = os.path.expanduser("~/comms/MEMORY.md")

def summarize_recent_posts():
    if not os.path.exists(TOKEN_PATH):
        print(f"CRITICAL: Token not found at {TOKEN_PATH}")
        return

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/blogger'])
        service = build('blogger', 'v3', credentials=creds)
        
        print(f"--- [NC-COMMS-015] Fetching Recent Intelligence from BMM ---")
        request = service.posts().list(blogId=BLOG_ID, maxResults=3)
        response = request.execute()
        
        posts = response.get('items', [])
        print(f"Retrieved {len(posts)} posts.")
        
        memory_content = f"# Senti-001 Intelligence Memory\n*Updated: {datetime.datetime.now().isoformat()}*\n\n"
        
        for post in posts:
            title = post.get('title')
            url = post.get('url')
            # Stripping HTML for a clean markdown summary
            content = post.get('content', '')
            # Very basic cleanup (could be improved with BeautifulSoup)
            import re
            clean_content = re.sub('<[^<]+?>', '', content)
            
            memory_content += f"## [{title}]({url})\n"
            memory_content += f"{clean_content[:500]}...\n\n" # Truncate for memory brevity
            
        with open(MEMORY_PATH, 'w') as f:
            f.write(memory_content)
        print(f"MEMORY.md successfully updated at {MEMORY_PATH}")

    except Exception as e:
        print(f"Summarization FAILED: {e}")

if __name__ == "__main__":
    summarize_recent_posts()
