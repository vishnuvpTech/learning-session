# Python SSRF Prevention & Secure HTTP Request Standard

**Document Type:** Security & Code Review Standard  
**Technology:** Python  
**Scope:** Python applications, APIs, microservices, background workers, integrations, and external HTTP/HTTPS communication

---

## 1. Purpose

This standard defines secure practices for making outbound HTTP/HTTPS requests from Python applications and preventing **Server-Side Request Forgery (SSRF)** vulnerabilities.

The objective is to ensure that applications:

- Do not allow attackers to control outbound request destinations.
- Restrict requests to trusted external services.
- Prevent access to internal infrastructure and cloud metadata services.
- Validate URLs before passing them to HTTP clients.
- Apply appropriate network and application-level controls.
- Handle HTTP errors and timeouts securely.
- Satisfy static analysis and SAST requirements.

---

# 2. What is SSRF?

**Server-Side Request Forgery (SSRF)** occurs when an attacker can influence a server into making an HTTP request to a destination that the attacker should not be able to access.

Typical attack flow:

```text
User Input
    |
    v
Application
    |
    v
HTTP Client
    |
    +----> Trusted External API       ✓
    |
    +----> Internal Service           ✗
    |
    +----> Cloud Metadata Endpoint    ✗
    |
    +----> Localhost/Admin Service    ✗
```

For example, insecure code may look like:

```python
url = request.json["url"]

response = requests.get(url)
```

An attacker could potentially provide an internal destination instead of the expected external URL.

---

# 3. Why SSRF is Dangerous

An SSRF vulnerability can potentially allow an attacker to:

- Access internal APIs.
- Access services bound to `localhost`.
- Scan internal network services.
- Access cloud instance metadata services.
- Retrieve credentials or temporary cloud credentials.
- Bypass network-level access restrictions.
- Interact with administrative endpoints.
- Access services that are not publicly exposed.

The actual impact depends on the application's network permissions, cloud configuration, authentication controls, and target infrastructure.

---

# 4. Common SSRF Sources

Developers should consider a URL **untrusted** when it originates directly or indirectly from:

- HTTP request parameters.
- JSON request bodies.
- Form fields.
- HTTP headers.
- Database values controlled by users.
- Uploaded files.
- Webhooks.
- Configuration supplied by customers.
- Message queues.
- External API responses.
- User-controlled redirect URLs.
- Dynamically generated URLs.

Example:

```python
url = request.data.get("callback_url")

requests.post(url)
```

This should be treated as a potential SSRF vulnerability.

---

# 5. Common SSRF Sink

Static analysis tools commonly identify HTTP clients as SSRF sinks.

Examples include:

```python
requests.get(url)
requests.post(url)
requests.put(url)
requests.delete(url)
requests.patch(url)
```

Other HTTP clients may also be affected:

```python
httpx.get(url)
httpx.AsyncClient().get(url)

urllib.request.urlopen(url)

aiohttp.ClientSession().get(url)
```

The security concern is not the HTTP library itself.

The concern is:

```text
Untrusted URL
      ↓
HTTP Client
      ↓
Outbound Request
```

---

# 6. Example: Current Vulnerable Pattern

Consider:

```python
response = requests.post(
    f"{self.base_url}/customers",
    headers=headers,
    data=json.dumps(customer_data),
)
```

A SAST tool may report:

```text
Possible SSRF: tainted URL passed to HTTP client
```

The potential data flow is:

```text
self.base_url
     ↓
f"{self.base_url}/customers"
     ↓
requests.post()
```

The scanner cannot determine whether `self.base_url` is trusted.

Therefore, it reports the HTTP request as a potential SSRF sink.

---

# 7. Preferred Architecture

The preferred architecture is:

```text
Application Configuration
          |
          v
Trusted API Configuration
          |
          v
URL Validation
          |
          v
Allowed Host / Scheme Validation
          |
          v
HTTP Client
          |
          v
External API
```

Avoid:

```text
User Input
    |
    v
Dynamic URL
    |
    v
HTTP Client
```

---

# 8. Best Practice #1 — Prefer Fixed API Destinations

If the application communicates with known third-party APIs, the API destination should be defined by application configuration rather than user input.

### Preferred

```python
CUSTOMER_API_URL = "https://api.example.com"
```

or:

```python
CUSTOMER_API_URL = os.environ["CUSTOMER_API_URL"]
```

with validation.

