# Educational WAF Testing Script: Requests with Custom Cookies
# Purpose: Demonstrates sending HTTP requests with potentially suspicious cookie values
# Learning Goal: Shows how WAFs inspect and validate cookie content for malicious patterns
# WAF Context: Tests cookie-based security rules and session token validation
# Comparison: Unlike cookieless requests (01_-08_), this includes custom cookie headers
# Usage: Learn how WAFs analyze cookie values for signs of session hijacking or XSS

import requests
import time
import json

import os
from dotenv import load_dotenv
load_dotenv()
from requests.exceptions import RequestException

TARGET_URL = os.getenv("TARGET_URL")
COOKIES = os.getenv("COOKIES")
REQUEST_COUNT = 10

# Define the cookie to be sent in the request header.
# The key 'custom_cookie' is arbitrary; the value is the one requested.
CUSTOM_COOKIES = {"custom_cookie": COOKIES}

# Set the headers for the request, including the random user agent.
# headers = {
#     # Valid User-Agents
#     # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
#     # Alternative User-Agents to try if the above still fails:
#     # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#     # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# }  

def send_cookie_requests(url, count, cookies):
    """
    Sends a specified number of HTTP GET requests to a given URL,
    including a pre-defined cookie in the request header for each call.
    """
    print(f"Starting {count} GET requests with cookie to: {url}")
    print(f"Cookie being sent: {json.dumps(cookies)}\n")
    
    for i in range(1, count + 1):
        print(f"--- Request {i}/{count} ---")
        try:
            # Use the GET method (which is suitable for carrying cookies)
            # and pass the defined cookies dictionary directly.
            response = requests.request("GET", url,  cookies=cookies, timeout=5)
            
            # Check for successful response (status codes in the 200s)
            if response.ok:
                print(f"Status Code: {response.status_code} (OK)")
                
                # The response body is a JSON object that includes an entry 
                # for the cookies the server received. We parse and display it.
                try:
                    data = response.json()
                    # web server echoes the received cookies under the 'cookies' key
                    echoed_cookies = data.get('cookies', {})

                    print("\nEchoed Cookies Received by Server (Verification):")
                    print("==============================================")
                    print(json.dumps(echoed_cookies, indent=4))
                    print("==============================================\n")
                    
                except json.JSONDecodeError:
                    print("Error decoding JSON response for verification.\n")

            else:
                print(f"Status Code: {response.status_code} (Error)")
                print(f"Response Content: {response.text[:150]}...\n")
                
        except RequestException as e:
            # Handle network errors, timeouts, or DNS failures
            print(f"An error occurred during the request: {e}\n")
            
        # Optional: Add a small delay between requests
        time.sleep(0.1)

if __name__ == "__main__":
    send_cookie_requests(TARGET_URL, REQUEST_COUNT, CUSTOM_COOKIES)
    print("Script finished.")

