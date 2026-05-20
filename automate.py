import requests
import json
import string
import random
import time

import os
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_ENDPOINT = "rest/user/login"
FEEDBACK_ENDPOINT = "api/Feedbacks/"

# Credentials from your login script
EMAIL = os.getenv("EMAIL1")
PASSWORD = os.getenv("PASSWORD1")
ITERATIONS = 10

def get_bearer_token():
    """Logs in and returns the authentication token."""
    login_url = TARGET_URL + LOGIN_ENDPOINT
    payload = {"email": EMAIL, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}

    print(f"[*] Attempting login for: {EMAIL}")
    try:
        response = requests.post(login_url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Juice Shop nests the token inside ['authentication']['token']
            data = response.json()
            token = data.get('authentication', {}).get('token')
            if token:
                print("[+] Login Successful. Token acquired.")
                return token
        
        print(f"[-] Login Failed. Status: {response.status_code}")
        return None
    except Exception as e:
        print(f"[-] Connection Error: {e}")
        return None

def generate_random_comment(length=12):
    """Generates a random string for the comment field."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) + " (anonymous)"

def run_automation():
    # 1. Get the dynamic token
    token = get_bearer_token()
    if not token:
        print("[-] Aborting: Could not obtain Bearer token.")
        return

    # 2. Setup headers with the dynamic token
    feedback_url = TARGET_URL + FEEDBACK_ENDPOINT
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Origin": TARGET_URL,
        "Referer": TARGET_URL
    }

    print(f"[*] Starting {ITERATIONS} feedback submissions...")

    # 3. Loop 100 times
    for i in range(ITERATIONS):
        payload = {
            "captchaId": 5,
            "captcha": "-36",
            "comment": generate_random_comment(),
            "rating": 2
        }

        try:
            # requests calculates Content-Length automatically
            res = requests.post(feedback_url, headers=headers, json=payload)
            print(f"[{i+1}/100] Status: {res.status_code} | Comment: {payload['comment']}")
        except Exception as e:
            print(f"[{i+1}/100] Failed: {e}")
        
        # Optional: Tiny sleep to avoid overwhelming the server
        # time.sleep(0.1)

if __name__ == "__main__":
    run_automation()