# Educational WAF Testing Script: Basic HTTP POST Request
# Purpose: Demonstrates sending data to a WAF-protected endpoint using POST method
# Learning Goal: Shows proper JSON payload structure and Content-Type headers
# WAF Context: Tests how WAFs inspect and validate POST request bodies and headers
# Comparison: Unlike GET (01_), this sends data in the request body to modify server state
# Usage: Run after GET test to understand how WAFs handle data submission requests

import requests
from urllib.parse import urlparse

import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("TARGET_URL_API")

def get_host_from_url(url):
    """Extract host from URL"""
    parsed_url = urlparse(url)
    return parsed_url.netloc

host = get_host_from_url(url)
print(f"Host: {host}")

# Updated headers for a POST request delivering JSON data
headers = {
    "Host": get_host_from_url(url),
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-us",
    "Accept": "application/json",
    "Connection": "keep-alive",
    "Content-Type": "application/json",  # Telling the server we are sending JSON
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Cache-Control": "max-age=0",
    "X-Forwarded-For": "127.0.0.1"
}

# The data payload you want to send to the FastAPI server.
# Change these keys and values to match whatever schema your specific endpoint expects.
payload = {
    "sample_key": "sample_value",
    "test_mode": True
}

try:
    print(f"Sending POST request to FastAPI endpoint: {url}...")
    
    # Executing the POST request. 
    # Using the 'json' parameter automatically stringifies the payload and 
    # ensures it matches the 'application/json' Content-Type.
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    
    # Output the results
    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
        
    # Print the API response body
    print("\nResponse Body:")
    try:
        print(response.json())
    except ValueError:
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")