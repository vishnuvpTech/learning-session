# Python REST API Best Practices & Style Guide

**Version:** 1.0  
**Audience:** Python Backend Developers, Architects, QA  
**Framework:** FastAPI / Django REST Framework / Flask  
**Scope:** Company-wide Python REST API development

---

# 1. Core Principles

Python REST APIs should follow these principles:

- **Resource-oriented:** APIs should expose resources/nouns rather than implementation-specific verbs.
- **PEP 8 compliant:** Python code must follow standard Python style conventions.
- **Consistency over cleverness:** Follow common naming, structure, validation, and response patterns.
- **Predictable responses:** Success and error responses should follow a consistent structure.
- **Stateless:** APIs should not maintain client-specific session state unless explicitly required.
- **Type-safe:** Use Python type hints throughout the application.
- **Validated:** Validate all external input before processing.
- **Secure by default:** Never expose secrets or sensitive information.
- **Testable:** Business logic should be separated from API/controller logic.
- **Documented:** OpenAPI/Swagger documentation must be maintained.
- **Maintainable:** Follow clear separation of concerns and modular architecture.

---

# 2. Python Naming Conventions

Python follows **snake_case**, as recommended by PEP 8.

## 2.1 Variables

Use `snake_case`.

```python
user_name = "John"
account_status = "active"
customer_id = 1001
```

Avoid:

```python
userName = "John"
accountStatus = "active"
customerId = 1001
```

---

## 2.2 Boolean Variables

Boolean variables should use meaningful prefixes such as:

- `is_`
- `has_`
- `can_`
- `should_`
- `was_`
- `needs_`

Recommended:

```python
is_active = True
has_subscription = True
can_redeem = False
should_notify = True
is_verified = True
```

Avoid:

```python
active = True
subscription = True
redeem = False
notify = True
verified = True
```

### API JSON vs Python

The API contract may use camelCase:

```json
{
  "isActive": true,
  "hasSubscription": true,
  "canRedeem": false
}
```

But Python code should use:

```python
is_active = True
has_subscription = True
can_redeem = False
```

Use Pydantic aliases when required.

```python
from pydantic import BaseModel, Field


class CustomerResponse(BaseModel):
    is_active: bool = Field(alias="isActive")
    has_subscription: bool = Field(alias="hasSubscription")
    can_redeem: bool = Field(alias="canRedeem")
```

---

# 3. Python Naming Standards

| Component | Convention | Example |
|---|---|---|
| Variable | `snake_case` | `user_name` |
| Function | `snake_case` | `get_user()` |
| Method | `snake_case` | `validate_user()` |
| Class | `PascalCase` | `UserService` |
| Exception | `PascalCase` | `UserNotFoundError` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Module | `snake_case` | `user_service.py` |
| Package | `snake_case` | `payment_service` |
| Private variable | `_snake_case` | `_access_token` |
| Boolean | `is_/has_/can_/should_` | `is_active` |

---

# 4. Functions and Methods

Functions must use `snake_case`.

```python
def get_customer(customer_id: int):
    pass


def create_customer(customer_data: dict):
    pass


def validate_customer(customer_id: int):
    pass
```

Avoid:

```python
def getCustomer(customerId):
    pass
```

---

# 5. Classes

Classes must use `PascalCase`.

```python
class CustomerService:
    pass


class PaymentRepository:
    pass


class AuthenticationService:
    pass
```

Avoid:

```python
class customer_service:
    pass
```

---

# 6. Constants

Constants must use `UPPER_SNAKE_CASE`.

```python
MAX_RETRY_COUNT = 3
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
ACCESS_TOKEN_EXPIRY = 3600
```

---

# 7. Type Hints

Use type hints for function parameters, return values, class attributes, and important variables.

Recommended:

```python
def get_customer(customer_id: int) -> Customer:
    ...
```

For collections:

```python
from typing import list

def get_customer_ids() -> list[int]:
    ...
```

For optional values:

```python
def get_customer(customer_id: int) -> Customer | None:
    ...
```

For dictionaries:

```python
def get_customer_metadata() -> dict[str, str]:
    ...
```

