# Python & Backend Security Best Practices

A practical reference for securing Python backend applications (FastAPI, Django, Flask) across the full stack — code, dependencies, infrastructure, and CI/CD.

---

## 1. Secrets Management

**Never hardcode passwords, API keys, or secrets in source code.**

```python
# ❌ BAD
API_KEY = "sk-live-abc123xyz"
DB_PASSWORD = "SuperSecret123"

# ✅ GOOD — load from environment
import os
from functools import lru_cache

API_KEY = os.environ["API_KEY"]  # raises if missing — fail fast
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```

- Store secrets in environment variables, `.env` files (excluded via `.gitignore`), or a dedicated secrets manager.
- Use **AWS Secrets Manager**, **AWS Parameter Store (SSM)**, **HashiCorp Vault**, **Azure Key Vault**, or **GCP Secret Manager** for production.
- Rotate secrets on a schedule and immediately after any suspected exposure.
- Add `git-secrets` or `detect-secrets` as a pre-commit hook to catch accidental commits.
- Never log secrets, and scrub them from error tracebacks (e.g., Sentry `before_send` hooks).

```python
# Example: pulling a secret from AWS Secrets Manager
import boto3
import json

def get_secret(secret_name: str, region: str = "us-east-1") -> dict:
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
```

---

## 2. Authentication & Authorization

- Use **JWT**, **OAuth2**, or **SSO (SAML/OIDC)** for authentication — avoid rolling your own auth scheme.
- Enforce **Role-Based Access Control (RBAC)** (or ABAC for finer granularity) on every protected endpoint.
- Require **MFA** for administrative and privileged accounts.
- Enforce strong password policies (length, complexity, breach-list checks via Have I Been Pwned API).
- Hash passwords with **bcrypt** or **Argon2** — never MD5/SHA1/plain SHA256.

```python
# Password hashing with Argon2 (preferred) via passlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

```python
# JWT issuing/validation with short-lived access tokens + refresh tokens
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"

def create_access_token(subject: str, expires_minutes: int = 15) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire, "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

- Keep access tokens short-lived (e.g., 15 min); use refresh tokens with rotation and revocation lists.
- Store JWTs in `HttpOnly`, `Secure`, `SameSite=Strict` cookies rather than `localStorage` where possible, to reduce XSS token theft risk.

---

## 3. Input Validation

Validate and sanitize **all** user input — query params, path params, headers, JSON bodies, file uploads.

- **FastAPI** → Pydantic models (built-in).
- **Django** → Forms / DRF Serializers.
- **Flask** → Marshmallow or Pydantic.

```python
# FastAPI + Pydantic
from pydantic import BaseModel, EmailStr, Field, constr

class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    age: int = Field(gt=0, lt=150)
```

Guard specifically against:

| Threat | Mitigation |
|---|---|
| SQL Injection | Parameterized queries / ORM only — never string-format SQL |
| XSS | Auto-escaping templates (Jinja2 autoescape on), sanitize HTML with `bleach`, set `Content-Security-Policy` |
| SSRF | Allow-list outbound destinations, block internal IP ranges (169.254.x.x, 10.x, 127.x) before making server-side requests |
| Command Injection | Never build shell strings from user input; use `subprocess.run([...], shell=False)` with a list of args |
| Path Traversal | Resolve and validate paths against an allowed base directory before file access |

```python
# SSRF-safe outbound request check
import ipaddress
from urllib.parse import urlparse
import socket

def is_safe_url(url: str) -> bool:
    host = urlparse(url).hostname
    if not host:
        return False
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    return not (ip.is_private or ip.is_loopback or ip.is_link_local)
```

---

## 4. Database Security

- Use **ORM frameworks** (SQLAlchemy, Django ORM, Tortoise) — they parameterize queries by default.
- If raw SQL is unavoidable, always use parameterized queries — never f-strings or `%` formatting.

