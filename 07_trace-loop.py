# Educational WAF Testing Script: HTTP TRACE Method Requests
# Purpose: Demonstrates TRACE method which echoes request headers back in response
# Learning Goal: Shows how WAFs handle potentially dangerous HTTP methods
# WAF Context: Tests method-based security controls since TRACE can expose sensitive headers
# Comparison: Unlike HEAD (06_), TRACE returns request data which may reveal internal info
# Usage: Learn if WAFs block TRACE method or allow this diagnostic functionality

import requests
import time

import os
from dotenv import load_dotenv
load_dotenv()
from requests.exceptions import RequestException

# Define the safe, educational endpoint for TRACE testing.
TARGET_URL = os.getenv("TARGET_URL")
REQUEST_COUNT = 10

def send_trace_requests(url, count):
    """
    Sends a specified number of HTTP TRACE requests to a given URL.

    The HTTP TRACE method is primarily used for debugging and diagnostics,
    as the server echoes the received request back to the client in the response body.
    """
    print(f"Starting {count} TRACE requests to: {url}\n")
    
    # Set the headers for the request, including the random user agent.
    headers = {
        'User-Agent': "python TRACE UA Test 1.0"
    }        
    for i in range(1, count + 1):
        print(f"--- Request {i}/{count} ---")
        try:
            # The requests library allows calling the TRACE method directly.
            response = requests.request("TRACE", url, headers=headers,timeout=5 , allow_redirects=False)
            
            # Print the HTTP method being used
            print(f"HTTP Method: {response.request.method}")

            # Print all request headers in a loop
            print("Request Headers:")
            for header_name, header_value in response.request.headers.items():
                print(f"  {header_name}: {header_value}")
            print()
                        
            # Check for successful response (status codes in the 200s)
            if response.ok:
                print(f"Status Code: {response.status_code} (OK)")
                
                # The body of a TRACE response contains the request headers the server received
                # print("\nEchoed Request Body (Headers Received by Server):")
                # print("==============================================")
                # Decode the response text to show the echoed request content
                # print(response.text.strip())
                # print("==============================================\n")
            else:
                print(f"Status Code: {response.status_code} (Error)")
                print(f"Response Content: {response.text[:150]}...\n")
                
        except RequestException as e:
            # Handle network errors, timeouts, or DNS failures
            print(f"An error occurred during the request: {e}\n")
            
        # Optional: Add a small delay between requests
        time.sleep(0.1)

if __name__ == "__main__":
    send_trace_requests(TARGET_URL, REQUEST_COUNT)
    print("Script finished.")
