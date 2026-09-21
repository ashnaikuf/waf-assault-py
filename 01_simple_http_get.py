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

# Cleaned up headers for a standard GET request
headers = {
    "Host": host,
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-us",
    "Accept": "application/json",  # Changed to JSON since FastAPI backends typically return JSON
    "Connection": "keep-alive",
    "Cookie": "",
    "Content-Type": "application/json, application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Cache-Control": "max-age=0",
    "X-Forwarded-For": "127.0.0.1"
}

try:
    print(f"Sending GET request to FastAPI endpoint: {url}...")
    
    # Executing the GET request
    response = requests.get(url, headers=headers, timeout=10)
    
    # Output the results
    # print(f"Request Code:")
    print(f"Request Code: {response.request.method}")
    # Notice we call it on 'response.request', not the 'requests' library
    print("Request Headers:")
    for key, value in response.request.headers.items():
        print(f"  {key}: {value}")

    print(f"Status Code: {response.status_code}")
    print("\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
        
    # Print the API response body
    print("\nResponse Body:")
    try:
        # If the API returns valid JSON, pretty-print it
        print(response.json())
    except ValueError:
        # Fallback to plain text if it's not JSON
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")