### Avoid

```python
customer_url = request.json["customer_url"]

requests.post(customer_url)
```

---

# 9. Best Practice #2 — Use an Allowlist

For applications communicating with known services, use an explicit hostname allowlist.

Example:

```python
ALLOWED_HOSTS = {
    "api.example.com",
    "sandbox.example.com",
}
```

Validate the hostname before making the request.

```python
from urllib.parse import urlparse


def validate_api_url(url: str) -> str:
    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("Invalid API hostname")

    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Untrusted API host")

    return url.rstrip("/")
```

This is preferable to simply checking whether the URL starts with a particular string.

---

# 10. Do Not Use Weak Host Validation

Avoid:

```python
if "example.com" in url:
    ...
```

This can incorrectly allow:

```text
https://example.com.attacker.com
```

Also avoid:

```python
if url.startswith("https://example.com"):
    ...
```

because URL parsing and hostname validation should be performed structurally.

Prefer:

```python
parsed = urlparse(url)

if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("Untrusted host")
```

---

# 11. Best Practice #3 — Allow HTTPS Only

For production integrations:

```python
if parsed.scheme != "https":
    raise ValueError("Only HTTPS URLs are allowed")
```

Avoid allowing:

```text
http://
file://
ftp://
gopher://
```

unless there is a documented and justified business requirement.

For normal REST/API integrations, HTTPS should be mandatory.

---

# 12. Best Practice #4 — Prevent Internal IP Access

If the application accepts a user-controlled URL, hostname allowlisting is preferred.

Where arbitrary destinations are genuinely required, additional validation should prevent connections to private, loopback, link-local, multicast, and other reserved addresses.

Examples of sensitive destinations include:

```text
127.0.0.1
localhost
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
169.254.0.0/16
::1
fc00::/7
```

Cloud metadata services are particularly important to protect.

For example, cloud environments commonly expose metadata services through link-local addresses.

Do not rely only on checking the hostname before DNS resolution. DNS can resolve a permitted hostname to an unexpected internal address.

---

# 13. DNS Rebinding Consideration

A common mistake is:

```text
Validate hostname
       ↓
DNS resolution
       ↓
HTTP request
```

If the hostname can resolve differently between validation and connection, an attacker may attempt DNS rebinding.

For high-risk applications, SSRF protection should therefore consider:

```text
Hostname validation
        +
DNS resolution validation
        +
IP address validation
        +
Network egress controls
```

Where possible, use a trusted outbound proxy or network security layer.

---

# 14. Best Practice #5 — Do Not Accept Arbitrary URLs

If the application only supports a fixed set of integrations, do not expose a generic URL field.

Instead of:

```json
{
    "url": "https://anything.example.com"
}
```

prefer:

```json
{
    "provider": "salesforce"
}
```

Then the application determines the destination:

```python
API_URLS = {
    "salesforce": "https://api.salesforce.com",
    "learnupon": "https://api.learnupon.com",
}
```

This significantly reduces the SSRF attack surface.

---

# 15. Best Practice #6 — Use `json=` Instead of Manual JSON Serialization

Avoid:

```python
requests.post(
    url,
    data=json.dumps(payload),
)
```

Prefer:

```python
requests.post(
    url,
    json=payload,
)
```

Advantages include:

- Automatic JSON serialization.
- Cleaner code.
- Correct JSON content handling.
- Reduced unnecessary serialization logic.

---

# 16. Best Practice #7 — Always Configure a Timeout

Never rely on the default behavior of an HTTP client.

Avoid:

```python
requests.get(url)
```

Prefer:

```python
requests.get(
    url,
    timeout=30,
)
```

For more controlled behavior:

```python
requests.get(
    url,
    timeout=(5, 30),
)
```

Where:

```text
5 seconds  → connection timeout
30 seconds → read timeout
```

Timeouts help prevent:

- Hanging worker processes.
- Resource exhaustion.
- Connection pool exhaustion.
- Long-running requests.

---

# 17. Best Practice #8 — Handle Specific Exceptions

Avoid overly broad exception handling such as:

```python
except Exception as e:
    raise Exception(str(e))
```

Prefer specific exceptions:

```python
try:
    response = requests.post(
        url,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

except requests.exceptions.Timeout as exc:
    raise CustomerAPIError(
        "Customer API request timed out"
    ) from exc

except requests.exceptions.ConnectionError as exc:
    raise CustomerAPIError(
        "Unable to connect to customer API"
    ) from exc

except requests.exceptions.HTTPError as exc:
    raise CustomerAPIError(
        "Customer API returned an HTTP error"
    ) from exc
```

