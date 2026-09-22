# WAF Assault Python Scripts

A comprehensive collection of Python scripts designed for educational purposes to demonstrate various web attack vectors and HTTP request techniques against web applications protected by Web Application Firewalls (WAFs). These scripts are ideal for learning how different attack patterns interact with WAF detection mechanisms.

## 🎯 Purpose

This repository provides hands-on learning materials for understanding:
- How different HTTP request patterns behave against WAF-protected applications
- Various web attack vectors and their implementations
- Traffic generation techniques for security testing
- Browser automation for complex user interactions

## 📚 Script Categories

### Basic HTTP Methods (01-04)
- **01_simple_http_get.py** - Demonstrates basic HTTP GET requests with standard headers
- **02_simple_http_post.py** - Shows HTTP POST requests with JSON payloads
- **03_get-post-loop.py** - Combines GET and POST requests in continuous loops
- **04_http-ua-random.py** - Implements User-Agent header rotation to avoid detection

### Authentication Testing (05, 10-11, 21)
- **05_login-attempt-single.py** - Single legitimate login attempt for baseline testing
- **10_login-attempt-loop.py** - Repeated login attempts to test rate limiting
- **11_login-bruteforce.py** - Classic brute force attack simulation
- **21_login-bruteforce-somecorrectpasswd.py** - Mixed valid/invalid credential attacks

### HTTP Method Variations (06-07)
- **06_head-loop.py** - HTTP HEAD method requests for reconnaissance
- **07_trace-loop.py** - HTTP TRACE method testing for information disclosure

### Header and Request Manipulation (08-09)
- **08_malformed-request.py** - Intentionally malformed requests to test WAF parsing
- **09_request-cookie-ashmalicious.py** - Custom cookie injection techniques

### Web Application Attacks (12-18)
- **12_sqlinjection1.py** - SQL injection attack patterns and payloads
- **13_xss-request.py** - Cross-Site Scripting (XSS) payload delivery
- **14_lfi-rfi.py** - Local and Remote File Inclusion vulnerability testing
- **15_traversal.py** - Basic directory traversal attack patterns
- **16_traversal2.py** - Advanced directory traversal with encoding variations
- **17_ssrf.py** - Server-Side Request Forgery (SSRF) attack simulation
- **18_crlf-attack.py** - CRLF injection and HTTP header splitting attacks

### Application Interaction (19-20)
- **19_submit_feedback.py** - Automated feedback form submission
- **20_automate.py** - Multi-step application workflow automation

### Browser Automation (22-23)
- **22_selenium-open-feedback.py** - Basic browser automation for page navigation
- **23_selenium-open-feedback_ui.py** - Advanced form interaction with Selenium

## 🛠 Configuration Files

- **`.env`** - Environment variables including target URLs and configuration
- **`best1050.txt`** - Comprehensive payload collection for various attack vectors
- **`run_allpy.sh`** - Batch execution script for running multiple attack scenarios
- **`run_bots.sh`** - Specialized script for automated bot execution
- **`run_login.sh`** - Focused login attack automation script

## 🚀 Getting Started

1. **Install Dependencies:**
   ```bash
   pip install requests selenium python-dotenv
   ```

2. **Configure Environment:**
   - Copy `.env.example` to `.env` (if available)
   - Set `TARGET_URL_API` and other required variables in `.env`

3. **Run Individual Scripts:**
   ```bash
   python 01_simple_http_get.py
   ```

4. **Execute Batch Operations:**
   ```bash
   ./run_allpy.sh
   ```

## 📖 Learning Path

### Beginners
Start with basic HTTP methods to understand fundamentals:
1. `01_simple_http_get.py` - Learn basic GET requests
2. `02_simple_http_post.py` - Understand POST request structure
3. `05_login-attempt-single.py` - See legitimate authentication

### Intermediate
Explore traffic patterns and evasion techniques:
1. `04_http-ua-random.py` - User-Agent rotation
2. `03_get-post-loop.py` - Traffic generation patterns
3. `08_malformed-request.py` - Request manipulation

### Advanced
Study specific attack vectors:
1. `12_sqlinjection1.py` - SQL injection techniques
2. `17_ssrf.py` - Server-side request forgery
3. `20_automate.py` - Complex multi-step attacks

## ⚠️ Important Notes

- **Educational Use Only**: These scripts are for learning and authorized security testing
- **WAF Detection**: Each script demonstrates different techniques that may trigger WAF rules
- **Target Environment**: Designed for testing against OWASP Juice Shop or similar vulnerable applications
- **Rate Limiting**: Some scripts include deliberate delays to avoid overwhelming target systems

## 🔒 Ethical Considerations

- Only use these scripts against applications you own or have explicit permission to test
- Respect rate limits and server resources
- These tools are for defensive security education and authorized penetration testing
- Always follow responsible disclosure practices for any vulnerabilities discovered

## 📝 Contributing

When adding new scripts, ensure they:
- Include educational comments explaining their purpose
- Follow the naming convention (number_description.py)
- Demonstrate a specific aspect of WAF testing or web security
- Include appropriate error handling and logging