# Educational WAF Testing Script: Malformed HTTP Request Headers
# Purpose: Demonstrates sending requests with mismatched Content-Type and payload
# Learning Goal: Shows how WAFs detect and handle inconsistent header/body combinations
# WAF Context: Tests protocol validation and malformed request detection capabilities
# Comparison: Unlike well-formed requests (01_, 02_), this deliberately sends conflicting headers
# Usage: Learn how WAFs respond to requests that violate HTTP protocol standards

import requests
import json
import time

import os
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL")


# 1. The ACTUAL payload data (JSON format)
actual_json_payload = {
    "user_id": 1001,
    "session_token": "abc-123-xyz",
    "data_update": time.time()
}

# 2. Convert the payload to a JSON string (the data that will be sent)
json_data_string = json.dumps(actual_json_payload)

# 3. Define the MISLEADING headers
# We are sending JSON data, but we are explicitly setting the Content-Type header
# to 'application/x-www-form-urlencoded', which tells the server to expect
# key1=value1&key2=value2 format. This is the malformation we are simulating.
# 'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15"
# 'User-Agent': "python Misleading UA Test 1.0"

# misleading_headers = {
#     # The header says the content is URL-encoded form data...
#     'Content-Type': 'application/x-www-form-urlencoded',
#     # We also include Content-Length for accuracy, calculated from the JSON string length
#     'Content-Length': str(len(json_data_string)),
#             # Valid User-Agents
#         # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
#         # Alternative User-Agents to try if the above still fails:
#         # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }


misleading_headers = {
    "Content-Type": 'application/x-www-form-urlencoded',
    "Content-Length": str(len(json_data_string)),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # 'User-Agent': "python Misleading UA Test 1.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}
# --- Request Execution ---
print("--- Starting Malformed Request Simulation ---")
print(f"Target URL: {TARGET_URL}")
print(f"Misleading Headers: {misleading_headers}")
print(f"Raw Body Sent: {json_data_string[:60]}...") # Show a snippet of the raw body

try:
    # Send the POST request
    response = requests.post(
        TARGET_URL,
        headers=misleading_headers,
        data=json_data_string
    )

    # --- Response Analysis ---
    print("\n--- Response Received ---")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        # web serverreturns 200 and details about the request it received.
        response_json = response.json()

        # The 'form' section shows how the server tried to parse the body
        print("\nServer's Attempt to Parse the Body ('form' field):")
        # In this case, some web apps, expecting form data, sees the entire JSON string
        # as a single key with an empty value, or just raw data.
        print(json.dumps(response_json.get('form', {}), indent=4))

        # The 'data' section shows the raw body received
        print("\nRaw Body received by server ('data' field):")
        print(response_json.get('data', 'N/A'))

        # The 'headers' section confirms what was sent
        print("\nHeaders received by server:")
        print(json.dumps(response_json.get('headers', {}).get('Content-Type'), indent=4))


    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response text:\n{response.text}")
# TODO Status Code: 200 but I still get [An error occurred during the request: Expecting value: line 1 column 1 (char 0)]

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred during the request: {e}")

print("\n--- Simulation Complete ---")
# print("Note: A real-world server (e.g., a Flask or Node API) might return a 400 Bad Request or 415 Unsupported Media Type.")

