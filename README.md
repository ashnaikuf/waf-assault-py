# waf-assault-py

A collection of Python scripts for testing and simulating various web attack vectors against OWASP Juice Shop or similar web applications.

## Files and purpose

- `automate.py` - Runs a set of predefined attack routines automatically.
- `crlf-attack.py` - Sends requests crafted to test CRLF injection and header splitting.
- `get-post-loop.py` - Repeatedly sends GET and POST requests in a loop for traffic generation.
- `head-loop.py` - Sends repeated HTTP HEAD requests to the target.
- `http-ua-random.py` - Sends requests with randomized User-Agent strings.
- `http2-ua-multiple-urls.py` - Issues HTTP/2 requests with User-Agent variation across URLs.
- `lfi-rfi.py` - Tests local file inclusion and remote file inclusion vulnerabilities.
- `login-attempt-loop.py` - Performs repeated login attempts in a loop.
- `login-attempt-single.py` - Attempts a single login request.
- `login-attempt-wrong-password.py` - Sends login requests with incorrect password payloads.
- `login-bruteforce.py` - Automates brute-force login attempts.
- `malformed-request.py` - Sends intentionally malformed HTTP requests.
- `request-cookie-ashmalicious.py` - Sends requests with a malicious cookie value.
- `scrapper1.py` - Crawls or fetches web pages for testing or analysis.
- `selenium-auto-feedback.py` - Uses Selenium to automatically submit feedback forms.
- `selenium-open-feedback.py` - Opens the feedback form page using Selenium.
- `selenium-open-feedback2.py` - Alternative Selenium feedback form automation.
- `selenium-open-feedback3.py` - Additional variant of Selenium feedback automation.
- `sqlinjection1.py` - Tests for SQL injection vulnerabilities.
- `ssrf.py` - Attempts Server-Side Request Forgery payloads.
- `submit_feedback.py` - Submits feedback form data to the target application.
- `trace-loop.py` - Sends repeated HTTP TRACE requests.
- `traversal.py` - Attempts directory traversal attacks.
- `traversal2.py` - Second variant of directory traversal testing.
- `xss-request.py` - Sends payloads to test for reflected XSS.

## Notes

- `best1050.txt` contains payloads or configuration data used by the scripts.
- `run_allpy.sh` can be used to execute multiple Python attack scripts in sequence.

