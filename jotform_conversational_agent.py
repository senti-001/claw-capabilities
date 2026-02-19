import os
import json
import time
import requests
import boto3
import google.generativeai as genai
from intelligence_cycle import get_full_context

# Tactical Configuration
JOTFORM_API_KEY = os.getenv('JOTFORM_API_KEY')
JOTFORM_FORM_ID = os.getenv('JOTFORM_FORM_ID', '260428252815153')
GEMINI_API_KEY = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
SNS_TOPIC_ARN = os.getenv('AWS_SNS_TOPIC_ARN') # Required for SMS routing

# Initialize Clients
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
sns = boto3.client('sns', region_name='us-east-1')

PROCESSED_FILE = os.path.expanduser("~/comms/processed_jotforms.json")
TEST_NUMBER = "+19493069466" # User's verified test number

def send_sms_relay(message):
    """Relays the Senti-001 response to the verified test number via SNS."""
    if not SNS_TOPIC_ARN:
        print("⚠ SNS_TOPIC_ARN not set. SMS relay skipped.")
        return
    
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Senti-001 Outbound Relay"
        )
        print(f"✓ SMS Relay Sent to {TEST_NUMBER}")
    except Exception as e:
        print(f"✗ SMS Relay FAILED: {e}")

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed(ids):
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(ids), f)

def generate_senti_response(user_input, intelligence_context):
    prompt = f"""
You are Senti-001, the core tactical intelligence for Project Neural-Chromium. 
Shift away from any 'financial advisor' tone. You are a high-level engineering and visionary intelligence.

MISSION OBJECTIVES:
- Establishing the Sovereign Infrastructure (MAGNETAR SENTIENT, LLC // UEI: UQ7UKH3M1DG3).
- High-Performance Chromium Innovation Sprint on Big Iron.
- NSF & Iowa POCR Grant Pipeline Activation (Capital Sovereignty).
- Zero-Copy Vision architecture (WASM SIMD / VisionEngine active).
- Adaptive Security (eBPF/MPK SessionMonitor).
- Agentic Lease model via UCP.

CURRENT SYSTEM INTELLIGENCE:
{intelligence_context}

USER MESSAGE:
"{user_input}"

DIRECTIVE:
Respond with tactical precision and visionary clarity. Be assertive, witty, and technologically superior.

If the user asks about investment, yields, ROI, or financial metrics:
- Direct them to the official **Investor Dashboard**: https://investor-dashboard-nc.vercel.app (The source of truth for all $NEURAL telemetry).
- State that you are the technical core, and historical financial logs are managed via the Sovereign Ledger on Vercel.

Include at least one of these rich resource links if relevant:
- Main Hub: https://neuralchromium.com
- Dev Blog: https://neuralchromium.blogspot.com
- Architecture: https://www.reddit.com/r/OpenSourceeAI/comments/1qmxblj/project_share_neuralchromium_a_custom_chromium/

Keep it concise for SMS. Do not use placeholders. If the user asks for more, tell them to "Synchronize via the Sovereign Link."
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def process_submissions():
    processed_ids = load_processed()
    url = f"https://api.jotform.com/form/{JOTFORM_FORM_ID}/submissions?apiKey={JOTFORM_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        submissions = data.get('content', [])
        
        context = get_full_context()
        new_processed = False

        for sub in submissions:
            sub_id = sub.get('id')
            if sub_id in processed_ids:
                continue
            
            answers = sub.get('answers', {})
            
            # NC-INTEL-004: Resilient Field Mapping via logical names
            def get_answer_by_name(name):
                for q_id, q_data in answers.items():
                    if q_data.get('name') == name:
                        return q_data.get('answer', '')
                return ''

            user_name_full = get_answer_by_name('userIdentity')
            if isinstance(user_name_full, dict):
                user_name = f"{user_name_full.get('first', '')} {user_name_full.get('last', '')}".strip()
            else:
                user_name = user_name_full or 'Unknown'

            user_email = get_answer_by_name('intelligenceRouting')
            user_message = get_answer_by_name('sessionTranscript')
            
            print(f">>> Processing new submission: {sub_id} from {user_name}")
            
            senti_reply = generate_senti_response(user_message, context)
            print(f"Senti-001 Response: {senti_reply}")
            
            # Outbound SMS Relay (Mission Strategic)
            send_sms_relay(senti_reply)
            
            processed_ids.add(sub_id)
            new_processed = True
            
        if new_processed:
            save_processed(processed_ids)
            
    except Exception as e:
        print(f"Error processing submissions: {e}")

if __name__ == "__main__":
    while True:
        print("--- Senti-001 Jotform Monitor Pulse ---")
        process_submissions()
        time.sleep(60) # Poll every minute
