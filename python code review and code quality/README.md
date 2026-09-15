# Python Code Review & Static Analysis Standard

**Document Type:** Engineering / Development Standard  
**Technology:** Python, Django, FastAPI  
**Applicable To:** Backend APIs, Microservices, Web Applications, Automation Services  
**Primary Goals:** Code Quality, Security, Maintainability, Reliability, Testing and Technical Debt Reduction

---

# 1. Purpose

This document defines the standard approach for reviewing Python code using automated static analysis, security scanning, testing, dependency scanning, dead-code detection and manual code review.

The objective is to ensure that Python applications meet consistent standards for:

- Code quality
- Readability
- Maintainability
- Security
- Performance
- Architecture
- API design
- Database practices
- Testing
- Error handling
- Logging and observability
- Dependency security
- Technical debt reduction

Automated tools support the review process but **do not replace manual code review**.

---

# 2. Scope

This standard applies to:

- Django applications
- Django REST Framework applications
- FastAPI applications
- Python REST APIs
- Python microservices
- Background workers
- Celery applications
- Automation services
- CLI applications
- Python libraries
- Data-processing services

The standard should be applied to:

1. New development
2. Bug fixes
3. Refactoring
4. Security fixes
5. Dependency upgrades
6. Production releases
7. Pull requests

---

# 3. Code Review Strategy

The code-review process consists of several layers.

```text
Developer
    │
    ▼
Pre-Commit Checks
    │
    ▼
Ruff
    │
    ▼
Pylint
    │
    ▼
Pytest
    │
    ├───────────────┐
    ▼               ▼
  MyPy            Security
                    │
             ┌──────┴──────┐
             ▼             ▼
          Bandit         Semgrep
             │             │
             └──────┬──────┘
                    ▼
             Dependency Scan
                    │
                    ▼
             Secret Scanning
                    │
                    ▼
              Pull Request
                    │
                    ▼
          Manual Code Review
                    │
                    ▼
         Architecture Review
                    │
                    ▼
                  Merge
```

Dead-code analysis is handled separately:

```text
Vulture / Skylos
       │
       ▼
Code Health Report
       │
       ▼
Manual Validation
       │
       ▼
Refactor / Remove
```

---

# 4. Toolset

The following tools are recommended as the standard Python code-review toolset.

| Tool | Category | Primary Responsibility | Recommended Usage |
|---|---|---|---|
| Ruff | Linting / Formatting | Fast Python quality checks | Local + CI |
| Pylint | Static Analysis | Deep Python code analysis | Local + CI |
| Bandit | Security | Python security checks | CI |
| Semgrep | SAST | Application security/custom rules | CI |
| Vulture | Dead Code | Unused code detection | Periodic |
| Skylos | Code Health | Dead code/maintainability | Periodic |
| MyPy | Type Checking | Static type validation | Local + CI |
| Pytest | Testing | Unit/integration testing | Local + CI |
| pip-audit | Dependency Security | Vulnerable dependency detection | CI |
| Secret Scanning | Security | Credential/secret detection | CI |
| pre-commit | Developer Automation | Local automated checks | Local |

---

# 5. Ruff

## 5.1 Purpose

Ruff is the primary fast Python linter and formatter.

It should be used as the **first-line developer check**.

## 5.2 Use Cases

Ruff can detect:

- Unused imports
- Undefined names
- Import issues
- Syntax-related problems
- Code-style violations
- Common programming errors
- Formatting issues
- Selected complexity problems
- Modern Python syntax opportunities

## 5.3 Local Commands

Check code:

```bash
ruff check .
```

Automatically fix supported issues:

```bash
ruff check . --fix
```

Format:

```bash
ruff format .
```

Check formatting without changing files:

```bash
ruff format --check .
```

## 5.4 CI Policy

Ruff should be a **blocking Pull Request check**.

---

# 6. Pylint

## 6.1 Purpose

Pylint provides deeper Python static analysis and focuses on code quality, maintainability and design.

## 6.2 Use Cases

Pylint can identify:

- Poor naming
- Unused variables
- Import problems
- Complex functions
- Excessive arguments
- Excessive branching
- Poor class design
- Broad exception handling
- Potential programming errors
- Maintainability issues
- Framework-related problems

For Django:

```bash
pylint --load-plugins=pylint_django .
```

## 6.3 CI Policy