Avoid untyped functions:

```python
def get_customer(customer_id):
    ...
```

---

# 8. Project Structure

Python REST applications should follow a modular structure.

Example:

```text
app/
├── api/
│   └── v1/
│       ├── customers.py
│       ├── orders.py
│       └── authentication.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py
│
├── models/
│   ├── customer.py
│   └── order.py
│
├── schemas/
│   ├── customer.py
│   └── order.py
│
├── services/
│   ├── customer_service.py
│   └── order_service.py
│
├── repositories/
│   ├── customer_repository.py
│   └── order_repository.py
│
├── exceptions/
│   └── customer.py
│
├── middleware/
│   └── logging.py
│
└── main.py
```

Business logic should not be placed directly inside API route/controller functions.

---

# 9. API Versioning

Version every public API.

Recommended:

```text
/api/v1/customers
/api/v1/orders
/api/v2/customers
```

Python structure:

```text
app/
└── api/
    ├── v1/
    │   ├── customers.py
    │   └── orders.py
    │
    └── v2/
        ├── customers.py
        └── orders.py
```

Keep business/domain logic version-independent.

Avoid:

```python
if api_version == "v1":
    ...
elif api_version == "v2":
    ...
```

---

# 10. URL Design

Use plural resource names.

Recommended:

```text
GET    /api/v1/customers
POST   /api/v1/customers
GET    /api/v1/customers/{customer_id}
PATCH  /api/v1/customers/{customer_id}
DELETE /api/v1/customers/{customer_id}
```

Avoid:

```text
/createCustomer
/getCustomer
/deleteCustomer
```

URLs represent resources. HTTP methods represent actions.

---

# 11. Nested Resources

Nested resources should generally not exceed two levels.

Recommended:

```text
GET /api/v1/customers/{customer_id}/orders
GET /api/v1/orders/{order_id}/items
```

Avoid deeply nested URLs:

```text
/customers/{id}/orders/{id}/items/{id}/products/{id}
```

---

# 12. Action Endpoints

Use action endpoints only when the operation does not naturally map to CRUD.

Examples:

```text
POST /api/v1/customers/{customer_id}/activate
POST /api/v1/orders/{order_id}/refund
POST /api/v1/auth/login
POST /api/v1/auth/logout
```

---

# 13. HTTP Methods

| Method | Purpose | Idempotent |
|---|---|---|
| GET | Retrieve resource | Yes |
| POST | Create/action | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | Ideally |
| DELETE | Delete resource | Yes |

Example:

```text
GET    /customers
POST   /customers
GET    /customers/{customer_id}
PUT    /customers/{customer_id}
PATCH  /customers/{customer_id}
DELETE /customers/{customer_id}
```

---

# 14. Idempotency

Idempotency must be implemented for operations where duplicate execution can cause business or financial impact.

Examples:

- Payments
- Orders
- Coupon redemption
- Loyalty redemption
- Transactions

Request:

```http
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

The server should return the same result when the same idempotency key is submitted again.

Example:

```python
def process_payment(
    payment_request: PaymentRequest,
    idempotency_key: str,
) -> PaymentResponse:
    ...
```

---

# 15. Request Schema Validation

Never trust incoming request data.

Use Pydantic, Django serializers, or an equivalent validation mechanism.

FastAPI example:

```python
from pydantic import BaseModel, EmailStr, Field


class CreateCustomerRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(gt=0)
```

Validation should happen before business logic execution.

---

# 16. JSON Naming Convention

### Python

Use:

```python
first_name
last_name
date_of_birth
phone_number
created_at
updated_at
```

### API JSON

If the organization standard is camelCase:

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "dateOfBirth": "1990-12-24",
  "phoneNumber": "+919999999999"
}
```

Do not mix naming conventions within the same API.

---

# 17. Pydantic Naming and Aliases

Recommended FastAPI approach:

```python
from pydantic import BaseModel, ConfigDict


class CustomerResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda value: ''.join(
            [
                value.split('_')[0],
                *[
                    word.capitalize()
                    for word in value.split('_')[1:]
                ],
            ]
        ),
    )

    customer_id: int
    first_name: str
    is_active: bool
    created_at: str
```

