import requests
import time

import os
from dotenv import load_dotenv
load_dotenv()
from requests.exceptions import RequestException

# Define the safe, educational endpoint for HEAD testing.
# We use a general endpoint like /get, as HEAD is typically used to retrieve metadata
# (headers) for a resource without downloading the body.
TARGET_URL = os.getenv("TARGET_URL")
REQUEST_COUNT = 10

def send_head_requests(url, count):
    """
    Sends a specified number of HTTP HEAD requests to a given URL.

    The HTTP HEAD method is identical to GET but without the response body.
    It is used to retrieve response headers (metadata) only.
    """
    print(f"Starting {count} HEAD requests to: {url}\n")
    
    for i in range(1, count + 1):
        print(f"--- Request {i}/{count} ---")
        try:
            # The requests library allows calling the HEAD method directly.
            response = requests.request("HEAD", url, timeout=5)
            
            # Check for successful response (status codes in the 200s)
            if response.ok:
                print(f"Status Code: {response.status_code} (OK)")
                
                # HEAD responses contain headers but an empty body.
                print("\nReceived Response Headers (Metadata):")
                print("==============================================")
                # Iterate and print the response headers
                for header, value in response.headers.items():
                    print(f"{header}: {value}")
                print("==============================================\n")
            else:
                print(f"Status Code: {response.status_code} (Error)")
                # Print a small excerpt of the body, though it should typically be empty for HEAD
                print(f"Response Content (usually empty for HEAD error): {response.text[:150]}...\n")
                
        except RequestException as e:
            # Handle network errors, timeouts, or DNS failures
            print(f"An error occurred during the request: {e}\n")
            
        # Optional: Add a small delay between requests
        time.sleep(0.1)

if __name__ == "__main__":
    send_head_requests(TARGET_URL, REQUEST_COUNT)
    print("Script finished.")

