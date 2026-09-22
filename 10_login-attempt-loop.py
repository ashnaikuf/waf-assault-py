# Educational WAF Testing Script: Repeated Login Attempts
# Purpose: Demonstrates multiple login attempts with the same credentials in a loop
# Learning Goal: Shows how WAFs detect repeated authentication attempts from same source
# WAF Context: Tests account lockout mechanisms and login attempt rate limiting
# Comparison: Unlike single login (05_), this creates patterns that may trigger WAF alerts
# Usage: Observe how repeated valid logins are handled differently than brute force attempts

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

#TODO add more users and passwords to test against
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
        "Content-Type": "application/json",
        # Valid User-Agents
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        # Alternative User-Agents to try if the above still fails:
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
        #TODO Why Login Status is UNEXPECTED RESPONSE (200) when Response Body has "{'authentication': {'token': ...""
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