This allows Python code to remain `snake_case` while the API can expose camelCase.

Example JSON:

```json
{
  "customerId": 1001,
  "firstName": "John",
  "isActive": true,
  "createdAt": "2026-09-07T10:30:00Z"
}
```

---

# 18. Date and Time

Use ISO 8601 format.

Recommended:

```json
{
  "birthDate": "1990-12-24",
  "createdAt": "2026-09-07T10:30:00Z",
  "updatedAt": "2026-09-07T16:00:00+05:30"
}
```

Python:

```python
from datetime import datetime, date

birth_date: date
created_at: datetime
updated_at: datetime
```

Always prefer timezone-aware `datetime` values for timestamps.

Avoid:

```python
datetime.now()
```

when timezone awareness is required.

Prefer:

```python
from datetime import datetime, timezone

created_at = datetime.now(timezone.utc)
```

---

# 19. Null vs Missing Fields

Use `null` only when the API intentionally communicates that a value is empty.

Example:

```json
{
  "middleName": null
}
```

For optional response fields where the value is not applicable, omission may be preferable:

```json
{
  "firstName": "John",
  "lastName": "Smith"
}
```

Define this behavior consistently across APIs.

---

# 20. Response Structure

All APIs should follow a consistent response structure.

### Success

```json
{
  "success": true,
  "data": {
    "id": "U123",
    "firstName": "John",
    "tier": "GOLD"
  },
  "meta": {
    "traceId": "abc123"
  }
}
```

### Python Schema

```python
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    meta: dict | None = None
```

---

# 21. Error Response

Use a consistent error structure.

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "details": {},
    "traceId": "req-55493"
  }
}
```

Python:

```python
class ApiError(BaseModel):
    code: str
    message: str
    details: dict | None = None
    trace_id: str | None = None
```

---

# 22. Custom Exceptions

Create domain-specific exceptions instead of returning arbitrary errors from business logic.

```python
class CustomerNotFoundError(Exception):
    pass


class CustomerAlreadyExistsError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass
```

Map exceptions to HTTP responses centrally.

Example:

```python
@app.exception_handler(CustomerNotFoundError)
async def customer_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": {
                "code": "CUSTOMER_NOT_FOUND",
                "message": "Customer not found.",
            },
        },
    )
```

---

# 23. HTTP Status Codes

## 2xx Success

| Code | Meaning | Example |
|---|---|---|
| 200 | Successful response | GET customer |
| 201 | Resource created | POST customer |
| 202 | Accepted | Async processing |
| 204 | No content | DELETE success |

## 4xx Client Errors

| Code | Meaning |
|---|---|
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 409 | Conflict |
| 422 | Validation failed |
| 429 | Rate limit exceeded |

## 5xx Server Errors

| Code | Meaning |
|---|---|
| 500 | Unexpected server error |
| 502 | Bad gateway |
| 503 | Service unavailable |
| 504 | Gateway timeout |

---

# 24. Validation Errors

### Single Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "details": {
      "email": [
        "The email field is required."
      ]
    }
  }
}
```