Pylint should be a **blocking PR check** for production Python projects.

A project-specific configuration should be maintained instead of disabling large groups of rules globally.

---

# 7. Bandit

## 7.1 Purpose

Bandit performs Python-specific security analysis.

## 7.2 Use Cases

Bandit should identify potentially dangerous patterns involving:

- `eval()`
- `exec()`
- `subprocess`
- `shell=True`
- Unsafe deserialization
- Weak cryptography
- Insecure random generation
- Unsafe temporary files
- Potential hardcoded credentials
- Unsafe YAML handling
- SSL/TLS configuration

## 7.3 Local Command

```bash
bandit -r .
```

Example:

```bash
bandit -r . \
  -x .venv,venv,tests,migrations \
  -lll
```

Exclusions must be reviewed carefully.

## 7.4 CI Policy

High-confidence security findings should block the Pull Request.

---

# 8. Semgrep – SAST

## 8.1 Purpose

Semgrep provides Static Application Security Testing (SAST) and custom code-analysis rules.

It should be used as the primary application-level security scanning layer.

## 8.2 Use Cases

Semgrep can identify:

- SQL Injection
- Command Injection
- XSS
- Path Traversal
- Insecure Deserialization
- Authentication weaknesses
- Authorization issues
- Hardcoded secrets
- Unsafe framework usage
- Insecure API patterns
- Dangerous data flows

## 8.3 Custom Architecture Rules

Semgrep can also enforce internal architecture.

For example:

```text
API
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Database
```

A custom rule can identify situations where API code directly accesses database operations.

This is especially useful for Django/FastAPI microservice architectures.

## 8.4 Command

```bash
semgrep scan --config auto .
```

For project-specific rules:

```bash
semgrep scan --config .semgrep/ .
```

## 8.5 CI Policy

Confirmed High/Critical security findings should block the Pull Request.

---

# 9. Vulture – Dead Code Detection

## 9.1 Purpose

Vulture identifies potentially unused Python code.

## 9.2 Use Cases

It can identify:

- Unused functions
- Unused classes
- Unused variables
- Unused imports
- Unused methods
- Unused attributes

Command:

```bash
vulture .
```

## 9.3 Important Consideration

Vulture findings must be manually validated before deletion.

Django and other frameworks use dynamic behavior.

Potential examples include:

- Django models
- URL patterns
- Signals
- Celery tasks
- Management commands
- Admin classes
- Serializer methods
- Plugin registrations

## 9.4 CI Policy

Vulture should initially be **non-blocking**.

It should be used for periodic technical-debt analysis.

---

# 10. Skylos

## 10.1 Purpose

Skylos can provide additional code-health and dead-code analysis.

It is useful for:

- Large repositories
- Legacy applications
- Refactoring
- Technical-debt reduction
- Code-health monitoring

## 10.2 Recommended Usage

Skylos should initially be used as a reporting tool.

Avoid making both Vulture and Skylos mandatory blocking checks until the team has evaluated:

- Finding overlap
- False positives
- Framework compatibility
- Developer impact

The exact Skylos command/options should be validated against the version adopted by the project.

---

# 11. MyPy – Type Checking

## 11.1 Purpose

MyPy provides static type checking.

It identifies type-related issues that linting tools may not detect.

Example:

```python
def calculate_total(amount: int) -> int:
    return amount + "100"
```

## 11.2 Use Cases

MyPy is especially useful for:

- Large applications
- Microservices
- Shared libraries
- Complex business logic
- Financial applications
- API contracts

Command:

```bash
mypy .
```

## 11.3 Adoption Strategy

For an existing application, introduce type checking gradually.

Recommended progression:

```text
Existing code
     │
     ▼
Type hints for new code
     │
     ▼
Critical modules
     │
     ▼
Service layer
     │
     ▼
Full project
     │
     ▼
Strict checking
```

---

# 12. Pytest – Automated Testing

Static analysis cannot prove application behavior.

Automated tests are therefore mandatory for production code.

Run:

```bash
pytest
```

With coverage:

```bash
pytest \
  --cov=. \
  --cov-report=term-missing
```

Recommended test categories:

- Unit tests
- Integration tests
- API tests
- Database tests
- Authentication tests
- Authorization tests
- Regression tests
- Critical business-logic tests

---

# 13. pip-audit – Dependency Security

