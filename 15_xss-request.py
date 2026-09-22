# Educational WAF Testing Script: Cross-Site Scripting (XSS) Attack
# Purpose: Demonstrates XSS payload injection in request parameters
# Learning Goal: Shows how WAFs detect and sanitize malicious JavaScript content
# WAF Context: Tests XSS protection rules and script injection filtering
# Comparison: Unlike safe content, this sends HTML/JavaScript tags to trigger WAF alerts
# Usage: Learn how WAFs identify and block client-side attack vectors

import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

# --- Configuration for Educational Simulation ---
# We use a safe echo service to inspect the request, NOT a vulnerable server.
# A real-world XSS attack targets an endpoint that accepts user input 
# and reflects it back to the user without proper sanitization.
TARGET_URL = os.getenv("TARGET_URL")

# 1. Define the Malicious XSS Payload
# This is a classic non-persistent (reflected) XSS payload designed to
# execute JavaScript in the victim's browser, typically causing an alert
# or stealing cookies/session data.
# ATTACK_PAYLOAD = "<script>alert('XSS Test');</script>"
ATTACK_PAYLOAD = "<iframe src=\"javascript:alert('xss')\">"

# 2. Define the Request Parameter
# This simulates an attacker trying to inject the malicious payload into a 
# vulnerable query parameter (e.g., 'search', 'query', or 'message').
QUERY_PARAMETERS = {
    "search": ATTACK_PAYLOAD
}

# --- Request Execution ---
print("--- Starting XSS Request Simulation (Educational) ---")
print(f"Target URL: {TARGET_URL}")
print(f"Simulated XSS Payload: {ATTACK_PAYLOAD}")

try:
    # Send the GET request with the XSS payload in the query parameter
    response = requests.get(
        TARGET_URL,
        params=QUERY_PARAMETERS,
        # Set a user-agent to make the request appear non-malicious
        headers={'User-Agent': 'XSS-Defense-Simulator/1.0'}
    )

    # --- Response Analysis ---
    print("\n--- Server Response (Echo) ---")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        response_json = response.json()
        
        # The 'args' section shows how the server received and parsed the URL parameters.
        # Note how the browser automatically URL-encodes the payload.
        print("\nRequest Parameters Received by Server ('args' field):")
        print(json.dumps(response_json.get('args', {}), indent=4))
        
        # The 'url' field confirms the full URL constructed, showing the URL-encoded payload
        print("\nFull URL Constructed (showing URL-encoded payload):")
        print(response_json.get('url'))

        print("\nNote: In a vulnerable application, this payload would be reflected back into the HTML response without being stripped or properly escaped, causing the browser to execute the script.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response text:\n{response.text}")

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred during the request: {e}")

print("\n--- Simulation Complete ---")

