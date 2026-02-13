import gpsoauth
import sys

def debug_gps():
    email = 'williamtflynn@gmail.com'
    password = 'smagsndsqlbdzbje'
    
    print(f"DEBUG: Attempting direct gpsoauth for {email}...")
    
    try:
        # Attempt to get a master token
        res = gpsoauth.perform_master_login(email, password, "android_id_is_here")
        print(f"Response: {res}")
        
        if "Token" in res:
            print("SUCCESS: Master Token obtained.")
        else:
            print(f"FAILED: {res.get('Error')} - {res.get('Info')}")
            if res.get('Url'):
                print(f"ACTION REQUIRED: Visit {res.get('Url')}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    debug_gps()