Python dependencies can contain known vulnerabilities.

Use:

```bash
pip-audit -r requirements.txt
```

This should be included in CI/CD.

Dependency upgrades should follow a controlled process.

---

# 14. Secret Scanning

Secrets must never be committed to source control.

Examples include:

```text
AWS Access Keys
Database Passwords
API Keys
JWT Secrets
Private Keys
OAuth Secrets
Cloud Credentials
Third-party API Tokens
```

Recommended options:

- GitHub Secret Scanning
- detect-secrets
- Semgrep secret rules

Example:

```bash
detect-secrets scan
```

Secret scanning should be a **blocking security check** when a confirmed secret is detected.

---

# 15. Pre-Commit

Pre-commit provides early feedback before code is pushed.

Recommended flow:

```text
git commit
    │
    ▼
pre-commit
    │
    ├── Ruff
    ├── Ruff format
    ├── Pylint
    ├── Bandit
    └── Secret scanning
    │
    ▼
Commit
```

This reduces unnecessary CI failures.

---

# 16. Manual Code Review

Automated tools do not replace manual review.

Reviewers should check the following.

## 16.1 Architecture

- Does the implementation follow the approved architecture?
- Is business logic in the correct layer?
- Are responsibilities separated?
- Is unnecessary coupling introduced?
- Are existing services/utilities reused?
- Does the change introduce architectural debt?

## 16.2 API

Review:

- HTTP methods
- Status codes
- Request validation
- Response schemas
- Authentication
- Authorization
- Pagination
- Filtering
- Rate limiting where required
- Sensitive data exposure

## 16.3 Database

Review:

- SQL injection
- Parameterized queries
- Dynamic SQL
- Indexes
- N+1 queries
- Transactions
- Constraints
- Relationships
- Migrations
- Query performance

### Dynamic SQL

Parameter values should use parameterized queries.

Dynamic table, column or field identifiers require a different approach because they cannot normally be passed as ordinary query parameters. They must be validated against an approved allowlist or safely constructed through framework/database mechanisms.

## 16.4 Security

Review:

- Authentication
- Authorization
- Input validation
- Output handling
- Secrets
- File uploads
- Path traversal
- SQL injection
- Command injection
- SSRF
- CORS
- CSRF
- Session management
- Encryption
- Sensitive logging

## 16.5 Error Handling

Avoid:

```python
try:
    ...
except Exception:
    pass
```

Review:

- Appropriate exception types
- Meaningful handling
- No swallowed exceptions
- Correct API responses
- No sensitive error information
- Proper logging

## 16.6 Logging

Logs should:

- Provide useful diagnostic information
- Support correlation/request tracking where appropriate
- Never expose passwords
- Never expose access tokens
- Avoid unnecessary sensitive/personal information

---

# 17. Performance Review

## 17.1 Database

Review:

- N+1 queries
- Missing indexes
- Large result sets
- Unnecessary joins
- Repeated queries
- Long-running transactions
- Connection management

## 17.2 API

Review:

- Pagination
- Caching
- Response size
- External API calls
- Timeouts
- Retry strategy
- Connection pooling

## 17.3 Background Jobs

Review:

- Retry strategy
- Idempotency
- Task timeout
- Queue configuration
- Failure handling
- Duplicate processing

---

# 18. Code Complexity

Reviewers should avoid unnecessarily complex code.

Watch for:

- Excessive nesting
- Too many branches
- Too many parameters
- Large functions
- Multiple responsibilities
- Deep conditional logic

Prefer:

```text
Large Function
      │
      ▼
Extract Responsibilities
      │
      ▼
Focused Functions
```

Complexity warnings should be evaluated based on business requirements rather than blindly targeting a numerical score.

---

# 19. Tool Responsibility Matrix

| Review Area | Ruff | Pylint | Bandit | Semgrep | Vulture | Skylos | MyPy |
|---|---:|---:|---:|---:|---:|---:|---:|
| Formatting | ✅ | | | | | | |
| Basic linting | ✅ | ✅ | | | | | |
| Code quality | ✅ | ✅ | | | | ✅ | |
| Design analysis | | ✅ | | | | ✅ | |
| Security | | | ✅ | ✅ | | | |
| SAST | | | Limited | ✅ | | | |
| Dead code | Limited | Limited | | | ✅ | ✅ | |
| Complexity | Limited | ✅ | | | | ✅ | |
| Type safety | | | | | | | ✅ |
| Custom security rules | | | | ✅ | | | |

