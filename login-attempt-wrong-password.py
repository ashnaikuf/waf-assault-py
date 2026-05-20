import requests

import os
from dotenv import load_dotenv
load_dotenv()

TARGET_URL = os.getenv("TARGET_URL")
EMAIL = os.getenv("EMAIL2")
PASSWORD = os.getenv("PASSWORD2")


headers = {
    "Cookie": "language=en; welcomebanner_status=dismiss",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json, text/plain, */*",
    "Sec-Ch-Ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Origin": f"{TARGET_URL}",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": f"{TARGET_URL}",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
    "Connection": "keep-alive"
}

data = {
    "email": EMAIL,
    "password": PASSWORD
}

response = requests.post(TARGET_URL, headers=headers, json=data)

# Print the results
print(f"Status Code: {response.status_code}")
print("Response Body:", response.text)
