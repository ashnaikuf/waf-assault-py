from selenium import webdriver

import os
from dotenv import load_dotenv
load_dotenv()
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_ENDPOINT = "rest/user/login"
CONTACT_URL = f"{TARGET_URL}#/contact"

# Credentials from your file
EMAIL = os.getenv("EMAIL1")
PASSWORD = os.getenv("PASSWORD1")

def get_bearer_token():
    """Performs login via API to retrieve the Bearer Token."""
    login_url = TARGET_URL + LOGIN_ENDPOINT
    payload = {"email": EMAIL, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}

    print(f"[*] Fetching token for {EMAIL}...")
    try:
        response = requests.post(login_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            # Extracting token from the Juice Shop response structure
            token = response.json().get('authentication', {}).get('token')
            if token:
                print("[+] Token successfully retrieved.")
                return token
        print(f"[-] Failed to get token. Status: {response.status_code}")
        return None
    except Exception as e:
        print(f"[-] Request Error: {e}")
        return None

def open_authenticated_browser():
    # 1. Get the token first
    token = get_bearer_token()
    if not token:
        return

    # 2. Setup Selenium Wire to intercept and inject headers
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Define the header injection logic
    def interceptor(request):
        # We only inject headers into requests going to the Juice Shop domain
        if TARGET_URL in request.url:
            # Remove any existing Auth header and add our Bearer token
            del request.headers['Authorization']
            request.headers['Authorization'] = f'Bearer {token}'
            request.headers['Accept-Language'] = 'en-US,en;q=0.9'

    # Set the interceptor on the driver
    driver.request_interceptor = interceptor

    try:
        print(f"[*] Navigating to: {CONTACT_URL}")
        # When this loads, all background API calls will include your Bearer token
        driver.get(CONTACT_URL)
        
        print("[+] Page loaded with Bearer Token. Staying open for 30 seconds.")
        time.sleep(30)

    except Exception as e:
        print(f"[-] Browser Error: {e}")
    finally:
        print("[*] Shutting down.")
        driver.quit()

if __name__ == "__main__":
    open_authenticated_browser()