---

# 20. Quality Gate Policy

## 20.1 Pull Request – Blocking

The following should normally be blocking:

```text
Ruff
Pylint
Bandit
Semgrep
Pytest
pip-audit
Secret Scanning
```

MyPy should become blocking after the project reaches sufficient type coverage.

## 20.2 Periodic / Reporting

```text
Vulture
Skylos
```

These should initially generate reports rather than block development.

---

# 21. Severity Policy

| Severity | Action |
|---|---|
| Critical | Must fix before merge |
| High | Must fix before merge |
| Medium | Fix before merge or documented exception |
| Low | Review and fix where practical |
| Informational | Developer/reviewer decision |

Security exceptions must be documented.

Example:

```text
Finding:
Semgrep SQL injection rule

Decision:
False positive

Reason:
Query uses an approved parameterized query mechanism.

Reviewed By:
Technical Lead

Date:
YYYY-MM-DD
```

---

# 22. Local Developer Workflow

Developers should run the following before creating a Pull Request.

### Code Quality

```bash
ruff check .
ruff format --check .
pylint --load-plugins=pylint_django .
```

### Security

```bash
bandit -r .
semgrep scan --config auto .
```

### Testing

```bash
pytest
```

### Type Checking

```bash
mypy .
```

### Dependency Security

```bash
pip-audit -r requirements.txt
```

### Dead Code – Periodic

```bash
vulture .
```

Skylos can also be run periodically according to the project's selected version/configuration.

---

# 23. GitHub Actions CI/CD

The GitHub Actions pipeline should reproduce the important local checks.

Recommended structure:

```text
.github/
└── workflows/
    ├── code-quality.yml
    ├── security.yml
    ├── tests.yml
    ├── code-health.yml
    └── secret-scan.yml
```

---

# 24. Code Quality Workflow

File:

```text
.github/workflows/code-quality.yml
```

```yaml
name: Python Code Quality

on:
  push:
    branches:
      - main
      - develop
      - staging

  pull_request:
    branches:
      - main
      - develop
      - staging

permissions:
  contents: read

jobs:
  ruff:
    name: Ruff
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Ruff
        run: pip install ruff

      - name: Ruff lint
        run: ruff check .

      - name: Ruff format check
        run: ruff format --check .

  pylint:
    name: Pylint
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pylint pylint-django

      - name: Run Pylint
        run: |
          pylint --load-plugins=pylint_django .
```

---

# 25. Security Workflow

File:

```text
.github/workflows/security.yml
```

```yaml
name: Python Security

on:
  push:
    branches:
      - main
      - develop
      - staging

  pull_request:
    branches:
      - main
      - develop
      - staging

permissions:
  contents: read

jobs:
  bandit:
    name: Bandit Security Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Bandit
        run: pip install bandit

      - name: Run Bandit
        run: |
          bandit -r . \
            -x .venv,venv,tests,migrations \
            -lll

  semgrep:
    name: Semgrep SAST
    runs-on: ubuntu-latest

    container:
      image: semgrep/semgrep

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run Semgrep
        run: |
          semgrep scan \
            --config auto \
            --error

  dependency-scan:
    name: Dependency Security
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install pip-audit
        run: pip install pip-audit

      - name: Audit dependencies
        run: |
          pip-audit -r requirements.txt
```

---

# 26. Test and Type-Check Workflow

File:

```text
.github/workflows/tests.yml
```

```yaml
name: Python Tests

on:
  pull_request:
    branches:
      - main
      - develop
      - staging

permissions:
  contents: read

jobs:
  test:
    name: Pytest
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest \
            --cov=. \
            --cov-report=term-missing \
            --cov-report=xml

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

  mypy:
    name: MyPy
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install mypy

      - name: Run MyPy
        run: |
          mypy .
```

---

# 27. Code Health Workflow

File:

```text
.github/workflows/code-health.yml
```

This workflow is intended for periodic analysis rather than PR blocking.

