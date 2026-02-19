from twilio.rest import Client
import sys
import os

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Configuration
PETER_D_NUMBER = '+19493069466' # User's verified test channel
SENTI_NUMBER = '+18664773684'

# The "Handshake" Payload
HANDSHAKE_MSG = (
    "Senti: Intelligence cycle complete. Build status: 28.7%. Integrity: 1.0. "
    "I am ready to brief you on the Sovereign Browser initiative. "
    "Reply 'DOSSIER' for the link, or call this line to speak with the core."
)

print(f'>>> INITIALIZING SENTI SMS OUTREACH <<<')
try:
    message = client.messages.create(
        body=HANDSHAKE_MSG,
        from_=SENTI_NUMBER,
        to=PETER_D_NUMBER
    )
    print(f'✓ SMS DISPATCHED. SID: {message.sid}')
    print(f'Content: "{HANDSHAKE_MSG}"')
except Exception as e:
    print(f'✗ SMS FAILURE: {e}')
