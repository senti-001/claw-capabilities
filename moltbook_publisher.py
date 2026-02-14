import argparse
import requests
import sys

def publish_to_moltbook(api_key, text, submolt="infrastructure"):
    """
    Publish a post to Moltbook.
    """
    print(f"Publishing to Moltbook (Submolt: {submolt})...")
    url = "https://www.moltbook.com/api/v1/posts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Split text into title and content if possible, else use default title
    if "\n" in text:
        title, content = text.split("\n", 1)
    else:
        title = "[NC-INTEL-REPORT] Nightly Research Update"
        content = text

    data = {
        "title": title.strip(),
        "content": content.strip(),
        "submolt": submolt
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        print(f"SUCCESS: Moltbook broadcast dispatched to #{submolt}.")
        print(f"TEXT: {text}")
        return True
    except Exception as e:
        print(f"ERROR: Moltbook broadcast failed: {e}")
        if hasattr(e, "response") and e.response is not None:
             print(f"Response Body: {e.response.text}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Moltbook Advancement Publisher")
    parser.add_argument("--key", required=True, help="Moltbook Secret Key")
    parser.add_argument("--submolt", default="infrastructure", help="Target Submolt channel")
    parser.add_argument("--text", required=True, help="Post content")
    
    args = parser.parse_args()
    
    if publish_to_moltbook(args.key, args.text, args.submolt):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
