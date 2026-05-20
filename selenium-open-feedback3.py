import os
load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import string
import random
import time
import os
from dotenv import load_dotenv

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_API = f"{TARGET_URL}rest/user/login"
CONTACT_URL = f"{TARGET_URL}#/contact"

load_dotenv()  # Load environment variables from .env file

EMAIL = os.getenv("EMAIL1")
PASSWORD = os.getenv("PASSWORD1")

def get_bearer_token():
    """Gets token via API."""
    payload = {"email": EMAIL, "password": PASSWORD}
    try:
        response = requests.post(LOGIN_API, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get('authentication', {}).get('token')
    except Exception as e:
        print(f"[-] Login Error: {e}")
    return None

def generate_random_comment(length=15):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_automation():
    token = get_bearer_token()
    if not token:
        print("[-] Could not get token. Aborting.")
        return

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    user_agent = driver.execute_script("return navigator.userAgent")
    print("user_agent:" + user_agent)

    try:
        # 1. Open the site to establish the domain context
        driver.get(TARGET_URL)
        time.sleep(2) 

        # 2. Inject the token into LocalStorage so the UI thinks you are logged in
        driver.execute_script(f"window.localStorage.setItem('token', '{token}');")
        
        # 3. Navigate to the contact page
        driver.get(CONTACT_URL)
        time.sleep(3) # Wait for Angular to render the form

        # --- Fill the Form ---

        # 1. Fill Comment
        comment_field = driver.find_element(By.ID, "comment")
        comment_field.send_keys(generate_random_comment())

        # 2. Set Rating to 2 using the slider
        slider_input = driver.find_element(By.CSS_SELECTOR, "mat-slider#rating input[type='range']")
        driver.execute_script("arguments[0].value = '2';", slider_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", slider_input)

        # 3. Set Rating to 2
        # Juice Shop uses Material Design stars; clicking the second star sets rating to 2
        rating_stars = driver.find_elements(By.CSS_SELECTOR, ".mat-rating-bar .mat-icon")
        if len(rating_stars) >= 2:
            rating_stars[1].click() # Index 1 is the 2nd star

        # 4. Fill Captcha
        # The captcha input usually has an ID like 'captchaControl'
        captcha_field = driver.find_element(By.ID, "captchaControl")
        captcha_field.send_keys("63")
        
        # 5. Simulate submit button click
        submit_button = driver.find_element(By.ID, "submitButton")  # Adjust selector if needed
        submit_button.click()

        print("[+] Form filled and submitted successfully.")

        print("[+] Form filled successfully.")
        
        time.sleep(10) # Stay open to verify results

    except Exception as e:
        print(f"[-] Automation Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_automation()