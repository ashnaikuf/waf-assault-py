# Educational WAF Testing Script: Browser Automation for Page Navigation
# Purpose: Demonstrates simple browser automation to navigate to application pages
# Learning Goal: Shows basic browser fingerprinting and navigation pattern detection
# WAF Context: Tests user agent validation and human-like browsing behavior analysis
# Comparison: Unlike headless requests, this uses actual browser with full JavaScript execution
# Usage: Learn how WAFs detect and validate legitimate browser vs automation tools

from selenium import webdriver

import os
from dotenv import load_dotenv

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Configuration ---
load_dotenv()
TARGET_URL = os.getenv("TARGET_URL")

def open_browser():
    # Automatically downloads and manages the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        print(f"[*] Opening browser to: {TARGET_URL}")
        # Navigate to the URL
        driver.get(TARGET_URL)

        # Wait so the browser doesn't close immediately
        print("[+] Page loaded. Keeping browser open for 10 seconds...")
        time.sleep(10)

    except Exception as e:
        print(f"[-] An error occurred: {e}")
    finally:
        print("[*] Closing browser.")
        driver.quit()

if __name__ == "__main__":
    open_browser()