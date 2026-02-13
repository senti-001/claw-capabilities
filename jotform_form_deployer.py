import requests
import os

# Tactical Configuration
# API Key from Neural-Chromium Memory
API_KEY = os.getenv('JOTFORM_API_KEY', 'e8710b5c30d36ede9673e2dc74f6b441')
BASE_URL = "https://api.jotform.com/form"

# Form Schema Definition [NC-COMMS-011]
form_data = {
    "questions[0][type]": "control_head",
    "questions[0][text]": "Neural-Chromium Senti-001 Bridge",
    
    "questions[1][type]": "control_fullname",
    "questions[1][text]": "User Identity",
    "questions[1][order]": "1",
    
    "questions[2][type]": "control_email",
    "questions[2][text]": "Intelligence Routing Email",
    "questions[2][order]": "2",
    
    "questions[3][type]": "control_textarea",
    "questions[3][text]": "Session Transcript / Query",
    "questions[3][order]": "3",

    "properties[title]": "Senti-001 Intelligence Bridge",
    "properties[emails][0][type]": "notification",
    "properties[emails][0][name]": "Internal Alert",
    "properties[emails][0][from]": "default",
    "properties[emails][0][to]": "senti-001@neuralchromium.com" # Target AWS WorkMail
}

def deploy_form():
    print(f">>> [NC-COMMS-011] Deploying form to Jotform...")
    response = requests.post(f"{BASE_URL}?apiKey={API_KEY}", data=form_data)
    if response.status_code == 200:
        content = response.json().get('content', {})
        form_id = content.get('id')
        print(f"Success! Form Deployed. ID: {form_id}")
        print(f"URL: https://www.jotform.com/build/{form_id}")
        return form_id
    else:
        print(f"Deployment Failed: {response.text}")
        return None

if __name__ == "__main__":
    deploy_form()
