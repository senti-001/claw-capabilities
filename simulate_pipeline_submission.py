import requests

API_KEY = 'e8710b5c30d36ede9673e2dc74f6b441'
FORM_ID = '260428252815153'
BASE_URL = f"https://api.jotform.com/form/{FORM_ID}/submissions"

# Simulation Data [NC-COMMS-012]
submission_data = {
    "submission[2][first]": "Pipeline",
    "submission[2][last]": "Tester",
    "submission[3]": "williamtflynn@gmail.com",
    "submission[4]": "SIMULATED TRANSCRIPT: This is a test of the Zero-Copy Intelligence Bridge. Confirming data-bucket ingestion for NC-COMMS-012."
}

def simulate_submission():
    print(f">>> [NC-COMMS-012] Simulating Voice Agent submission...")
    response = requests.post(f"{BASE_URL}?apiKey={API_KEY}", data=submission_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        content = response.json().get('content', {})
        submission_id = content[0]['submission_id'] if isinstance(content, list) and content else content.get('submission_id')
        print(f"Success! Submission Pushed. ID: {submission_id}")
    else:
        print(f"Simulation Failed: {response.text}")

if __name__ == "__main__":
    simulate_submission()