```yaml
name: Python Code Health

on:
  schedule:
    - cron: "0 3 * * 1"

  workflow_dispatch:

permissions:
  contents: read

jobs:
  vulture:
    name: Vulture Dead Code
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Vulture
        run: pip install vulture

      - name: Run Vulture
        continue-on-error: true
        run: |
          vulture . \
            --exclude .venv \
            --exclude venv \
            --exclude migrations

  skylos:
    name: Skylos Code Health
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Skylos
        run: pip install skylos

      - name: Run Skylos
        continue-on-error: true
        run: |
          skylos .
```

**Note:** Skylos command-line options should be verified against the version adopted by the project.

---

# 28. Secret Scanning Workflow

File:

```text
.github/workflows/secret-scan.yml
```

```yaml
name: Secret Scanning

on:
  push:
    branches:
      - main
      - develop
      - staging

  pull_request:
    branches:
      - main
      - develop
      - staging

permissions:
  contents: read

jobs:
  detect-secrets:
    name: Detect Secrets
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install detect-secrets
        run: pip install detect-secrets

      - name: Scan repository
        run: |
          detect-secrets scan \
            --exclude-files '.*\.lock$' \
            --exclude-files '.*\.min\.js$'
```

---

# 29. Recommended Repository Structure

```text
project/
│
├── .github/
│   └── workflows/
│       ├── code-quality.yml
│       ├── security.yml
│       ├── tests.yml
│       ├── code-health.yml
│       └── secret-scan.yml
│
├── .semgrep/
│   └── rules/
│       ├── django.yml
│       ├── fastapi.yml
│       └── architecture.yml
│
├── .pre-commit-config.yaml
├── pyproject.toml
├── .pylintrc
├── requirements.txt
└── ...
```

---

# 30. Recommended Pull Request Process

```text
Developer Creates Branch
        │
        ▼
Implement Feature
        │
        ▼
Run Local Checks
        │
        ├── Ruff
        ├── Pylint
        ├── Pytest
        ├── Bandit
        └── Semgrep
        │
        ▼
Create Pull Request
        │
        ▼
GitHub Actions
        │
        ├── Code Quality
        ├── Security
        ├── Tests
        ├── Dependency Scan
        └── Secret Scan
        │
        ▼
All Gates Passed
        │
        ▼
Manual Code Review
        │
        ├── Business Logic
        ├── Architecture
        ├── Database
        ├── Security
        ├── Performance
        └── Maintainability
        │
        ▼
Approval
        │
        ▼
Merge
```

---

# 31. Code Review Checklist

## Code Quality

- [ ] Ruff checks passed
- [ ] Pylint checks passed
- [ ] Code follows project standards
- [ ] Naming is clear
- [ ] Functions/classes have appropriate responsibilities
- [ ] No unnecessary duplication
- [ ] Complexity is reasonable

## Security

- [ ] Bandit passed
- [ ] Semgrep passed
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Authorization verified
- [ ] Sensitive data protected
- [ ] SQL queries are safe
- [ ] File handling is safe
- [ ] External requests have appropriate timeout/retry controls

## Database

- [ ] Queries are optimized
- [ ] No obvious N+1 queries
- [ ] Required indexes exist
- [ ] Transactions are appropriate
- [ ] Migrations are correct
- [ ] Dynamic identifiers are safely handled
- [ ] Parameterized queries are used

## API

- [ ] Correct HTTP methods
- [ ] Correct status codes
- [ ] Request validation
- [ ] Response validation
- [ ] Authentication
- [ ] Authorization
- [ ] Pagination where required
- [ ] Error responses are consistent
- [ ] Sensitive fields are not exposed

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added where required
- [ ] Regression tests added where applicable
- [ ] Critical business logic covered
- [ ] All tests pass

## Deployment / Operations

- [ ] Configuration is externalized
- [ ] Secrets are not committed
- [ ] Logging is appropriate
- [ ] Monitoring/observability considered
- [ ] Database migration considered
- [ ] Backward compatibility considered
- [ ] Rollback impact considered

---

# 32. Quality Gate Summary

| Check | Local | PR | Release | Periodic |
|---|---:|---:|---:|---:|
| Ruff | ✅ | ✅ Block | ✅ | |
| Pylint | ✅ | ✅ Block | ✅ | |
| Bandit | ✅ | ✅ Block | ✅ | |
| Semgrep | Optional | ✅ Block | ✅ | |
| Pytest | ✅ | ✅ Block | ✅ | |
| MyPy | ✅ | Recommended* | ✅ | |
| pip-audit | Optional | ✅ Block | ✅ | |
| Secret Scanning | Optional | ✅ Block | ✅ | |
| Vulture | Optional | | | ✅ |
| Skylos | Optional | | | ✅ |

