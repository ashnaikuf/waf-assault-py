import requests
import json
import time

import os
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_ENDPOINT = "/rest/user/login"
EMAIL = os.getenv("EMAIL1")
PASSWORD = os.getenv("PASSWORD1")

# The payload structure required by the Juice Shop API for login
payload = {
    "email": EMAIL,
    "password": PASSWORD
}

def perform_login_attempt(url, endpoint, data):
    """
    Attempts to log in to the specified Juice Shop endpoint.
    """
    full_url = url + endpoint
    headers = {
        "Content-Type": "application/json"
    }

    print(f"--- Login Attempt Started ---")
    print(f"Target URL: {full_url}")
    print(f"Attempting login with email: {data['email']}")

    try:
        # Send the POST request with the JSON payload
        response = requests.post(full_url, data=json.dumps(data), headers=headers, timeout=5)

        print(f"\nResponse Status Code: {response.status_code}")

        # Try to parse the response body as JSON
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            response_json = {"message": "Response content was not valid JSON."}

        # Check for success (usually 200 OK) or failure status
        #TODO Why Login Statusis UNEXPECTED RESPONSE (200) when Response Body has "{'authentication': {'token': ...""
        if response.status_code == 200 and 'token' in response_json:
            print("Login Status: SUCCESS!")
            print(f"User Token (Authentication Successful): {response_json.get('token')[:30]}...")
            print("--- The user was successfully authenticated. ---")
        elif response.status_code == 401 or response.status_code == 403:
            # Juice Shop typically returns 401 for bad credentials
            error_message = response_json.get('error', response_json.get('message', 'Authentication Failed'))
            print(f"Login Status: FAILED (Unauthorized/Forbidden)")
            print(f"Error Detail: {error_message}")
            print("--- Authentication failed due to incorrect credentials or missing user. ---")
        else:
            print(f"Login Status: UNEXPECTED RESPONSE ({response.status_code})")
            print(f"Response Body: {response_json}")

    except requests.exceptions.Timeout:
        print("Login Status: FAILED")
        print("Error: Request timed out. Is the Juice Shop application running?")
    except requests.exceptions.RequestException as e:
        print("Login Status: FAILED")
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Wait briefly to ensure the terminal output is clear
    time.sleep(0.5)
    perform_login_attempt(TARGET_URL, LOGIN_ENDPOINT, payload)

