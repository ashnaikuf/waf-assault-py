import requests

import os
from dotenv import load_dotenv
load_dotenv()

# Use a generic placeholder target (e.g., localhost or a test environment)
TARGET_URL = os.getenv("TARGET_URL")

# Payloads commonly monitored and blocked by WAF rule sets (like ModSecurity CRS)
payloads = [
    "/etc/passwd",
    "/file:///etc/styles.css",
    "/file:///etc/vendor.js"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "X-WAF-Test": "Traversal-Simulation"
}

def simulate_traversal_attack():
    print("Initializing Path Traversal Simulation...\n")
    
    for payload in payloads:
        # Construct the target URL with the payload appended
        target_endpoint = f"{TARGET_URL}{payload}"
        
        print(f"[*] Testing Endpoint: {target_endpoint}")
        
        try:
            response = requests.get(target_endpoint, headers=headers, timeout=5)
            
            print(f"    - Status Code: {response.status_code}")
            
            # WAFs generally block these requests and return a 403 Forbidden or 406 Not Acceptable
            if response.status_code == 403:
                print("    - [WAF Action] Detected and Blocked: Access Denied.")
            else:
                print(f"    - [Response Received] Content Length: {len(response.content)} bytes")
                
        except requests.exceptions.RequestException as e:
            print(f"    - [x] Connection Error (Target may not be reachable): {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    simulate_traversal_attack()