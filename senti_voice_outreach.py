from twilio.rest import Client
import sys
import os

# Twilio Credentials (Vercel ENV equivalents)
# SECRETS REDACTED FOR REPO COMMIT - User must inject env vars or run locally with .env
# Twilio Credentials (Vercel ENV equivalents)
# SECRETS REDACTED FOR REPO COMMIT - User must inject env vars or run locally with .env
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Target Configuration
# PETER_D_NUMBER = '+1xxxxxxxxxx' # Replace with Peter's actual number
PETER_D_NUMBER = '+19493069466' # User's verified test channel
SENTI_NUMBER = '+18664773684' 

# SOTA Infrastructure Config
SENTI_HANDSHAKE_URL = 'https://api.us.elevenlabs.io/twilio/voice/inbound_call?agent_id=agent_6101khj3773zesqrh2pwcsenxy59'
SENTI_NUMBER = '+18664773684'
PETER_D_NUMBER = '+19493069466'

print(f'>>> INITIALIZING SENTI VOICE OUTREACH <<<')
print(f'Target: {PETER_D_NUMBER}')
print(f'Persona: Senti (Industrial Intelligence)')

try:
    print(f'... Dispatching Call via {SENTI_NUMBER} ...')
    call = client.calls.create(
        to=PETER_D_NUMBER,
        from_=SENTI_NUMBER,
        url=SENTI_HANDSHAKE_URL,
        machine_detection='Enable' # Prevents Senti from talking to voicemails
    )
    print(f'✓ CALL DISPATCHED. SID: {call.sid}')
    print('Monitor the Big Iron logs for stream connection.')
except Exception as e:
    print(f'✗ DISPATCH FAILURE: {e}')