`*` MyPy should become a mandatory blocking check after the project has established sufficient type coverage.

---

# 33. Recommended Overall Architecture

```text
                         PYTHON PROJECT
                               │
              ┌────────────────┼────────────────┐
              │                │                │
           QUALITY          SECURITY          TESTING
              │                │                │
         ┌────┴────┐      ┌────┴────┐          │
         │         │      │         │          │
       Ruff     Pylint  Bandit   Semgrep     Pytest
         │         │      │         │          │
         └────┬────┘      └────┬────┘          │
              │                │               │
              └────────┬───────┴───────────────┘
                       │
                   MyPy
                       │
                pip-audit
                       │
               Secret Scanning
                       │
                       ▼
                 Pull Request
                       │
                       ▼
               Manual Code Review
                       │
                       ▼
              Architecture Review
                       │
                       ▼
                     MERGE
                       │
                       ▼
              Periodic Code Health
                       │
                 ┌─────┴─────┐
                 │           │
              Vulture      Skylos
```

---

# 34. Tool Selection Principle

The objective is **not** to run as many tools as possible.

Each tool should have a clearly defined responsibility.

```text
Ruff
→ Fast linting and formatting

Pylint
→ Deep Python code-quality analysis

Bandit
→ Python-specific security

Semgrep
→ Application SAST and custom security/architecture rules

MyPy
→ Type safety

Pytest
→ Functional correctness

pip-audit
→ Dependency vulnerabilities

Secret Scanning
→ Credential protection

Vulture
→ Dead-code detection

Skylos
→ Code-health analysis
```

Avoid duplicating tools without a measurable benefit.

---

# 35. Final Recommended Standard

For production Python applications, the recommended baseline is:

### Mandatory PR Gates

```text
1. Ruff
2. Pylint
3. Bandit
4. Semgrep
5. Pytest
6. pip-audit
7. Secret Scanning
```

### Recommended

```text
8. MyPy
9. pre-commit
```

### Periodic

```text
10. Vulture
11. Skylos
```

---

# 36. Engineering Principle

The purpose of this standard is not to achieve a perfect static-analysis score.

The objective is to ensure that every change is:

> **Readable, maintainable, secure, tested, performant, architecturally consistent and production-ready.**

Automated tools identify potential issues. Developers and technical reviewers remain responsible for evaluating findings and making the final engineering decision.

---

# 37. Ownership

### Developer

Responsible for:

- Running local checks
- Fixing findings
- Adding tests
- Following architecture
- Addressing security issues

### Reviewer

Responsible for:

- Reviewing implementation
- Validating business logic
- Checking architecture
- Reviewing security and performance
- Confirming appropriate test coverage

### Technical Lead / Architect

Responsible for:

- Defining coding standards
- Maintaining static-analysis configuration
- Defining architecture rules
- Managing security exceptions
- Reviewing major architectural changes
- Monitoring code-quality trends

### DevOps / Platform Team

Responsible for:

- Maintaining CI/CD workflows
- Managing pipeline permissions
- Maintaining security tooling
- Managing dependency/security automation
- Monitoring pipeline reliability

---

# 38. Success Metrics

The effectiveness of this standard should be measured using engineering metrics such as:

- PR quality-gate pass rate
- Number of high/critical security findings
- Reopened defects
- Production defects
- Test coverage trend
- Technical-debt trend
- Pylint/Ruff issue trend
- Dead-code trend
- Dependency vulnerabilities
- Mean time to remediate security findings
- PR review turnaround time

The objective should be **continuous improvement**, not simply increasing tool scores.

---

# 39. Conclusion

A layered Python code-review strategy provides stronger protection than relying on a single static-analysis tool.

The recommended approach is:

```text
Ruff
  +
Pylint
  +
Bandit
  +
Semgrep
  +
Pytest
  +
MyPy
  +
pip-audit
  +
Secret Scanning
  +
Manual Review
```

with:

```text
Vulture + Skylos
```

used periodically for technical-debt and code-health analysis.

This approach provides balanced coverage across **code quality, security, SAST, type safety, testing, dependency security, secret protection, dead code and maintainability** while avoiding unnecessary duplication between tools.