### Multiple Errors

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "details": {
      "email": [
        "Invalid email format."
      ],
      "password": [
        "Must be at least 8 characters.",
        "Must contain one uppercase letter."
      ]
    }
  }
}
```

---

# 25. Pagination

Use consistent pagination parameters.

Recommended:

```text
GET /api/v1/customers?page=1&page_size=20
```

If the external API contract requires camelCase:

```text
GET /api/v1/customers?page=1&pageSize=20
```

Response:

```json
{
  "success": true,
  "data": [
    {}
  ],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 250,
    "totalPages": 13
  }
}
```

Define a maximum page size.

```python
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
```

---

# 26. Filtering

Basic filtering:

```text
GET /api/v1/customers?tier=gold&isActive=true
```

Python query parameter:

```python
is_active: bool | None = None
```

---

# 27. Advanced Filtering

Use consistent suffix-based operators.

| Operator | Meaning | Example |
|---|---|---|
| `_gt` | Greater than | `salary_gt=20000` |
| `_gte` | Greater/equal | `amount_gte=5000` |
| `_lt` | Less than | `age_lt=60` |
| `_lte` | Less/equal | `quantity_lte=5` |
| `_ne` | Not equal | `status_ne=inactive` |
| `_in` | In list | `tier_in=gold,silver` |
| `_between` | Range | `amount_between=500,5000` |

Example:

```text
GET /api/v1/employees?filter[salary_gt]=20000
```

---

# 28. Sorting

Use:

```text
sort=field_name
```

Descending:

```text
sort=-field_name
```

Multiple fields:

```text
sort=amount,-created_at
```

Example:

```text
GET /api/v1/customers?sort=-created_at
```

API JSON fields may remain camelCase:

```text
GET /api/v1/customers?sort=-createdAt
```

---

# 29. Repository Pattern

Database access should be separated from business logic.

Example:

```python
class CustomerRepository:

    def get_by_id(self, customer_id: int) -> Customer | None:
        ...

    def create(self, customer: Customer) -> Customer:
        ...

    def update(self, customer: Customer) -> Customer:
        ...

    def delete(self, customer_id: int) -> None:
        ...
```

Avoid putting database queries directly into API routes.

Bad:

```python
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    return customer
```

Prefer:

```python
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    return customer_service.get_customer(customer_id)
```

---

# 30. Service Layer

Business logic should live inside service classes/functions.

```python
class CustomerService:

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repository.get_by_id(customer_id)

        if not customer:
            raise CustomerNotFoundError()

        return customer
```

Recommended flow:

```text
API Controller
      ↓
Schema Validation
      ↓
Service
      ↓
Repository
      ↓
Database
```

---

# 31. Dependency Injection

Use dependency injection for:

- Database sessions
- Services
- Repositories
- Authentication
- External clients
- Configuration

FastAPI example:

```python
def get_customer_service() -> CustomerService:
    return CustomerService(
        repository=CustomerRepository()
    )
```

---

# 32. Database Standards

Use an ORM where appropriate.

Examples:

- SQLAlchemy
- Django ORM

Database naming should follow:

```text
snake_case
```

Example:

```text
customer_id
first_name
created_at
updated_at
is_active
```

Avoid database columns such as:

```text
customerId
firstName
createdAt
```

---

# 33. Database Primary Keys

Use consistent primary key strategies across services.

Example:

```python
id: int
```

or UUID:

```python
from uuid import UUID

id: UUID
```

For distributed systems and microservices, UUIDs are often preferred where globally unique identifiers are required.

---

# 34. Transactions

Business operations requiring multiple database changes should use transactions.

Example:

```python
with session.begin():
    order = create_order()
    create_order_items(order)
    update_inventory()
```

Never partially complete a transaction without explicit business justification.

---

# 35. Security

Authentication:

```http
Authorization: Bearer <token>
```

Never expose:

- Passwords
- OTPs
- API keys
- Access tokens
- Refresh tokens
- Secrets
- Private encryption keys
- Database credentials

---

# 36. Password Handling

Never store plaintext passwords.

Use a secure password hashing algorithm such as:

- Argon2
- bcrypt

Example:

```python
hashed_password = password_hasher.hash(password)
```

Never:

```python
password = user.password
```

for logging or API responses.

---

# 37. Sensitive Logging

Never log:

```text
password
otp
access_token
refresh_token
api_key
secret
authorization
```

Bad:

```python
logger.info("Login request: %s", request.dict())
```

if the request contains credentials.

Prefer:

```python
logger.info(
    "Login attempt for user_id=%s",
    user_id,
)
```

---

# 38. Rate Limiting

APIs should implement rate limiting where required.

Example response headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 755
X-RateLimit-Reset: 1737480912
```

When exceeded:

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Retry after 60 seconds."
  }
}
```

Return:

```http
429 Too Many Requests
```

---

# 39. Concurrency Control

Use ETags or another concurrency mechanism for resources where concurrent updates are possible.

Example:

```http
GET /api/v1/customers/123

ETag: "v7"
```

Update:

```http
PUT /api/v1/customers/123

