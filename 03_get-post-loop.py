import requests
import time

# Configuration
import os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv("TARGET_URL")
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

REQUEST_COUNT = 10
def run_enrollment_loop():
    for i in range(1, REQUEST_COUNT + 1):  # Loops exactly 10 times (1 through 10)
        print(f"=== Iteration {i}/{REQUEST_COUNT} ===")
        
        # 1. Send GET Request
        try:
            print("Sending GET request...")
            get_response = requests.get(URL, headers={"accept": "application/json"})
            print(f"GET Status: {get_response.status_code}")
            # Optional: print(get_response.text) if you need to see the body
            
        except requests.exceptions.RequestException as e:
            print(f"GET request failed on iteration {i}: {e}")

        # Small pause between GET and POST (optional, adjust as needed)
        time.sleep(0.5)

        # 2. Send POST Request
        # Note: Define your JSON body structure here depending on what the API expects
        payload = {
            "iteration": i,
            "status": "testing"
        }
        
        try:
            print("Sending POST request...")
            post_response = requests.post(URL, headers=HEADERS, json=payload)
            print(f"POST Status: {post_response.status_code}")
            print(f"POST Response: {post_response.text}")
            
        except requests.exceptions.RequestException as e:
            print(f"POST request failed on iteration {i}: {e}")
            
        print("-" * 30, "\n")
        
        # Optional: Cool down pause before the next loop iteration starts
        time.sleep(1)

if __name__ == "__main__":
    run_enrollment_loop()