This provides clearer error handling and avoids unnecessarily exposing internal response details.

---

# 18. Best Practice #9 — Do Not Expose Sensitive Response Data

Avoid:

```python
raise Exception(f"API error: {response.text}")
```

because the response may contain:

- Credentials.
- Tokens.
- Personal information.
- Internal infrastructure information.
- Sensitive API details.

Prefer:

```python
raise CustomerAPIError(
    f"Customer API request failed with status {response.status_code}"
)
```

Log detailed information only when appropriate and ensure sensitive data is not included.

---

# 19. Best Practice #10 — Validate Redirects

An SSRF vulnerability can also occur through redirects.

For example:

```text
https://api.example.com
        ↓ 302
http://internal-service/
```

For sensitive integrations, consider disabling automatic redirects:

```python
response = requests.get(
    url,
    timeout=30,
    allow_redirects=False,
)
```

Or validate every redirect destination against the same security policy.

Do not assume that validating only the original URL is sufficient.

---

# 20. Recommended Secure HTTP Client

A reusable HTTP client can centralize the security controls.

Example:

```python
from urllib.parse import urlparse

import requests


ALLOWED_HOSTS = {
    "api.example.com",
    "sandbox.example.com",
}


class SecureAPIClient:

    def __init__(self, base_url: str):
        self.base_url = self._validate_base_url(base_url)

    @staticmethod
    def _validate_base_url(base_url: str) -> str:
        parsed = urlparse(base_url)

        if parsed.scheme != "https":
            raise ValueError("Only HTTPS URLs are allowed")

        if not parsed.hostname:
            raise ValueError("Invalid API hostname")

        if parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError("Untrusted API hostname")

        return base_url.rstrip("/")

    def post(self, path: str, payload: dict):
        url = f"{self.base_url}/{path.lstrip('/')}"

        return requests.post(
            url,
            json=payload,
            timeout=(5, 30),
        )
```

Usage:

```python
client = SecureAPIClient(settings.CUSTOMER_API_URL)

response = client.post(
    "/customers",
    customer_data,
)
```

---

# 21. Applying the Standard to the Original Code

### Before

```python
try:
    response = requests.post(
        f"{self.base_url}/customers",
        headers=headers,
        data=json.dumps(customer_data),
    )

    customer = self.handle_response(response)
    customer_id = customer["customers"]["id"]

    return customer_id

except requests.exceptions.HTTPError as e:
    raise Exception(
        f"Failed to create customer: {e.response.text}"
    )

except Exception as e:
    raise Exception(
        f"Unexpected error during customer creation: {str(e)}"
    )
```

### After

```python
try:
    response = requests.post(
        f"{self.base_url}/customers",
        headers=headers,
        json=customer_data,
        timeout=(5, 30),
    )

    customer = self.handle_response(response)
    customer_id = customer["customers"]["id"]

    return customer_id

except requests.exceptions.Timeout as exc:
    raise Exception(
        "Customer API request timed out"
    ) from exc

except requests.exceptions.ConnectionError as exc:
    raise Exception(
        "Unable to connect to customer API"
    ) from exc

except requests.exceptions.HTTPError as exc:
    raise Exception(
        f"Customer API returned HTTP {exc.response.status_code}"
    ) from exc

except requests.exceptions.RequestException as exc:
    raise Exception(
        "Customer API request failed"
    ) from exc
```

The important SSRF control is not merely changing `data=` to `json=`. The critical control is ensuring that `self.base_url` has already been validated and restricted to trusted destinations.

---

# 22. Recommended Configuration Pattern

Use environment-specific configuration:

```text
Development
    ↓
https://sandbox.example.com

UAT
    ↓
https://uat.example.com

Production
    ↓
https://api.example.com
```

Example:

```python
API_BASE_URLS = {
    "development": "https://sandbox.example.com",
    "uat": "https://uat.example.com",
    "production": "https://api.example.com",
}
```

Then:

```python
environment = settings.ENVIRONMENT

if environment not in API_BASE_URLS:
    raise ValueError("Invalid environment")

base_url = API_BASE_URLS[environment]
```

The application should not allow an end user to select an arbitrary URL.

---

# 23. SSRF Protection Layers

