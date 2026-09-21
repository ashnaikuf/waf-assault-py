import requests
import time
import random

import os
from dotenv import load_dotenv
load_dotenv()

# A list of common user agents to rotate through.

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy S22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.36",
    "Mozilla/5.0 (iPod touch; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1",
    # Non-browser / scripts / scrapers
    "curl/7.88.1",
    "Wget/1.21.3 (linux-gnu)",
    "python-requests/2.28.1",
    "python-urllib3/1.26.14",
    "Scrapy/2.9.0 (+https://scrapy.org)",
    "PostmanRuntime/7.32.3",
    "Go-http-client/2.0",
    "Java/11.0.19",
    "Apache-HttpClient/4.5.14 (Java/11.0.19)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckgo-help/faq-about-our-crawler)",
    "PostmanRuntime/7.30.1"
]


TARGET_URL = os.getenv("TARGET_URL")

# The number of requests you want to send.
num_requests = 10

print(f"Sending {num_requests} requests to {TARGET_URL} with a one-second delay...")

# Loop to send multiple requests.
for i in range(num_requests):
    try:
        # Randomly select a user agent from the list.
        random_user_agent = random.choice(user_agents)

        # Set the headers for the request, including the random user agent.
        headers = {
            'User-Agent': random_user_agent
        }

        # Send a GET request to the URL with the specified headers.
        print(f"Request {i+1}: Using User-Agent: {random_user_agent}")
        response = requests.get(TARGET_URL, headers=headers)

        # Print the status code to confirm the request was successful.
        print(f"Request {i+1}: Status Code: {response.status_code}")

        # Check for a successful response (status code 200).
        if response.status_code == 200:
            print(f"Request {i+1}: Success!")
        else:
            print(f"Request {i+1}: Failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle potential errors, such as connection issues or invalid URLs.
        print(f"Request {i+1}: An error occurred: {e}")

    # Wait for one second before the next request to be respectful of the server.
    if i < num_requests - 1:
        print("Sleeping for 1 second...")
        time.sleep(1)

print("All requests complete.")

