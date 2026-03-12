# Python Backend Development - Best Practices Guide
## Comprehensive Guide to Professional Python Backend Development

**Version:** 1.0  
**Last Updated:** March 2026  
**Target Audience:** Python backend developers at all levels  
**Purpose:** Production-ready code standards and industry best practices

---

## Table of Contents

1. [Code Quality & Style](#code-quality)
2. [Project Structure](#project-structure)
3. [Configuration Management](#configuration)
4. [Database Best Practices](#database)
5. [API Design Best Practices](#api-design)
6. [Error Handling](#error-handling)
7. [Logging & Monitoring](#logging)
8. [Security Best Practices](#security)
9. [Testing Best Practices](#testing)
10. [Performance Optimization](#performance)
11. [Async Programming](#async)
12. [Docker & Deployment](#docker)
13. [Documentation](#documentation)
14. [Code Review Checklist](#code-review)

---

<a name="code-quality"></a>
## 1. Code Quality & Style

### 1.1 Follow PEP 8

```python
# ✅ GOOD: Follow PEP 8 naming conventions

# Constants in UPPER_CASE
MAX_RETRY_ATTEMPTS = 3
DATABASE_URL = "postgresql://localhost/db"

# Functions and variables in snake_case
def calculate_total_price(items: list) -> float:
    total_price = sum(item.price for item in items)
    return total_price

# Classes in PascalCase
class UserRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url
    
    def get_user_by_id(self, user_id: int):
        pass

# Private methods with leading underscore
class DataProcessor:
    def process(self, data: dict):
        validated_data = self._validate_data(data)
        return self._transform_data(validated_data)
    
    def _validate_data(self, data: dict) -> dict:
        # Private method
        return data
    
    def _transform_data(self, data: dict) -> dict:
        # Private method
        return data

# ❌ BAD: Inconsistent naming
MaxRetryAttempts = 3  # Should be UPPER_CASE
def CalculateTotalPrice(items):  # Should be snake_case
    TotalPrice = 0  # Should be snake_case
    return TotalPrice

class user_repository:  # Should be PascalCase
    pass
```

### 1.2 Type Hints

```python
from typing import List, Dict, Optional, Union, Any, Callable
from dataclasses import dataclass
from datetime import datetime

# ✅ GOOD: Use type hints everywhere
def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID.
    
    Args:
        user_id: The unique user identifier
        
    Returns:
        User dictionary if found, None otherwise
    """
    # Implementation
    pass

def process_users(
    users: List[Dict[str, Any]],
    filter_func: Callable[[Dict], bool]
) -> List[Dict[str, Any]]:
    """Process and filter users.
    
    Args:
        users: List of user dictionaries
        filter_func: Function to filter users
        
    Returns:
        Filtered list of users
    """
    return [user for user in users if filter_func(user)]

# Use dataclasses for complex return types
@dataclass
class UserResponse:
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool = True

def get_user_typed(user_id: int) -> Optional[UserResponse]:
    """Get user with typed response."""
    # Implementation
    pass

# ❌ BAD: No type hints
def get_user(user_id):  # What type is user_id?
    pass  # What does this return?

def process_data(data):  # Unclear what data is
    result = do_something(data)  # What's the result type?
    return result
```

### 1.3 Use Linters and Formatters

```bash
# Install tools
pip install black isort flake8 mypy pylint bandit

# pyproject.toml configuration
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# Run formatters
black .
isort .

# Run linters
flake8 .
mypy .
pylint src/
bandit -r src/

# Pre-commit hook (.pre-commit-config.yaml)
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

### 1.4 Write Clean, Readable Code

```python
# ✅ GOOD: Clear, self-documenting code
def calculate_discounted_price(
    original_price: float,
    discount_percentage: float,
    is_premium_member: bool
) -> float:
    """Calculate final price after applying discount.
    
    Premium members get an additional 10% discount.
    """
    if not 0 <= discount_percentage <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    base_discount = original_price * (discount_percentage / 100)
    discounted_price = original_price - base_discount
    
    if is_premium_member:
        additional_discount = discounted_price * 0.10
        discounted_price -= additional_discount
    
    return round(discounted_price, 2)

# ❌ BAD: Unclear, hard to read
def calc(p, d, pm):  # What do these parameters mean?
    x = p * (d / 100)  # What is x?
    p = p - x
    if pm:
        p = p - (p * 0.10)
    return p

# ✅ GOOD: Early returns reduce nesting
def process_order(order: dict) -> dict:
    """Process an order."""
    if not order:
        return {"error": "Order is empty"}
    
    if not order.get("items"):
        return {"error": "No items in order"}
    
    if order["total"] <= 0:
        return {"error": "Invalid total"}
    
    # Main processing logic
    return {"status": "success", "order_id": order["id"]}

# ❌ BAD: Nested if statements
def process_order(order):
    if order:
        if order.get("items"):
            if order["total"] > 0:
                # Main logic buried deep
                return {"status": "success"}
            else:
                return {"error": "Invalid total"}
        else:
            return {"error": "No items"}
    else:
        return {"error": "Order is empty"}

# ✅ GOOD: List comprehensions for simple transformations
user_emails = [user["email"] for user in users if user.get("is_active")]

# ❌ BAD: Unnecessary loops
user_emails = []
for user in users:
    if user.get("is_active"):
        user_emails.append(user["email"])

# ✅ GOOD: Use descriptive variable names
total_active_users = len([u for u in users if u["is_active"]])
maximum_retry_attempts = 3
database_connection_timeout = 30

# ❌ BAD: Cryptic variable names
n = 10  # What is n?
tmp = []  # Temporary what?
data2 = process(data1)  # Why data2?
```

---

<a name="project-structure"></a>
## 2. Project Structure

### 2.1 Recommended Structure

```
my_project/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD configuration
├── docs/
│   ├── api.md                     # API documentation
│   ├── deployment.md              # Deployment guide
│   └── architecture.md            # Architecture decisions
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py                # Application entry point
│       ├── config.py              # Configuration
│       ├── api/
│       │   ├── __init__.py
│       │   ├── dependencies.py   # FastAPI dependencies
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   ├── users.py
│       │   │   ├── products.py
│       │   │   └── orders.py
│       │   └── schemas/
│       │       ├── __init__.py
│       │       ├── users.py      # Pydantic models
│       │       └── products.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py           # Base model class
│       │   ├── user.py           # User model
│       │   └── product.py        # Product model
│       ├── repositories/
│       │   ├── __init__.py
│       │   ├── base.py           # Base repository
│       │   ├── user.py           # User repository
│       │   └── product.py        # Product repository
│       ├── services/
│       │   ├── __init__.py
│       │   ├── user.py           # Business logic
│       │   ├── product.py
│       │   └── email.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── security.py       # Auth, JWT, etc.
│       │   ├── database.py       # DB connection
│       │   └── cache.py          # Redis/caching
│       └── utils/
│           ├── __init__.py
│           ├── validators.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── unit/
│   │   ├── test_services.py
│   │   └── test_repositories.py
│   ├── integration/
│   │   └── test_api.py
│   └── e2e/
│       └── test_flows.py
├── scripts/
│   ├── init_db.py                # Database initialization
│   ├── seed_data.py              # Seed test data
│   └── migrate.sh                # Migration script
├── .env.example                  # Example environment variables
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml                # Project metadata & dependencies
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
└── README.md
```

### 2.2 Layered Architecture

```python
# ✅ GOOD: Separation of concerns with layers

# models/user.py - Data layer
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

# repositories/user.py - Data access layer
from typing import Optional, List
from sqlalchemy.orm import Session
from models.user import User

class UserRepository:
    """Handle database operations for users."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

# services/user.py - Business logic layer
from typing import Optional
from repositories.user import UserRepository
from core.security import hash_password, verify_password
from schemas.user import UserCreate, UserResponse

class UserService:
    """Business logic for user operations."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if user exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        created_user = self.user_repo.create(user)
        
        return UserResponse.from_orm(created_user)
    
    def authenticate(self, email: str, password: str) -> Optional[UserResponse]:
        user = self.user_repo.get_by_email(email)
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return UserResponse.from_orm(user)

# api/routes/users.py - API layer
from fastapi import APIRouter, Depends, HTTPException, status
from services.user import UserService
from schemas.user import UserCreate, UserResponse
from api.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        return user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# ❌ BAD: Everything in one place (god object)
@router.post("/users/")
async def create_user(user_data: dict):
    # DB connection logic
    # Password hashing
    # Validation
    # Email sending
    # All mixed together
    pass
```

---

<a name="configuration"></a>
## 3. Configuration Management

### 3.1 Environment-Based Configuration

```python
# ✅ GOOD: Use Pydantic for configuration

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "My API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    
    # AWS
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Usage
settings = get_settings()
print(f"Connecting to: {settings.database_url}")

# .env file
"""
# Application
APP_NAME=My API
DEBUG=false
VERSION=1.0.0

# Database
DATABASE_URL=postgresql://user:pass@localhost/db
DATABASE_POOL_SIZE=20

# Secret Key (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
"""

# ❌ BAD: Hardcoded configuration
DATABASE_URL = "postgresql://user:pass@localhost/db"  # Never hardcode
SECRET_KEY = "super-secret-key-123"  # Never commit secrets
DEBUG = True  # Should be environment-based

# ❌ BAD: Using os.environ directly everywhere
import os
db_url = os.environ["DATABASE_URL"]  # No type checking, no defaults
```

### 3.2 Multiple Environments

```python
# config.py
from enum import Enum
from typing import Dict, Any

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class BaseConfig(BaseSettings):
    """Base configuration."""
    environment: Environment = Environment.DEVELOPMENT
    
    class Config:
        env_file = ".env"

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    debug: bool = True
    database_url: str = "postgresql://localhost/dev_db"
    log_level: str = "DEBUG"

class StagingConfig(BaseConfig):
    """Staging configuration."""
    debug: bool = False
    database_url: str  # From environment
    log_level: str = "INFO"

class ProductionConfig(BaseConfig):
    """Production configuration."""
    debug: bool = False
    database_url: str  # From environment
    log_level: str = "WARNING"
    
    # Strict requirements for production
    secret_key: str  # Must be set
    
    class Config:
        validate_assignment = True

def get_config() -> BaseSettings:
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    config_map: Dict[str, type[BaseSettings]] = {
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()

# Usage
config = get_config()
```

### 3.3 Secrets Management

```python
# ✅ GOOD: Never commit secrets

# Use environment variables
from os import getenv

SECRET_KEY = getenv("SECRET_KEY")  # From environment
DATABASE_PASSWORD = getenv("DATABASE_PASSWORD")

# Use .env file (not committed to git)
# Add .env to .gitignore

# Provide .env.example for documentation
"""
# .env.example
SECRET_KEY=your-secret-key-here
DATABASE_PASSWORD=your-db-password
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
"""

# Use secret managers in production
from boto3 import client

def get_secret(secret_name: str) -> Dict[str, Any]:
    """Get secret from AWS Secrets Manager."""
    secrets_client = client('secretsmanager', region_name='us-east-1')
    response = secrets_client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# ❌ BAD: Committing secrets
SECRET_KEY = "hardcoded-secret-key-123"  # NEVER DO THIS
API_KEY = "sk-1234567890abcdef"  # NEVER COMMIT API KEYS
```

---

<a name="database"></a>
## 4. Database Best Practices

### 4.1 Use Connection Pooling

```python
# ✅ GOOD: Connection pooling with SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,              # Maintain 20 connections
    max_overflow=10,           # Allow 10 additional connections
    pool_timeout=30,           # Wait 30s for connection
    pool_recycle=3600,         # Recycle connections after 1 hour
    pool_pre_ping=True,        # Verify connections before using
    echo=settings.debug,       # Log SQL in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ❌ BAD: Creating new connection for each request
def get_user(user_id: int):
    engine = create_engine(DATABASE_URL)  # Don't create new engine!
    session = sessionmaker(bind=engine)()
    user = session.query(User).get(user_id)
    session.close()
    engine.dispose()
    return user
```

### 4.2 Always Use Transactions

```python
# ✅ GOOD: Explicit transaction management

from sqlalchemy.orm import Session
from contextlib import contextmanager

@contextmanager
def transaction_scope(session: Session):
    """Provide a transactional scope."""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
def create_order(order_data: dict):
    with transaction_scope(SessionLocal()) as session:
        # Create order
        order = Order(**order_data)
        session.add(order)
        
        # Update inventory
        for item in order.items:
            product = session.query(Product).get(item.product_id)
            product.stock -= item.quantity
        
        # All or nothing - transaction commits or rolls back

# With FastAPI dependency
@router.post("/orders/")
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        # Create order
        order = Order(**order_data.dict())
        db.add(order)
        
        # Update inventory
        update_inventory(db, order.items)
        
        # Commit transaction
        db.commit()
        db.refresh(order)
        
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ❌ BAD: No transaction management
def create_order(order_data: dict):
    order = Order(**order_data)
    db.add(order)
    db.commit()  # What if this fails?
    
    # This might execute even if order creation failed
    update_inventory(order.items)
```

### 4.3 Prevent N+1 Queries

```python
# ✅ GOOD: Use eager loading

from sqlalchemy.orm import joinedload, selectinload

# Use joinedload for single relationships
def get_posts_with_authors():
    """Load posts with authors in single query."""
    return db.query(Post).options(
        joinedload(Post.author)
    ).all()

# Use selectinload for collections
def get_authors_with_posts():
    """Load authors with their posts."""
    return db.query(Author).options(
        selectinload(Author.posts)
    ).all()

# Multiple levels of eager loading
def get_posts_with_related():
    """Load posts with authors and comments."""
    return db.query(Post).options(
        joinedload(Post.author),
        selectinload(Post.comments).joinedload(Comment.author)
    ).all()

# ❌ BAD: N+1 query problem
def get_posts_with_authors():
    posts = db.query(Post).all()  # 1 query
    
    for post in posts:
        print(post.author.name)  # N additional queries!
    
    return posts

# ✅ GOOD: Use select_related in Django
# Django ORM
posts = Post.objects.select_related('author').all()

# ✅ GOOD: Use prefetch_related for many-to-many
posts = Post.objects.prefetch_related('tags', 'comments').all()
```

### 4.4 Use Indexes Properly

```python
# ✅ GOOD: Add indexes for frequently queried columns

from sqlalchemy import Index

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(150), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # Define indexes
    __table_args__ = (
        # Single column index
        Index('idx_users_email', 'email'),
        
        # Composite index for common queries
        Index('idx_users_username_created', 'username', 'created_at'),
        
        # Partial index (PostgreSQL)
        Index(
            'idx_active_users',
            'created_at',
            postgresql_where=(Column('is_active') == True)
        ),
    )

# ✅ GOOD: Use database-specific features
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    tags = Column(ARRAY(String))
    
    __table_args__ = (
        # GIN index for array column (PostgreSQL)
        Index('idx_posts_tags', 'tags', postgresql_using='gin'),
        
        # Full-text search index
        Index(
            'idx_posts_search',
            'search_vector',
            postgresql_using='gin'
        ),
    )

# Check index usage with EXPLAIN
def analyze_query():
    from sqlalchemy import text
    
    query = db.query(User).filter(User.email == 'test@example.com')
    explain = db.execute(text(f"EXPLAIN ANALYZE {query}"))
    
    for row in explain:
        print(row)
```

### 4.5 Avoid SELECT *

```python
# ✅ GOOD: Select only needed columns

from sqlalchemy import select

# Select specific columns
def get_user_emails():
    stmt = select(User.id, User.email).where(User.is_active == True)
    return db.execute(stmt).all()

# With ORM - use defer for large columns
def get_users_without_bio():
    from sqlalchemy.orm import defer
    
    return db.query(User).options(
        defer(User.bio),  # Don't load bio column
        defer(User.profile_image)  # Don't load image
    ).all()

# Load specific columns only
def get_user_summary():
    return db.query(
        User.id,
        User.username,
        User.email
    ).all()

# ❌ BAD: SELECT *
def get_users():
    return db.query(User).all()  # Loads ALL columns, even if not needed

# ❌ BAD: Loading large BLOBs unnecessarily
def list_users():
    # This loads profile images for all users!
    return db.query(User).all()
```

### 4.6 Use Database Migrations

```python
# ✅ GOOD: Use Alembic for migrations

# alembic/versions/001_create_users_table.py
"""Create users table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 10:00:00
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(150), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade():
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')

# Run migrations
"""
alembic upgrade head      # Apply all migrations
alembic downgrade -1      # Rollback one migration
alembic revision --autogenerate -m "Add column"  # Create migration
"""

# ❌ BAD: Manual SQL changes in production
# Don't do this:
db.execute("ALTER TABLE users ADD COLUMN new_field VARCHAR(100)")
```

---

<a name="api-design"></a>
## 5. API Design Best Practices

### 5.1 RESTful API Design

```python
# ✅ GOOD: Follow REST conventions

from fastapi import APIRouter, status, HTTPException
from typing import List

router = APIRouter(prefix="/api/v1", tags=["users"])

# Use proper HTTP methods
@router.get("/users/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100):
    """List all users."""
    return user_service.list_users(skip=skip, limit=limit)

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user."""
    return user_service.create_user(user)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a specific user."""
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    """Update a user."""
    return user_service.update_user(user_id, user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user."""
    user_service.delete_user(user_id)
    return None

# ❌ BAD: Non-RESTful design
@router.get("/get_all_users")  # Should be GET /users/
async def get_all_users():
    pass

@router.post("/user/create")  # Should be POST /users/
async def create_user():
    pass

@router.get("/user/delete/{id}")  # Should be DELETE /users/{id}
async def delete_user(id: int):
    pass
```

### 5.2 Use Pydantic for Validation

```python
# ✅ GOOD: Comprehensive validation with Pydantic

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=200)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

class UserCreate(UserBase):
    """Schema for creating users."""
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserUpdate(BaseModel):
    """Schema for updating users."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    
    class Config:
        # Allow partial updates
        validate_assignment = True

class UserResponse(UserBase):
    """Schema for user responses."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Enable ORM mode

# ❌ BAD: No validation
@router.post("/users/")
async def create_user(user: dict):  # Accepting any dict
    # No validation of email, username, password
    return user_service.create_user(user)
```

### 5.3 Consistent Error Responses

```python
# ✅ GOOD: Standardized error responses

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    path: Optional[str] = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.status_code,
            message=exc.detail,
            path=str(request.url)
        ).dict()
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle value errors."""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="validation_error",
            message=str(exc),
            path=str(request.url)
        ).dict()
    )

# Custom exception
class UserNotFoundError(Exception):
    """User not found exception."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    """Handle user not found."""
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="user_not_found",
            message=str(exc),
            details={"user_id": exc.user_id},
            path=str(request.url)
        ).dict()
    )

# ❌ BAD: Inconsistent error responses
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        return {"error": "not found"}  # Inconsistent structure
    return user

@router.post("/users/")
async def create_user(user: dict):
    if not user.get("email"):
        raise HTTPException(status_code=400, detail="Missing email")  # Different format
    # ...
```

### 5.4 API Versioning

```python
# ✅ GOOD: Version your APIs

from fastapi import APIRouter

# Version 1
router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])

@router_v1.get("/users/{user_id}")
async def get_user_v1(user_id: int):
    """Version 1 - returns basic user info."""
    return {"id": user_id, "username": "user"}

# Version 2
router_v2 = APIRouter(prefix="/api/v2", tags=["v2"])

@router_v2.get("/users/{user_id}")
async def get_user_v2(user_id: int):
    """Version 2 - returns extended user info."""
    return {
        "id": user_id,
        "username": "user",
        "created_at": "2024-01-01",
        "metadata": {}
    }

# Include both versions
app.include_router(router_v1)
app.include_router(router_v2)

# Alternative: Header-based versioning
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    api_version: str = Header(default="1")
):
    """Get user with header-based versioning."""
    if api_version == "2":
        return get_user_v2_logic(user_id)
    return get_user_v1_logic(user_id)

# ❌ BAD: Breaking changes without versioning
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    # Changed response structure - breaks existing clients!
    return {"userId": user_id}  # Was "id" before
```

### 5.5 Pagination

```python
# ✅ GOOD: Implement pagination

from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

@router.get("/users/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """List users with pagination."""
    skip = (page - 1) * page_size
    
    users = user_service.list_users(skip=skip, limit=page_size)
    total = user_service.count_users()
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )

# Cursor-based pagination for large datasets
class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Cursor-based pagination."""
    items: List[T]
    next_cursor: Optional[str] = None
    has_more: bool

@router.get("/posts/", response_model=CursorPaginatedResponse[PostResponse])
async def list_posts(
    cursor: Optional[str] = None,
    limit: int = Query(20, le=100)
):
    """List posts with cursor pagination."""
    posts, next_cursor = post_service.list_posts(cursor=cursor, limit=limit)
    
    return CursorPaginatedResponse(
        items=posts,
        next_cursor=next_cursor,
        has_more=next_cursor is not None
    )

# ❌ BAD: No pagination
@router.get("/users/")
async def list_users():
    # Returns ALL users - can be millions!
    return db.query(User).all()
```

---

<a name="error-handling"></a>
## 6. Error Handling

### 6.1 Use Specific Exceptions

```python
# ✅ GOOD: Create custom exceptions

class ApplicationError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(ApplicationError):
    """Validation error."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(ApplicationError):
    """Resource not found."""
    def __init__(self, resource: str, identifier: Any):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id {identifier} not found")

class AuthenticationError(ApplicationError):
    """Authentication failed."""
    pass

class AuthorizationError(ApplicationError):
    """User not authorized."""
    pass

# Use in services
class UserService:
    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user
    
    def validate_email(self, email: str):
        if "@" not in email:
            raise ValidationError("email", "Invalid email format")

# Handle in API layer
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        return user_service.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ❌ BAD: Generic exceptions
def get_user(user_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise Exception("Error")  # Too generic!
    return user
```

### 6.2 Handle Errors Gracefully

```python
# ✅ GOOD: Try-except with specific handling

import logging

logger = logging.getLogger(__name__)

async def process_payment(order_id: int, payment_data: dict):
    """Process payment with proper error handling."""
    try:
        # Validate payment data
        validate_payment_data(payment_data)
        
        # Process payment
        result = await payment_gateway.charge(payment_data)
        
        # Update order
        update_order_status(order_id, "paid")
        
        # Send confirmation email
        await send_confirmation_email(order_id)
        
        return result
        
    except ValidationError as e:
        logger.warning(f"Payment validation failed for order {order_id}: {e}")
        raise
        
    except PaymentGatewayError as e:
        logger.error(f"Payment gateway error for order {order_id}: {e}")
        # Mark order as payment failed
        update_order_status(order_id, "payment_failed")
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error processing payment for order {order_id}: {e}")
        # Rollback any changes
        rollback_order(order_id)
        raise

# ❌ BAD: Catching all exceptions without handling
async def process_payment(order_id: int, payment_data: dict):
    try:
        # ... payment logic
        pass
    except Exception:
        pass  # Silently swallowing errors!

# ❌ BAD: Not logging errors
async def process_payment(order_id: int, payment_data: dict):
    try:
        # ... payment logic
        pass
    except Exception as e:
        raise  # No logging - can't debug issues!
```

### 6.3 Retry Logic

```python
# ✅ GOOD: Implement retry with exponential backoff

import time
from functools import wraps
from typing import Callable, TypeVar, Type

T = TypeVar('T')

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"All {max_attempts} attempts failed: {e}")
                        raise
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
def fetch_external_data(url: str) -> dict:
    """Fetch data from external API."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

# Async version
async def async_retry(
    func: Callable,
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0
):
    """Async retry helper."""
    current_delay = delay
    
    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(current_delay)
            current_delay *= backoff

# ❌ BAD: No retry logic for external calls
def fetch_data(url: str):
    response = requests.get(url)  # Fails permanently on temporary errors
    return response.json()
```

---

<a name="logging"></a>
## 7. Logging & Monitoring

### 7.1 Structured Logging

```python
# ✅ GOOD: Use structured logging

import logging
import json
from datetime import datetime
from typing import Dict, Any

# Configure structured logging
class JSONFormatter(logging.Formatter):
    """Format logs as JSON."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        return json.dumps(log_data)

# Configure logger
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Usage with context
logger.info(
    "User login successful",
    extra={"user_id": 123, "request_id": "abc-123"}
)

logger.error(
    "Payment processing failed",
    extra={"order_id": 456, "amount": 99.99},
    exc_info=True  # Include exception traceback
)

# ❌ BAD: Unstructured logging
logger.info(f"User 123 logged in")  # Hard to parse
logger.error("Error occurred")  # No context
```

### 7.2 Log Levels

```python
# ✅ GOOD: Use appropriate log levels

import logging

logger = logging.getLogger(__name__)

# DEBUG: Detailed diagnostic information
logger.debug(f"Database query: {query}")
logger.debug(f"Function called with params: {params}")

# INFO: General informational messages
logger.info("User registration completed", extra={"user_id": user.id})
logger.info("Email sent successfully", extra={"recipient": email})

# WARNING: Warning messages for potentially harmful situations
logger.warning(
    "API rate limit approaching",
    extra={"current_rate": 950, "limit": 1000}
)
logger.warning("Deprecated function called", extra={"function": "old_method"})

# ERROR: Error events that might still allow the application to continue
logger.error(
    "Failed to send email",
    extra={"recipient": email, "error": str(e)},
    exc_info=True
)

# CRITICAL: Very severe error events
logger.critical(
    "Database connection lost",
    extra={"db_host": db_host},
    exc_info=True
)

# ❌ BAD: Using print statements
print("User logged in")  # Goes to stdout, not logged properly
print(f"Error: {e}")  # No log level, no structure

# ❌ BAD: Using wrong log levels
logger.error("User logged in")  # This is INFO, not ERROR
logger.debug("Critical system failure")  # Should be CRITICAL
```

### 7.3 Request Logging Middleware

```python
# ✅ GOOD: Log all requests

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all HTTP requests."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_ip": request.client.host,
            }
        )
        
        # Process request
        start_time = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration": f"{duration:.3f}s",
                }
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration": f"{duration:.3f}s",
                    "error": str(e),
                },
                exc_info=True
            )
            raise

# Add middleware to app
app.add_middleware(RequestLoggingMiddleware)
```

### 7.4 Application Monitoring

```python
# ✅ GOOD: Add metrics and monitoring

from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

# Middleware to track metrics
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Record metrics
            request_count.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            duration = time.time() - start_time
            request_duration.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            return response
            
        except Exception as e:
            request_count.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            raise

# Expose metrics endpoint
from prometheus_client import make_asgi_app

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Custom business metrics
def track_user_login(user_id: int):
    """Track user login."""
    active_users.inc()
    logger.info("User logged in", extra={"user_id": user_id})

def track_user_logout(user_id: int):
    """Track user logout."""
    active_users.dec()
    logger.info("User logged out", extra={"user_id": user_id})
```

---

**[This is Part 1 of the Best Practices Guide. Would you like me to continue with the remaining sections: Security, Testing, Performance, Async Programming, Docker & Deployment, Documentation, and Code Review Checklist?]**

What's covered so far:
✅ Code Quality & Style (PEP 8, type hints, linters)
✅ Project Structure (layered architecture)
✅ Configuration Management (environment-based, secrets)
✅ Database Best Practices (pooling, transactions, N+1, indexes, migrations)
✅ API Design (REST, validation, error handling, versioning, pagination)
✅ Error Handling (exceptions, retry logic)
✅ Logging & Monitoring (structured logging, metrics)

Shall I continue with the remaining sections?