If-Match: "v7"
```

If the version has changed:

```http
409 Conflict
```

---

# 40. Logging and Observability

Every API request should provide sufficient information for troubleshooting.

Log:

- HTTP method
- Request path
- HTTP status
- Response latency
- Trace ID
- Request ID
- Service name
- Environment

Example:

```python
logger.info(
    "API request completed",
    extra={
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency_ms": latency_ms,
        "trace_id": trace_id,
    },
)
```

Never log sensitive information.

---

# 41. Trace ID

Every request should have a trace ID.

Example:

```http
X-Trace-Id: 7b7e3c8a-7b4d-4c1d-a6a8-123456789abc
```

The trace ID should be propagated across microservices.

```text
Client
  ↓
API Gateway
  ↓
Service A
  ↓
Service B
  ↓
Database
```

All services should retain the same trace/correlation ID where appropriate.

---

# 42. External API Calls

External API communication should be isolated behind a client/service.

Example:

```python
class PaymentClient:

    async def create_payment(
        self,
        amount: float,
        currency: str,
    ) -> PaymentResponse:
        ...
```

Do not make external HTTP calls directly inside API route functions.

---

# 43. External API Timeouts

Always define connection and read timeouts.

Avoid:

```python
requests.get(url)
```

Prefer:

```python
requests.get(
    url,
    timeout=10,
)
```

For async applications, use an async HTTP client such as `httpx`.

---

# 44. Retry Strategy

Retries should only be used for transient failures.

Examples:

- Connection timeout
- Temporary network failure
- 502
- 503
- 504

Do not blindly retry:

- 400
- 401
- 403
- 404
- Validation errors

Use exponential backoff.

```text
1s
2s
4s
8s
```

Set a maximum retry count.

```python
MAX_RETRIES = 3
```

---

# 45. Async Programming

Use `async`/`await` for I/O-bound operations when the application framework supports asynchronous execution.

Example:

```python
async def get_customer(customer_id: int) -> Customer:
    customer = await repository.get_by_id(customer_id)
    return customer
```

Do not perform blocking operations inside an async function without appropriate handling.

Avoid:

```python
async def get_customer():
    time.sleep(10)
```

Prefer:

```python
await asyncio.sleep(10)
```

when a sleep is actually required.

---

# 46. Background Tasks

Long-running operations should not block API requests.

Examples:

- Email sending
- Report generation
- Large file processing
- Notifications
- AI processing
- Data synchronization

Use:

- Celery
- RQ
- Cloud queues
- Kafka
- AWS SQS
- OCI queues
- Other appropriate message brokers

API response:

```http
202 Accepted
```

Example:

```json
{
  "success": true,
  "data": {
    "jobId": "JOB-12345",
    "status": "processing"
  }
}
```

---

# 47. Configuration Management

Never hardcode environment-specific configuration.

Bad:

```python
DATABASE_URL = "postgresql://user:password@server/db"
```

Prefer:

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

Use environment variables or a secure secret manager.

Examples:

- AWS Secrets Manager
- OCI Vault
- Azure Key Vault
- Kubernetes Secrets

---

# 48. Environment Separation

Maintain separate configuration for:

```text
development
testing
staging
production
```

Never use production credentials in development environments.

---

# 49. Dependency Management

Pin dependencies where appropriate.

Example:

```text
fastapi==0.116.1
sqlalchemy==2.0.43
pydantic==2.11.7
```

Regularly scan dependencies for known vulnerabilities.

Recommended tools:

- pip-audit
- Snyk
- Dependabot
- Trivy

---

# 50. Code Quality

Python projects should use automated code-quality tools.

Recommended:

### Formatting

```text
Black
Ruff
```

### Linting

```text
Ruff
Pylint
```

### Type Checking

```text
mypy
```

### Security

```text
Bandit
pip-audit
```

Code should pass automated checks before merging.

---

# 51. Docstrings

Public classes, functions, and complex business logic should have meaningful docstrings.

```python
def calculate_discount(
    amount: float,
    discount_percentage: float,
) -> float:
    """Calculate the discount amount for a given purchase."""
    return amount * discount_percentage / 100