SSRF protection should not depend on a single control.

Recommended defense-in-depth:

```text
                Application
                     |
          +----------+----------+
          |                     |
      Input Control        URL Validation
          |                     |
          +----------+----------+
                     |
               Host Allowlist
                     |
              HTTPS Enforcement
                     |
              Redirect Control
                     |
             DNS/IP Validation
                     |
              Egress Firewall
                     |
              Outbound Proxy
                     |
              External API
```

---

# 24. Network-Level Protection

Application validation should be supported by infrastructure controls.

Recommended controls include:

- Restrict outbound network access.
- Use firewall/security-group rules.
- Block access to internal administrative services.
- Restrict access to cloud metadata endpoints.
- Use an outbound proxy where appropriate.
- Separate application and management networks.
- Apply least-privilege network rules.
- Monitor unexpected outbound connections.

Application-level validation alone should not be considered the only SSRF defense for high-risk systems.

---

# 25. SAST / Semgrep Considerations

Static analysis tools may report:

```text
Possible SSRF: tainted URL passed to HTTP client
```

This should be reviewed rather than immediately suppressed.

Review the complete data flow:

```text
Source
  ↓
Does the URL originate from user input?
  ↓
Is it configuration?
  ↓
Is the host allowlisted?
  ↓
Is HTTPS enforced?
  ↓
Can redirects change the destination?
  ↓
Can DNS resolve to internal IPs?
  ↓
HTTP Client
```

---

# 26. When a Semgrep Finding Can Be Considered Safe

A finding may be considered a false positive or mitigated when all relevant conditions are demonstrated.

Example:

```python
ALLOWED_HOSTS = {
    "api.example.com",
}

base_url = validate_api_url(
    settings.CUSTOMER_API_URL
)
```

If:

- URL is deployment-controlled.
- HTTPS is required.
- Hostname is explicitly allowlisted.
- User input cannot modify the destination.
- Redirect behavior is controlled.
- Network egress is appropriately restricted.

then the SSRF risk is substantially reduced.

The finding should still be documented according to the project's SAST exception process rather than silently ignored.

---

# 27. Do Not Use `# nosemgrep` Without Review

Avoid:

```python
# nosemgrep: possible-ssrf
requests.post(url)
```

unless the security review has established and documented the mitigation.

Recommended process:

```text
SAST Finding
     ↓
Developer Review
     ↓
Trace Data Flow
     ↓
Confirm Source
     ↓
Apply Security Control
     ↓
Retest
     ↓
Document Exception if Required
```

---

# 28. Secure HTTP Request Checklist

Before approving Python HTTP client code, verify:

| Check | Required |
|---|---|
| URL source is identified | Yes |
| User-controlled URL is avoided | Yes |
| Host allowlist is used where applicable | Yes |
| HTTPS is enforced | Yes |
| Internal/private destinations are blocked when arbitrary URLs are required | Yes |
| Redirect behavior is controlled | Recommended |
| DNS/IP validation is considered for high-risk flows | Recommended |
| HTTP timeout is configured | Yes |
| Specific exceptions are handled | Yes |
| Sensitive response data is not logged | Yes |
| API credentials are not hardcoded | Yes |
| Secrets are stored securely | Yes |
| Outbound network access is restricted | Recommended |
| SAST/SSRF findings are reviewed | Yes |

---

# 29. Code Review Red Flags

The following patterns should trigger security review:

### Dynamic URL

```python
requests.get(request.args["url"])
```

### Database-controlled URL

```python
url = integration.callback_url

requests.post(url)
```

### String concatenation

```python
url = base_url + user_path
requests.get(url)
```

### User-controlled redirect

```python
requests.get(user_supplied_url)
```

### Weak hostname validation

```python
if "trusted.com" in url:
    requests.get(url)
```

### Missing timeout

```python
requests.get(url)
```

### Disabled certificate verification

```python
requests.get(
    url,
    verify=False,
)
```

The last pattern is not itself SSRF, but it introduces a separate TLS/security weakness and should generally be avoided.

---

# 30. Recommended Standard for Python Projects

All Python projects using outbound HTTP communication should follow these rules:

### Mandatory

1. Use HTTPS for external APIs.
2. Do not accept arbitrary URLs from users unless there is a documented business requirement.
3. Validate externally configurable URLs.
4. Use hostname allowlists for known integrations.
5. Configure HTTP timeouts.
6. Do not disable TLS certificate verification.
7. Do not log credentials, tokens, or sensitive response bodies.
8. Review all SAST SSRF findings.
9. Keep API credentials in secure configuration/secrets management.
10. Apply least-privilege network access.

