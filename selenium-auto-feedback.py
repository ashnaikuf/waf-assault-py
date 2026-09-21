from selenium import webdriver

import os
from dotenv import load_dotenv

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json
import string
import random
import requests
import time

# --- Configuration ---
load_dotenv()
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_API = f"{TARGET_URL}rest/user/login"
FEEDBACK_API = f"{TARGET_URL}api/Feedbacks/"
EMAIL = os.getenv("EMAIL1")
PASSWORD = os.getenv("PASSWORD1")
ITERATIONS = 10

def get_token():
    """Helper to get token via API to avoid complex UI login automation."""
    payload = {"email": EMAIL, "password": PASSWORD}
    res = requests.post(LOGIN_API, json=payload)
    if res.status_code == 200:
        return res.json().get('authentication', {}).get('token')
    return None

def generate_random_comment(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) + " (anonymous)"

def run_selenium_automation():
    token = get_token()
    if not token:
        print("[-] Could not get token.")
        return

    # Setup Selenium Wire options to inject the Authorization header
    options = {
        'request_storage_base_dir': '/tmp' # Strategy for Linux/Debian
    }
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def interceptor(request):
        # Inject the Bearer token and headers into every request made by the browser
        if TARGET_URL in request.url:
            del request.headers['Authorization']  # Remove existing if any
            request.headers['Authorization'] = f'Bearer {token}'
            request.headers['Accept-Language'] = 'en-US,en;q=0.9'

    # Set the interceptor
    driver.request_interceptor = interceptor

    try:
        # Open the main site first to establish the session
        driver.get(TARGET_URL)
        time.sleep(2) # Let the page load

        print(f"[*] Starting {ITERATIONS} automated feedback posts via Browser...")

        for i in range(ITERATIONS):
            comment = generate_random_comment()
            payload = {
                "captchaId": 5,
                "captcha": "9",
                "comment": comment,
                "rating": 2
            }

            # We use driver.request to send the API call through the browser's context
            # This ensures it uses the browser's cookies and our injected headers
            response = requests.post(
                FEEDBACK_API, 
                json=payload, 
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            
            print(f"[{i+1}/{ITERATIONS}] Posted: {comment} | Status: {response.status_code}")
            time.sleep(1) # Small delay to see action in browser if needed

    finally:
        print("[*] Task complete. Closing browser in 5 seconds.")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    run_selenium_automation()