```

Avoid meaningless docstrings:

```python
def calculate_discount():
    """This function calculates discount."""
```

---

# 52. Exception Handling

Avoid broad exception handling.

Bad:

```python
try:
    process_order()
except Exception:
    pass
```

Prefer:

```python
try:
    process_order()
except PaymentGatewayError as exc:
    logger.exception("Payment processing failed")
    raise
```

Never silently swallow exceptions.

---

# 53. Database Exception Handling

Database-specific exceptions should be handled at the appropriate layer.

Example:

```python
try:
    repository.create(customer)
except IntegrityError:
    raise CustomerAlreadyExistsError()
```

Do not expose raw database exceptions to API clients.

---

# 54. API Documentation

Every API must maintain OpenAPI documentation.

Documentation should include:

- Endpoint description
- Request parameters
- Request schema
- Response schema
- HTTP status codes
- Authentication requirements
- Error responses
- Examples

FastAPI automatically generates:

```text
/docs
/redoc
/openapi.json
```

---

# 55. Testing Requirements

Every API should include:

- Unit tests
- Integration tests
- API tests
- Contract tests where applicable
- Smoke tests
- Security tests where applicable

Recommended Python tools:

```text
pytest
pytest-asyncio
httpx
```

---

# 56. Unit Testing

Business logic should be independently testable.

Example:

```python
def test_calculate_discount():
    result = calculate_discount(
        amount=1000,
        discount_percentage=10,
    )

    assert result == 100
```

---

# 57. API Testing

Example:

```python
def test_get_customer(client):
    response = client.get("/api/v1/customers/123")

    assert response.status_code == 200
    assert response.json()["success"] is True
```

---

# 58. Test Naming

Test names should clearly describe the expected behavior.

Recommended:

```python
def test_create_customer_with_valid_data():
    ...


def test_create_customer_with_duplicate_email():
    ...


def test_get_customer_returns_404_when_not_found():
    ...
```

Avoid:

```python
def test_customer():
    ...
```

---

# 59. Git Standards

Use meaningful branch names.

Examples:

```text
feature/customer-registration
feature/payment-integration
bugfix/customer-validation
hotfix/payment-timeout
refactor/customer-service
```

Commit messages should clearly describe the change.

Example:

```text
feat: add customer registration API
fix: handle duplicate customer email
refactor: move payment logic to service layer
test: add customer API tests
```

---

# 60. Code Review Requirements

Before merging, reviewers should verify:

- Python naming conventions
- PEP 8 compliance
- Type hints
- Error handling
- Input validation
- Security
- Database performance
- API consistency
- Logging
- Tests
- Documentation
- No sensitive information
- No hardcoded secrets

---

# 61. API Review Checklist

## API Design

- [ ] API follows resource-oriented design
- [ ] API version is included
- [ ] HTTP methods are used correctly
- [ ] URLs use consistent naming
- [ ] Nested resources do not exceed recommended depth
- [ ] Action endpoints are used only when necessary

## Python Code

- [ ] PEP 8 followed
- [ ] Variables use `snake_case`
- [ ] Functions use `snake_case`
- [ ] Classes use `PascalCase`
- [ ] Constants use `UPPER_SNAKE_CASE`
- [ ] Boolean variables use `is_`, `has_`, `can_`, `should_`
- [ ] Type hints are provided
- [ ] Docstrings added where required
- [ ] No unnecessary complexity

## Request/Response

- [ ] Request validation implemented
- [ ] JSON naming convention is consistent
- [ ] Boolean API fields are clearly named
- [ ] Date/time uses ISO 8601
- [ ] Null/missing field behavior is defined
- [ ] Success response envelope is consistent
- [ ] Error response envelope is consistent

## Database

- [ ] Database access is separated from business logic
- [ ] Repository/service patterns are followed where appropriate
- [ ] Transactions are handled correctly
- [ ] Database queries are optimized
- [ ] N+1 queries are avoided
- [ ] Database indexes are reviewed

## Security

- [ ] Authentication implemented
- [ ] Authorization implemented
- [ ] Sensitive data is not returned
- [ ] Secrets are not hardcoded
- [ ] Passwords are hashed
- [ ] Input validation implemented
- [ ] Rate limiting considered
- [ ] Security headers configured where applicable

## Performance

- [ ] Pagination implemented
- [ ] Filtering implemented
- [ ] Sorting implemented
- [ ] Database queries optimized
- [ ] External API timeouts configured
- [ ] Retry strategy implemented where required
- [ ] Background processing used for long-running tasks

## Observability

- [ ] Trace ID implemented
- [ ] Request logging implemented
- [ ] Response latency monitored
- [ ] Errors logged
- [ ] Sensitive information excluded from logs

## Testing

- [ ] Unit tests completed
- [ ] Integration tests completed
- [ ] API tests completed
- [ ] Negative test cases covered
- [ ] Authentication/authorization tests covered
- [ ] OpenAPI documentation updated

---

# 62. Recommended Python API Architecture

For medium and large Python applications, use:

```text
                    Client
                      │
                      ▼
                API Gateway
                      │
                      ▼
              ┌───────────────┐
              │ API / Router  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Schema Layer  │
              │  Validation   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Service Layer │
              │ Business Logic│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Repository   │
              │ Data Access   │
              └───────┬───────┘
                      │
                      ▼
                 Database
