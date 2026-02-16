from flask import Flask, request, Response
import requests
import json
import datetime
import os
from twilio.rest import Client

app = Flask(__name__)

# Twilio Credentials (Vercel ENV equivalents)
# SECRETS REDACTED FOR REPO SYNC
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'REDACTED_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'REDACTED_TOKEN')
TWILIO_NUMBER = '+18664773684'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Intelligence Stream Data
BUILD_STATUS = "28.7%"
MISSION_ROOT = "https://v0-investor-dashboard-design-ten.vercel.app/"

@app.route('/sms', methods=['POST'])
def sms_reply():
    from_number = request.form.get('From', '')
    body = request.form.get('Body', '').strip().lower()
    
    print(f"[INCOMING] {from_number}: {body}")
    
    # Senti Persona Logic
    if 'status' in body or 'build' in body:
        response_text = f"Senti here. Build integrity is at 1.0. Current progress: {BUILD_STATUS} on the Zero-Copy core. We're holding the line."
    elif 'dossier' in body or 'mission' in body or 'link' in body:
        response_text = f"Direct link to the mission dossier: {MISSION_ROOT}. Watch it live."
    elif 'hello' in body or 'hi' in body:
        response_text = "This is Senti. Big Iron node is active. How can I help you navigate the Sovereign Browser initiative today?"
    else:
        response_text = "I'm focused on the mission. Reply 'Status' for the build update or 'Dossier' for the portal link."

    # Send Response via Twilio
    if TWILIO_AUTH_TOKEN == 'REDACTED_TOKEN':
        print(f"[MOCK SEND] To {from_number}: {response_text}")
    else:
        try:
            client.messages.create(
                body=response_text,
                from_=TWILIO_NUMBER,
                to=from_number
            )
            print(f"[OUTGOING] To {from_number}: {response_text}")
        except Exception as e:
            print(f"[ERROR] Twilio Send Failed: {e}")

    return Response('', mimetype='text/xml')

@app.route('/senti-handshake', methods=['POST', 'GET'])
def senti_handshake():
    agent_id = 'agent_6101khj3773zesqrh2pwcsenxy59'
    # SECRET REDACTED FOR REPO SYNC
    api_key = os.getenv('XI_API_KEY', 'REDACTED_SECRET')
    
    stream_url = f'wss://api.elevenlabs.io/v1/convai/conversation?agent_id={agent_id}&xi-api-key={api_key}'
    
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{stream_url}" />
    </Connect>
    <Pause length="30"/>
</Response>'''
    return Response(twiml, mimetype='text/xml')

@app.route('/status', methods=['GET'])
def status():
    return json.dumps({"status": BUILD_STATUS, "integrity": "1.0", "persona": "Senti"}), 200

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
