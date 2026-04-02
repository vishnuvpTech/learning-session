# 🐍 Python Advanced – Structured Learning & Interview Preparation Guide

> **Level:** Intermediate → Expert  
> **Prerequisites:** Python Basics (variables, functions, OOP, file I/O)  
> **Goal:** Master advanced Python internals and patterns to excel in senior-level interviews and production codebases

---

## Table of Contents
1. [Module 1: Iterators & Generators](#module-1)
2. [Module 2: Decorators & Closures](#module-2)
3. [Module 3: Context Managers](#module-3)
4. [Module 4: Functional Programming Tools](#module-4)
5. [Module 5: Advanced OOP – Metaclasses, Descriptors & Slots](#module-5)
6. [Module 6: Concurrency – Threading, Multiprocessing & AsyncIO](#module-6)
7. [Module 7: Memory Management & Performance Optimization](#module-7)
8. [Module 8: Type Hints, Protocols & Structural Subtyping](#module-8)
9. [Module 9: Advanced Data Structures & Collections](#module-9)
10. [Module 10: Design Patterns in Python](#module-10)
11. [Interview Questions](#interview-questions)
12. [Coding Challenges](#coding-challenges)
13. [Final Summary](#final-summary)

---

## Module 1: Iterators & Generators {#module-1}

### 📖 Explanation
An **iterator** is any object implementing `__iter__()` and `__next__()`. A **generator** is a special function using `yield` that automatically creates an iterator — lazily producing values one at a time. This is the foundation of Python's memory-efficient data pipelines.

### 🔑 Key Concepts
- **Iterable** — has `__iter__()` (list, str, dict, etc.)
- **Iterator** — has `__iter__()` + `__next__()` + raises `StopIteration`
- **Generator function** — uses `yield` instead of `return`
- **Generator expression** — `(x for x in iterable)`
- **`yield from`** — delegate to sub-generators
- **`send()`** — send values into a running generator (coroutine pattern)
- **Infinite iterators** — `itertools.count`, `itertools.cycle`

### 💻 Example
```python
# --- Custom Iterator ---
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self         # iterator is itself

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for n in CountDown(3):
    print(n)    # 3, 2, 1


# --- Generator Function ---
def fibonacci():
    """Infinite Fibonacci generator — never runs out of memory."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# --- yield from (delegating generators) ---
def chain(*iterables):
    for it in iterables:
        yield from it

print(list(chain([1, 2], "AB", (3, 4))))
# [1, 2, 'A', 'B', 3, 4]


# --- send() — two-way communication ---
def accumulator():
    """Generator that accumulates sent values."""
    total = 0
    while True:
        value = yield total    # yields current total, receives next value
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)           # prime the generator (advance to first yield)
print(acc.send(10)) # 10
print(acc.send(20)) # 30
print(acc.send(5))  # 35


# --- Generator Pipeline (lazy data pipeline) ---
def read_lines(filepath):
    with open(filepath) as f:
        yield from f

def grep(pattern, lines):
    return (line for line in lines if pattern in line)

def parse_numbers(lines):
    for line in lines:
        yield float(line.strip())

# Pipeline: each stage is lazy — only pulls data when needed
# total = sum(parse_numbers(grep("ERROR", read_lines("log.txt"))))
```

### 🏭 Real-world Use Cases
- Streaming large CSV/log files without loading into memory
- Infinite sequences (IDs, timestamps, Fibonacci)
- Data pipeline stages in ETL processes
- Implementing coroutines for async-style logic

### ⚠️ Common Mistakes
```python
# Generators are exhausted after one pass!
gen = (x**2 for x in range(5))
print(list(gen))  # [0, 1, 4, 9, 16]
print(list(gen))  # [] ← already exhausted!

# Forgetting to prime send()-based generators
def gen():
    val = yield
    yield val * 2

g = gen()
# g.send(5)   # ❌ TypeError: can't send non-None to just-started generator
next(g)       # ✅ prime it first
print(g.send(5))  # 10

# Using list() on infinite generators
# list(fibonacci())  # ❌ MemoryError / hangs forever
from itertools import islice
print(list(islice(fibonacci(), 10)))  # ✅ Take only 10
```

### ✅ Best Practices
- Use generators for large data — never load everything into memory
- Use `itertools.islice()` to safely slice infinite generators
- Prefer `yield from` over manual loops when delegating
- Use `@contextlib.contextmanager` (built on generators) for clean resource management
- Document whether a function returns a generator or a list

### 📝 Mini Summary
> Generators are Python's lazy evaluation engine. They power memory-efficient pipelines, infinite sequences, and even async patterns — mastering `yield` is essential for senior Python work.

---

## Module 2: Decorators & Closures {#module-2}

### 📖 Explanation
A **closure** is a function that remembers variables from its enclosing scope even after that scope has finished. A **decorator** is a higher-order function that wraps another function to extend its behavior — built on closures. Decorators are everywhere: Flask routes, Django views, `@property`, `@staticmethod`, `@lru_cache`.

### 🔑 Key Concepts
- **First-class functions** — functions are objects in Python
- **Closure** — inner function + captured free variables
- **`functools.wraps`** — preserve wrapped function metadata
- **Decorator with arguments** — factory pattern (3-level nesting)
- **Class-based decorators** — using `__call__`
- **Stacking decorators** — applied bottom-up
- **`functools.lru_cache`** — memoization decorator

### 💻 Example
```python
import functools
import time
import logging

# --- Closure ---
def make_multiplier(factor):
    """Returns a function that multiplies by factor (closure)."""
    def multiply(x):
        return x * factor    # 'factor' is a free variable
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
print(double.__closure__[0].cell_contents)  # 2


# --- Basic Decorator ---
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

add(3, 4)


# --- Decorator with Arguments (factory) ---
def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Retry decorator with configurable attempts and delay."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
def fetch_data(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Timeout")
    return f"Data from {url}"


# --- Class-based Decorator (stateful) ---
class RateLimit:
    """Allow at most `calls` per `period` seconds."""
    def __init__(self, calls=5, period=60):
        self.calls = calls
        self.period = period
        self.timestamps = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove timestamps outside the window
            self.timestamps = [t for t in self.timestamps
                               if now - t < self.period]
            if len(self.timestamps) >= self.calls:
                raise RuntimeError(
                    f"Rate limit exceeded: {self.calls} calls/{self.period}s"
                )
            self.timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper


@RateLimit(calls=3, period=10)
def send_email(to, subject):
    print(f"Email sent to {to}: {subject}")


# --- Stacking Decorators ---
def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold          # applied second
@italic        # applied first
def greet(name):
    return f"Hello, {name}"

print(greet("Alice"))  # <b><i>Hello, Alice</i></b>


# --- lru_cache (built-in memoization) ---
@functools.lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(50))          # Instant, no recomputation
print(fib.cache_info()) # CacheInfo(hits=48, misses=51, ...)
```

### 🏭 Real-world Use Cases
- `@login_required` — authentication in Django/Flask
- `@retry` — resilient API calls and DB connections
- `@lru_cache` / `@cache` — expensive computation memoization
- `@timer` — performance profiling
- `@validate_input` — input sanitization and type checking

### ⚠️ Common Mistakes
```python
# Forgetting @functools.wraps — breaks introspection
def decorator(func):
    def wrapper(*args, **kwargs):    # ❌ wrapper has wrong __name__
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_func(): pass
print(my_func.__name__)  # 'wrapper' ❌ — should be 'my_func'

# With @functools.wraps:
def decorator(func):
    @functools.wraps(func)          # ✅
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Decorators execute at DEFINITION time, not call time
def register(func):
    print(f"Registering {func.__name__}")  # runs at import!
    return func

@register          # ← this runs when the module is loaded
def my_view(): pass
```

### ✅ Best Practices
- Always use `@functools.wraps` in decorators
- Keep decorator logic minimal — single responsibility
- Use class-based decorators when you need state (rate limiting, counting)
- Document what your decorator does and any side effects
- Test decorated functions using `func.__wrapped__` if available

### 📝 Mini Summary
> Decorators are Python's elegant meta-programming tool. Built on closures and first-class functions, they enable clean cross-cutting concerns — authentication, caching, logging — without modifying business logic.

---

## Module 3: Context Managers {#module-3}

### 📖 Explanation
Context managers define setup and teardown logic for a block of code using the `with` statement. They guarantee cleanup happens — even if exceptions occur — making them critical for resource management.

### 🔑 Key Concepts
- `__enter__` / `__exit__` protocol
- `contextlib.contextmanager` — generator-based shorthand
- `contextlib.suppress` — suppress specific exceptions
- `contextlib.ExitStack` — dynamic context manager stacking
- `contextlib.asynccontextmanager` — async version
- Nesting and combining context managers

### 💻 Example
```python
import contextlib
import time
import sqlite3

# --- Class-based Context Manager ---
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        print(f"Opening connection to {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        return self.conn     # value bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Exception occurred: {exc_val} — rolling back")
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        print("Connection closed")
        return False  # False = don't suppress the exception

with DatabaseConnection(":memory:") as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")


# --- Generator-based (contextlib.contextmanager) ---
@contextlib.contextmanager
def timer(label=""):
    """Measure execution time of a block."""
    start = time.perf_counter()
    try:
        yield        # block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] {elapsed:.4f}s")

with timer("matrix multiply"):
    result = sum(i*j for i in range(1000) for j in range(100))


@contextlib.contextmanager
def managed_temp_dir():
    """Create and clean up a temporary directory."""
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp)
        print(f"Cleaned up {tmp}")

with managed_temp_dir() as tmpdir:
    print(f"Working in {tmpdir}")


# --- contextlib.suppress ---
with contextlib.suppress(FileNotFoundError):
    import os
    os.remove("nonexistent.txt")   # silently ignored
print("Continued after suppressed error")


# --- ExitStack — dynamic context managers ---
def process_files(paths):
    """Open a variable number of files safely."""
    with contextlib.ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in paths]
        # All files auto-closed when block exits, even on exception
        for f in files:
            print(f.readline())


# --- Reusable context manager ---
class Indent:
    level = 0
    def __enter__(self):
        Indent.level += 1
        return self
    def __exit__(self, *args):
        Indent.level -= 1

    @staticmethod
    def print(msg):
        print("  " * Indent.level + msg)

with Indent():
    Indent.print("Level 1")
    with Indent():
        Indent.print("Level 2")
    Indent.print("Back to Level 1")
```

### 🏭 Real-world Use Cases
- Database transactions (auto commit/rollback)
- File/network resource management
- Thread locks (`threading.Lock()` as context manager)
- Mocking in tests (`unittest.mock.patch`)
- Temporary directory/file creation
- Performance profiling blocks

### ⚠️ Common Mistakes
```python
# __exit__ signature must accept 3 args (exc_type, exc_val, exc_tb)
class CM:
    def __enter__(self): return self
    def __exit__(self):  pass   # ❌ TypeError — wrong signature
    def __exit__(self, exc_type, exc_val, exc_tb): pass  # ✅

# Accidentally suppressing exceptions by returning True
def __exit__(self, exc_type, exc_val, exc_tb):
    cleanup()
    return True   # ❌ Swallows ALL exceptions silently!
    return False  # ✅ Re-raises exceptions

# Generator-based: code after yield is the __exit__
@contextlib.contextmanager
def bad_cm():
    resource = acquire()
    yield resource
    # ❌ If yield raises, cleanup below never runs!

@contextlib.contextmanager
def good_cm():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)    # ✅ Always runs
```

### ✅ Best Practices
- Always use `try/finally` inside generator-based context managers
- Return `False` (or `None`) from `__exit__` unless you intentionally suppress exceptions
- Use `ExitStack` for dynamic or variable numbers of context managers
- Prefer `@contextmanager` over class-based for simple use cases
- Combine `with` statements: `with open(f1) as a, open(f2) as b:`

### 📝 Mini Summary
> Context managers are Python's RAII pattern. They guarantee cleanup regardless of exceptions — essential for databases, files, locks, and any resource with lifecycle management.

---

## Module 4: Functional Programming Tools {#module-4}

### 📖 Explanation
Python supports functional programming through first-class functions, `map`, `filter`, `reduce`, and the powerful `itertools` and `functools` modules. FP encourages pure functions, immutability, and composability — producing more testable and predictable code.

### 🔑 Key Concepts
- Pure functions (no side effects)
- `map()`, `filter()`, `zip()`, `enumerate()`
- `functools.reduce()`, `functools.partial()`, `functools.compose`
- `itertools` — combinatoric and infinite iterators
- `operator` module — function versions of operators
- Function composition
- Immutability patterns

### 💻 Example
```python
from functools import reduce, partial
import itertools
import operator

# --- map / filter / zip ---
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares   = list(map(lambda x: x**2, nums))
evens     = list(filter(lambda x: x % 2 == 0, nums))
total     = reduce(operator.add, nums)         # 55
product   = reduce(operator.mul, nums[:5])     # 120

names  = ["Alice", "Bob", "Charlie"]
scores = [95, 82, 77]
paired = list(zip(names, scores))
# [('Alice', 95), ('Bob', 82), ('Charlie', 77)]


# --- functools.partial — pre-fill arguments ---
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube   = partial(power, exponent=3)
print(square(5))   # 25
print(cube(3))     # 27

# Real use case: pre-configure a logger
import logging
log_error = partial(logging.log, logging.ERROR)
log_debug = partial(logging.log, logging.DEBUG)


# --- Function Composition ---
def compose(*funcs):
    """compose(f, g, h)(x) == f(g(h(x)))"""
    def composed(x):
        for func in reversed(funcs):
            x = func(x)
        return x
    return composed

strip     = str.strip
lower     = str.lower
normalize = compose(lower, strip)
print(normalize("  Hello World  "))  # "hello world"


# --- itertools ---
# count / cycle / repeat (infinite)
counter = itertools.count(start=10, step=2)   # 10, 12, 14, ...
cycler  = itertools.cycle("ABC")              # A, B, C, A, B, C, ...

# Slicing infinite iterators
print(list(itertools.islice(counter, 5)))  # [10, 12, 14, 16, 18]

# chain — flatten iterables
flat = list(itertools.chain([1,2], [3,4], [5,6]))   # [1,2,3,4,5,6]

# combinations / permutations / product
items = ["A", "B", "C"]
print(list(itertools.combinations(items, 2)))
# [('A','B'), ('A','C'), ('B','C')]

print(list(itertools.permutations(items, 2)))
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

print(list(itertools.product([0,1], repeat=3)))
# All 3-bit binary numbers: [(0,0,0), (0,0,1), ... (1,1,1)]

# groupby — group consecutive items
data = sorted([
    {"dept": "Eng", "name": "Alice"},
    {"dept": "Eng", "name": "Bob"},
    {"dept": "HR",  "name": "Carol"},
], key=lambda x: x["dept"])

for dept, members in itertools.groupby(data, key=lambda x: x["dept"]):
    print(dept, [m["name"] for m in members])
# Eng ['Alice', 'Bob']
# HR  ['Carol']

# takewhile / dropwhile
nums = [1, 3, 5, 2, 7, 9]
print(list(itertools.takewhile(lambda x: x % 2 != 0, nums)))  # [1, 3, 5]
print(list(itertools.dropwhile(lambda x: x % 2 != 0, nums)))  # [2, 7, 9]
```

### 🏭 Real-world Use Cases
- `partial` — pre-configuring HTTP clients, loggers, validators
- `itertools.groupby` — report generation, log analysis
- `itertools.product` — generating test parameter combinations
- `reduce` — aggregation in data pipelines
- `compose` — building transformation pipelines

### ⚠️ Common Mistakes
```python
# map/filter return iterators in Python 3, not lists
result = map(str, [1, 2, 3])
print(result)        # <map object at 0x...> ← not a list!
print(list(result))  # ['1', '2', '3'] ✅

# groupby only groups consecutive identical keys
# Must sort by key FIRST
data = [{"g": "A"}, {"g": "B"}, {"g": "A"}]
# groupby(data, key=...) → 3 groups (A, B, A), NOT 2!
data_sorted = sorted(data, key=lambda x: x["g"])  # ✅ Sort first

# reduce with no initializer on empty sequence
reduce(operator.add, [])   # ❌ TypeError
reduce(operator.add, [], 0) # ✅ Provide initializer
```

### ✅ Best Practices
- Prefer list comprehensions over `map()`/`filter()` for readability
- Use `itertools` instead of writing manual loops for combinatorics
- Always sort before `groupby`
- Use `partial` to avoid repetitive argument passing
- Keep functions pure (no side effects) for easier testing

### 📝 Mini Summary
> Python's functional tools enable elegant, composable data transformations. `itertools` is your toolkit for efficient iteration; `functools` for function manipulation. Know them cold for interviews.

---

## Module 5: Advanced OOP – Metaclasses, Descriptors & Slots {#module-5}

### 📖 Explanation
Advanced OOP in Python goes beyond basic inheritance. **Metaclasses** control class creation itself. **Descriptors** power `@property`, `@staticmethod`, and attribute access. **`__slots__`** optimizes memory layout. These are the internals that frameworks like Django, SQLAlchemy, and Pydantic are built on.

### 🔑 Key Concepts
- **Metaclass** — the class of a class (`type` is the default metaclass)
- **`__new__` vs `__init__`** — object creation vs initialization
- **Descriptor protocol** — `__get__`, `__set__`, `__delete__`
- **`__slots__`** — replaces `__dict__` with fixed memory layout
- **`__init_subclass__`** — hook for subclass creation
- **Abstract Base Classes (ABC)**
- **`dataclasses`** — auto-generated OOP boilerplate

### 💻 Example
```python
# --- Metaclass ---
class SingletonMeta(type):
    """Metaclass that ensures only one instance of a class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, url):
        self.url = url
        print(f"Connecting to {url}")

db1 = Database("postgres://localhost/mydb")
db2 = Database("ignored")
print(db1 is db2)   # True — same instance


# --- Metaclass for auto-registration ---
class PluginMeta(type):
    registry = {}
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:   # skip the base class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    def run(self): raise NotImplementedError

class JSONPlugin(Plugin):
    def run(self): print("Processing JSON")

class XMLPlugin(Plugin):
    def run(self): print("Processing XML")

print(PluginMeta.registry)  # {'JSONPlugin': ..., 'XMLPlugin': ...}
PluginMeta.registry["JSONPlugin"]().run()  # Processing JSON


# --- Descriptors ---
class Validated:
    """Descriptor that validates attribute values."""
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self     # accessed on class, not instance
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        pass

class PositiveNumber(Validated):
    def validate(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{self.name} must be a positive number, got {value!r}")

class NonEmptyString(Validated):
    def validate(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{self.name} must be a non-empty string")

class Product:
    name  = NonEmptyString()
    price = PositiveNumber()
    stock = PositiveNumber()

    def __init__(self, name, price, stock):
        self.name  = name
        self.price = price
        self.stock = stock

p = Product("Widget", 9.99, 100)
# Product("", 9.99, 100)      # ❌ ValueError: name must be a non-empty string
# Product("Widget", -1, 100)  # ❌ ValueError: price must be a positive number


# --- __slots__ ---
class Point:
    __slots__ = ("x", "y")   # No __dict__ — fixed attributes only

    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
p_slot  = Point(1, 2)
# p_slot.z = 3   # ❌ AttributeError — can't add new attributes

# Memory comparison
class PointDict:
    def __init__(self, x, y): self.x, self.y = x, y

print(sys.getsizeof(Point(1,2).__class__))      # Smaller
print(sys.getsizeof(PointDict(1,2).__dict__))   # ~200 bytes overhead


# --- Abstract Base Classes ---
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self):
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self):      return 3.14159 * self.r ** 2
    def perimeter(self): return 2 * 3.14159 * self.r

# Shape()  # ❌ TypeError: Can't instantiate abstract class
print(Circle(5).describe())  # Circle: area=78.54


# --- dataclasses ---
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Point3D:
    x: float
    y: float
    z: float = 0.0
    tags: list = field(default_factory=list, compare=False)

    def distance_from_origin(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

p1 = Point3D(1, 2, 3)
p2 = Point3D(1, 2, 3)
print(p1 == p2)   # True (auto __eq__)
print(p1 < Point3D(2, 0, 0))  # True (auto __lt__)
# p1.x = 99     # ❌ FrozenInstanceError (frozen=True)
```

### 🏭 Real-world Use Cases
- **Metaclasses** — Django ORM's model registration, Pydantic validation
- **Descriptors** — SQLAlchemy column definitions, form field validation
- **`__slots__`** — High-performance objects (game entities, numeric computing)
- **ABCs** — Plugin systems, interface contracts
- **dataclasses** — Configuration objects, DTOs, value objects

### ⚠️ Common Mistakes
```python
# Metaclass conflict — multiple metaclasses can't be combined naively
class Meta1(type): pass
class Meta2(type): pass
# class Conflict(metaclass=Meta1, metaclass=Meta2): pass  # ❌ SyntaxError

# __slots__ and inheritance — child must also define __slots__
class Base:
    __slots__ = ("x",)

class Child(Base):
    # Without __slots__, Child gets __dict__ back! Wastes memory
    __slots__ = ("y",)   # ✅ Chain __slots__ in subclasses

# Forgetting __set_name__ in descriptors (Python 3.6+)
# Without it, descriptor doesn't know its attribute name
```

### ✅ Best Practices
- Avoid metaclasses unless genuinely needed — `__init_subclass__` solves many use cases more simply
- Use `dataclasses` for simple data containers over manual `__init__`
- Use `__slots__` for frequently instantiated small objects
- Use ABCs to define interfaces for plugin systems
- Always implement `__repr__` for custom classes

### 📝 Mini Summary
> Metaclasses, descriptors, and `__slots__` are the internals of Python's most powerful frameworks. Understanding them separates Python users from Python experts.

---

## Module 6: Concurrency – Threading, Multiprocessing & AsyncIO {#module-6}

### 📖 Explanation
Python offers three concurrency models. Choosing the right one depends on whether your bottleneck is I/O-bound or CPU-bound. **Threading** for I/O-bound work. **Multiprocessing** for CPU-bound work. **AsyncIO** for high-concurrency I/O with minimal overhead.

### 🔑 Key Concepts
- **GIL** — prevents true parallel threading for CPU work
- **`threading`** — threads share memory; GIL limits parallelism
- **`multiprocessing`** — separate processes, no GIL; separate memory
- **`concurrent.futures`** — high-level thread/process pool API
- **`asyncio`** — single-threaded cooperative concurrency via event loop
- **`async/await`** — coroutines syntax
- **`asyncio.gather`** — run coroutines concurrently
- **`asyncio.Queue`** — async producer/consumer pattern

### 💻 Example
```python
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import time

# --- Threading (I/O-bound) ---
def download(url):
    time.sleep(1)      # simulate I/O wait
    return f"Downloaded {url}"

urls = [f"http://example.com/{i}" for i in range(5)]

start = time.time()
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(download, urls))
print(f"Threading: {time.time()-start:.2f}s")  # ~1s (parallel I/O)


# --- Multiprocessing (CPU-bound) ---
def cpu_task(n):
    """CPU-heavy computation."""
    return sum(i*i for i in range(n))

data = [10**6] * 4

start = time.time()
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_task, data))
print(f"Multiprocessing: {time.time()-start:.2f}s")  # ~4x faster than serial


# --- Thread Safety with Locks ---
class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1    # atomic operation

    @property
    def count(self):
        return self._count

counter = ThreadSafeCounter()
threads = [threading.Thread(target=counter.increment) for _ in range(1000)]
for t in threads: t.start()
for t in threads: t.join()
print(counter.count)   # 1000 (always correct with lock)


# --- AsyncIO (High-concurrency I/O) ---
import asyncio

async def fetch(session, url):
    """Simulate async HTTP request."""
    await asyncio.sleep(0.5)   # non-blocking I/O wait
    return f"Response from {url}"

async def main():
    urls = [f"http://api.example.com/{i}" for i in range(10)]
    # Run all 10 concurrently — takes ~0.5s total, not 5s
    results = await asyncio.gather(*[fetch(None, url) for url in urls])
    return results

results = asyncio.run(main())
print(f"Got {len(results)} responses")


# --- AsyncIO Producer/Consumer ---
async def producer(queue, n):
    for i in range(n):
        await asyncio.sleep(0.1)
        await queue.put(f"item_{i}")
        print(f"Produced item_{i}")
    await queue.put(None)    # sentinel

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        queue.task_done()

async def pipeline():
    queue = asyncio.Queue(maxsize=3)
    await asyncio.gather(
        producer(queue, 5),
        consumer(queue)
    )

asyncio.run(pipeline())


# --- asyncio.timeout (Python 3.11+) ---
async def slow_operation():
    await asyncio.sleep(10)

async def main_with_timeout():
    try:
        async with asyncio.timeout(2.0):
            await slow_operation()
    except TimeoutError:
        print("Operation timed out!")

asyncio.run(main_with_timeout())
```

### 🏭 Real-world Use Cases
- **ThreadPoolExecutor** — concurrent file uploads, DB queries
- **ProcessPoolExecutor** — image processing, ML inference, data transforms
- **AsyncIO** — web scrapers, chat servers, REST API clients (with `aiohttp`)
- **asyncio.Queue** — event-driven microservices, task queues

### ⚠️ Common Mistakes
```python
# Using threading for CPU-bound work — GIL kills parallelism
# with ThreadPoolExecutor() as ex:
#     results = ex.map(cpu_heavy, data)  # ❌ No speedup due to GIL

# Forgetting to join threads
t = threading.Thread(target=work)
t.start()
# Program may exit before thread finishes! Always call:
t.join()   # ✅

# Mixing sync and async code incorrectly
async def bad():
    time.sleep(1)    # ❌ Blocks the entire event loop!
    await asyncio.sleep(1)  # ✅ Non-blocking

# Creating new event loop instead of using asyncio.run()
# loop = asyncio.get_event_loop()  # ❌ deprecated pattern
asyncio.run(main())  # ✅ Clean entry point
```

### ✅ Best Practices
- Use `concurrent.futures` over raw `threading`/`multiprocessing` for simplicity
- Use `asyncio` for thousands of concurrent I/O operations (web servers, scrapers)
- Always protect shared mutable state with `Lock` / `asyncio.Lock`
- Use `asyncio.run()` as the single entry point for async programs
- Profile before parallelizing — not all code benefits from concurrency

### 📝 Mini Summary
> Match your concurrency model to your problem: AsyncIO for massive I/O concurrency, multiprocessing for CPU parallelism, threading for simple I/O parallelism. The GIL is the key to understanding when each applies.

---

## Module 7: Memory Management & Performance Optimization {#module-7}

### 📖 Explanation
Python manages memory automatically, but understanding how it works lets you write significantly faster, lower-memory code. Key tools: profilers, `__slots__`, generators, `array`/`numpy`, `sys.getsizeof`, and the `tracemalloc` module.

### 🔑 Key Concepts
- Reference counting + cyclic GC
- `sys.getsizeof()` — object size in bytes
- `tracemalloc` — memory allocation tracing
- `cProfile` / `line_profiler` — CPU profiling
- `__slots__` — eliminate `__dict__` overhead
- `array` module — typed arrays vs lists
- `memoryview` — zero-copy buffer protocol
- Integer interning, string interning
- `weakref` — references that don't prevent GC

### 💻 Example
```python
import sys
import tracemalloc
import cProfile
import weakref
import gc
from array import array

# --- Object sizes ---
print(sys.getsizeof([]))          # 56 bytes (empty list)
print(sys.getsizeof([1]*1000))    # ~8056 bytes
print(sys.getsizeof({}))          # 64 bytes (empty dict)
print(sys.getsizeof("hello"))     # 54 bytes

# List vs generator memory
list_mem = sys.getsizeof(list(range(100000)))
gen_mem  = sys.getsizeof(x for x in range(100000))
print(f"List: {list_mem:,} bytes")  # ~800,056 bytes
print(f"Gen:  {gen_mem} bytes")     # 112 bytes!


# --- tracemalloc ---
tracemalloc.start()

# Some allocations
data = [dict(i=i, v=i*2) for i in range(10000)]

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
for stat in top_stats[:3]:
    print(stat)    # shows file, line, size


# --- Typed array vs list ---
int_list  = list(range(1_000_000))
int_array = array("i", range(1_000_000))   # 'i' = C int

print(sys.getsizeof(int_list))    # ~8,000,056 bytes
print(sys.getsizeof(int_array))   # ~4,000,064 bytes (2x smaller!)


# --- memoryview (zero-copy slicing) ---
data = bytearray(b"Hello, World!")
view = memoryview(data)
chunk = view[7:12]              # No copy! Just a view into the buffer
print(bytes(chunk))             # b'World'


# --- weakref (avoid memory leaks in caches) ---
class ExpensiveObject:
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print(f"{self.name} deleted")

obj = ExpensiveObject("resource_1")
weak = weakref.ref(obj)

print(weak())       # <ExpensiveObject>
del obj             # Original deleted; GC can collect it
print(weak())       # None — object is gone


# --- CPU Profiling ---
def slow_function():
    return sum(i**2 for i in range(100000))

cProfile.run("slow_function()", sort="cumtime")


# --- Optimized string building ---
import timeit

# Slow: O(n²)
def concat_slow(n):
    s = ""
    for i in range(n):
        s += str(i)
    return s

# Fast: O(n)
def concat_fast(n):
    return "".join(str(i) for i in range(n))

slow = timeit.timeit(lambda: concat_slow(10000), number=100)
fast = timeit.timeit(lambda: concat_fast(10000), number=100)
print(f"Slow: {slow:.3f}s | Fast: {fast:.3f}s")


# --- Integer interning ---
a = 256
b = 256
print(a is b)   # True  — cached (range: -5 to 256)

a = 257
b = 257
print(a is b)   # False — not cached (CPython-specific)
```

### 🏭 Real-world Use Cases
- Profiling slow API endpoints with `cProfile`
- Using `array`/`numpy` for numerical data processing
- `weakref` in LRU caches to avoid memory leaks
- `tracemalloc` for debugging memory growth in long-running services
- `memoryview` in network protocol implementations

### ⚠️ Common Mistakes
```python
# Circular references can delay GC (but cyclic GC handles it eventually)
class Node:
    def __init__(self):
        self.next = None

a, b = Node(), Node()
a.next = b
b.next = a    # Circular — use weakref.ref for one side

# Holding references in class variables (memory leak)
class Cache:
    _store = {}   # ❌ grows forever, shared across instances

    @classmethod
    def add(cls, key, val):
        cls._store[key] = val    # Never freed!

# Premature optimization — profile first!
# Don't use __slots__ everywhere "for performance"
# without measuring actual memory usage first.
```

### ✅ Best Practices
- Profile before optimizing — use `cProfile` + `snakeviz`
- Use generators for large data streams
- Use `__slots__` for small, frequently created objects
- Use `array` or `numpy` for homogeneous numeric data
- Use `weakref` in caches to prevent memory leaks
- Use `tracemalloc` for memory leak investigation

### 📝 Mini Summary
> Python's memory management is automatic but not magic. Know your object sizes, profile before optimizing, and use the right data structure — generators, typed arrays, and `__slots__` can yield 10-100x improvements.

---

## Module 8: Type Hints, Protocols & Structural Subtyping {#module-8}

### 📖 Explanation
Type hints (PEP 484+) make Python code self-documenting, enable static analysis with `mypy`, and power IDE autocompletion. **Protocols** (PEP 544) enable structural subtyping — "duck typing" made explicit without requiring inheritance.

### 🔑 Key Concepts
- Basic hints: `int`, `str`, `list[int]`, `dict[str, Any]`
- `Optional[T]` = `T | None`
- `Union[A, B]` → `A | B` (Python 3.10+)
- `TypeVar` — generic functions
- `Generic[T]` — generic classes
- `Protocol` — structural subtyping (duck typing formalized)
- `TypedDict` — typed dictionaries
- `Literal`, `Final`, `ClassVar`
- `overload` — multiple signatures
- `runtime_checkable` Protocol

### 💻 Example
```python
from typing import (
    Optional, Union, TypeVar, Generic, Protocol,
    TypedDict, Literal, Final, overload, runtime_checkable,
    Callable, Iterator, Any
)

# --- Basic Type Hints ---
def greet(name: str, times: int = 1) -> str:
    return (f"Hello, {name}! " * times).strip()

def process(value: int | str | None) -> str:
    if value is None:
        return "nothing"
    return str(value)


# --- TypeVar and Generics ---
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

s: Stack[int] = Stack()
s.push(1)
s.push(2)
print(s.pop())   # 2


# --- Protocol (structural subtyping) ---
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def area(self) -> float: ...

class Circle:                    # Does NOT inherit Drawable
    def __init__(self, r: float):
        self.r = r
    def draw(self) -> str:
        return f"O (r={self.r})"
    def area(self) -> float:
        return 3.14159 * self.r**2

class Rectangle:                 # Does NOT inherit Drawable
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h
    def draw(self) -> str:
        return f"[] ({self.w}x{self.h})"
    def area(self) -> float:
        return self.w * self.h

def render(shapes: list[Drawable]) -> None:
    for s in shapes:
        print(f"{s.draw()} — area: {s.area():.2f}")

# Works without inheritance!
render([Circle(5), Rectangle(3, 4)])

# Runtime check
print(isinstance(Circle(1), Drawable))   # True


# --- TypedDict ---
class UserProfile(TypedDict):
    id: int
    name: str
    email: str
    age: int | None

def create_user(profile: UserProfile) -> str:
    return f"User {profile['name']} ({profile['email']})"


# --- Literal and Final ---
Direction = Literal["north", "south", "east", "west"]
MAX_RETRIES: Final = 3

def move(direction: Direction) -> None:
    print(f"Moving {direction}")

move("north")    # ✅
# move("up")     # mypy error: Argument 1 has incompatible type "Literal['up']"


# --- overload ---
@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...

def double(x):
    if isinstance(x, str):
        return x * 2
    return x * 2

result1: int = double(5)     # type: int
result2: str = double("hi")  # type: str
```

### 🏭 Real-world Use Cases
- `Protocol` — plugin systems, adapter patterns without inheritance coupling
- `TypedDict` — typing JSON API responses and configs
- `Generic[T]` — reusable data structures (queues, trees, repositories)
- `Literal` — state machines, enum-like string constants
- Full type hints + `mypy` — CI pipeline type checking to prevent runtime errors

### ⚠️ Common Mistakes
```python
# Type hints are NOT enforced at runtime by default!
def add(a: int, b: int) -> int:
    return a + b

add("hello", "world")  # No error at runtime — "helloworld" returned
# Use mypy for static checking, or pydantic for runtime validation

# mutable default in typed functions
def fn(items: list[int] = []) -> None:   # ❌ mutable default!
    items.append(1)

# Optional[X] means X | None, NOT "optional parameter"
from typing import Optional
def fn(x: Optional[int]) -> None:   # parameter CAN be None
    pass

# Wrong use of List vs list (Python 3.9+)
from typing import List     # ❌ Old style
def fn(x: list[int]): pass  # ✅ Modern (Python 3.9+)
```

### ✅ Best Practices
- Use `mypy --strict` in CI pipelines
- Prefer `Protocol` over ABCs when you don't control the implementors
- Use `TypedDict` for typed dict structures (API responses, configs)
- Use `X | None` over `Optional[X]` in Python 3.10+
- Add type hints incrementally — start with public APIs

### 📝 Mini Summary
> Type hints transform Python from a "hope it works" language to one with IDE superpowers and static analysis. `Protocol` is the crown jewel — enabling duck typing with formal contracts.

---

## Module 9: Advanced Data Structures & Collections {#module-9}

### 📖 Explanation
Python's `collections`, `heapq`, `bisect`, and `queue` modules provide specialized data structures that solve real problems efficiently. Knowing when to use each is a hallmark of an experienced engineer.

### 🔑 Key Concepts
- `collections.deque` — O(1) both-end append/pop
- `collections.Counter` — multiset / frequency map
- `collections.defaultdict` — auto-initialize dict values
- `collections.OrderedDict` — ordered dict with extra methods
- `collections.ChainMap` — layered dict lookup
- `heapq` — min-heap (priority queue)
- `bisect` — binary search on sorted lists
- `queue.PriorityQueue` — thread-safe priority queue

### 💻 Example
```python
from collections import deque, Counter, defaultdict, ChainMap, OrderedDict
import heapq
import bisect

# --- deque (double-ended queue) ---
dq = deque([1, 2, 3], maxlen=5)
dq.appendleft(0)    # O(1) — [0, 1, 2, 3]
dq.append(4)        # O(1) — [0, 1, 2, 3, 4]
dq.rotate(2)        # [3, 4, 0, 1, 2]
print(list(dq))

# Sliding window using deque
def max_sliding_window(nums, k):
    result, window = [], deque()
    for i, n in enumerate(nums):
        while window and nums[window[-1]] < n:
            window.pop()
        window.append(i)
        if window[0] == i - k:
            window.popleft()
        if i >= k - 1:
            result.append(nums[window[0]])
    return result

print(max_sliding_window([1,3,-1,-3,5,3,6,7], 3))
# [3, 3, 5, 5, 6, 7]


# --- Counter ---
text = "the quick brown fox jumps over the lazy dog"
freq = Counter(text.split())
print(freq.most_common(3))      # [('the', 2), ('quick', 1), ...]

# Arithmetic on Counters
c1 = Counter(a=3, b=2, c=1)
c2 = Counter(a=1, b=2, c=3)
print(c1 + c2)   # Counter({'a': 4, 'c': 4, 'b': 4})
print(c1 - c2)   # Counter({'a': 2}) — drops non-positive
print(c1 & c2)   # Counter({'b': 2, 'a': 1, 'c': 1}) — min
print(c1 | c2)   # Counter({'a': 3, 'c': 3, 'b': 2}) — max


# --- defaultdict ---
graph = defaultdict(list)   # adjacency list
edges = [(1,2),(1,3),(2,4),(3,4)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
print(dict(graph))

# Word grouper
from collections import defaultdict
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
anagram_groups = defaultdict(list)
for w in words:
    anagram_groups[tuple(sorted(w))].append(w)
print(dict(anagram_groups))
# {('a','e','t'): ['eat','tea','ate'], ('a','n','t'): ['tan','nat'], ...}


# --- ChainMap (layered config) ---
defaults = {"theme": "dark", "lang": "en", "timeout": 30}
user_cfg = {"theme": "light"}
env_cfg  = {"timeout": 60}

config = ChainMap(env_cfg, user_cfg, defaults)
print(config["theme"])    # "light" (user_cfg wins)
print(config["timeout"])  # 60     (env_cfg wins)
print(config["lang"])     # "en"   (from defaults)


# --- heapq (min-heap / priority queue) ---
tasks = []
heapq.heappush(tasks, (3, "low priority"))
heapq.heappush(tasks, (1, "urgent"))
heapq.heappush(tasks, (2, "medium"))

while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"[{priority}] {task}")
# [1] urgent → [2] medium → [3] low priority

# nlargest / nsmallest
scores = [34, 78, 12, 99, 45, 67]
print(heapq.nlargest(3, scores))    # [99, 78, 67]
print(heapq.nsmallest(3, scores))   # [12, 34, 45]

# Merge sorted iterables
merged = list(heapq.merge([1,3,5], [2,4,6], [0,7,8]))
print(merged)  # [0, 1, 2, 3, 4, 5, 6, 7, 8]


# --- bisect (binary search) ---
sorted_list = [1, 3, 5, 7, 9, 11]
pos = bisect.bisect_left(sorted_list, 6)    # 3 (insertion point)
bisect.insort(sorted_list, 6)               # [1,3,5,6,7,9,11] ← sorted insert

# Grade calculator using bisect
def grade(score):
    breakpoints = [60, 70, 80, 90]
    grades = "FDCBA"
    return grades[bisect.bisect(breakpoints, score)]

print([grade(s) for s in [55, 65, 75, 85, 95]])
# ['F', 'D', 'C', 'B', 'A']
```

### 🏭 Real-world Use Cases
- `deque` — BFS queues, sliding window algorithms, log buffers
- `Counter` — word frequency, A/B test tallying, inventory counts
- `defaultdict` — graph adjacency lists, grouping/bucketing data
- `heapq` — Dijkstra's algorithm, task schedulers, top-K problems
- `bisect` — maintaining sorted lists, range queries, grade boundaries
- `ChainMap` — layered config (env > user > defaults)

### ⚠️ Common Mistakes
```python
# heapq is a min-heap only — for max-heap, negate values
import heapq
max_heap = []
for val in [3, 1, 4, 1, 5, 9]:
    heapq.heappush(max_heap, -val)      # negate to simulate max-heap
print(-heapq.heappop(max_heap))         # 9 ✅

# Counter.update vs Counter reassignment
c = Counter("hello")
c.update("world")          # ✅ Adds counts
c = Counter("hello") + Counter("world")  # ✅ Also works

# deque maxlen silently drops old items
dq = deque(maxlen=3)
dq.extend([1,2,3,4,5])
print(list(dq))  # [3, 4, 5] — 1 and 2 silently dropped!
```

### ✅ Best Practices
- Use `deque` instead of `list` when you need O(1) left append/pop
- Use `Counter` over manual dict counting
- Use `heapq.nlargest/nsmallest` for top-K over sorting full list
- Use `bisect` for maintaining sorted order without re-sorting
- Use `ChainMap` for layered config instead of `{**d1, **d2}` (preserves source tracking)

### 📝 Mini Summary
> The `collections` and `heapq` modules are interview goldmines. Many classic algorithm problems become one-liners with `Counter`, `deque`, and `heapq`. Know them deeply.

---

## Module 10: Design Patterns in Python {#module-10}

### 📖 Explanation
Design patterns are reusable solutions to common software design problems. Python's dynamic nature lets many patterns be implemented more elegantly than in statically-typed languages. Some patterns are built into the language itself.

### 🔑 Key Concepts
- **Creational:** Singleton, Factory, Builder
- **Structural:** Adapter, Decorator (already in Python!), Proxy
- **Behavioral:** Observer, Strategy, Command, Iterator (built-in)
- Pythonic patterns: using `__call__`, `Protocol`, generators

### 💻 Example
```python
# --- Singleton (via metaclass) ---
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {}

c1, c2 = Config(), Config()
assert c1 is c2   # True


# --- Factory Pattern ---
class Notification:
    def send(self, message): raise NotImplementedError

class EmailNotification(Notification):
    def send(self, message): print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message): print(f"SMS: {message}")

class SlackNotification(Notification):
    def send(self, message): print(f"Slack: {message}")

class NotificationFactory:
    _types = {
        "email": EmailNotification,
        "sms":   SMSNotification,
        "slack": SlackNotification,
    }

    @classmethod
    def create(cls, type_: str) -> Notification:
        if type_ not in cls._types:
            raise ValueError(f"Unknown notification type: {type_!r}")
        return cls._types[type_]()

    @classmethod
    def register(cls, name: str, klass: type):
        cls._types[name] = klass

NotificationFactory.create("email").send("Hello!")


# --- Observer Pattern ---
from typing import Callable

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = defaultdict(list)

    def on(self, event: str, callback: Callable):
        self._listeners[event].append(callback)
        return self   # enable chaining

    def emit(self, event: str, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

    def off(self, event: str, callback: Callable):
        self._listeners[event].remove(callback)

emitter = EventEmitter()
emitter.on("user.created", lambda u: print(f"Welcome email to {u}"))
emitter.on("user.created", lambda u: print(f"Audit log: {u} created"))
emitter.emit("user.created", "alice@example.com")


# --- Strategy Pattern ---
from typing import Protocol

class SortStrategy(Protocol):
    def sort(self, data: list) -> list: ...

class BubbleSort:
    def sort(self, data: list) -> list:
        d = data[:]
        for i in range(len(d)):
            for j in range(len(d)-i-1):
                if d[j] > d[j+1]:
                    d[j], d[j+1] = d[j+1], d[j]
        return d

class QuickSort:
    def sort(self, data: list) -> list:
        if len(data) <= 1: return data
        pivot = data[len(data)//2]
        return (self.sort([x for x in data if x < pivot]) +
                [x for x in data if x == pivot] +
                self.sort([x for x in data if x > pivot]))

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data: list) -> list:
        return self.strategy.sort(data)

sorter = Sorter(QuickSort())
print(sorter.sort([3,1,4,1,5,9]))

sorter.strategy = BubbleSort()  # swap strategy at runtime
print(sorter.sort([3,1,4,1,5,9]))


# --- Builder Pattern ---
class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._conditions: list[str] = []
        self._columns: list[str] = ["*"]
        self._limit: int | None = None
        self._order: str | None = None

    def select(self, *cols: str):
        self._columns = list(cols)
        return self

    def where(self, condition: str):
        self._conditions.append(condition)
        return self

    def order_by(self, col: str, direction: str = "ASC"):
        self._order = f"{col} {direction}"
        return self

    def limit(self, n: int):
        self._limit = n
        return self

    def build(self) -> str:
        query = f"SELECT {', '.join(self._columns)} FROM {self._table}"
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        if self._order:
            query += f" ORDER BY {self._order}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

query = (QueryBuilder("users")
    .select("id", "name", "email")
    .where("age > 18")
    .where("active = 1")
    .order_by("name")
    .limit(10)
    .build())

print(query)
# SELECT id, name, email FROM users WHERE age > 18 AND active = 1
# ORDER BY name ASC LIMIT 10
```

### 🏭 Real-world Use Cases
- **Factory** — notification systems, payment gateway adapters
- **Observer** — event systems, WebSocket broadcasting, DOM events
- **Strategy** — pluggable algorithms (sorting, compression, auth)
- **Builder** — SQL query builders, HTTP request builders, test fixtures
- **Singleton** — database connection pools, application config

### ⚠️ Common Mistakes
```python
# Overusing Singleton — leads to tight coupling, hard to test
# Prefer dependency injection over singletons where possible

# Observer memory leaks — listeners holding references to objects
# Use weakref for listener lists in long-lived emitters

# Builder not returning self — breaks method chaining
class BadBuilder:
    def set_name(self, name):
        self.name = name
        # ❌ missing: return self

class GoodBuilder:
    def set_name(self, name):
        self.name = name
        return self    # ✅ enables chaining
```

### ✅ Best Practices
- Use Python's built-in tools before implementing patterns (decorators, generators, protocols)
- Prefer composition over inheritance
- Use `Protocol` to define interfaces for Strategy/Observer without coupling
- Implement Builder with method chaining (return `self`)
- Test patterns in isolation — they should be easy to unit test

### 📝 Mini Summary
> Python makes many design patterns lightweight and elegant. The Factory, Observer, Strategy, and Builder patterns appear constantly in production codebases and are frequent interview topics.

---

## Interview Questions {#interview-questions}

### 🟢 Basic Level

**Q1: What is the difference between a generator function and a regular function?**

**Answer:**
A regular function executes completely and returns a single value with `return`. A generator function uses `yield`, suspending execution and returning a **generator object** that produces values lazily one at a time. Generator objects implement the iterator protocol.
```python
def regular():
    return [1, 2, 3]    # all in memory

def generator():
    yield 1             # produces one value, suspends
    yield 2
    yield 3

gen = generator()
next(gen)   # 1
next(gen)   # 2
next(gen)   # 3
next(gen)   # StopIteration
```
Key difference: generators are memory-efficient for large sequences; they don't compute all values upfront.

---

**Q2: What does `@functools.wraps` do and why is it important?**

**Answer:**
`@functools.wraps(func)` copies the wrapped function's metadata (`__name__`, `__doc__`, `__module__`, `__qualname__`, `__annotations__`, `__dict__`) onto the wrapper function. Without it, introspection tools, debuggers, and documentation generators see the wrapper instead of the original:
```python
def decorator(func):
    def wrapper(*args, **kwargs):       # ← hides original metadata
        return func(*args, **kwargs)
    return wrapper

def better_decorator(func):
    @functools.wraps(func)              # ← preserves metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@better_decorator
def my_func():
    """Does something important."""
    pass

print(my_func.__name__)  # 'my_func' ✅ (not 'wrapper')
print(my_func.__doc__)   # 'Does something important.' ✅
```

---

**Q3: What is the difference between `threading` and `multiprocessing` in Python?**

**Answer:**
| | `threading` | `multiprocessing` |
|---|---|---|
| Execution | Same process, multiple threads | Separate OS processes |
| Memory | Shared memory | Separate memory (use `Queue`/`Pipe` to communicate) |
| GIL | Affected — only one thread runs Python at a time | No GIL — true parallelism |
| Best for | I/O-bound tasks (network, file) | CPU-bound tasks (computation) |
| Overhead | Low | Higher (process spawn cost) |

Use `threading` for concurrent web requests; use `multiprocessing` for parallel data processing.

---

**Q4: What are `__enter__` and `__exit__` used for?**

**Answer:**
They implement the **context manager protocol** for use with `with` statements:
- `__enter__` — runs at the start of the `with` block; its return value is bound to the `as` variable
- `__exit__(exc_type, exc_val, exc_tb)` — always runs on exit; receives exception info if one occurred; returning `True` suppresses the exception, `False`/`None` re-raises it

This guarantees cleanup (closing files, releasing locks, committing/rolling back transactions) even when exceptions occur.

---

**Q5: What is the difference between `@staticmethod` and `@classmethod`?**

**Answer:**
- `@staticmethod` — doesn't receive any implicit first argument; it's just a regular function namespaced inside a class; doesn't have access to `cls` or `self`.
- `@classmethod` — receives `cls` (the class itself) as the first argument; can access and modify class state; commonly used for alternative constructors.
```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_iso(cls, s):         # alternative constructor
        return cls(*map(int, s.split("-")))

    @staticmethod
    def is_leap_year(year):       # utility — no class/instance needed
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

---

### 🟡 Intermediate Level

**Q6: Explain the difference between `__new__` and `__init__`. When would you override `__new__`?**

**Answer:**
- `__new__(cls, ...)` — called first; **creates and returns** the new instance; controls object allocation
- `__init__(self, ...)` — called after `__new__`; **initializes** the already-created instance

Override `__new__` when you need to control object creation itself:
```python
# Singleton
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Immutable custom type (subclassing immutable built-ins)
class PositiveInt(int):
    def __new__(cls, value):
        if value <= 0:
            raise ValueError(f"Must be positive, got {value}")
        return super().__new__(cls, value)

n = PositiveInt(5)    # 5
# PositiveInt(-1)     # ❌ ValueError
```

---

**Q7: What is a closure? Give a practical example.**

**Answer:**
A closure is an inner function that **remembers and accesses variables from its enclosing scope** even after the outer function has returned. The captured variables are called **free variables**.

Practical example — a configurable validator factory:
```python
def make_range_validator(min_val, max_val):
    """Returns a validator function with captured range."""
    def validate(value):
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"Value {value} outside [{min_val}, {max_val}]"
            )
        return value
    return validate    # validate closes over min_val, max_val

validate_age    = make_range_validator(0, 150)
validate_score  = make_range_validator(0, 100)
validate_rating = make_range_validator(1, 5)

validate_age(25)     # ✅
validate_score(105)  # ❌ ValueError
print(validate_age.__code__.co_freevars)  # ('max_val', 'min_val')
```

---

**Q8: What is the GIL and how does `asyncio` avoid its limitations?**

**Answer:**
The **Global Interpreter Lock (GIL)** is a mutex in CPython that allows only one thread to execute Python bytecode at a time. This prevents true CPU parallelism with threads.

**AsyncIO avoids the GIL problem because it doesn't use multiple threads.** It uses a **single-threaded event loop** with cooperative multitasking:
- When a coroutine hits `await`, it voluntarily yields control back to the event loop
- The event loop picks up another ready coroutine
- No shared state between concurrent coroutines → no need for locks

```python
# No GIL issues — everything on one thread
async def fetch(url):
    # At 'await', control returns to event loop
    # Event loop runs other coroutines while waiting for I/O
    response = await aiohttp.get(url)
    return response

# 1000 concurrent requests on ONE thread — event loop manages all
await asyncio.gather(*[fetch(url) for url in 1000_urls])
```
For CPU-bound work, `asyncio` doesn't help — use `multiprocessing`.

---

**Q9: What are Python Protocols and how do they differ from ABCs?**

**Answer:**
Both define interfaces, but differ in how compliance is checked:

| | `Protocol` | `ABC` |
|---|---|---|
| Subtyping | **Structural** ("duck typing") — matches by shape | **Nominal** — must explicitly inherit |
| Inheritance required | ❌ No | ✅ Yes |
| Runtime check | With `@runtime_checkable` | Always via `isinstance` |
| Use case | You don't control the implementors | You do control the hierarchy |

```python
# Protocol — works without inheritance
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:         # No inheritance!
    def draw(self): return "O"

def render(d: Drawable): print(d.draw())
render(Circle())  # ✅ Works — Circle structurally matches

# ABC — requires inheritance
class Shape(ABC):
    @abstractmethod
    def draw(self) -> str: ...

class Square(Shape):   # Must inherit
    def draw(self): return "□"
```

---

**Q10: How does `functools.lru_cache` work? What are its limitations?**

**Answer:**
`@lru_cache(maxsize=N)` memoizes function results using a **Least Recently Used** cache. It stores `(args, kwargs) → result` mappings and evicts the least recently used entry when `maxsize` is reached.

**Mechanism:** Uses an ordered dict + doubly-linked list internally for O(1) cache operations.

**Limitations:**
```python
@functools.lru_cache(maxsize=128)
def expensive(n):
    return sum(range(n))

# ❌ Arguments must be hashable (no lists, dicts)
expensive([1,2,3])  # TypeError: unhashable type: 'list'

# ❌ Doesn't work with instance methods easily (self is part of cache key)
class MyClass:
    @functools.lru_cache  # ❌ Caches per instance but holds strong ref
    def compute(self, n): ...

# ✅ Use functools.cached_property for instance-level caching
class MyClass:
    @functools.cached_property
    def result(self):       # computed once, cached on instance
        return expensive_computation()

# ❌ Cache doesn't expire — use cachetools for TTL-based caching
# Cache grows until maxsize — monitor memory in long-running services
print(expensive.cache_info())   # CacheInfo(hits=..., misses=..., ...)
expensive.cache_clear()         # Manual clear
```

---

### 🔴 Advanced Level

**Q11: Explain Python's descriptor protocol. How does `@property` use it?**

**Answer:**
The descriptor protocol allows objects to customize attribute access. A descriptor is any object defining `__get__`, `__set__`, or `__delete__`. Python checks for descriptors in the MRO before returning attributes from `__dict__`.

- **Non-data descriptor** — defines only `__get__` (e.g., functions/methods)
- **Data descriptor** — defines `__get__` + `__set__`/`__delete__` (takes priority over instance `__dict__`)

`@property` is a built-in data descriptor:
```python
# What @property does internally:
class property:
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget, self.fset, self.fdel = fget, fset, fdel

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        if self.fget is None: raise AttributeError
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None: raise AttributeError("can't set")
        self.fset(obj, value)

# Lookup order: data descriptors > instance __dict__ > non-data descriptors
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property          # descriptor on the class
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

t = Temperature(100)
print(t.fahrenheit)  # 212.0 — calls __get__
# t.fahrenheit = 0   # ❌ AttributeError (no setter)
```

---

**Q12: What is Python's MRO and how does C3 linearization work?**

**Answer:**
**MRO (Method Resolution Order)** determines the order Python searches for attributes/methods in a class hierarchy. Python uses the **C3 linearization algorithm** (since Python 2.3) to compute a consistent, monotonic order.

**C3 algorithm rule:** `L(C) = C + merge(L(B1), L(B2), ..., [B1, B2, ...])`

Select the head of each list if it doesn't appear in the tail of any other list:
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Why? C3 ensures:
# 1. D comes before its parents
# 2. B comes before C (as declared)
# 3. Both before A (their common parent)
# 4. Monotonicity: subclass order is preserved

class X(B, C): pass
class Y(C, B): pass
# class Z(X, Y): pass  # ❌ TypeError: Cannot create consistent MRO
```
C3 prevents the "diamond problem" by establishing a clear, unambiguous lookup order.

---

**Q13: How would you implement a thread-safe LRU cache from scratch?**

**Answer:**
```python
import threading
from collections import OrderedDict
from typing import Generic, TypeVar, Optional

K = TypeVar("K")
V = TypeVar("V")

class LRUCache(Generic[K, V]):
    """Thread-safe LRU cache with O(1) get and put."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self._cache: OrderedDict[K, V] = OrderedDict()
        self._lock = threading.RLock()   # reentrant lock
        self._hits = 0
        self._misses = 0

    def get(self, key: K) -> Optional[V]:
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            self._cache.move_to_end(key)   # mark as recently used
            self._hits += 1
            return self._cache[key]

    def put(self, key: K, value: V) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)   # evict LRU (first item)

    def __len__(self) -> int:
        return len(self._cache)

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    def __repr__(self) -> str:
        return (f"LRUCache(capacity={self.capacity}, "
                f"size={len(self)}, hit_rate={self.hit_rate:.1%})")

# Usage
cache: LRUCache[str, int] = LRUCache(3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
print(cache.get("a"))   # 1 (a moves to end: b, c, a)
cache.put("d", 4)       # evicts b (LRU): c, a, d
print(cache.get("b"))   # None (evicted)
print(cache)            # LRUCache(capacity=3, size=3, hit_rate=50.0%)
```

---

**Q14: What are Python's `__slots__` and when should you use them? What are the tradeoffs?**

**Answer:**
`__slots__` replaces the per-instance `__dict__` with a fixed, C-level array of slots. This provides:

**Benefits:**
- ~40-50% memory reduction per instance
- ~10-20% faster attribute access
- Prevents accidental attribute creation

**Tradeoffs / Restrictions:**
```python
class Point:
    __slots__ = ("x", "y")

p = Point()
p.x, p.y = 1, 2
# p.z = 3        # ❌ AttributeError
# p.__dict__     # ❌ AttributeError — no __dict__

# ❌ Can't use __slots__ with multiple inheritance if both bases define __slots__
# ❌ Can't pickle by default without __getstate__/__setstate__
# ❌ Mixins with __dict__ break __slots__ efficiency

# When to use:
# ✅ Millions of small objects (particles, vectors, records)
# ✅ Objects with fixed, known attributes
# ✅ Performance-critical inner loop objects
# ❌ Don't use for objects needing dynamic attributes
# ❌ Don't use for complex inheritance hierarchies

import sys
class WithDict:
    def __init__(self, x, y): self.x, self.y = x, y

class WithSlots:
    __slots__ = ("x", "y")
    def __init__(self, x, y): self.x, self.y = x, y

print(sys.getsizeof(WithDict(1,2)) + sys.getsizeof(WithDict(1,2).__dict__))
# ~344 bytes
print(sys.getsizeof(WithSlots(1,2)))
# ~56 bytes → ~6x smaller!
```

---

**Q15: Explain `asyncio`'s event loop, coroutines, and tasks. How does `gather` differ from sequential `await`?**

**Answer:**
```
Event Loop
  │
  ├── Coroutine: async def fn() — a pausable function, not running yet
  │
  ├── Task: wraps coroutine, scheduled to run on event loop
  │          created by asyncio.create_task() or asyncio.gather()
  │
  └── Future: low-level awaitable representing an eventual result
```

```python
import asyncio, time

async def fetch(id, delay):
    print(f"Start {id}")
    await asyncio.sleep(delay)   # yields control back to event loop
    print(f"Done  {id}")
    return f"result_{id}"

# --- Sequential: total time = sum of delays ---
async def sequential():
    start = time.time()
    r1 = await fetch(1, 1.0)    # waits 1s
    r2 = await fetch(2, 1.0)    # then waits 1s
    print(f"Sequential: {time.time()-start:.2f}s")  # ~2.0s

# --- Concurrent with gather: total time = max delay ---
async def concurrent():
    start = time.time()
    r1, r2 = await asyncio.gather(
        fetch(1, 1.0),
        fetch(2, 1.0)
    )   # both run concurrently
    print(f"Concurrent: {time.time()-start:.2f}s")  # ~1.0s

asyncio.run(sequential())
asyncio.run(concurrent())

# gather vs create_task:
# gather(*coros) — schedules all, returns when ALL complete
# create_task(coro) — schedules immediately, returns Task (can be awaited later)

async def with_tasks():
    task1 = asyncio.create_task(fetch(1, 1.0))   # starts immediately
    task2 = asyncio.create_task(fetch(2, 0.5))   # starts immediately
    r2 = await task2   # get result of faster task first
    r1 = await task1
    return r1, r2
```

The event loop continuously:
1. Picks the next ready coroutine
2. Runs it until it hits `await`
3. Registers the I/O callback
4. Moves to the next ready coroutine
5. Resumes suspended coroutines when their I/O completes

---

## Coding Challenges {#coding-challenges}

### Challenge 1: Async Rate-Limited API Client

**📋 Problem:**
Implement an async function `batch_fetch(urls, max_concurrent=5)` that:
1. Fetches all URLs concurrently
2. Limits to `max_concurrent` requests at a time (using `asyncio.Semaphore`)
3. Retries failed requests up to 3 times with exponential backoff
4. Returns a list of `(url, result_or_error)` tuples preserving original order

**📥 Input/Output:**
```python
urls = [f"https://api.example.com/item/{i}" for i in range(20)]
results = asyncio.run(batch_fetch(urls, max_concurrent=5))
# [
#   ("https://api.example.com/item/0", "data_0"),
#   ("https://api.example.com/item/1", "ERROR: Timeout"),
#   ...
# ]
```

**✅ Solution:**
```python
import asyncio
import random
from typing import Any

async def fetch_with_retry(
    session,
    url: str,
    semaphore: asyncio.Semaphore,
    max_retries: int = 3
) -> tuple[str, Any]:
    """Fetch a URL with semaphore-limited concurrency and retry logic."""

    async def attempt() -> str:
        # Simulate real HTTP call
        await asyncio.sleep(random.uniform(0.1, 0.5))
        if random.random() < 0.2:              # 20% failure rate
            raise ConnectionError("Timeout")
        return f"data_from_{url.split('/')[-1]}"

    async with semaphore:                      # enforce concurrency limit
        last_error = None
        for attempt_num in range(max_retries):
            try:
                result = await attempt()
                return (url, result)
            except Exception as e:
                last_error = e
                backoff = 2 ** attempt_num * 0.1    # 0.1s, 0.2s, 0.4s
                if attempt_num < max_retries - 1:
                    print(f"Retry {attempt_num+1}/{max_retries} for {url}: {e}")
                    await asyncio.sleep(backoff)
        return (url, f"ERROR: {last_error}")        # all retries exhausted


async def batch_fetch(
    urls: list[str],
    max_concurrent: int = 5
) -> list[tuple[str, Any]]:
    """
    Fetch all URLs concurrently with rate limiting and retry.

    Args:
        urls:           List of URLs to fetch
        max_concurrent: Maximum simultaneous requests

    Returns:
        List of (url, result_or_error) in original order
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async with asyncio.TaskGroup() as tg:     # Python 3.11+
        tasks = [
            tg.create_task(fetch_with_retry(None, url, semaphore))
            for url in urls
        ]

    # Results preserve original order (task.result() per task)
    return [task.result() for task in tasks]


# Test
async def main():
    urls = [f"https://api.example.com/item/{i}" for i in range(15)]

    import time
    start = time.time()
    results = await batch_fetch(urls, max_concurrent=5)
    elapsed = time.time() - start

    success = sum(1 for _, r in results if not str(r).startswith("ERROR"))
    errors  = len(results) - success

    print(f"\nCompleted {len(results)} requests in {elapsed:.2f}s")
    print(f"Success: {success} | Errors: {errors}")
    for url, result in results[:5]:
        print(f"  {url.split('/')[-1]}: {result}")

asyncio.run(main())
```

**💡 Explanation:**
- `asyncio.Semaphore(5)` — at most 5 coroutines inside the `async with` block simultaneously
- Exponential backoff: `2^attempt * 0.1` → 0.1s, 0.2s, 0.4s between retries
- `asyncio.TaskGroup` (Python 3.11+) — structured concurrency; cancels all tasks if any raises
- Original order preserved by using `task.result()` per task in order
- Total time ≈ `max(task_times)` not `sum(task_times)` — true concurrency

---

### Challenge 2: Generic Event System with Type Safety

**📋 Problem:**
Build a type-safe, generic event system `EventBus[T]` that:
1. Supports typed events using `TypeVar` and `Generic`
2. Allows subscribing handlers with `@bus.on(EventType)`
3. Emits events asynchronously to all subscribed handlers
4. Supports unsubscribing and one-time listeners (`once`)
5. Provides middleware support for event transformation

**📥 Input/Output:**
```python
@dataclass
class UserCreated:
    user_id: int
    email: str

bus = EventBus()
bus.emit(UserCreated(1, "alice@example.com"))
# → Handler 1: New user #1 (alice@example.com)
# → Audit: UserCreated event fired
```

**✅ Solution:**
```python
import asyncio
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Awaitable, Any
from collections import defaultdict
import functools
import inspect

T = TypeVar("T")
Handler = Callable[[Any], Awaitable[None] | None]
Middleware = Callable[[Any, Callable], Awaitable[None]]


class EventBus:
    """
    Type-safe async event bus with middleware support.

    Supports sync and async handlers, one-time listeners,
    and event transformation middleware.
    """

    def __init__(self):
        self._handlers: dict[type, list[tuple[Handler, bool]]] = defaultdict(list)
        # (handler, is_once)
        self._middleware: list[Middleware] = []
        self._event_count: dict[type, int] = defaultdict(int)

    def use(self, middleware: Middleware) -> "EventBus":
        """Add middleware. middleware(event, next) → called before handlers."""
        self._middleware.append(middleware)
        return self

    def on(self, event_type: type) -> Callable:
        """Decorator to subscribe a handler to an event type."""
        def decorator(handler: Handler) -> Handler:
            self._handlers[event_type].append((handler, False))
            return handler
        return decorator

    def once(self, event_type: type) -> Callable:
        """Decorator: handler called only once, then auto-unsubscribed."""
        def decorator(handler: Handler) -> Handler:
            self._handlers[event_type].append((handler, True))
            return handler
        return decorator

    def off(self, event_type: type, handler: Handler) -> None:
        """Unsubscribe a handler."""
        self._handlers[event_type] = [
            (h, once) for h, once in self._handlers[event_type]
            if h is not handler
        ]

    async def emit(self, event: Any) -> None:
        """Emit an event, running all handlers (with middleware)."""
        event_type = type(event)
        self._event_count[event_type] += 1

        async def run_handlers(evt):
            handlers = self._handlers.get(event_type, [])
            # Collect one-time handlers to remove
            to_remove = []
            for handler, is_once in handlers:
                if is_once:
                    to_remove.append(handler)
                # Support both sync and async handlers
                if inspect.iscoroutinefunction(handler):
                    await handler(evt)
                else:
                    handler(evt)
            # Remove one-time handlers
            for h in to_remove:
                self.off(event_type, h)

        # Build middleware chain
        async def dispatch(evt):
            await run_handlers(evt)

        chain = dispatch
        for mw in reversed(self._middleware):
            current_chain = chain
            async def make_chain(e, mw=mw, next_=current_chain):
                await mw(e, next_)
            chain = make_chain

        await chain(event)

    def stats(self) -> dict[str, int]:
        return {t.__name__: c for t, c in self._event_count.items()}


# --- Usage ---
@dataclass
class UserCreated:
    user_id: int
    email: str

@dataclass
class OrderPlaced:
    order_id: str
    amount: float
    user_id: int


async def main():
    bus = EventBus()

    # --- Middleware: logging ---
    async def logging_middleware(event, next_handler):
        print(f"[MW] Event fired: {type(event).__name__}")
        await next_handler(event)
        print(f"[MW] Event handled: {type(event).__name__}")

    bus.use(logging_middleware)

    # --- Subscribe handlers ---
    @bus.on(UserCreated)
    async def send_welcome_email(event: UserCreated):
        await asyncio.sleep(0.01)    # simulate async email send
        print(f"  📧 Welcome email sent to {event.email}")

    @bus.on(UserCreated)
    def audit_log(event: UserCreated):
        print(f"  📋 Audit: User #{event.user_id} created")

    @bus.once(UserCreated)
    def first_user_bonus(event: UserCreated):
        print(f"  🎁 First-user bonus applied to #{event.user_id}")

    @bus.on(OrderPlaced)
    async def process_payment(event: OrderPlaced):
        print(f"  💳 Processing payment of ${event.amount} for order {event.order_id}")

    # --- Emit events ---
    print("=== First UserCreated ===")
    await bus.emit(UserCreated(1, "alice@example.com"))

    print("\n=== Second UserCreated ===")
    await bus.emit(UserCreated(2, "bob@example.com"))
    # Note: first_user_bonus NOT called (once listener removed)

    print("\n=== OrderPlaced ===")
    await bus.emit(OrderPlaced("ORD-001", 99.99, 1))

    print("\n=== Stats ===")
    print(bus.stats())
    # {'UserCreated': 2, 'OrderPlaced': 1}


asyncio.run(main())
```

**💡 Explanation:**
- `defaultdict(list)` — auto-initializes handler lists per event type
- Middleware chain — built using closure composition; each middleware wraps `next_handler`
- `inspect.iscoroutinefunction` — transparently supports both sync and async handlers
- One-time handlers tracked with `(handler, is_once)` tuples; removed after first call
- `EventBus` is fully decoupled — emitters don't know about subscribers
- Async-first design with `asyncio` — non-blocking handler execution

---

## Final Summary {#final-summary}

```
╔══════════════════════════════════════════════════════════════════╗
║            PYTHON ADVANCED — KNOWLEDGE MAP                       ║
╠══════════════════════════════════════════════════════════════════╣
║  Module 1   → Iterators, Generators, yield from, send()          ║
║  Module 2   → Decorators, Closures, lru_cache, Class Decorators  ║
║  Module 3   → Context Managers, ExitStack, contextmanager        ║
║  Module 4   → Functional: itertools, functools, partial          ║
║  Module 5   → Metaclasses, Descriptors, __slots__, ABCs          ║
║  Module 6   → Threading, Multiprocessing, AsyncIO                ║
║  Module 7   → Memory Management, Profiling, Optimization         ║
║  Module 8   → Type Hints, Generics, Protocols                    ║
║  Module 9   → Advanced Collections: deque, Counter, heapq        ║
║  Module 10  → Design Patterns: Factory, Observer, Builder        ║
╠══════════════════════════════════════════════════════════════════╣
║  TOP ADVANCED PYTHON TRAPS:                                      ║
║  1. Generators exhausted after one pass                          ║
║  2. Forgetting @functools.wraps in decorators                    ║
║  3. Using threading for CPU-bound work (GIL blocks you)          ║
║  4. Blocking the event loop with sync code in async functions    ║
║  5. __exit__ returning True silently suppresses exceptions       ║
║  6. heapq is min-heap only — negate for max-heap                 ║
║  7. lru_cache requires hashable arguments                        ║
╠══════════════════════════════════════════════════════════════════╣
║  SENIOR ENGINEER CHECKLIST:                                      ║
║  ✅ Can explain GIL and its concurrency implications              ║
║  ✅ Can implement decorators with and without arguments           ║
║  ✅ Knows when to use async vs threading vs multiprocessing       ║
║  ✅ Understands descriptor protocol and how @property works       ║
║  ✅ Can implement thread-safe data structures                     ║
║  ✅ Profiles before optimizing                                    ║
║  ✅ Uses type hints + mypy in production code                     ║
╠══════════════════════════════════════════════════════════════════╣
║  NEXT STEPS:                                                     ║
║  → Python Internals (bytecode, dis module, CPython source)       ║
║  → Advanced AsyncIO (aiohttp, FastAPI, Starlette)                ║
║  → Python packaging (pyproject.toml, hatch, uv)                  ║
║  → Testing: pytest fixtures, mocking, property-based testing     ║
║  → C Extensions & Cython for performance-critical code           ║
╚══════════════════════════════════════════════════════════════════╝
```

> 💡 **Senior Engineer Mindset:** Advanced Python isn't about using every feature — it's about knowing *why* each tool exists, *when* to reach for it, and *what tradeoffs* it brings. The engineers who master generators, descriptors, and async patterns write code that is not just correct, but elegant and performant at scale.

---
*Guide created for advanced learning and senior-level interview preparation. Python version: 3.10+*