```python
# ❌ BAD — SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# ✅ GOOD — parameterized
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# ✅ GOOD — SQLAlchemy ORM
user = session.query(User).filter(User.email == email).first()
```

- Encrypt sensitive columns at rest (e.g., `pgcrypto`, application-level field encryption via `cryptography.fernet`).
- Apply **least privilege**: app DB user should have only the CRUD permissions it needs — no `DROP`, `ALTER`, or superuser rights.
- Use separate DB credentials per environment/service; never share a single admin credential across services.
- Enable connection encryption (`sslmode=require` for Postgres, `ssl=true` for MySQL).

---

## 5. API Security

- Enforce **HTTPS / TLS 1.2+** everywhere; redirect HTTP → HTTPS; enable HSTS.
- Implement **rate limiting** per IP/user/API key to blunt brute-force and abuse.
- Protect API documentation (`/docs`, `/redoc`, `/swagger`) in production — disable or put behind auth.
- Validate authentication **and** authorization on every request — don't rely on client-side checks or "security by obscure URL."
- Set strict CORS origins (never `allow_origins=["*"]` with credentials enabled).
- Return generic error messages externally; log detailed errors internally only.

```python
# FastAPI: disable docs in production
from fastapi import FastAPI

app = FastAPI(
    docs_url=None if os.environ.get("ENV") == "production" else "/docs",
    redoc_url=None if os.environ.get("ENV") == "production" else "/redoc",
)
```

---

## 6. Secure Coding Practices

| Avoid | Why | Prefer |
|---|---|---|
| `eval()` | Executes arbitrary code | Safe parsing (`ast.literal_eval` for literals) |
| `exec()` | Executes arbitrary code | Explicit logic / dispatch tables |
| `pickle.loads()` on untrusted data | Arbitrary code execution on deserialization | `json.loads()`, or `pickle` only for fully trusted internal data |
| `os.system()` | Shell injection risk | `subprocess.run([...], shell=False)` |
| Raw SQL string concatenation | SQL injection | ORM queries / parameterized SQL |
| `yaml.load()` | Can execute arbitrary tags | `yaml.safe_load()` |

```python
# subprocess done safely
import subprocess
subprocess.run(["git", "clone", repo_url], check=True, shell=False)
```

---

## 7. Dependency Security

Keep dependencies patched and scan continuously:

```bash
pip-audit                  # scans installed packages for known CVEs
safety check                # vulnerability scanning against a curated DB
bandit -r ./app             # static analysis for common Python security issues
semgrep --config auto ./app # broader static analysis / custom rule support
```

- Pin dependency versions (`requirements.txt` + hashes, or `poetry.lock` / `pip-compile`).
- Enable **Dependabot** or **Renovate** for automated PRs on vulnerable/outdated packages.
- Avoid unmaintained or low-adoption packages for security-sensitive functionality.

---

## 8. Logging & Monitoring

- Log security-relevant events: logins, failed logins, permission denials, password resets, admin actions.
- Monitor for spikes in auth failures (possible brute force) and unusual access patterns.
- **Never log** passwords, tokens, API keys, session IDs, or full credit card numbers.

```python
import logging

logger = logging.getLogger("security")

def log_login_attempt(username: str, success: bool, ip: str):
    logger.info("login_attempt", extra={"username": username, "success": success, "ip": ip})
    # Never do: logger.info(f"password={password}")
```

- Centralize logs (ELK, CloudWatch, Datadog) and set alerts on anomalies.
- Redact sensitive fields at the logging-handler level as a safety net, not just at call sites.

---

## 9. Data Protection

- Encrypt sensitive data **at rest** (disk/DB-level encryption, e.g., AWS RDS encryption, EBS encryption) and **in transit** (TLS everywhere, including internal service-to-service calls).
- Use a managed key management service (AWS KMS, GCP KMS, Vault Transit) rather than hand-rolled crypto.
- Encrypt backups; restrict access to backup storage with least-privilege IAM policies.
- Apply data minimization: only collect/store what's needed, and set retention/deletion policies for PII.

