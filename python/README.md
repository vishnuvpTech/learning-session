# Senior Python Backend Developer - Complete Skills Tutorial
## Master the Skills Required for Senior-Level Python Backend Engineering

**Version:** 1.0  
**Last Updated:** March 2026  
**Target Audience:** Mid-level Python developers transitioning to senior roles  
**Prerequisites:** 2-3 years Python backend experience  

---

## Table of Contents

1. [Senior Role Requirements](#requirements)
2. [Advanced Python Mastery](#python-mastery)
3. [FastAPI - Modern Python Framework](#fastapi)
4. [Django & Django REST Framework](#django)
5. [Database Mastery](#database)
6. [API Design & Architecture](#api-design)
7. [Microservices Architecture](#microservices)
8. [Authentication & Security](#security)
9. [Testing & Quality Assurance](#testing)
10. [Performance Optimization](#performance)
11. [DevOps & Deployment](#devops)
12. [System Design](#system-design)
13. [Practical Projects](#projects)
14. [Senior Skills Assessment](#assessment)

---

<a name="requirements"></a>
## 1. Senior Role Requirements

### What Distinguishes a Senior Backend Developer?

| Mid-Level | Senior Level |
|-----------|--------------|
| Implements features | **Designs architecture** |
| Follows patterns | **Chooses appropriate patterns** |
| Writes code | **Reviews and mentors** |
| Fixes bugs | **Prevents bugs systematically** |
| Uses tools | **Evaluates and selects tools** |
| Completes tasks | **Defines technical strategy** |
| Works on tickets | **Breaks down complex problems** |
| Individual contributor | **Technical leader** |

### Core Senior Competencies

**Technical Skills:**
- ✅ Advanced Python programming (async, metaclasses, decorators)
- ✅ Architectural design patterns
- ✅ Database optimization and sharding
- ✅ API design best practices
- ✅ Microservices architecture
- ✅ Security and authentication
- ✅ Performance optimization
- ✅ Testing strategies (TDD/BDD)
- ✅ DevOps and CI/CD
- ✅ System design and scalability

**Soft Skills:**
- ✅ Mentoring junior developers
- ✅ Technical documentation
- ✅ Code review leadership
- ✅ Architecture decision making
- ✅ Cross-team collaboration
- ✅ Technical debt management

---

<a name="python-mastery"></a>
## 2. Advanced Python Mastery

### 2.1 Async Programming Deep Dive

#### Understanding asyncio

```python
import asyncio
from typing import List, Dict, Any

# Basic async function
async def fetch_user(user_id: int) -> Dict[str, Any]:
    """Simulate async database call"""
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}

# Running async function
async def main():
    user = await fetch_user(1)
    print(user)

# Run
asyncio.run(main())

# Concurrent execution
async def fetch_multiple_users(user_ids: List[int]) -> List[Dict[str, Any]]:
    """Fetch users concurrently"""
    tasks = [fetch_user(uid) for uid in user_ids]
    users = await asyncio.gather(*tasks)
    return users

# Usage
async def main():
    users = await fetch_multiple_users([1, 2, 3, 4, 5])
    print(f"Fetched {len(users)} users concurrently")

asyncio.run(main())
```

#### Async Context Managers

```python
import aiofiles
from contextlib import asynccontextmanager

class AsyncDatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    async def __aenter__(self):
        """Called when entering context"""
        print("Connecting to database...")
        await asyncio.sleep(0.1)  # Simulate connection
        self.connection = f"Connected to {self.connection_string}"
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting context"""
        print("Closing database connection...")
        await asyncio.sleep(0.1)  # Simulate cleanup
        self.connection = None
    
    async def execute(self, query: str):
        """Execute query"""
        if not self.connection:
            raise RuntimeError("Not connected")
        print(f"Executing: {query}")
        await asyncio.sleep(0.05)
        return {"status": "success"}

# Usage
async def main():
    async with AsyncDatabaseConnection("postgresql://localhost/db") as db:
        result = await db.execute("SELECT * FROM users")
        print(result)

asyncio.run(main())

# Using asynccontextmanager decorator
@asynccontextmanager
async def get_db_connection(connection_string: str):
    """Context manager for database connection"""
    connection = await connect_to_database(connection_string)
    try:
        yield connection
    finally:
        await connection.close()

async def connect_to_database(connection_string: str):
    """Simulate database connection"""
    await asyncio.sleep(0.1)
    return {"connection": connection_string}

# Usage
async def main():
    async with get_db_connection("postgresql://localhost/db") as conn:
        print(f"Using connection: {conn}")
```

#### Async Generators

```python
async def fetch_users_paginated(page_size: int = 100):
    """Async generator for paginated results"""
    page = 1
    while True:
        # Simulate API call
        await asyncio.sleep(0.1)
        users = [
            {"id": i, "name": f"User {i}"} 
            for i in range((page-1)*page_size, page*page_size)
        ]
        
        if not users:
            break
        
        for user in users:
            yield user
        
        page += 1
        if page > 5:  # Limit for demo
            break

# Usage
async def main():
    count = 0
    async for user in fetch_users_paginated(page_size=10):
        count += 1
        if count <= 5:
            print(user)
    print(f"Total users: {count}")

asyncio.run(main())
```

### 2.2 Advanced Type Hints

```python
from typing import (
    TypeVar, Generic, Protocol, Union, Optional,
    List, Dict, Callable, Awaitable, overload
)
from dataclasses import dataclass
from datetime import datetime

# Generic types
T = TypeVar('T')

class Repository(Generic[T]):
    """Generic repository pattern"""
    
    def __init__(self, model_class: type[T]):
        self.model_class = model_class
        self._storage: List[T] = []
    
    def add(self, item: T) -> T:
        self._storage.append(item)
        return item
    
    def get(self, id: int) -> Optional[T]:
        for item in self._storage:
            if hasattr(item, 'id') and item.id == id:
                return item
        return None
    
    def all(self) -> List[T]:
        return self._storage.copy()

# Usage
@dataclass
class User:
    id: int
    name: str
    email: str

user_repo = Repository[User](User)
user = user_repo.add(User(id=1, name="Alice", email="alice@example.com"))

# Protocol for duck typing
class Saveable(Protocol):
    """Protocol for objects that can be saved"""
    def save(self) -> None: ...
    def delete(self) -> None: ...

def persist(obj: Saveable) -> None:
    """Function that works with any Saveable object"""
    obj.save()

# Callable types
UserValidator = Callable[[User], bool]

def validate_user(user: User, validator: UserValidator) -> bool:
    return validator(user)

# Example validator
def is_valid_email(user: User) -> bool:
    return '@' in user.email

# Awaitable for async functions
async def fetch_data(url: str) -> Dict[str, Any]:
    await asyncio.sleep(0.1)
    return {"data": "value"}

DataFetcher = Callable[[str], Awaitable[Dict[str, Any]]]

# Function overloading
@overload
def process_data(data: str) -> str: ...

@overload
def process_data(data: int) -> int: ...

@overload
def process_data(data: List[str]) -> List[str]: ...

def process_data(data: Union[str, int, List[str]]) -> Union[str, int, List[str]]:
    """Process different types of data"""
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, int):
        return data * 2
    elif isinstance(data, list):
        return [item.upper() for item in data]
    raise TypeError(f"Unsupported type: {type(data)}")
```

### 2.3 Decorators and Metaclasses

```python
import functools
import time
from typing import Callable, Any

# Function decorator with arguments
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator with configurable attempts and delay"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, delay=0.5)
def fetch_data_from_api(url: str) -> dict:
    # Simulate API call that might fail
    import random
    if random.random() < 0.7:
        raise ConnectionError("API temporarily unavailable")
    return {"data": "success"}

# Class decorator
def singleton(cls):
    """Singleton pattern decorator"""
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        print(f"Creating database connection to {connection_string}")

# Usage
db1 = Database("postgresql://localhost/db")
db2 = Database("postgresql://localhost/db")
print(db1 is db2)  # True - same instance

# Metaclass example
class APIEndpoint(type):
    """Metaclass for automatic API endpoint registration"""
    
    endpoints = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        
        # Register endpoint if it has a path attribute
        if 'path' in attrs:
            mcs.endpoints[attrs['path']] = cls
        
        return cls

class UserEndpoint(metaclass=APIEndpoint):
    path = "/api/users"
    
    @classmethod
    def get(cls):
        return {"users": []}
    
    @classmethod
    def post(cls, data):
        return {"created": True}

class ProductEndpoint(metaclass=APIEndpoint):
    path = "/api/products"
    
    @classmethod
    def get(cls):
        return {"products": []}

# Access registered endpoints
print(APIEndpoint.endpoints)
# {'/api/users': <class 'UserEndpoint'>, '/api/products': <class 'ProductEndpoint'>}

# Performance measurement decorator
def measure_time(func: Callable) -> Callable:
    """Measure execution time of function"""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    
    # Return appropriate wrapper based on function type
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper

# Works with both sync and async functions
@measure_time
def process_data(data: List[int]) -> int:
    time.sleep(0.1)
    return sum(data)

@measure_time
async def fetch_data(url: str) -> dict:
    await asyncio.sleep(0.2)
    return {"data": "value"}
```

### 2.4 Context Managers and Resource Management

```python
from contextlib import contextmanager, suppress
from typing import Generator

# Custom context manager
class FileHandler:
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # Return False to propagate exceptions
        return False

# Using contextmanager decorator
@contextmanager
def database_transaction(connection):
    """Context manager for database transaction"""
    transaction = connection.begin()
    try:
        yield transaction
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise

# Multiple context managers
class ResourcePool:
    """Pool of reusable resources"""
    
    def __init__(self, create_resource: Callable, max_size: int = 10):
        self.create_resource = create_resource
        self.max_size = max_size
        self._available = []
        self._in_use = set()
    
    @contextmanager
    def acquire(self) -> Generator[Any, None, None]:
        """Acquire resource from pool"""
        if self._available:
            resource = self._available.pop()
        elif len(self._in_use) < self.max_size:
            resource = self.create_resource()
        else:
            raise RuntimeError("No resources available")
        
        self._in_use.add(resource)
        try:
            yield resource
        finally:
            self._in_use.remove(resource)
            self._available.append(resource)

# Usage
def create_connection():
    return {"connection": "db"}

pool = ResourcePool(create_connection, max_size=5)

with pool.acquire() as conn:
    print(f"Using connection: {conn}")

# Suppress specific exceptions
with suppress(FileNotFoundError):
    # This won't raise if file doesn't exist
    with open('nonexistent.txt') as f:
        content = f.read()
```

### 2.5 Advanced Data Structures

```python
from collections import defaultdict, Counter, deque, namedtuple
from dataclasses import dataclass, field
from typing import Dict, List, Set
from datetime import datetime
import heapq

# Using defaultdict for grouping
def group_users_by_role(users: List[Dict]) -> Dict[str, List[Dict]]:
    """Group users by their role"""
    grouped = defaultdict(list)
    for user in users:
        grouped[user['role']].append(user)
    return dict(grouped)

# Counter for frequency analysis
def analyze_log_levels(logs: List[str]) -> Dict[str, int]:
    """Count log level occurrences"""
    levels = [log.split()[0] for log in logs if log]
    return Counter(levels)

# Deque for efficient queue operations
class TaskQueue:
    """Efficient task queue using deque"""
    
    def __init__(self):
        self._queue = deque()
    
    def add_task(self, task: Dict[str, Any], priority: bool = False):
        """Add task to queue"""
        if priority:
            self._queue.appendleft(task)
        else:
            self._queue.append(task)
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get next task from queue"""
        if self._queue:
            return self._queue.popleft()
        return None
    
    def __len__(self):
        return len(self._queue)

# Priority Queue with heapq
class PriorityTaskQueue:
    """Priority queue for tasks"""
    
    def __init__(self):
        self._queue = []
        self._counter = 0
    
    def add_task(self, priority: int, task: Dict[str, Any]):
        """Add task with priority (lower number = higher priority)"""
        # Counter ensures FIFO for same priority
        heapq.heappush(self._queue, (priority, self._counter, task))
        self._counter += 1
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get highest priority task"""
        if self._queue:
            _, _, task = heapq.heappop(self._queue)
            return task
        return None

# Advanced dataclass with custom methods
@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    roles: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role"""
        return role in self.roles
    
    def add_role(self, role: str) -> None:
        """Add role to user"""
        if role not in self.roles:
            self.roles.append(role)
    
    def __post_init__(self):
        """Validation after initialization"""
        if '@' not in self.email:
            raise ValueError(f"Invalid email: {self.email}")

# Immutable dataclass
@dataclass(frozen=True)
class Config:
    """Immutable configuration"""
    api_url: str
    api_key: str
    timeout: int = 30
    
    def with_timeout(self, timeout: int) -> 'Config':
        """Create new config with different timeout"""
        return Config(
            api_url=self.api_url,
            api_key=self.api_key,
            timeout=timeout
        )

# Named tuple for lightweight data structures
UserRecord = namedtuple('UserRecord', ['id', 'name', 'email'])

# Usage
user = UserRecord(id=1, name='Alice', email='alice@example.com')
print(user.name)  # Alice
print(user._asdict())  # {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}
```

---

<a name="fastapi"></a>
## 3. FastAPI - Modern Python Framework

### 3.1 FastAPI Fundamentals

```python
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="User Management API",
    description="API for managing users",
    version="1.0.0"
)

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

# In-memory database (replace with real DB)
users_db: Dict[int, User] = {}
user_id_counter = 1

# Endpoints
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    global user_id_counter
    
    # Check if username exists
    if any(u.username == user.username for u in users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        created_at=datetime.now()
    )
    
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    return new_user

@app.get("/users/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False
):
    """List all users with pagination"""
    users = list(users_db.values())
    
    if active_only:
        users = [u for u in users if u.is_active]
    
    return users[skip : skip + limit]

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """Update user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    stored_user = users_db[user_id]
    update_data = user_update.dict(exclude_unset=True)
    
    updated_user = stored_user.copy(update=update_data)
    users_db[user_id] = updated_user
    
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    del users_db[user_id]
    return None
```

### 3.2 Dependency Injection

```python
from fastapi import Depends, Header, HTTPException
from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Database dependency
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Authentication dependency
async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """Get current authenticated user"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Verify token (simplified)
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    token = authorization[7:]
    # Verify and decode token here
    user = {"id": 1, "username": "testuser"}
    return user

# Permission dependency
class PermissionChecker:
    """Check if user has required permission"""
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    async def __call__(
        self,
        current_user: Dict = Depends(get_current_user)
    ) -> Dict[str, Any]:
        if not self.has_permission(current_user, self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    def has_permission(self, user: Dict, permission: str) -> bool:
        # Check user permissions
        return True  # Simplified

# Using dependencies
@app.get("/users/me")
async def get_current_user_info(
    current_user: Dict = Depends(get_current_user)
):
    """Get current user information"""
    return current_user

@app.get("/admin/users")
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
    current_user: Dict = Depends(PermissionChecker("admin"))
):
    """Admin-only endpoint"""
    # Access db and current_user here
    return {"message": "Admin access granted"}

# Multiple dependencies
class CommonParams:
    """Common query parameters"""
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None
    ):
        self.skip = skip
        self.limit = limit
        self.sort_by = sort_by

@app.get("/items/")
async def list_items(
    commons: CommonParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """List items with common parameters"""
    return {
        "skip": commons.skip,
        "limit": commons.limit,
        "sort_by": commons.sort_by
    }
```

### 3.3 Background Tasks and Async

```python
from fastapi import BackgroundTasks
from fastapi.concurrency import run_in_threadpool
import asyncio
import aiofiles
from datetime import datetime

# Background task
def send_email(email: str, message: str):
    """Simulate sending email"""
    import time
    print(f"Sending email to {email}")
    time.sleep(2)  # Simulate slow operation
    print(f"Email sent to {email}")

@app.post("/users/signup")
async def signup_user(
    user: UserCreate,
    background_tasks: BackgroundTasks
):
    """Create user and send welcome email in background"""
    # Create user
    new_user = await create_user(user)
    
    # Add background task
    background_tasks.add_task(
        send_email,
        user.email,
        f"Welcome {user.username}!"
    )
    
    return new_user

# Multiple background tasks
@app.post("/users/bulk-import")
async def import_users(
    users: List[UserCreate],
    background_tasks: BackgroundTasks
):
    """Import multiple users"""
    created_users = []
    
    for user in users:
        new_user = await create_user(user)
        created_users.append(new_user)
        
        # Send welcome email for each
        background_tasks.add_task(send_email, user.email, "Welcome!")
    
    # Also create audit log
    background_tasks.add_task(
        log_bulk_import,
        len(created_users),
        datetime.now()
    )
    
    return {"imported": len(created_users)}

async def log_bulk_import(count: int, timestamp: datetime):
    """Log bulk import operation"""
    async with aiofiles.open('import_log.txt', 'a') as f:
        await f.write(f"{timestamp}: Imported {count} users\n")

# Running CPU-bound tasks
@app.post("/process-data")
async def process_large_dataset(data: List[int]):
    """Process CPU-intensive data"""
    # Run in thread pool to avoid blocking event loop
    result = await run_in_threadpool(cpu_intensive_task, data)
    return {"result": result}

def cpu_intensive_task(data: List[int]) -> int:
    """Simulate CPU-intensive operation"""
    return sum(x ** 2 for x in data)

# Async file operations
@app.post("/upload-file")
async def upload_file(content: str):
    """Upload file asynchronously"""
    filename = f"upload_{datetime.now().timestamp()}.txt"
    
    async with aiofiles.open(filename, 'w') as f:
        await f.write(content)
    
    return {"filename": filename, "size": len(content)}

# Concurrent API calls
import httpx

async def fetch_user_details(user_id: int) -> Dict:
    """Fetch user details from external API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

@app.get("/users/{user_id}/complete-profile")
async def get_complete_user_profile(user_id: int):
    """Get user profile from multiple sources"""
    # Fetch from multiple sources concurrently
    local_user, external_data = await asyncio.gather(
        get_user(user_id),
        fetch_user_details(user_id)
    )
    
    return {
        "local": local_user,
        "external": external_data
    }
```

### 3.4 Middleware and Error Handling

```python
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
import time
import logging

# Custom middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Before request
        start_time = time.time()
        request_id = str(time.time())
        
        logging.info(f"Request {request_id}: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # After request
        duration = time.time() - start_time
        logging.info(
            f"Request {request_id} completed in {duration:.2f}s "
            f"with status {response.status_code}"
        )
        
        # Add custom header
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(duration)
        
        return response

# Apply middleware
app.add_middleware(RequestLoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler
class UserNotFoundError(Exception):
    """Custom exception for user not found"""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    """Handle UserNotFoundError"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "user_not_found",
            "message": str(exc),
            "user_id": exc.user_id
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred"
        }
    )

# Validation error handler
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation error response"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "detail": exc.errors(),
        }
    )
```

### 3.5 API Versioning

```python
from fastapi import APIRouter

# Version 1 router
router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])

@router_v1.get("/users/{user_id}")
async def get_user_v1(user_id: int):
    """Version 1 of get user endpoint"""
    return {"version": 1, "user_id": user_id}

# Version 2 router
router_v2 = APIRouter(prefix="/api/v2", tags=["v2"])

@router_v2.get("/users/{user_id}")
async def get_user_v2(user_id: int):
    """Version 2 with additional fields"""
    return {
        "version": 2,
        "user_id": user_id,
        "created_at": datetime.now(),
        "metadata": {}
    }

# Include routers
app.include_router(router_v1)
app.include_router(router_v2)

# Header-based versioning
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    api_version: str = Header(default="1")
):
    """Get user with header-based versioning"""
    if api_version == "2":
        return await get_user_v2(user_id)
    return await get_user_v1(user_id)
```

---

<a name="django"></a>
## 4. Django & Django REST Framework

### 4.1 Django ORM Advanced Patterns

```python
from django.db import models
from django.db.models import (
    Q, F, Count, Sum, Avg, Max, Min,
    Prefetch, Case, When, Value
)
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MinValueValidator, MaxValueValidator

# Advanced model with custom methods
class User(models.Model):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    @property
    def is_premium(self):
        """Check if user has active premium subscription"""
        return self.subscriptions.filter(
            is_active=True,
            plan__tier='premium'
        ).exists()

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = ArrayField(models.CharField(max_length=50), default=list)
    metadata = models.JSONField(default=dict)
    view_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'posts'
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['published_at']),
        ]
    
    def increment_views(self):
        """Atomic increment of view count"""
        Post.objects.filter(pk=self.pk).update(view_count=F('view_count') + 1)

# Complex queries
class UserQuerySet(models.QuerySet):
    """Custom queryset with reusable filters"""
    
    def active(self):
        return self.filter(is_active=True)
    
    def with_post_count(self):
        return self.annotate(post_count=Count('posts'))
    
    def premium_users(self):
        return self.filter(
            subscriptions__is_active=True,
            subscriptions__plan__tier='premium'
        ).distinct()

class UserManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def with_post_count(self):
        return self.get_queryset().with_post_count()

# Apply custom manager
User.objects = UserManager()

# Usage examples:
# users = User.objects.active().with_post_count()
# premium = User.objects.premium_users()

# Optimized queries with select_related and prefetch_related
def get_posts_with_author():
    """Fetch posts with author in single query"""
    return Post.objects.select_related('author').all()

def get_users_with_posts():
    """Fetch users with their posts"""
    return User.objects.prefetch_related('posts').all()

# Complex prefetch
def get_users_with_published_posts():
    """Fetch users with only published posts"""
    published_posts = Prefetch(
        'posts',
        queryset=Post.objects.filter(published_at__isnull=False),
        to_attr='published_posts_list'
    )
    return User.objects.prefetch_related(published_posts)

# Aggregation queries
def get_post_statistics():
    """Get statistics about posts"""
    from django.db.models import Avg, Max, Min, Count
    
    stats = Post.objects.aggregate(
        total_posts=Count('id'),
        avg_views=Avg('view_count'),
        max_views=Max('view_count'),
        min_views=Min('view_count')
    )
    return stats

# Annotate with conditional expressions
def get_users_with_premium_status():
    """Annotate users with premium status"""
    from django.db.models import Case, When, Value, BooleanField
    
    return User.objects.annotate(
        is_premium=Case(
            When(
                subscriptions__is_active=True,
                subscriptions__plan__tier='premium',
                then=Value(True)
            ),
            default=Value(False),
            output_field=BooleanField()
        )
    )

# Complex Q objects
def search_users(query: str):
    """Search users by username, email, or full name"""
    return User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(full_name__icontains=query)
    )

# Bulk operations
def bulk_create_posts(posts_data: List[Dict]):
    """Bulk create posts"""
    posts = [Post(**data) for data in posts_data]
    Post.objects.bulk_create(posts, batch_size=1000)

def bulk_update_views(post_ids: List[int]):
    """Bulk update view counts"""
    posts = Post.objects.filter(id__in=post_ids)
    posts.update(view_count=F('view_count') + 1)
```

### 4.2 Django REST Framework

```python
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Serializers
class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'post_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_username(self, value):
        """Custom validation for username"""
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters"
            )
        return value

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_id', 'title', 'content',
            'tags', 'view_count', 'published_at', 'created_at'
        ]
        read_only_fields = ['id', 'view_count', 'created_at']
    
    def create(self, validated_data):
        """Custom create with default values"""
        validated_data['view_count'] = 0
        return super().create(validated_data)

# Nested serializer
class UserDetailSerializer(UserSerializer):
    posts = PostSerializer(many=True, read_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['posts']

# Custom pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# ViewSets
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Custom queryset with filtering"""
        queryset = User.objects.active().with_post_count()
        
        # Filter by query parameter
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializer for detail view"""
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Custom action to deactivate user"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})
    
    @action(detail=False, methods=['get'])
    def premium(self, request):
        """List premium users"""
        premium_users = User.objects.premium_users()
        serializer = self.get_serializer(premium_users, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model"""
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set author to current user"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a post"""
        post = self.get_object()
        post.published_at = timezone.now()
        post.save()
        return Response({'status': 'post published'})
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment view count"""
        post = self.get_object()
        post.increment_views()
        return Response({'view_count': post.view_count})

# Router setup
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

# URL patterns
from django.urls import path, include

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 4.3 Django Signals and Celery Integration

```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from celery import shared_task

# Signals
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """Signal handler for user creation"""
    if created:
        # Send welcome email asynchronously
        send_welcome_email.delay(instance.id)

@receiver(pre_delete, sender=Post)
def post_deleted(sender, instance, **kwargs):
    """Clean up before deleting post"""
    # Log deletion
    import logging
    logging.info(f"Deleting post {instance.id}: {instance.title}")

# Celery tasks
@shared_task
def send_welcome_email(user_id: int):
    """Send welcome email to new user"""
    try:
        user = User.objects.get(id=user_id)
        # Send email logic here
        print(f"Sending welcome email to {user.email}")
        return f"Email sent to {user.email}"
    except User.DoesNotExist:
        return f"User {user_id} not found"

@shared_task
def process_batch_posts(post_ids: List[int]):
    """Process posts in batch"""
    posts = Post.objects.filter(id__in=post_ids)
    
    for post in posts:
        # Process each post
        post.increment_views()
    
    return f"Processed {posts.count()} posts"

@shared_task(bind=True, max_retries=3)
def fetch_external_data(self, url: str):
    """Fetch data from external API with retry"""
    import requests
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

# Periodic tasks (celerybeat)
from celery.schedules import crontab

@shared_task
def cleanup_old_posts():
    """Delete posts older than 1 year"""
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=365)
    deleted_count, _ = Post.objects.filter(
        created_at__lt=cutoff_date
    ).delete()
    
    return f"Deleted {deleted_count} old posts"

# Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'cleanup-old-posts': {
        'task': 'myapp.tasks.cleanup_old_posts',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
}
```

---

<a name="database"></a>
## 5. Database Mastery

### 5.1 PostgreSQL Advanced Features

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, TSVECTOR
from sqlalchemy import func

Base = declarative_base()

# Advanced PostgreSQL features
class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    tags = Column(ARRAY(String))  # PostgreSQL array
    metadata = Column(JSONB)  # JSON column with indexing support
    search_vector = Column(TSVECTOR)  # Full-text search
    created_at = Column(DateTime, server_default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_articles_tags', 'tags', postgresql_using='gin'),  # GIN index for arrays
        Index('idx_articles_metadata', 'metadata', postgresql_using='gin'),  # GIN index for JSONB
        Index('idx_articles_search', 'search_vector', postgresql_using='gin'),  # Full-text search index
    )

# JSONB queries
def query_jsonb_field(session):
    """Query JSONB fields"""
    # Query nested JSON
    articles = session.query(Article).filter(
        Article.metadata['author']['name'].astext == 'John Doe'
    ).all()
    
    # Check if key exists
    articles = session.query(Article).filter(
        Article.metadata.has_key('published')
    ).all()
    
    # Containment query
    articles = session.query(Article).filter(
        Article.metadata.contains({'category': 'tech'})
    ).all()
    
    return articles

# Array queries
def query_array_field(session):
    """Query array fields"""
    # Check if array contains value
    articles = session.query(Article).filter(
        Article.tags.contains(['python'])
    ).all()
    
    # Check for overlap
    articles = session.query(Article).filter(
        Article.tags.overlap(['python', 'django'])
    ).all()
    
    return articles

# Full-text search
def full_text_search(session, query: str):
    """Perform full-text search"""
    # Create tsvector from text
    search_query = func.to_tsquery('english', query)
    
    articles = session.query(Article).filter(
        Article.search_vector.match(search_query)
    ).order_by(
        func.ts_rank(Article.search_vector, search_query).desc()
    ).all()
    
    return articles

# Window functions
def get_ranked_articles(session):
    """Get articles with ranking"""
    from sqlalchemy import func, over
    
    articles = session.query(
        Article,
        func.row_number().over(
            order_by=Article.created_at.desc()
        ).label('rank'),
        func.dense_rank().over(
            partition_by=Article.tags,
            order_by=Article.created_at.desc()
        ).label('rank_in_category')
    ).all()
    
    return articles

# CTEs (Common Table Expressions)
def get_articles_with_stats(session):
    """Use CTE to get articles with statistics"""
    from sqlalchemy import select, func
    
    # Define CTE
    article_stats = select(
        Article.id,
        func.array_length(Article.tags, 1).label('tag_count')
    ).cte('article_stats')
    
    # Use CTE in main query
    results = session.query(
        Article,
        article_stats.c.tag_count
    ).join(
        article_stats,
        Article.id == article_stats.c.id
    ).all()
    
    return results

# Partitioning (manual example)
def create_partitioned_table(engine):
    """Create partitioned table"""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE logs (
                id SERIAL,
                message TEXT,
                created_at TIMESTAMP NOT NULL
            ) PARTITION BY RANGE (created_at);
            
            CREATE TABLE logs_2024_01 PARTITION OF logs
            FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
            
            CREATE TABLE logs_2024_02 PARTITION OF logs
            FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
        """))
```

### 5.2 Query Optimization

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import time

# Query analysis
def analyze_query(session: Session, query):
    """Analyze query performance"""
    # Get EXPLAIN output
    explain = session.execute(
        text(f"EXPLAIN ANALYZE {query}")
    ).fetchall()
    
    for row in explain:
        print(row[0])

# Index strategies
def create_indexes(engine):
    """Create appropriate indexes"""
    with engine.connect() as conn:
        # B-tree index (default)
        conn.execute(text(
            "CREATE INDEX idx_articles_title ON articles(title)"
        ))
        
        # Partial index (for common filters)
        conn.execute(text(
            "CREATE INDEX idx_active_articles ON articles(created_at) "
            "WHERE deleted_at IS NULL"
        ))
        
        # Composite index (for common query patterns)
        conn.execute(text(
            "CREATE INDEX idx_articles_author_date "
            "ON articles(author_id, created_at DESC)"
        ))
        
        # Covering index (include non-key columns)
        conn.execute(text(
            "CREATE INDEX idx_articles_covering "
            "ON articles(author_id) INCLUDE (title, created_at)"
        ))

# Connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,  # Number of connections to maintain
    max_overflow=10,  # Maximum overflow connections
    pool_timeout=30,  # Timeout for getting connection from pool
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Verify connections before using
)

# Batch operations
def bulk_insert_optimized(session: Session, data: List[Dict]):
    """Optimized bulk insert"""
    # Use bulk_insert_mappings for better performance
    session.bulk_insert_mappings(Article, data)
    session.commit()

def bulk_update_optimized(session: Session, updates: List[Dict]):
    """Optimized bulk update"""
    # Use bulk_update_mappings
    session.bulk_update_mappings(Article, updates)
    session.commit()

# N+1 query prevention
def get_articles_with_authors(session: Session):
    """Prevent N+1 queries with eager loading"""
    from sqlalchemy.orm import joinedload
    
    # Bad: N+1 queries
    # articles = session.query(Article).all()
    # for article in articles:
    #     print(article.author.name)  # Triggers separate query for each
    
    # Good: Single query with join
    articles = session.query(Article).options(
        joinedload(Article.author)
    ).all()
    
    for article in articles:
        print(article.author.name)  # No additional queries
    
    return articles

# Query result caching
from functools import lru_cache

@lru_cache(maxsize=128)
def get_popular_tags(session_id: str) -> List[str]:
    """Cache query results"""
    # This would be called with actual session
    # Simplified for example
    return ['python', 'django', 'fastapi']

# Database replication (read replicas)
# Create separate engines for read and write operations
write_engine = create_engine('postgresql://master/db')
read_engine = create_engine('postgresql://replica/db')

class RoutedSession(Session):
    """Session that routes reads to replica"""
    
    def get_bind(self, mapper=None, clause=None):
        if self._flushing:
            return write_engine
        return read_engine

# Usage
def get_data_from_replica():
    """Read from replica"""
    session = RoutedSession()
    articles = session.query(Article).all()
    session.close()
    return articles
```

### 5.3 Database Migrations

```python
# Alembic migrations
"""
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add user table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
"""

# Example migration file
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    """Upgrade database schema"""
    # Create table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(150), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    
    # Add column to existing table
    op.add_column('articles', sa.Column('view_count', sa.Integer(), server_default='0'))
    
    # Create enum type
    status_enum = postgresql.ENUM('draft', 'published', 'archived', name='article_status')
    status_enum.create(op.get_bind())
    op.add_column('articles', sa.Column('status', status_enum, server_default='draft'))

def downgrade():
    """Rollback database schema"""
    # Drop column
    op.drop_column('articles', 'status')
    op.drop_column('articles', 'view_count')
    
    # Drop enum type
    op.execute('DROP TYPE article_status')
    
    # Drop index
    op.drop_index('idx_users_email', table_name='users')
    
    # Drop table
    op.drop_table('users')

# Data migrations
def upgrade():
    """Migrate data"""
    from sqlalchemy import table, column
    from sqlalchemy.sql import select
    
    # Define table structure for data migration
    users = table('users',
        column('id', sa.Integer),
        column('username', sa.String),
        column('legacy_field', sa.String),
        column('new_field', sa.String)
    )
    
    # Get connection
    conn = op.get_bind()
    
    # Migrate data
    results = conn.execute(select(users.c.id, users.c.legacy_field))
    
    for row in results:
        # Transform and update data
        new_value = transform_legacy_data(row.legacy_field)
        conn.execute(
            users.update().where(users.c.id == row.id).values(new_field=new_value)
        )
    
    # Remove old column
    op.drop_column('users', 'legacy_field')

def transform_legacy_data(value: str) -> str:
    """Transform legacy data to new format"""
    return value.upper()  # Example transformation
```

---