```

External integrations should be isolated:

```text
Service
   │
   ├── Repository → Database
   │
   ├── API Client → External API
   │
   ├── Queue → Background Worker
   │
   └── Cache → Redis
```

---

# 63. Recommended FastAPI Project Structure

For FastAPI projects:

```text
app/
├── main.py
│
├── api/
│   └── v1/
│       ├── router.py
│       ├── auth.py
│       ├── customers.py
│       └── orders.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   └── logging.py
│
├── models/
│   ├── customer.py
│   └── order.py
│
├── schemas/
│   ├── customer.py
│   └── order.py
│
├── services/
│   ├── customer_service.py
│   └── order_service.py
│
├── repositories/
│   ├── customer_repository.py
│   └── order_repository.py
│
├── clients/
│   └── payment_client.py
│
├── exceptions/
│   └── handlers.py
│
└── middleware/
    ├── logging.py
    └── tracing.py

tests/
├── unit/
├── integration/
└── api/
```

---

# 64. Python vs API Naming Standard

The most important rule for Python REST APIs is to distinguish **internal Python naming** from the **external API contract**.

### Python code

```python
class CustomerService:

    def get_customer(
        self,
        customer_id: int,
    ) -> CustomerResponse:

        customer = self.repository.get_by_id(
            customer_id
        )

        if not customer:
            raise CustomerNotFoundError()

        return CustomerResponse(
            customer_id=customer.id,
            first_name=customer.first_name,
            is_active=customer.is_active,
            has_subscription=customer.has_subscription,
        )
```

### API response

```json
{
  "success": true,
  "data": {
    "customerId": 1001,
    "firstName": "John",
    "isActive": true,
    "hasSubscription": true
  }
}
```

Therefore:

```text
Python             API JSON
--------------------------------
customer_id    →   customerId
first_name     →   firstName
is_active      →   isActive
has_subscription → hasSubscription
created_at     →   createdAt
```

This gives the project **PEP 8-compliant Python code** while maintaining the existing company API contract.

---

# 65. Final Standard

All Python backend projects should follow these primary conventions:

```text
Python Variables       → snake_case
Python Functions       → snake_case
Python Methods         → snake_case
Python Classes         → PascalCase
Python Constants       → UPPER_SNAKE_CASE
Python Booleans        → is_/has_/can_/should_
Python Modules         → snake_case

API URLs               → /api/v1/customers
API URL Parameters     → Standardized consistently
API JSON               → camelCase
API Boolean Fields     → isActive / hasSubscription / canRedeem
API Dates              → ISO 8601
API Responses          → Standard response envelope
API Errors             → Standard error envelope

Database Fields        → snake_case
Environment Variables  → UPPER_SNAKE_CASE
```

The key principle is:

> **Use Python conventions inside the application and maintain a consistent API naming contract at the boundary.**