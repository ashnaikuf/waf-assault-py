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
misleading_headers = {
    # The header says the content is URL-encoded form data...
    'Content-Type': 'application/x-www-form-urlencoded',
    # We also include Content-Length for accuracy, calculated from the JSON string length
    'Content-Length': str(len(json_data_string))
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

