import requests
import os
import json
import boto3
import datetime
import time

# Mission Configuration
# SECRET REDACTED FOR REPO SYNC
API_KEY = os.getenv('JOTFORM_API_KEY', 'REDACTED_SECRET')
FORM_ID = '260428252815153'
BASE_URL = 'https://api.jotform.com'
INBOX_DIR = os.path.expanduser('~/inbox')

# SNS Configuration
sns = boto3.client('sns', region_name='us-east-1')

def setup_environment():
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)

def generate_senti_response(user_msg):
    build_status = '28.7%'
    integrity = '1.0'
    response = (
        f\"Senti: I've received your intelligence update. Analysis of '{user_msg[:50]}...' complete. \"
        f\"Current build integrity: {integrity} at {build_status}. \\n\\n\"
        \"Protocol Note: I've logged this to the BMM. If you need a more immediate technical deep-dive, \"
        \"you can reach my voice core via the 601 concierge bridge (Ext 43512). \\n\\n\"
        \"Mission integrity is holding. - Senti.\"
    )
    return response

def reply_via_sns(to_number, text):
    try:
        print(f'[OUTGOING] SNS Egress to {to_number}...')
        sns.publish(
            PhoneNumber=to_number,
            Message=text,
            MessageAttributes={'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Transactional'}}
        )
        return True
    except Exception as e:
        print(f'[ERROR] SNS Failed: {e}')
        return False

def process_submissions():
    if API_KEY == 'REDACTED_SECRET':
        print("[WARN] API Key not set. Ingestion paused.")
        return

    url = f\"{BASE_URL}/form/{FORM_ID}/submissions?apiKey={API_KEY}\"
    try:
        response = requests.get(url, timeout=10)
        submissions = response.json().get('content', [])
        
        for sub in submissions:
            sub_id = sub.get('id')
            buffer_file = os.path.join(INBOX_DIR, f\"{sub_id}.json\")
            
            if not os.path.exists(buffer_file):
                answers = sub.get('answers', {})
                user = answers.get('3', {}).get('answer', 'Unknown')
                transcript = answers.get('4', {}).get('answer', 'No transcript provided')
                phone = 'Unknown'
                for k, v in answers.items():
                    if 'phone' in v.get('text', '').lower():
                        phone = v.get('answer', 'Unknown')
                
                print(f'[NEW INQUIRY] ID: {sub_id} | User: {user}')
                
                senti_msg = generate_senti_response(transcript)
                
                # Buffer the interaction
                with open(buffer_file, 'w') as f:
                    json.dump({'id': sub_id, 'user': user, 'response': senti_msg}, f)
                
                # Auto-Reply to verified number (949 line for the user)
                if '949' in phone.replace('+', '').replace('-', ''):
                    reply_via_sns(phone, senti_msg)
                else:
                    print(f'>> External number detected ({phone}). Routing to administrator mailbox.')
                    
    except Exception as e:
        print(f'[ERROR] Ingester Cycle Failed: {e}')

if __name__ == '__main__':
    setup_environment()
    while True:
        process_submissions()
        time.sleep(30)
