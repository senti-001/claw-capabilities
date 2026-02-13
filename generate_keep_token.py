import gpsoauth
import sys

def get_local_token():
    email = 'williamtflynn@gmail.com'
    password = 'smagsndsqlbdzbje'
    
    print(f"--- [NC-COMMS-014] Attempting LOCAL Token Generation: {email} ---")
    
    try:
        # Attempt to get a master token from the "familiar" local machine
        res = gpsoauth.perform_master_login(email, password, "android_id_identity_001")
        
        if "Token" in res:
            print(f"SUCCESS! Master Token Generated.")
            print(f"TOKEN_START: {res['Token']}")
            # We will use this token to authenticate on EC2
        else:
            print(f"FAILED: {res.get('Error')} - {res.get('Info')}")
            if res.get('Url'):
                print(f"ACTION: Check {res.get('Url')}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    get_local_token()
