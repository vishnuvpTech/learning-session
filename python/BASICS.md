## 📂 Python Learning Files
[**Basics**](BASICS.md) | [Advanced](ADVANCED.md) | [SQL](SQL.md) | [Senior Dev Guide](README.md)

---

# 🐍 Python Basics – Structured Learning & Interview Preparation Guide

> **Level:** Beginner → Advanced Basics  
> **Role:** Software Engineer / Technical Trainer / Interviewer  
> **Goal:** Master Python fundamentals and ace technical interviews

---

## Table of Contents
1. [Module 1: Python Introduction & Setup](#module-1)
2. [Module 2: Variables, Data Types & Operators](#module-2)
3. [Module 3: Control Flow – Conditionals & Loops](#module-3)
4. [Module 4: Functions](#module-4)
5. [Module 5: Data Structures – Lists, Tuples, Sets, Dicts](#module-5)
6. [Module 6: String Manipulation](#module-6)
7. [Module 7: File Handling](#module-7)
8. [Module 8: Exception Handling](#module-8)
9. [Module 9: Modules, Packages & Imports](#module-9)
10. [Module 10: OOP Basics in Python](#module-10)
11. [Interview Questions](#interview-questions)
12. [Coding Challenges](#coding-challenges)
13. [Final Summary](#final-summary)

---

## Module 1: Python Introduction & Setup {#module-1}

### 📖 Explanation
Python is a high-level, interpreted, dynamically-typed, general-purpose programming language. It emphasizes readability and simplicity, making it one of the most beginner-friendly and widely-used languages in the world — from web development to data science and AI.

### 🔑 Key Concepts
- **Interpreted:** Code runs line by line; no compilation step needed.
- **Dynamically typed:** Variable types are inferred at runtime.
- **Indentation-based:** Python uses whitespace (indentation) instead of `{}` for blocks.
- **Garbage collected:** Memory is managed automatically.
- **CPython:** The default and most widely used Python interpreter.

### 💻 Example
```python
# Your first Python program
print("Hello, World!")

# Python version check
import sys
print(sys.version)
```

### 🏭 Real-world Use Cases
- Scripting & automation (DevOps pipelines)
- Web development (Django, Flask, FastAPI)
- Data Science & ML (NumPy, Pandas, TensorFlow)
- API development and microservices

### ⚠️ Common Mistakes
- Mixing tabs and spaces (causes `IndentationError`)
- Using Python 2 syntax in Python 3 environments
- Forgetting that Python is case-sensitive (`Print` ≠ `print`)

### ✅ Best Practices
- Always use Python 3.8+
- Use virtual environments (`venv` or `conda`) per project
- Follow PEP 8 style guide for clean, readable code
- Use `python --version` to verify your environment

### 📝 Mini Summary
> Python is readable, versatile, and beginner-friendly. Its clean syntax and massive ecosystem make it the top choice for beginners and professionals alike.

---

## Module 2: Variables, Data Types & Operators {#module-2}

### 📖 Explanation
Variables are named containers for storing data. Python is dynamically typed, meaning you don't declare types explicitly. Python supports several built-in data types and a rich set of operators.

### 🔑 Key Concepts
| Category | Types |
|---|---|
| Numeric | `int`, `float`, `complex` |
| Text | `str` |
| Boolean | `bool` (`True` / `False`) |
| None | `NoneType` |
| Operators | Arithmetic, Comparison, Logical, Assignment, Bitwise, Identity (`is`), Membership (`in`) |

### 💻 Example
```python
# Variables & types
name = "Alice"          # str
age = 30                # int
height = 5.7            # float
is_active = True        # bool
score = None            # NoneType

# Type checking
print(type(name))       # <class 'str'>
print(isinstance(age, int))  # True

# Operators
x, y = 10, 3
print(x + y)    # 13  → Arithmetic
print(x // y)   # 3   → Floor division
print(x ** y)   # 1000 → Exponent
print(x % y)    # 1   → Modulus
print(x > y and y > 0)  # True → Logical

# Identity & Membership
a = [1, 2, 3]
print(2 in a)       # True
print(a is a)       # True
print(a is [1,2,3]) # False (different objects)

# Type conversion
print(int("42"))    # 42
print(str(100))     # "100"
print(float("3.14"))# 3.14
```

### 🏭 Real-world Use Cases
- Storing user form inputs (strings, ints)
- Tracking boolean feature flags
- Processing prices and calculations (float)
- Config values and environment variables

### ⚠️ Common Mistakes
```python
# Mutable default pitfall
x = None
print(x == None)  # Works but bad practice
print(x is None)  # ✅ Correct way to check None

# Integer division surprise
print(7 / 2)   # 3.5  (true division)
print(7 // 2)  # 3    (floor division)

# String + int without conversion
age = 25
# print("Age: " + age)      # ❌ TypeError
print("Age: " + str(age))   # ✅ Correct
```

### ✅ Best Practices
- Use `is` / `is not` for `None` comparisons, not `==`
- Use f-strings over `+` concatenation for readability
- Use descriptive variable names (`user_age` over `ua`)
- Avoid single-letter names except in loops (`i`, `j`, `k`)

### 📝 Mini Summary
> Python's dynamic typing makes it flexible but requires careful type awareness. Master operators and type conversions to avoid subtle bugs.

---

## Module 3: Control Flow – Conditionals & Loops {#module-3}

### 📖 Explanation
Control flow allows your program to make decisions (`if/elif/else`) and repeat actions (`for`/`while` loops). Python's clean syntax makes these constructs very readable.

### 🔑 Key Concepts
- `if / elif / else` — branching logic
- `for` — iterate over sequences
- `while` — loop while condition is True
- `break` — exit a loop early
- `continue` — skip current iteration
- `pass` — placeholder (no-op)
- `range()` — generate number sequences
- List comprehension — concise loop-based list creation

### 💻 Example
```python
# --- Conditionals ---
score = 85

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(f"Grade: {grade}")  # Grade: B

# Ternary (one-liner)
status = "Pass" if score >= 60 else "Fail"

# --- For Loop ---
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit.upper())

# With range
for i in range(1, 6):    # 1 to 5
    print(i, end=" ")    # 1 2 3 4 5

# Enumerate (index + value)
for idx, fruit in enumerate(fruits, start=1):
    print(f"{idx}. {fruit}")

# --- While Loop ---
count = 0
while count < 5:
    print(count)
    count += 1

# --- Break & Continue ---
for n in range(10):
    if n == 3:
        continue    # skip 3
    if n == 7:
        break       # stop at 7
    print(n)

# --- List Comprehension ---
squares = [x**2 for x in range(1, 6)]
# [1, 4, 9, 16, 25]

evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### 🏭 Real-world Use Cases
- Validating user inputs with conditions
- Iterating over API response lists
- Polling loops with `while` (e.g., retry logic)
- Filtering/transforming data with list comprehensions

### ⚠️ Common Mistakes
```python
# Infinite loop — forgetting to update condition
# while True:
#     print("oops")  # ❌ Never ends

# Modifying a list while iterating
items = [1, 2, 3, 4]
# for item in items:
#     items.remove(item)  # ❌ Skips elements

# Safe way — iterate over a copy
for item in items[:]:
    items.remove(item)  # ✅

# off-by-one with range
for i in range(5):   # 0,1,2,3,4 — NOT 5
    pass
```

### ✅ Best Practices
- Prefer list comprehensions over `map()`/`filter()` for readability
- Use `enumerate()` instead of `range(len(...))`
- Avoid deeply nested `if` blocks — use early returns
- Always ensure `while` loops have a termination condition

### 📝 Mini Summary
> Control flow is the backbone of any program. Python's for-loops and list comprehensions are especially powerful for processing collections efficiently.

---

## Module 4: Functions {#module-4}

### 📖 Explanation
Functions are reusable blocks of code that perform a specific task. They promote the DRY principle (Don't Repeat Yourself), improve readability, and make testing easier.

### 🔑 Key Concepts
- `def` — define a function
- Parameters vs Arguments
- Default parameters
- `*args` — variable positional arguments (tuple)
- `**kwargs` — variable keyword arguments (dict)
- Return values (multiple returns)
- Lambda functions (anonymous)
- Docstrings
- Scope: Local vs Global (`global`, `nonlocal`)

### 💻 Example
```python
# Basic function with docstring
def greet(name, greeting="Hello"):
    """Return a greeting string for the given name."""
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!

# *args and **kwargs
def summarize(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

summarize(1, 2, 3, name="Alice", role="Dev")
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'role': 'Dev'}

# Multiple return values (returns a tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 9, 5])
print(low, high)  # 1 9

# Lambda
square = lambda x: x ** 2
print(square(5))  # 25

# Useful with sorted()
students = [("Alice", 88), ("Bob", 72), ("Charlie", 95)]
ranked = sorted(students, key=lambda s: s[1], reverse=True)
print(ranked)

# Scope
x = 10  # global

def modify():
    global x
    x = 99

modify()
print(x)  # 99
```

### 🏭 Real-world Use Cases
- Encapsulating API call logic
- Validation functions reused across forms
- Lambda functions in `sorted()`, `map()`, `filter()`
- Utility/helper functions in larger applications

### ⚠️ Common Mistakes
```python
# Mutable default argument — classic Python gotcha!
def add_item(item, lst=[]):   # ❌ Shared across calls!
    lst.append(item)
    return lst

# ✅ Correct pattern
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

# Forgetting return
def add(a, b):
    result = a + b
    # Missing return → returns None ❌

# Confusing *args unpacking
def fn(a, b, c): pass
args = [1, 2, 3]
fn(*args)   # ✅ Correct unpacking
```

### ✅ Best Practices
- Always write docstrings for public functions
- Keep functions small — one responsibility per function
- Use type hints for clarity: `def greet(name: str) -> str:`
- Avoid `global` — pass data as parameters instead
- Prefer explicit `return` statements

### 📝 Mini Summary
> Functions are the building blocks of maintainable code. Master `*args`, `**kwargs`, and avoid the mutable default argument trap.

---

## Module 5: Data Structures – Lists, Tuples, Sets, Dicts {#module-5}

### 📖 Explanation
Python has four powerful built-in data structures. Choosing the right one for the right situation is a hallmark of a good Python developer.

### 🔑 Key Concepts
| Structure | Ordered | Mutable | Duplicates | Syntax |
|---|---|---|---|---|
| List | ✅ | ✅ | ✅ | `[1, 2, 3]` |
| Tuple | ✅ | ❌ | ✅ | `(1, 2, 3)` |
| Set | ❌ | ✅ | ❌ | `{1, 2, 3}` |
| Dict | ✅ (3.7+) | ✅ | Keys: ❌ | `{"k": "v"}` |

### 💻 Example
```python
# --- LIST ---
nums = [1, 2, 3, 4, 5]
nums.append(6)          # Add to end
nums.insert(0, 0)       # Insert at index
nums.remove(3)          # Remove by value
popped = nums.pop()     # Remove & return last
nums.sort(reverse=True)
print(nums[1:4])        # Slicing: [5, 4, 2]

# --- TUPLE ---
point = (10, 20)
x, y = point            # Unpacking
print(x, y)             # 10 20
# point[0] = 99         # ❌ TypeError — immutable

# Named tuple (more readable)
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)         # 3 4

# --- SET ---
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)   # Union:        {1,2,3,4,5,6}
print(a & b)   # Intersection: {3,4}
print(a - b)   # Difference:   {1,2}
print(a ^ b)   # Symmetric diff: {1,2,5,6}

# Remove duplicates from list
unique = list(set([1,2,2,3,3,3]))  # [1,2,3]

# --- DICT ---
user = {"name": "Alice", "age": 30, "active": True}
print(user["name"])             # Alice
print(user.get("email", "N/A")) # N/A (safe access)
user["email"] = "alice@x.com"   # Add/update
del user["active"]              # Delete key

# Iterating
for key, value in user.items():
    print(f"{key}: {value}")

# Dict comprehension
squares = {x: x**2 for x in range(1, 6)}
# {1:1, 2:4, 3:9, 4:16, 5:25}

# Merging dicts (Python 3.9+)
d1 = {"a": 1}
d2 = {"b": 2}
merged = d1 | d2    # {"a":1, "b":2}
```

### 🏭 Real-world Use Cases
- **List** — ordered collections, task queues, API response arrays
- **Tuple** — coordinates, DB records, function returns (immutable safety)
- **Set** — deduplication, membership testing, tag systems
- **Dict** — JSON-like data, caching, config objects, lookup tables

### ⚠️ Common Mistakes
```python
# Dict key access vs .get()
d = {"name": "Alice"}
# print(d["email"])        # ❌ KeyError
print(d.get("email"))      # ✅ None (safe)

# Comparing list vs set lookup — O(n) vs O(1)
big_list = list(range(100000))
big_set = set(range(100000))
# 99999 in big_list  → slow O(n)
# 99999 in big_set   → fast O(1) ✅

# Tuple with single item needs trailing comma
t = (42,)   # ✅ Tuple
t = (42)    # ❌ Just an integer
```

### ✅ Best Practices
- Use `dict.get()` with a default to avoid `KeyError`
- Prefer sets for membership testing over lists
- Use tuples for data that shouldn't change (safer + faster)
- Use `defaultdict` or `Counter` from `collections` when applicable

### 📝 Mini Summary
> Choosing the right data structure improves both correctness and performance. Know the tradeoffs: mutability, ordering, and lookup complexity.

---

## Module 6: String Manipulation {#module-6}

### 📖 Explanation
Strings in Python are immutable sequences of characters. Python provides an incredibly rich set of string methods, making text processing straightforward and powerful.

### 🔑 Key Concepts
- Strings are immutable — operations create new strings
- Indexing and slicing
- Common methods: `upper()`, `lower()`, `strip()`, `split()`, `join()`, `replace()`, `find()`, `startswith()`, `endswith()`
- f-strings (formatted string literals) — Python 3.6+
- Multiline strings with `"""`
- Raw strings `r"..."` for regex/paths

### 💻 Example
```python
s = "  Hello, World!  "

# Cleaning
print(s.strip())            # "Hello, World!"
print(s.lstrip())           # "Hello, World!  "

# Case
print(s.lower())            # "  hello, world!  "
print(s.upper())            # "  HELLO, WORLD!  "
print("hello world".title())# "Hello World"

# Search
print("World" in s)         # True
print(s.find("World"))      # 9
print(s.startswith("  H"))  # True

# Replace & Split
clean = s.strip()
print(clean.replace("World", "Python"))  # "Hello, Python!"
words = clean.split(", ")               # ['Hello', 'World!']

# Join
print(" | ".join(["a", "b", "c"]))  # "a | b | c"

# Slicing
text = "Python"
print(text[0])      # P
print(text[-1])     # n
print(text[1:4])    # yth
print(text[::-1])   # nohtyP  (reverse)

# f-strings (preferred)
name, age = "Alice", 30
print(f"Name: {name}, Age: {age}")          # basic
print(f"Pi: {3.14159:.2f}")                 # formatting
print(f"{'Alice':>10}")                     # right-align

# Multiline
msg = """
Dear Alice,
Welcome aboard!
"""

# Raw string (useful for regex and Windows paths)
path = r"C:\Users\Alice\Documents"
```

### 🏭 Real-world Use Cases
- Parsing CSV/log files with `split()`
- Sanitizing user input with `strip()` and `replace()`
- Building dynamic SQL queries or API URLs
- Template generation with f-strings

### ⚠️ Common Mistakes
```python
# String concatenation in loops — very slow!
result = ""
for i in range(1000):
    result += str(i)     # ❌ O(n²) — creates new string each time

result = "".join(str(i) for i in range(1000))  # ✅ O(n)

# Forgetting strings are immutable
s = "hello"
# s[0] = "H"    # ❌ TypeError
s = "H" + s[1:] # ✅ Create a new string
```

### ✅ Best Practices
- Use f-strings over `%` formatting or `.format()`
- Use `"".join(list)` for building strings in loops
- Use `str.strip()` to sanitize inputs before processing
- Use `str.splitlines()` to safely handle multiline text

### 📝 Mini Summary
> Python's string methods are expressive and powerful. Master f-strings and avoid concatenation in loops for production-quality code.

---

## Module 7: File Handling {#module-7}

### 📖 Explanation
File I/O allows programs to read from and write to files on the filesystem. Python's built-in `open()` function, combined with context managers (`with`), makes this safe and clean.

### 🔑 Key Concepts
- `open(filename, mode)` — modes: `r`, `w`, `a`, `x`, `rb`, `wb`
- Context manager `with open(...) as f:` — auto-closes file
- `read()`, `readline()`, `readlines()`
- `write()`, `writelines()`
- `os` and `pathlib` modules for path operations

### 💻 Example
```python
# --- Writing ---
with open("notes.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.writelines(["Line 3\n", "Line 4\n"])

# --- Reading ---
with open("notes.txt", "r") as f:
    content = f.read()          # Entire file as string
    print(content)

with open("notes.txt", "r") as f:
    for line in f:              # Memory-efficient
        print(line.strip())

with open("notes.txt", "r") as f:
    lines = f.readlines()       # List of lines

# --- Appending ---
with open("notes.txt", "a") as f:
    f.write("Line 5\n")

# --- JSON File (very common) ---
import json

data = {"name": "Alice", "scores": [95, 88, 92]}

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

with open("data.json", "r") as f:
    loaded = json.load(f)
    print(loaded["name"])       # Alice

# --- pathlib (modern approach) ---
from pathlib import Path

p = Path("notes.txt")
print(p.exists())           # True
print(p.suffix)             # .txt
print(p.stem)               # notes
p.write_text("New content") # Write directly
content = p.read_text()     # Read directly
```

### 🏭 Real-world Use Cases
- Reading config files (`.json`, `.yaml`, `.env`)
- Writing logs and reports
- Processing CSV/TSV data files
- Batch file operations in automation scripts

### ⚠️ Common Mistakes
```python
# Not using context manager — file may not close on error
f = open("file.txt", "r")
data = f.read()
# If exception happens here, f.close() is never called ❌
f.close()

# Always use with:
with open("file.txt", "r") as f:  # ✅ Auto-closes
    data = f.read()

# Overwriting instead of appending
with open("log.txt", "w") as f:   # ❌ Erases existing
    f.write("new log")

with open("log.txt", "a") as f:   # ✅ Appends
    f.write("new log\n")
```

### ✅ Best Practices
- Always use `with` statement for file operations
- Use `pathlib.Path` over `os.path` for modern code
- Specify encoding explicitly: `open("f.txt", "r", encoding="utf-8")`
- Use `json.dump/load` for structured data persistence

### 📝 Mini Summary
> Always use `with` blocks for file handling. Prefer `pathlib` for path manipulation and `json` module for structured data.

---

## Module 8: Exception Handling {#module-8}

### 📖 Explanation
Exceptions are errors that occur at runtime. Python's `try/except/else/finally` mechanism lets you handle errors gracefully without crashing the program.

### 🔑 Key Concepts
- `try` — code that might raise an exception
- `except` — handle specific exceptions
- `else` — runs if no exception occurred
- `finally` — always runs (cleanup)
- `raise` — manually raise an exception
- Custom exceptions by subclassing `Exception`
- Common built-ins: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, `ZeroDivisionError`

### 💻 Example
```python
# Basic try/except
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Math error: {e}")

# Multiple exceptions
def safe_convert(value):
    try:
        return int(value)
    except ValueError:
        print(f"Cannot convert '{value}' to int")
        return None
    except TypeError:
        print("Value must be a string or number")
        return None

# else & finally
def read_file(path):
    try:
        with open(path, "r") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File '{path}' not found")
        return None
    else:
        print("File read successfully")   # runs only if no exception
        return data
    finally:
        print("Attempted to read file")   # always runs

# Raising exceptions
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is out of valid range")
    return age

# Custom Exception
class InsufficientFundsError(Exception):
    def __init__(self, amount, balance):
        self.amount = amount
        self.balance = balance
        super().__init__(
            f"Cannot withdraw {amount}. Balance is only {balance}."
        )

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(amount, balance)
    return balance - amount

try:
    withdraw(100, 200)
except InsufficientFundsError as e:
    print(e)
```

### 🏭 Real-world Use Cases
- Handling network request failures (retries)
- Validating API input and raising HTTP errors
- Database connection failure handling
- File parsing with malformed data protection

### ⚠️ Common Mistakes
```python
# Catching bare Exception — hides bugs
try:
    do_something()
except:          # ❌ Catches EVERYTHING including SystemExit
    pass

# Catching too broadly
try:
    result = risky_operation()
except Exception as e:
    print("Something went wrong")    # ❌ Swallows detail
    # ✅ At minimum: log the error
    import logging
    logging.exception("Operation failed")

# Silently passing exceptions
try:
    int("abc")
except ValueError:
    pass    # ❌ Silent failure is dangerous in production
```

### ✅ Best Practices
- Catch specific exceptions, not bare `except:`
- Never silently `pass` exceptions in production code
- Use `finally` for cleanup (closing connections, files)
- Create custom exceptions for domain-specific errors
- Log exceptions with full traceback using `logging.exception()`

### 📝 Mini Summary
> Robust error handling separates amateur scripts from production code. Be specific, never silent, and always clean up in `finally`.

---

## Module 9: Modules, Packages & Imports {#module-9}

### 📖 Explanation
Modules allow you to organize code into reusable files. Packages are directories of modules. Python's standard library and the PyPI ecosystem give you access to thousands of pre-built tools.

### 🔑 Key Concepts
- `import module` — import entire module
- `from module import name` — import specific item
- `as` — aliasing
- `__name__ == "__main__"` guard
- Standard library essentials: `os`, `sys`, `math`, `datetime`, `random`, `collections`, `itertools`, `functools`
- `pip` — package manager for third-party packages
- Virtual environments — isolated dependency management

### 💻 Example
```python
# Different import styles
import math
from math import sqrt, pi
from datetime import datetime, timedelta
import os
import sys

# Using standard library
print(math.ceil(4.2))          # 5
print(sqrt(16))                # 4.0
print(f"Pi = {pi:.4f}")        # Pi = 3.1416

# datetime
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M"))
tomorrow = now + timedelta(days=1)

# os module
print(os.getcwd())             # Current directory
print(os.path.join("usr", "local", "bin"))  # Cross-platform path
files = os.listdir(".")        # List directory
os.environ.get("HOME", "/tmp") # Environment variable

# collections
from collections import Counter, defaultdict, deque

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
count = Counter(words)
print(count.most_common(2))    # [('apple', 3), ('banana', 2)]

dd = defaultdict(list)
dd["fruits"].append("apple")   # No KeyError!

q = deque([1, 2, 3])
q.appendleft(0)                # Efficient left insert
q.popleft()                    # Efficient left pop

# The __main__ guard
def main():
    print("Running as main script")

if __name__ == "__main__":
    main()   # Only runs when script is executed directly
```

### 🏭 Real-world Use Cases
- `os`/`pathlib` — file system operations in DevOps scripts
- `datetime` — logging timestamps, scheduling
- `collections.Counter` — word frequency, analytics
- `json` — REST API data parsing
- Third-party: `requests`, `pandas`, `numpy`, `pytest`

### ⚠️ Common Mistakes
```python
# Circular imports
# a.py imports b.py, b.py imports a.py → ImportError ❌

# Wildcard imports — pollutes namespace
from math import *   # ❌ Unclear where symbols come from

# Forgetting __main__ guard in scripts used as modules
# Without it, code runs on import unintentionally ❌
```

### ✅ Best Practices
- Avoid `from module import *` — be explicit
- Always use the `if __name__ == "__main__":` guard
- Group imports: stdlib → third-party → local (PEP 8)
- Use virtual environments for every project (`python -m venv venv`)
- Pin dependencies in `requirements.txt`

### 📝 Mini Summary
> Modules and packages are the foundation of scalable Python projects. Use the standard library aggressively before reaching for third-party tools.

---

## Module 10: OOP Basics in Python {#module-10}

### 📖 Explanation
Object-Oriented Programming (OOP) organizes code around objects — bundles of data (attributes) and behavior (methods). Python supports OOP fully with classes, inheritance, and encapsulation.

### 🔑 Key Concepts
- `class` — define a blueprint
- `__init__` — constructor method
- `self` — reference to the instance
- Instance vs Class attributes
- Instance vs Class vs Static methods
- Inheritance & `super()`
- Encapsulation with `_` (protected) and `__` (private)
- `__str__` and `__repr__` dunder methods
- `@property` decorator

### 💻 Example
```python
class BankAccount:
    bank_name = "PyBank"   # Class attribute (shared)

    def __init__(self, owner, balance=0.0):
        self.owner = owner            # Instance attribute
        self.__balance = balance      # Private (name mangling)
        self._transactions = []       # Protected

    # Property — controlled access
    @property
    def balance(self):
        return self.__balance

    # Instance method
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
        self._transactions.append(f"+{amount}")
        return self

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self._transactions.append(f"-{amount}")
        return self

    # Class method
    @classmethod
    def from_dict(cls, data):
        return cls(data["owner"], data["balance"])

    # Static method
    @staticmethod
    def validate_amount(amount):
        return isinstance(amount, (int, float)) and amount > 0

    # Dunder methods
    def __str__(self):
        return f"Account({self.owner}: ${self.__balance:.2f})"

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.__balance})"


# Inheritance
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0.0, interest_rate=0.03):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        return interest


# Usage
acc = BankAccount("Alice", 1000)
acc.deposit(500).withdraw(200)   # Method chaining
print(acc)                        # Account(Alice: $1300.00)
print(acc.balance)                # 1300.0

savings = SavingsAccount("Bob", 5000)
earned = savings.apply_interest()
print(f"Interest earned: ${earned:.2f}")

# Class method constructor
acc2 = BankAccount.from_dict({"owner": "Carol", "balance": 2000})
print(acc2)
```

### 🏭 Real-world Use Cases
- Modeling domain entities (User, Order, Product)
- Building REST API resource models
- Game objects (Player, Enemy, Item)
- Design patterns (Factory, Singleton, Observer)

### ⚠️ Common Mistakes
```python
# Forgetting self
class Dog:
    def bark():         # ❌ Missing self
        print("Woof")

# Mutable class attribute shared across instances
class Team:
    members = []        # ❌ Shared by ALL instances!

    def add(self, name):
        self.members.append(name)

# ✅ Fix: use instance attribute
class Team:
    def __init__(self):
        self.members = []   # Each instance gets its own list
```

### ✅ Best Practices
- Use `@property` over direct attribute access for validation
- Implement `__str__` for user-friendly output, `__repr__` for debugging
- Keep `__init__` simple — delegate complex logic to methods
- Favor composition over inheritance for flexibility
- Use `dataclasses` for simple data-holding classes (Python 3.7+)

### 📝 Mini Summary
> OOP in Python is clean and powerful. Master `self`, inheritance, and dunder methods to write professional, reusable code.

---

## Interview Questions {#interview-questions}

### 🟢 Basic Level

**Q1: What is the difference between a list and a tuple in Python?**

**Answer:**
- A **list** is mutable (can be changed after creation), defined with `[]`.
- A **tuple** is immutable (cannot be changed), defined with `()`.
- Tuples are slightly faster and are used for fixed data (e.g., coordinates, DB rows). Lists are used for collections that change.
- Tuples can be used as dictionary keys; lists cannot.

---

**Q2: What does `is` do vs `==` in Python?**

**Answer:**
- `==` checks **value equality** — whether two objects have the same value.
- `is` checks **identity** — whether two variables point to the **same object in memory**.
```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b   # True  (same value)
a is b   # False (different objects)

x = None
x is None  # True ✅ (correct way to check for None)
```

---

**Q3: What is the difference between `deepcopy` and `shallow copy`?**

**Answer:**
- **Shallow copy** (`copy.copy()` or `list[:]`) — creates a new container but references to nested objects are shared.
- **Deep copy** (`copy.deepcopy()`) — recursively copies all nested objects; fully independent.
```python
import copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original[0][0] = 99
print(shallow[0][0])  # 99 — affected! (shared reference)
print(deep[0][0])     # 1  — unaffected (independent)
```

---

**Q4: What is PEP 8?**

**Answer:**
PEP 8 is Python's official **style guide** for writing readable, consistent Python code. Key conventions include:
- 4 spaces for indentation (not tabs)
- Maximum 79 characters per line
- `snake_case` for variables/functions, `PascalCase` for classes
- Two blank lines between top-level functions/classes
- Imports organized: stdlib → third-party → local

---

**Q5: What is the difference between `append()` and `extend()` on a list?**

**Answer:**
- `append(x)` adds `x` as a **single element** to the end (even if x is a list).
- `extend(iterable)` adds each item from the iterable **individually**.
```python
a = [1, 2, 3]
a.append([4, 5])   # [1, 2, 3, [4, 5]] — nested list
a = [1, 2, 3]
a.extend([4, 5])   # [1, 2, 3, 4, 5]  — elements added
```

---

### 🟡 Intermediate Level

**Q6: Explain the mutable default argument trap. How do you fix it?**

**Answer:**
Default argument values are evaluated **once** when the function is defined, not each time it's called. If the default is a mutable object (list, dict), it's shared across all calls.
```python
# Bug
def add(item, lst=[]):
    lst.append(item)
    return lst

print(add(1))  # [1]
print(add(2))  # [1, 2] ← unexpected! lst persists

# Fix
def add(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

**Q7: What are `*args` and `**kwargs`? Give a real-world use case.**

**Answer:**
- `*args` collects extra **positional** arguments into a tuple.
- `**kwargs` collects extra **keyword** arguments into a dict.

Real-world use case — a flexible logging function or decorator wrapper:
```python
def log_event(event_type, *args, **kwargs):
    print(f"[{event_type}] args={args}, meta={kwargs}")

log_event("PURCHASE", "item_001", 2, user="alice", discount=True)
# [PURCHASE] args=('item_001', 2), meta={'user': 'alice', 'discount': True}
```

---

**Q8: What is a list comprehension vs a generator expression? When would you use each?**

**Answer:**
- **List comprehension** `[x for x in ...]` — evaluates eagerly, stores all results in memory.
- **Generator expression** `(x for x in ...)` — evaluates lazily, yields one item at a time.

Use generators when dealing with large data sets to save memory:
```python
# List comprehension — all in memory
squares_list = [x**2 for x in range(1_000_000)]

# Generator — lazy evaluation
squares_gen = (x**2 for x in range(1_000_000))

# Generator in action
total = sum(x**2 for x in range(1_000_000))  # Memory-efficient
```

---

**Q9: Explain Python's `with` statement and context managers.**

**Answer:**
The `with` statement provides a clean way to manage resources that need setup and teardown (files, DB connections, locks). It calls `__enter__` on entry and `__exit__` on exit — even if an exception occurs.
```python
# File handling
with open("file.txt", "r") as f:
    data = f.read()
# File is closed automatically here

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.3f}s")

with timer():
    sum(range(1_000_000))
```

---

**Q10: What is the difference between `@classmethod` and `@staticmethod`?**

**Answer:**
| | `@classmethod` | `@staticmethod` |
|---|---|---|
| First arg | `cls` (class reference) | None |
| Accesses class? | ✅ Yes | ❌ No |
| Use case | Alternative constructors, factory methods | Utility/helper functions related to the class |

```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_string(cls, s):       # "2024-01-15"
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_valid(y, m, d):
        return 1 <= m <= 12 and 1 <= d <= 31
```

---

### 🔴 Advanced Level

**Q11: How does Python's memory management and garbage collection work?**

**Answer:**
Python uses two mechanisms:
1. **Reference counting** — Every object tracks how many references point to it. When the count reaches 0, memory is freed immediately.
2. **Cyclic garbage collector** — Handles circular references (e.g., A → B → A) which reference counting can't resolve. The `gc` module controls this.

```python
import sys
x = [1, 2, 3]
print(sys.getrefcount(x))  # 2 (x + arg passed to getrefcount)
y = x
print(sys.getrefcount(x))  # 3

del y
print(sys.getrefcount(x))  # 2 again
```
Memory is managed by **CPython's memory allocator**, with an object pool for small integers (-5 to 256) and interned strings, which is why `a = 256; b = 256; a is b` is `True` but not for larger integers.

---

**Q12: Explain Python's GIL (Global Interpreter Lock). What are its implications for concurrency?**

**Answer:**
The **GIL** is a mutex in CPython that ensures only one thread executes Python bytecode at a time, even on multi-core CPUs.

**Implications:**
- **CPU-bound tasks** (computation): Threads don't run truly in parallel → use `multiprocessing` instead.
- **I/O-bound tasks** (network, disk): GIL is released during I/O → `threading` is effective here.

```python
# CPU-bound: use multiprocessing
from multiprocessing import Pool

def compute(n):
    return sum(range(n))

with Pool(4) as p:
    results = p.map(compute, [10**6]*4)

# I/O-bound: threading is fine
import threading
import requests

def fetch(url):
    return requests.get(url).status_code

threads = [threading.Thread(target=fetch, args=(url,)) for url in urls]
```
**Python 3.13** introduces an experimental "no-GIL" build (PEP 703).

---

**Q13: What are decorators? Write one from scratch.**

**Answer:**
A decorator is a function that **wraps another function** to extend its behavior without modifying it — a higher-order function pattern. Used extensively for logging, authentication, caching, timing, etc.

```python
import functools
import time

def timer(func):
    """Decorator that prints execution time."""
    @functools.wraps(func)   # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__!r} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(10_000_000)
# 'slow_sum' took 0.3821s

# Decorator with arguments
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    print(f"Retry {attempt + 1}/{times}: {e}")
        return wrapper
    return decorator

@retry(times=3)
def unstable_api_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Timeout")
    return "success"
```

---

**Q14: What is the difference between `__str__` and `__repr__`?**

**Answer:**
Both are dunder (magic) methods for string representation:
- `__str__` — human-readable, used by `print()` and `str()`. For end users.
- `__repr__` — unambiguous, used in REPL and `repr()`. Should ideally be valid Python to recreate the object. For developers/debugging.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"          # User-friendly

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})" # Dev-friendly

p = Point(3, 4)
print(str(p))   # (3, 4)
print(repr(p))  # Point(x=3, y=4)
print([p])      # [Point(x=3, y=4)]  — list uses __repr__
```

---

**Q15: Explain Python's MRO (Method Resolution Order) and how `super()` works in multiple inheritance.**

**Answer:**
MRO determines the order Python searches for methods in class hierarchies. Python uses the **C3 linearization algorithm**. Use `ClassName.__mro__` or `mro()` to inspect it.

```python
class A:
    def greet(self): return "A"

class B(A):
    def greet(self): return "B → " + super().greet()

class C(A):
    def greet(self): return "C → " + super().greet()

class D(B, C):
    def greet(self): return "D → " + super().greet()

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

d = D()
print(d.greet())
# D → B → C → A
```
`super()` doesn't mean "call parent" — it means "call the **next class in MRO**", enabling cooperative multiple inheritance.

---

## Coding Challenges {#coding-challenges}

### Challenge 1: FizzBuzz Pro

**📋 Problem:**
Write a function `fizzbuzz(n)` that returns a list of strings for numbers 1 through n:
- `"Fizz"` if divisible by 3
- `"Buzz"` if divisible by 5
- `"FizzBuzz"` if divisible by both
- The number as a string otherwise

Make it extensible: accept a custom rules dict `{divisor: label}`.

**📥 Input/Output:**
```
fizzbuzz(15)
→ ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz',
   '11', 'Fizz', '13', '14', 'FizzBuzz']

fizzbuzz(10, {2: "Even", 5: "Hi"})
→ ['1', 'Even', '3', 'Even', 'Hi', 'Even', '7', 'Even', '9', 'EvenHi']
```

**✅ Solution:**
```python
def fizzbuzz(n: int, rules: dict = None) -> list[str]:
    """
    Generate FizzBuzz sequence with extensible rules.

    Args:
        n: Upper bound (inclusive)
        rules: Dict of {divisor: label}, defaults to classic FizzBuzz

    Returns:
        List of strings
    """
    if rules is None:
        rules = {3: "Fizz", 5: "Buzz"}

    # Sort rules by divisor for consistent output
    sorted_rules = sorted(rules.items())
    result = []

    for i in range(1, n + 1):
        label = "".join(word for div, word in sorted_rules if i % div == 0)
        result.append(label if label else str(i))

    return result


# Tests
assert fizzbuzz(15)[-1] == "FizzBuzz"
assert fizzbuzz(15)[2] == "Fizz"
assert fizzbuzz(15)[4] == "Buzz"

print(fizzbuzz(15))
print(fizzbuzz(10, {2: "Even", 5: "Hi"}))
```

**💡 Explanation:**
- Uses a dictionary of rules for extensibility (Open/Closed principle)
- `"".join(...)` efficiently builds the combined label
- Falls back to the number string if no rule matches
- Sorting rules ensures deterministic output

---

### Challenge 2: Word Frequency Analyzer

**📋 Problem:**
Write a function `word_frequency(text, top_n=5)` that:
1. Accepts a paragraph of text
2. Normalizes it (lowercased, punctuation removed)
3. Returns the top N most frequent words as a list of `(word, count)` tuples
4. Excludes common stop words: `{"the", "a", "an", "is", "in", "it", "of", "and", "to", "was"}`

**📥 Input/Output:**
```
text = "The quick brown fox jumps over the lazy dog. The dog barked at the fox."
word_frequency(text, top_n=3)
→ [('fox', 2), ('dog', 2), ('quick', 1)]
```

**✅ Solution:**
```python
import re
from collections import Counter

def word_frequency(text: str, top_n: int = 5) -> list[tuple[str, int]]:
    """
    Analyze word frequency in a text, excluding stop words.

    Args:
        text:   Input paragraph
        top_n:  Number of top words to return

    Returns:
        List of (word, count) tuples, most common first
    """
    STOP_WORDS = {"the", "a", "an", "is", "in", "it",
                  "of", "and", "to", "was", "at", "over"}

    # Normalize: lowercase + remove punctuation
    cleaned = re.sub(r"[^\w\s]", "", text.lower())

    # Tokenize
    words = cleaned.split()

    # Filter stop words
    filtered = [w for w in words if w not in STOP_WORDS]

    # Count and return top N
    return Counter(filtered).most_common(top_n)


# Test
text = "The quick brown fox jumps over the lazy dog. The dog barked at the fox."
result = word_frequency(text, top_n=3)
print(result)
# [('fox', 2), ('dog', 2), ('quick', 1)]  ← order may vary for ties

# Edge cases
print(word_frequency("", top_n=3))          # []
print(word_frequency("hello hello hello"))  # [('hello', 3)]

# Validate
assert word_frequency(text, top_n=1)[0][0] in ("fox", "dog")
assert word_frequency(text, top_n=1)[0][1] == 2
print("All tests passed ✅")
```

**💡 Explanation:**
- `re.sub(r"[^\w\s]", "", ...)` removes punctuation cleanly using regex
- `Counter.most_common(n)` is O(n log n) — efficient for large texts
- Stop word filtering with a `set` is O(1) per lookup
- Handles edge cases: empty string, repeated words, all stop words

---

## Final Summary {#final-summary}

```
╔══════════════════════════════════════════════════════════════╗
║              PYTHON BASICS — KNOWLEDGE MAP                   ║
╠══════════════════════════════════════════════════════════════╣
║  Module 1   → Setup, Philosophy, PEP 8                       ║
║  Module 2   → Types, Variables, Operators                     ║
║  Module 3   → if/elif, for, while, comprehensions            ║
║  Module 4   → Functions, *args/**kwargs, lambdas             ║
║  Module 5   → List, Tuple, Set, Dict                         ║
║  Module 6   → String methods, f-strings, slicing            ║
║  Module 7   → File I/O, json, pathlib                        ║
║  Module 8   → try/except/finally, custom exceptions          ║
║  Module 9   → Modules, stdlib, imports, venv                 ║
║  Module 10  → Classes, OOP, inheritance, dunder methods      ║
╠══════════════════════════════════════════════════════════════╣
║  TOP 5 INTERVIEW TRAPS TO REMEMBER:                          ║
║  1. Mutable default arguments in functions                   ║
║  2. `is` vs `==` (identity vs equality)                      ║
║  3. GIL limits CPU threading → use multiprocessing           ║
║  4. Shared mutable class attributes                          ║
║  5. Generator vs list comprehension (memory efficiency)      ║
╠══════════════════════════════════════════════════════════════╣
║  NEXT STEPS:                                                  ║
║  → Iterators & Generators (yield)                            ║
║  → Decorators & Closures (advanced)                          ║
║  → Async/Await (asyncio)                                     ║
║  → Testing with pytest                                       ║
║  → Type hints & mypy                                         ║
║  → Python packaging (pyproject.toml)                         ║
╚══════════════════════════════════════════════════════════════╝
```

> 💡 **Pro Tip:** The best way to master Python is to build something real. Start with a CLI tool, then a REST API, then explore data science. Every module in this guide shows up daily in production Python codebases.

---
*Guide created for learning and interview preparation. Python version: 3.10+*