### Recommended

1. Centralize outbound HTTP communication.
2. Use a reusable secure HTTP client.
3. Control redirects.
4. Validate DNS/IP destinations for high-risk arbitrary URL use cases.
5. Apply network-level egress controls.
6. Monitor unexpected outbound traffic.
7. Add SSRF-specific security tests.

---

# 31. Testing Strategy

Security testing should cover at least the following scenarios.

### External trusted API

```text
https://api.example.com
```

Expected:

```text
Allowed
```

### HTTP instead of HTTPS

```text
http://api.example.com
```

Expected:

```text
Rejected
```

### Unknown domain

```text
https://attacker.example.com
```

Expected:

```text
Rejected
```

### Localhost

```text
http://127.0.0.1
```

Expected:

```text
Rejected
```

### Private network

```text
http://10.0.0.10
```

Expected:

```text
Rejected
```

### Link-local address

```text
http://169.254.x.x
```

Expected:

```text
Rejected
```

### Redirect to internal service

```text
Trusted API
    ↓ 302
Internal Service
```

Expected:

```text
Rejected or redirect controlled
```

---

# 32. Unit Test Example

```python
import pytest


def test_rejects_non_https():
    with pytest.raises(ValueError):
        validate_api_url(
            "http://api.example.com"
        )


def test_rejects_unknown_host():
    with pytest.raises(ValueError):
        validate_api_url(
            "https://attacker.example.com"
        )


def test_allows_trusted_host():
    result = validate_api_url(
        "https://api.example.com"
    )

    assert result == "https://api.example.com"
```

---

# 33. Architecture Recommendation

For applications with many third-party integrations, use a centralized integration layer:

```text
                    Application
                         |
                  Integration Layer
                         |
        +----------------+----------------+
        |                |                |
    Salesforce       LearnUpon        CallGear
        |                |                |
        +----------------+----------------+
                         |
                  Secure HTTP Client
                         |
             URL / Host Validation
                         |
                  Timeout / TLS
                         |
                 Network Controls
```

This avoids implementing security controls independently in every service.

---

# 34. Logging and Monitoring

Monitor outbound requests for unexpected behavior.

Useful events include:

- Requests to unapproved domains.
- Requests to private IP ranges.
- Requests to localhost.
- Requests to metadata endpoints.
- Excessive outbound requests.
- Unexpected HTTP methods.
- Repeated connection failures.

Do not log:

```text
Authorization headers
API keys
Access tokens
Passwords
Sensitive request bodies
Sensitive response bodies
```

---

# 35. Final Secure Coding Pattern

For known external APIs, the preferred pattern is:

```python
from urllib.parse import urlparse

import requests


ALLOWED_HOSTS = {
    "api.example.com",
    "sandbox.example.com",
}


def validate_base_url(base_url: str) -> str:
    parsed = urlparse(base_url)

    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("Invalid API URL")

    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Untrusted API host")

    return base_url.rstrip("/")


class CustomerClient:

    def __init__(self, base_url: str):
        self.base_url = validate_base_url(base_url)

    def create_customer(
        self,
        customer_data: dict,
        headers: dict,
    ) -> str:

        url = f"{self.base_url}/customers"

        response = requests.post(
            url,
            headers=headers,
            json=customer_data,
            timeout=(5, 30),
        )

        response.raise_for_status()

        customer = response.json()

        return customer["customers"]["id"]
```

---

# 36. Summary

The key SSRF principle is:

> **Never allow an untrusted source to directly determine where the server makes an HTTP request.**

For known third-party integrations, the preferred approach is:

```text
Configuration
     ↓
HTTPS
     ↓
Hostname Allowlist
     ↓
Validated Base URL
     ↓
Controlled HTTP Request
     ↓
Timeout
     ↓
Secure Error Handling
```

For high-risk applications, add:

```text
DNS/IP Validation
        +
Redirect Validation
        +
Network Egress Controls
        +
Outbound Proxy
        +
Monitoring
```

The Semgrep finding **“Possible SSRF: tainted URL passed to HTTP client”** should therefore be treated as a security review item. The correct remediation is to establish and enforce the trust boundary around `base_url`, rather than simply suppressing the SAST finding.