---

## 10. Container & Infrastructure Security

```dockerfile
# Run as non-root, minimal base image
FROM python:3.12-slim AS base

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
RUN pip install --no-cache-dir -r requirements.txt

USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Use minimal base images (`slim`, `distroless`, `alpine` where compatible) to shrink attack surface.
- Restrict container network access (network policies, security groups) — default deny, allow only required egress/ingress.
- Scan images with `trivy`, `grype`, or `docker scout` in CI.
- Put a **WAF** in front of public endpoints, enable infrastructure monitoring/alerting, and automate backups with tested restore procedures.
- Run containers with read-only root filesystems where possible; drop unnecessary Linux capabilities.

---

## 11. CI/CD Security

- Require code review (at least one approver) before merge, with security-focused checks for auth/data-handling changes.
- Run automated security scans in the pipeline: `bandit`, `semgrep`, `pip-audit`/`safety`, container image scans (`trivy`).
- Scan Infrastructure-as-Code (Terraform/CloudFormation) with `checkov` or `tfsec`.
- Store CI/CD secrets in the platform's native secret store (GitHub Actions Secrets, GitLab CI/CD Variables) — never in the pipeline YAML itself.
- Use short-lived, scoped credentials for deployment (OIDC federation to cloud providers instead of long-lived static keys, where supported).

---

## Framework-Specific Notes

### FastAPI
- Use Pydantic models for all request/response validation.
- Secure or disable Swagger/OpenAPI docs in production (see snippet above).
- Apply rate limiting via `slowapi` or an API gateway.
- Use `Depends()` for auth checks so they're enforced consistently across routes.

### Django
- Set `DEBUG = False` in production — `DEBUG = True` leaks stack traces and settings.
- Keep Django's CSRF protection enabled (`django.middleware.csrf.CsrfViewMiddleware`); don't blanket-exempt views.
- Use `django.middleware.security.SecurityMiddleware` and set `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`.
- Keep `ALLOWED_HOSTS` restricted to actual domains — never `["*"]` in production.

### Flask
- Ensure `app.run(debug=False)` (or unset) in production — debug mode exposes the Werkzeug interactive debugger, which allows RCE if reachable.
- Use **Flask-Talisman** for security headers (HSTS, CSP, X-Frame-Options, etc.).
- Use **Flask-Limiter** for rate limiting.
- Set `SESSION_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = "Lax"`.

---

## Security Checklist for Deployment

- [ ] **Secrets Management** — no hardcoded secrets; vault/env-based; rotation policy in place
- [ ] **Authentication & RBAC** — JWT/OAuth2/SSO, MFA for admins, role checks on every endpoint
- [ ] **Input Validation** — Pydantic/Serializers/Marshmallow on all inputs; SQLi/XSS/SSRF/command-injection mitigations verified
- [ ] **HTTPS Enforcement** — TLS 1.2+, HSTS, HTTP→HTTPS redirect
- [ ] **Database Security** — ORM/parameterized queries, least-privilege DB user, encryption at rest
- [ ] **Dependency Scanning** — `pip-audit`/`safety`/`bandit`/`semgrep` run in CI, no known critical CVEs open
- [ ] **Secure Logging** — audit events captured, no secrets/PII in logs, centralized + alerting
- [ ] **Data Encryption** — at rest and in transit, managed KMS, encrypted backups
- [ ] **Container Hardening** — non-root user, minimal image, image scanning, restricted network
- [ ] **CI/CD Security Scanning** — SAST/dependency/container scans gating merges, secrets in native secret store
- [ ] **Monitoring & Alerting** — auth failure spikes, anomaly detection, WAF, on-call alerting configured

---

*Treat this as a living checklist — revisit it each release cycle and after any incident or major dependency upgrade.*
