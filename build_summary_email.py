import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import datetime

# --- CONFIGURATION ---
WORKSPACE_ROOT = r"C:\Users\senti\OneDrive\Desktop\Claw" # Adjusted for local/remote context
# Metadata from Primary Intelligence (AWS SES SMTP)
SMTP_SERVER = "email-smtp.us-east-1.amazonaws.com"
SMTP_PORT = 587
SENDER_EMAIL = "senti-001@neuralchromium.com"

# SMTP Credentials (IAM User) with Hardcoded Fallbacks
SMTP_USERNAME = os.getenv('SES_SMTP_USER', "")
SMTP_PASSWORD = os.getenv('SES_SMTP_PASS', "BHMweC7r6AlK1Zmyri9l4sV+9X2xHKYqWofIS016MHv/")

def send_build_summary(summary_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    subject = f"🚀 [BUILD ALERT] Neural-Chromium Summary: {timestamp}"
    
    # Construct HTML Body
    html = f"""
    <html>
    <body style="font-family: monospace; background-color: #f4f4f4; padding: 20px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
            <h2 style="color: #2c3e50;">📡 Neural-Chromium Intelligence Pulse</h2>
            <p><b>Status:</b> {summary_data.get('status', 'OK')}</p>
            <p><b>Primary Node:</b> {summary_data.get('node', 'EC2 Big Iron')}</p>
            <hr>
            <h3 style="color: #2980b9;">🛠️ Build Metadata</h3>
            <pre style="background: #eee; padding: 10px;">{summary_data.get('details', 'No details provided.')}</pre>
            <hr>
            <p style="font-size: 0.8em; color: #7f8c8d;">Orch-ID: NC-ORCH-001 | Sync-Mode: Double-Helix</p>
        </div>
    </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = SENDER_EMAIL # Sending to self/team mailbox

    part = MIMEText(html, "html")
    message.attach(part)

    print(f"--- Initiating SES SMTP Handshake with {SMTP_SERVER} ---")
    try:
        # Using STARTTLS on Port 587
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1) # Enable debug for verification
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, SENDER_EMAIL, message.as_string())
        server.quit()
        print("Build Summary Email: SUCCESS")
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

if __name__ == "__main__":
    # Test Payload
    test_data = {
        "status": "GREEN",
        "node": "EC2 Ubuntu 24.04 (aws-intel-node-01)",
        "details": "Chromium Build V1.0: 450/450 targets synced. Zero-Copy Vision hooks active."
    }
    send_build_summary(test_data)
