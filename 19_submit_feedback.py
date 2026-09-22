# Educational WAF Testing Script: Automated Feedback Form Submission
# Purpose: Demonstrates automated form submission using browser automation
# Learning Goal: Shows how WAFs detect and handle automated form interactions
# WAF Context: Tests bot detection, form submission rate limiting, and user behavior analysis
# Comparison: Unlike HTTP requests (01_-18_), this simulates real browser interactions
# Usage: Learn how WAFs differentiate between human users and automated scripts

import os
import time
import random
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from sqlinjection1 import TARGET_URL

# Initialize Faker for realistic randomized user data
fake = Faker()

def generate_lorem_message():
    """Generates a unique 'lorem ipsum' style message."""
    return f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. {fake.paragraph()[:100]}"

def submit_feedback(driver, url, index):
    """
    Submits a single feedback entry to the OWASP Juice Shop contact form using Selenium.
    """
    try:
        # Navigate to the contact page
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Generate randomized user data
        name = fake.name()
        email = fake.email()
        message = generate_lorem_message()
        rating = random.randint(1, 5)

        # Wait for the Name field to be visible and enter data
        name_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "name")]'))
        )
        name_field.clear()
        name_field.send_keys(name)

        # Find and fill the Message field
        comment_field = driver.find_element(By.XPATH, '//textarea[contains(@placeholder, "message")]')
        comment_field.clear()
        comment_field.send_keys(f"Name: {name} | Email: {email} | Message: {message}")

        # Find and fill the Rating field
        rating_field = driver.find_element(By.XPATH, '//input[@formcontrolname="rating"]')
        rating_field.clear()
        rating_field.send_keys(str(rating))

        # Note: The OWASP Juice Shop form requires a CAPTCHA solution.
        # If running unattended, the CAPTCHA will need to be bypassed, solved, or pre-configured 
        # (e.g., by pinning the CAPTCHA ID as per standard challenge instructions).
        # A 10-second pause is included here to allow you to interact or view the page if needed.

        # Click the Submit button
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()
        
        # Brief pause to register the click
        time.sleep(1)

        print(f"[SUCCESS] Submission #{index}: Successfully submitted feedback for {name}.")
        return True

    except Exception as e:
        print(f"[FAILURE] Submission #{index}: Failed to submit feedback. Error: {str(e)[:100]}")
        return False

def main():

    # Target URL for the Juice Shop profile image endpoint
    TARGET_URL = os.getenv("TARGET_URL")
    target_url = f"{TARGET_URL}/#/contact"
    
    # Configure Chrome Options for Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment to run in headless mode
    
    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        print("Starting feedback submission process...\n")
        
        for i in range(1, 11):
            submit_feedback(driver, target_url, i)
            # Add a small delay between submissions to simulate real user behavior
            time.sleep(3)
            
        print("\nAll 10 submissions processed.")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()