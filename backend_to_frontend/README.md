# Backend-to-Frontend Learning Roadmap
## Complete Guide for Backend Teams Transitioning to Full-Stack Development

**Version:** 1.0  
**Last Updated:** March 2026  
**Target Audience:** Backend developers (Python, Node.js, Java, etc.) learning frontend technologies    
**Outcome:** Build production-ready React applications and become full-stack engineers

---

## Table of Contents

1. [Introduction](#introduction)
2. [Learning Strategy for Backend Developers](#learning-strategy)
3. [6-Month Roadmap Overview](#roadmap-overview)
4. [Phase 1: Web Fundamentals ](#phase-1)
5. [Phase 2: React Fundamentals ](#phase-2)
6. [Phase 3: State Management & API Integration ](#phase-3)
7. [Phase 4: Modern React & Tooling ](#phase-4)
8. [Phase 5: Production-Ready Skills ](#phase-5)
9. [Phase 6: Team Project ](#phase-6)

---

<a name="introduction"></a>
## 1. Introduction

### 🎯 Overview: Backend Developer → Full-Stack Engineer

As backend developers, you already understand **HTTP, APIs, data structures, and system architecture**. This roadmap leverages your existing knowledge to build frontend skills efficiently, focusing on modern tools and practical projects.

### Why This Roadmap Works for Backend Developers

This isn't a generic "learn React" tutorial. It's specifically designed for experienced backend developers who:
- ✅ Already know programming fundamentals
- ✅ Understand REST APIs and data flow
- ✅ Have experience with databases and state management
- ✅ Are familiar with testing and debugging
- ✅ Want practical, project-based learning

### What You'll Build

By the end of this roadmap, you will have:
- **5+ practical projects** connected to real backend APIs
- **Production-ready React applications** deployed to the web
- **Full-stack skills** to build complete applications independently
- **Portfolio** showcasing your frontend capabilities
- **Confidence** to join frontend discussions and code reviews

---

<a name="learning-strategy"></a>
## 2. Learning Strategy for Backend Developers

### Your Existing Advantages

As a backend developer, you bring powerful skills to frontend development:

| Backend Skill | Frontend Equivalent | Your Advantage |
|---------------|---------------------|----------------|
| **REST API Design** | Component API design (props) | You know what good interfaces look like |
| **Database Queries** | State management & data fetching | You understand data relationships |
| **Async/Await** | Async operations in browser | Same concepts, different context |
| **Testing** | Frontend testing | You already have a testing mindset |
| **Debugging** | Browser DevTools | Transfer your debugging skills |
| **Architecture** | Component architecture | You think in systems |
| **Version Control** | Same Git workflows | No learning curve here |

### Key Mindset Shifts

Understanding these differences will accelerate your learning:

#### 1. **Stateful UI vs Stateless Servers**
```
Backend:        Request → Process → Response (stateless)
Frontend:       User Action → Update State → Re-render UI (stateful)
```

**Backend mindset:**
```python
@app.get("/users")
def get_users():
    users = db.query(User).all()
    return users  # Send and forget
```

**Frontend mindset:**
```javascript
function UserList() {
  const [users, setUsers] = useState([])  // Component holds state
  
  useEffect(() => {
    fetchUsers().then(setUsers)  // State persists across renders
  }, [])
  
  return <ul>{users.map(u => <li>{u.name}</li>)}</ul>
}
```

#### 2. **Event-Driven Architecture**
```
Backend:        Event Queue → Worker → Process
Frontend:       User Click → Event Handler → Update UI
```

Both use event-driven patterns, but frontend events are user interactions.

#### 3. **Synchronous Rendering vs Async Operations**
```
Backend:        Everything can be async
Frontend:       Render is sync, but data fetching is async
```

#### 4. **Resource Constraints**
```
Backend:        More servers = more capacity
Frontend:       User's device limitations (bundle size, memory, CPU)
```

#### 5. **Immediate Feedback**
```
Backend:        Logs show what happened
Frontend:       Users see results immediately
```

### Learning Philosophy

**1. Build, Don't Just Read**
- Every concept must be practiced in code
- Small working projects > large theoretical knowledge
- Break things and fix them

**2. Connect to What You Know**
- React components = API endpoints (input → output)
- Props = function parameters
- State = database session
- useEffect = lifecycle hooks

**3. Focus on Modern Tools**
- Skip legacy approaches (class components, older patterns)
- Learn the current industry standard (React Hooks, Vite, Tailwind)
- Avoid analysis paralysis

**4. Team Learning**
- Learn together, not in isolation
- Pair programming sessions
- Code reviews help everyone
- Share discoveries and challenges

---

<a name="roadmap-overview"></a>

### Roadmap at a Glance

| Phase | Focus | Key Technologies | Outcome |
|-------|-------|------------------|---------|
| **Phase 1** | HTML/CSS/JS Fundamentals | HTML5, CSS3, ES6+ JavaScript | Build static interactive pages |
| **Phase 2** | React Fundamentals | React 18, Hooks, JSX | Build single-page applications |
| **Phase 3** | State & APIs | React Query, Context API, Fetch | Connect to your backend |
| **Phase 4** | Modern Tools | React Router, Tailwind CSS | Multi-page styled apps |
| **Phase 5** | Production Skills | Testing, Performance, Vite | Production-ready code |
| **Phase 6** | Team Project | Full Stack | Complete application |

### Skill Progression

---

<a name="phase-1"></a>
## 4. Phase 1: Web Fundamentals

### Overview
Learn the building blocks of web development: HTML for structure, CSS for styling, and JavaScript for interactivity.

---

### HTML & CSS Essentials

#### HTML (Structure Layer)

**What Backend Devs Need to Know:**

Think of HTML as the "database schema" of the web page. It defines the structure and relationships of content.

**Core Concepts:**

```html
<!-- Semantic HTML5 Elements (like proper data modeling) -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My App</title>
</head>
<body>
  <!-- Header section -->
  <header>
    <nav>
      <ul>
        <li><a href="#home">Home</a></li>
        <li><a href="#about">About</a></li>
      </ul>
    </nav>
  </header>
  
  <!-- Main content -->
  <main>
    <section id="home">
      <h1>Welcome</h1>
      <article>
        <h2>Article Title</h2>
        <p>Article content goes here.</p>
      </article>
    </section>
  </main>
  
  <!-- Footer -->
  <footer>
    <p>&copy; 2026 My Company</p>
  </footer>
</body>
</html>
```

**Forms (Similar to API Request Bodies):**

```html
<!-- Form = API request structure -->
<form id="userForm" action="/api/users" method="POST">
  <!-- Input fields = request parameters -->
  <label for="name">Name:</label>
  <input 
    type="text" 
    id="name" 
    name="name" 
    required 
    minlength="3"
    maxlength="50"
  >
  
  <label for="email">Email:</label>
  <input 
    type="email" 
    id="email" 
    name="email" 
    required
  >
  
  <label for="age">Age:</label>
  <input 
    type="number" 
    id="age" 
    name="age" 
    min="18" 
    max="120"
  >
  
  <label for="role">Role:</label>
  <select id="role" name="role">
    <option value="user">User</option>
    <option value="admin">Admin</option>
  </select>
  
  <button type="submit">Submit</button>
</form>
```

**Accessibility Basics:**

```html
<!-- Screen readers and SEO (like API documentation) -->
<img src="profile.jpg" alt="User profile picture">

<button aria-label="Close dialog">×</button>

<nav aria-label="Main navigation">
  <!-- Navigation items -->
</nav>
```

#### CSS (Styling Layer)

**What Backend Devs Need to Know:**

CSS is like configuration files. It styles HTML elements using selectors (similar to database queries).

**The Box Model (Foundation):**

```css
/* Every element is a box */
.element {
  /* Content */
  width: 200px;
  height: 100px;
  
  /* Padding (space inside border) */
  padding: 20px;
  
  /* Border */
  border: 2px solid #333;
  
  /* Margin (space outside border) */
  margin: 10px;
}
```

**Flexbox (Row/Column Layouts):**

```css
/* Container */
.container {
  display: flex;
  flex-direction: row;        /* or 'column' */
  justify-content: space-between; /* horizontal alignment */
  align-items: center;        /* vertical alignment */
  gap: 16px;                  /* space between items */
}

/* Items */
.item {
  flex: 1;  /* grow to fill space */
}
```

**CSS Grid (Complex Layouts):**

```css
/* Grid container */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 equal columns */
  gap: 20px;
}

/* Responsive grid */
.responsive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}
```

**Responsive Design (Media Queries):**

```css
/* Mobile-first approach */
.container {
  padding: 10px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 20px;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: 40px;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

**CSS Variables (Like Environment Variables):**

```css
:root {
  /* Define variables */
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --spacing-unit: 8px;
  --border-radius: 4px;
}

.button {
  /* Use variables */
  background-color: var(--primary-color);
  padding: calc(var(--spacing-unit) * 2);
  border-radius: var(--border-radius);
}
```

#### Learning Resources

**Free Resources:**
- **MDN Web Docs** - HTML & CSS documentation (https://developer.mozilla.org)
- **CSS-Tricks** - Complete Guide to Flexbox and Grid
- **freeCodeCamp** - Responsive Web Design Certification

**Practice:**
- Build 3-5 simple static pages
- Recreate your favorite website's layout
- Focus on structure, not perfection

#### Practice Project: Developer Portfolio Page

**Objective:** Build a personal portfolio page

**Requirements:**
- ✅ Responsive layout (works on mobile, tablet, desktop)
- ✅ Navigation bar with sections (About, Projects, Contact)
- ✅ Grid layout for projects showcase
- ✅ Contact form with validation
- ✅ Semantic HTML throughout
- ✅ No JavaScript yet (pure HTML/CSS)

**Skills Practiced:**
- Semantic HTML structure
- Flexbox and Grid layouts
- Responsive design
- Form elements
- CSS styling

**Deliverable:** Static portfolio page hosted on GitHub Pages

**Example Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>John Doe - Backend Developer</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav>
      <a href="#about">About</a>
      <a href="#projects">Projects</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>
  
  <main>
    <section id="about">
      <h1>Hi, I'm John</h1>
      <p>Backend developer learning frontend...</p>
    </section>
    
    <section id="projects">
      <h2>Projects</h2>
      <div class="project-grid">
        <div class="project-card">
          <h3>REST API</h3>
          <p>FastAPI backend...</p>
        </div>
        <!-- More projects -->
      </div>
    </section>
    
    <section id="contact">
      <h2>Contact Me</h2>
      <form>
        <!-- Contact form -->
      </form>
    </section>
  </main>
  
  <footer>
    <p>&copy; 2026 John Doe</p>
  </footer>
</body>
</html>
```

---

#### Modern JavaScript (ES6+)

**What Backend Devs Need to Know:**

JavaScript is similar to Python/Node.js, but it runs in the browser. Focus on modern syntax (ES6+).

#### 1. Variables and Data Types

```javascript
// const (like final/const in other languages)
const API_URL = 'https://api.example.com'
const user = { name: 'John', age: 30 }

// let (block-scoped, like local variables)
let count = 0
let isActive = true

// Don't use var (legacy)

// Data types
const string = 'Hello'
const number = 42
const boolean = true
const array = [1, 2, 3]
const object = { key: 'value' }
const nullValue = null
const undefinedValue = undefined
```

#### 2. Functions

```javascript
// Function declaration
function greet(name) {
  return `Hello, ${name}`
}

// Arrow function (preferred in React)
const greet = (name) => {
  return `Hello, ${name}`
}

// Concise arrow function
const greet = name => `Hello, ${name}`

// Multiple parameters
const add = (a, b) => a + b

// Default parameters
const greet = (name = 'Guest') => `Hello, ${name}`
```

#### 3. Array Methods (Like List Comprehensions)

```javascript
const users = [
  { id: 1, name: 'Alice', active: true },
  { id: 2, name: 'Bob', active: false },
  { id: 3, name: 'Charlie', active: true }
]

// map (transform each item)
const names = users.map(user => user.name)
// ['Alice', 'Bob', 'Charlie']

// filter (select items)
const activeUsers = users.filter(user => user.active)
// [{ id: 1, name: 'Alice', active: true }, ...]

// reduce (aggregate)
const ids = users.reduce((acc, user) => {
  acc.push(user.id)
  return acc
}, [])
// [1, 2, 3]

// find (first match)
const alice = users.find(user => user.name === 'Alice')

// some (at least one matches)
const hasActive = users.some(user => user.active)  // true

// every (all match)
const allActive = users.every(user => user.active)  // false
```

#### 4. Destructuring (Like Unpacking)

```javascript
// Object destructuring
const user = { name: 'Alice', age: 30, email: 'alice@example.com' }

const { name, email } = user
// name = 'Alice', email = 'alice@example.com'

// With renaming
const { name: userName, age: userAge } = user

// With defaults
const { role = 'user' } = user

// Array destructuring
const colors = ['red', 'green', 'blue']
const [first, second] = colors
// first = 'red', second = 'green'

// Skip elements
const [, , third] = colors  // third = 'blue'

// Rest operator
const [primary, ...others] = colors
// primary = 'red', others = ['green', 'blue']
```

#### 5. Spread Operator (...)

```javascript
// Copy array
const original = [1, 2, 3]
const copy = [...original]

// Merge arrays
const arr1 = [1, 2]
const arr2 = [3, 4]
const merged = [...arr1, ...arr2]  // [1, 2, 3, 4]

// Copy object
const user = { name: 'Alice', age: 30 }
const userCopy = { ...user }

// Merge objects (like dict.update() in Python)
const defaults = { theme: 'light', lang: 'en' }
const settings = { lang: 'es' }
const merged = { ...defaults, ...settings }
// { theme: 'light', lang: 'es' }

// Add properties
const updatedUser = { ...user, email: 'alice@example.com' }
```

#### 6. Template Literals

```javascript
// String interpolation
const name = 'Alice'
const age = 30
const message = `Hello, ${name}! You are ${age} years old.`

// Multi-line strings
const html = `
  <div>
    <h1>${name}</h1>
    <p>Age: ${age}</p>
  </div>
`

// Expressions
const total = `Total: ${price * quantity}`
```

#### 7. Async/Await (Same as Python)

```javascript
// Promise-based async operation
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch')
    }
    
    const user = await response.json()
    return user
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

// Multiple async operations
async function loadData() {
  // Sequential
  const user = await fetchUser(1)
  const posts = await fetchPosts(user.id)
  
  // Parallel (faster)
  const [user, posts] = await Promise.all([
    fetchUser(1),
    fetchPosts(1)
  ])
}
```

#### 8. Modules (Import/Export)

```javascript
// Export (utils.js)
export function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

export const API_URL = 'https://api.example.com'

export default function helper() {
  // Default export
}

// Import (app.js)
import helper, { formatDate, API_URL } from './utils.js'

// Import all
import * as utils from './utils.js'
utils.formatDate(new Date())
```

#### DOM Manipulation

**Think of the DOM as a Tree Structure (Like JSON)**

```javascript
// Select elements (like database queries)
const element = document.querySelector('#app')
const elements = document.querySelectorAll('.card')

// Modify content
element.textContent = 'Hello, World!'
element.innerHTML = '<h1>Hello</h1>'

// Modify attributes
element.setAttribute('class', 'active')
element.classList.add('highlight')
element.classList.remove('hidden')
element.classList.toggle('active')

// Modify styles
element.style.color = 'blue'
element.style.backgroundColor = 'yellow'

// Create elements
const newDiv = document.createElement('div')
newDiv.textContent = 'New element'
element.appendChild(newDiv)

// Remove elements
element.remove()
```

#### Event Handling

```javascript
// Click event
const button = document.querySelector('#myButton')

button.addEventListener('click', (event) => {
  console.log('Button clicked!')
  console.log(event.target)  // The clicked element
})

// Form submission
const form = document.querySelector('#myForm')

form.addEventListener('submit', (event) => {
  event.preventDefault()  // Stop default form submission
  
  const formData = new FormData(form)
  const data = {
    name: formData.get('name'),
    email: formData.get('email')
  }
  
  console.log(data)
})

// Input change
const input = document.querySelector('#search')

input.addEventListener('input', (event) => {
  console.log('Current value:', event.target.value)
})

// Multiple events
element.addEventListener('mouseenter', handleMouseEnter)
element.addEventListener('mouseleave', handleMouseLeave)
```

#### Browser APIs

**LocalStorage (Like Redis Key-Value Store)**

```javascript
// Store data (persists after page reload)
localStorage.setItem('user', JSON.stringify({ name: 'Alice' }))
localStorage.setItem('token', 'abc123')

// Retrieve data
const user = JSON.parse(localStorage.getItem('user'))
const token = localStorage.getItem('token')

// Remove data
localStorage.removeItem('token')

// Clear all
localStorage.clear()

// Check if exists
if (localStorage.getItem('user')) {
  // User data exists
}
```

**Fetch API (Like requests in Python)**

```javascript
// GET request
async function getUsers() {
  const response = await fetch('https://api.example.com/users')
  const users = await response.json()
  return users
}

// POST request
async function createUser(userData) {
  const response = await fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(userData)
  })
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  const newUser = await response.json()
  return newUser
}

// PUT request
async function updateUser(id, updates) {
  const response = await fetch(`https://api.example.com/users/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  })
  
  return response.json()
}

// DELETE request
async function deleteUser(id) {
  await fetch(`https://api.example.com/users/${id}`, {
    method: 'DELETE'
  })
}

// Error handling
async function fetchWithErrorHandling() {
  try {
    const response = await fetch('/api/data')
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Fetch error:', error)
    // Show user-friendly error message
  }
}
```

#### Learning Resources

**Free Resources:**
- **JavaScript.info** - Modern JavaScript Tutorial
- **MDN JavaScript Guide** - Comprehensive reference
- **Eloquent JavaScript** - Free online book

**Practice:**
- Build interactive components
- Practice array methods daily
- Make API calls to public APIs

#### Practice Project: Interactive To-Do App

**Objective:** Build a to-do list with vanilla JavaScript

**Requirements:**
- ✅ Add new tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Delete tasks
- ✅ Edit existing tasks
- ✅ Filter: All, Active, Completed
- ✅ Persist data in localStorage
- ✅ Show task count
- ✅ No frameworks (pure JavaScript)

**Skills Practiced:**
- DOM manipulation
- Event handling
- Array methods (map, filter)
- LocalStorage
- ES6+ syntax

**Example Code Structure:**

```javascript
// app.js
let todos = JSON.parse(localStorage.getItem('todos')) || []

function saveTodos() {
  localStorage.setItem('todos', JSON.stringify(todos))
}

function renderTodos(filter = 'all') {
  const list = document.querySelector('#todoList')
  list.innerHTML = ''
  
  const filtered = todos.filter(todo => {
    if (filter === 'active') return !todo.completed
    if (filter === 'completed') return todo.completed
    return true
  })
  
  filtered.forEach(todo => {
    const li = document.createElement('li')
    li.innerHTML = `
      <input type="checkbox" ${todo.completed ? 'checked' : ''}>
      <span class="${todo.completed ? 'completed' : ''}">${todo.text}</span>
      <button class="delete">Delete</button>
    `
    
    // Event listeners
    li.querySelector('input').addEventListener('change', () => {
      todo.completed = !todo.completed
      saveTodos()
      renderTodos(filter)
    })
    
    li.querySelector('.delete').addEventListener('click', () => {
      todos = todos.filter(t => t.id !== todo.id)
      saveTodos()
      renderTodos(filter)
    })
    
    list.appendChild(li)
  })
}

// Add todo
document.querySelector('#addForm').addEventListener('submit', (e) => {
  e.preventDefault()
  
  const input = document.querySelector('#todoInput')
  const text = input.value.trim()
  
  if (text) {
    todos.push({
      id: Date.now(),
      text,
      completed: false
    })
    
    saveTodos()
    renderTodos()
    input.value = ''
  }
})

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.dataset.filter
    renderTodos(filter)
  })
})

// Initial render
renderTodos()
```

**Deliverable:** Working to-do app with all features

---

<a name="phase-2"></a>
## 5. Phase 2: React Fundamentals

### Overview
Learn React, the most popular frontend framework. Build component-based user interfaces.

---


#### Why React for Backend Developers?

Think of React as:
- **Component-based** - Like microservices for UI
- **Declarative** - Describe what you want (like SQL)
- **Virtual DOM** - Optimized rendering (like query optimization)
- **Unidirectional data flow** - Predictable state management

#### Setting Up React

**Create a New React App (Recommended: Vite)**

```bash
# Using Vite (faster, modern)
npm create vite@latest my-react-app -- --template react
cd my-react-app
npm install
npm run dev

# Using Create React App (older, still popular)
npx create-react-app my-react-app
cd my-react-app
npm start
```

**Project Structure:**
```
my-react-app/
├── node_modules/
├── public/
│   └── index.html
├── src/
│   ├── App.jsx          # Main component
│   ├── main.jsx         # Entry point
│   ├── App.css          # Styles
│   └── components/      # Your components
├── package.json
└── vite.config.js
```

#### Core Concept 1: Components

**Components are Functions that Return UI**

```javascript
// Simple component
function Welcome() {
  return <h1>Hello, World!</h1>
}

// Component with JSX
function UserCard() {
  return (
    <div className="card">
      <h2>John Doe</h2>
      <p>Backend Developer</p>
      <button>View Profile</button>
    </div>
  )
}

// Arrow function syntax (preferred)
const UserCard = () => {
  return (
    <div className="card">
      <h2>John Doe</h2>
      <p>Backend Developer</p>
    </div>
  )
}

// Concise return (no braces needed for single element)
const Welcome = () => <h1>Hello, World!</h1>
```

**JSX = JavaScript + XML**

```javascript
// JSX looks like HTML but is JavaScript
const element = <h1>Hello</h1>

// JavaScript expressions in curly braces
const name = 'Alice'
const element = <h1>Hello, {name}!</h1>

// Expressions and calculations
const price = 100
const total = <p>Total: ${price * 1.2}</p>

// Calling functions
const formatDate = (date) => date.toLocaleDateString()
const element = <p>Today: {formatDate(new Date())}</p>

// Conditional rendering
const isLoggedIn = true
const element = (
  <div>
    {isLoggedIn ? <p>Welcome back!</p> : <p>Please log in</p>}
  </div>
)

// Logical AND (only render if true)
const hasError = true
const element = (
  <div>
    {hasError && <p className="error">Error occurred!</p>}
  </div>
)
```

**JSX Rules:**
- Class → `className` (because 'class' is a JS keyword)
- for → `htmlFor`
- Style must be object: `style={{ color: 'red', fontSize: '16px' }}`
- All tags must close: `<img />`, `<input />`
- Return single parent element (or use Fragment `<>...</>`)

#### Core Concept 2: Props (Component Parameters)

**Props = Function Arguments**

```javascript
// Component with props
function UserCard(props) {
  return (
    <div className="card">
      <h2>{props.name}</h2>
      <p>{props.role}</p>
      <p>Age: {props.age}</p>
    </div>
  )
}

// Destructuring props (preferred)
function UserCard({ name, role, age }) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>{role}</p>
      <p>Age: {age}</p>
    </div>
  )
}

// Using the component
function App() {
  return (
    <div>
      <UserCard 
        name="Alice" 
        role="Backend Developer" 
        age={30} 
      />
      <UserCard 
        name="Bob" 
        role="Frontend Developer" 
        age={28} 
      />
    </div>
  )
}

// Default props
function Button({ text = 'Click me', color = 'blue' }) {
  return (
    <button style={{ backgroundColor: color }}>
      {text}
    </button>
  )
}

// Props can be any data type
function Dashboard({ 
  user,           // object
  count,          // number
  isActive,       // boolean
  items,          // array
  onUpdate        // function
}) {
  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <p>Count: {count}</p>
      {isActive && <span>Active</span>}
      <ul>
        {items.map(item => <li key={item.id}>{item.name}</li>)}
      </ul>
      <button onClick={onUpdate}>Update</button>
    </div>
  )
}
```

**Children Prop:**

```javascript
// Children = content between component tags
function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  )
}

// Usage
<Card>
  <h2>Title</h2>
  <p>Content goes here</p>
</Card>
```

#### Core Concept 3: State (Component Memory)

**State = Data That Changes Over Time**

```javascript
import { useState } from 'react'

// Simple state
function Counter() {
  // [currentValue, setterFunction] = useState(initialValue)
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
      <button onClick={() => setCount(count - 1)}>
        Decrement
      </button>
      <button onClick={() => setCount(0)}>
        Reset
      </button>
    </div>
  )
}

// Multiple state variables
function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  
  return (
    <form>
      <input 
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input 
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <label>
        <input 
          type="checkbox"
          checked={rememberMe}
          onChange={(e) => setRememberMe(e.target.checked)}
        />
        Remember me
      </label>
    </form>
  )
}

// Object state
function UserProfile() {
  const [user, setUser] = useState({
    name: '',
    email: '',
    age: 0
  })
  
  // Update specific property (create new object)
  const updateName = (newName) => {
    setUser({ ...user, name: newName })
  }
  
  const updateEmail = (newEmail) => {
    setUser({ ...user, email: newEmail })
  }
  
  // Or use a generic handler
  const handleChange = (field, value) => {
    setUser({ ...user, [field]: value })
  }
  
  return (
    <div>
      <input 
        value={user.name}
        onChange={(e) => handleChange('name', e.target.value)}
      />
    </div>
  )
}

// Array state
function TodoList() {
  const [todos, setTodos] = useState([])
  
  const addTodo = (text) => {
    const newTodo = { id: Date.now(), text, completed: false }
    setTodos([...todos, newTodo])  // Add to end
  }
  
  const removeTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }
  
  const toggleTodo = (id) => {
    setTodos(todos.map(todo => 
      todo.id === id 
        ? { ...todo, completed: !todo.completed }
        : todo
    ))
  }
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input 
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo(todo.id)}
          />
          {todo.text}
          <button onClick={() => removeTodo(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  )
}
```

**Important State Rules:**
1. **Never mutate state directly**
   ```javascript
   // ❌ Wrong
   user.name = 'New Name'
   todos.push(newTodo)
   
   // ✅ Correct
   setUser({ ...user, name: 'New Name' })
   setTodos([...todos, newTodo])
   ```

2. **State updates are asynchronous**
   ```javascript
   // ❌ Wrong (may not work as expected)
   setCount(count + 1)
   setCount(count + 1)  // Still uses old count
   
   // ✅ Correct (use functional update)
   setCount(prevCount => prevCount + 1)
   setCount(prevCount => prevCount + 1)
   ```

#### Core Concept 4: Event Handling

```javascript
function EventExamples() {
  const [value, setValue] = useState('')
  
  // Click handler
  const handleClick = () => {
    console.log('Button clicked!')
  }
  
  // Handler with parameter
  const handleClickWithId = (id) => {
    console.log(`Clicked item ${id}`)
  }
  
  // Change handler
  const handleChange = (event) => {
    setValue(event.target.value)
  }
  
  // Form submit
  const handleSubmit = (event) => {
    event.preventDefault()  // Important!
    console.log('Form submitted with:', value)
  }
  
  return (
    <div>
      {/* Simple click */}
      <button onClick={handleClick}>Click me</button>
      
      {/* Inline function */}
      <button onClick={() => console.log('Clicked!')}>
        Inline
      </button>
      
      {/* Pass parameter */}
      <button onClick={() => handleClickWithId(123)}>
        Click with ID
      </button>
      
      {/* Input change */}
      <input 
        value={value}
        onChange={handleChange}
      />
      
      {/* Form submit */}
      <form onSubmit={handleSubmit}>
        <input value={value} onChange={handleChange} />
        <button type="submit">Submit</button>
      </form>
      
      {/* Other events */}
      <div 
        onMouseEnter={() => console.log('Mouse entered')}
        onMouseLeave={() => console.log('Mouse left')}
        onFocus={() => console.log('Focused')}
        onBlur={() => console.log('Blurred')}
      >
        Hover over me
      </div>
    </div>
  )
}
```

#### Core Concept 5: Conditional Rendering

```javascript
function ConditionalExamples({ isLoggedIn, user, error, items }) {
  // 1. Ternary operator
  return (
    <div>
      {isLoggedIn ? (
        <p>Welcome, {user.name}!</p>
      ) : (
        <p>Please log in</p>
      )}
      
      {/* 2. Logical AND (only show if true) */}
      {error && (
        <div className="error">{error}</div>
      )}
      
      {/* 3. Logical OR (fallback) */}
      <p>{user.name || 'Guest'}</p>
      
      {/* 4. If-else in variable */}
      {(() => {
        if (items.length === 0) {
          return <p>No items</p>
        } else if (items.length < 5) {
          return <p>Few items</p>
        } else {
          return <p>Many items</p>
        }
      })()}
      
      {/* 5. Early return in component */}
      {items.length === 0 ? (
        <p>No items to display</p>
      ) : (
        <ul>
          {items.map(item => <li key={item.id}>{item.name}</li>)}
        </ul>
      )}
    </div>
  )
}

// Separate loading/error states
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  // Early returns for different states
  if (loading) {
    return <div>Loading...</div>
  }
  
  if (error) {
    return <div>Error: {error}</div>
  }
  
  if (!user) {
    return <div>User not found</div>
  }
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

#### Core Concept 6: Lists and Keys

```javascript
function UserList({ users }) {
  return (
    <ul>
      {users.map(user => (
        // ✅ IMPORTANT: Always provide unique 'key'
        <li key={user.id}>
          {user.name}
        </li>
      ))}
    </ul>
  )
}

// More complex list with components
function ProductList({ products }) {
  return (
    <div className="grid">
      {products.map(product => (
        <ProductCard 
          key={product.id}  // Key goes on the top-level element
          product={product}
        />
      ))}
    </div>
  )
}

// Filtering and mapping
function FilteredList({ items, filter }) {
  const filteredItems = items.filter(item => 
    item.name.toLowerCase().includes(filter.toLowerCase())
  )
  
  return (
    <ul>
      {filteredItems.length === 0 ? (
        <li>No results found</li>
      ) : (
        filteredItems.map(item => (
          <li key={item.id}>{item.name}</li>
        ))
      )}
    </ul>
  )
}

// Index as key (only if no unique ID and list doesn't change)
function StaticList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item}</li>  // ⚠️ Only for static lists
      ))}
    </ul>
  )
}
```

**Why Keys Matter:**
- React uses keys to identify which items changed
- Without keys, React may re-render unnecessarily
- Use unique, stable IDs (not array index for dynamic lists)

#### Learning Resources

**Official Documentation:**
- **React Docs** (react.dev) - Start here!
- **React Tutorial** - Build tic-tac-toe

**Video Courses:**
- **Scrimba React Course** - Interactive
- **Net Ninja React Tutorial** - YouTube
- **Web Dev Simplified** - Modern React

**Practice:**
- Build small components daily
- Convert your to-do app to React
- Experiment with state and props

#### Practice Project: Blog Reader

**Objective:** Build a blog post reader with React

**Requirements:**
- ✅ Display list of blog posts (use mock data)
- ✅ Click to read full post
- ✅ Like/unlike posts
- ✅ Add comments to posts
- ✅ Filter posts (all, liked)
- ✅ Search posts by title

**Component Structure:**
```
App
├── Header
├── SearchBar
├── FilterButtons
├── PostList
│   └── PostCard (multiple)
│       ├── PostHeader
│       ├── PostContent
│       ├── LikeButton
│       └── CommentSection
│           └── Comment (multiple)
└── Footer
```

**Skills Practiced:**
- Component composition
- Props passing
- State management
- Event handling
- Conditional rendering
- Lists and keys
- Form handling

**Mock Data:**
```javascript
const mockPosts = [
  {
    id: 1,
    title: 'Learning React',
    content: 'React is a JavaScript library...',
    author: 'Alice',
    likes: 5,
    comments: [
      { id: 1, author: 'Bob', text: 'Great post!' }
    ]
  },
  // More posts...
]
```

**Deliverable:** Working blog reader with all features

---

### React Hooks & Side Effects

#### useState Deep Dive

**Complex State Patterns:**

```javascript
// 1. Lazy initialization (for expensive calculations)
function ExpensiveComponent() {
  const [data, setData] = useState(() => {
    // This only runs once on initial render
    return expensiveCalculation()
  })
}

// 2. Functional updates (when new state depends on old state)
function Counter() {
  const [count, setCount] = useState(0)
  
  const increment = () => {
    // ✅ Correct: Use function
    setCount(prevCount => prevCount + 1)
  }
  
  const incrementMultiple = () => {
    setCount(c => c + 1)
    setCount(c => c + 1)  // Will increment by 2
    setCount(c => c + 1)  // Will increment by 3
  }
}

// 3. Merging state (for objects)
function UserForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: 0
  })
  
  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }
}
```

#### useEffect - Side Effects Hook

**Think of useEffect as Lifecycle Hooks**

```javascript
import { useEffect } from 'react'

// 1. Run after every render
function Example1() {
  useEffect(() => {
    console.log('Component rendered or updated')
  })  // No dependency array
}

// 2. Run only once (componentDidMount)
function Example2() {
  useEffect(() => {
    console.log('Component mounted')
    
    // Fetch data on mount
    fetchData()
  }, [])  // Empty dependency array
}

// 3. Run when specific values change
function Example3({ userId }) {
  useEffect(() => {
    console.log('userId changed:', userId)
    fetchUserData(userId)
  }, [userId])  // Re-run when userId changes
}

// 4. Cleanup function (componentWillUnmount)
function Example4() {
  useEffect(() => {
    // Subscribe to something
    const subscription = subscribe()
    
    // Cleanup function
    return () => {
      subscription.unsubscribe()
    }
  }, [])
}
```

**Common useEffect Patterns:**

```javascript
// Pattern 1: Data fetching
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    // Reset states when userId changes
    setLoading(true)
    setError(null)
    
    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`)
        
        if (!response.ok) {
          throw new Error('Failed to fetch user')
        }
        
        const data = await response.json()
        setUser(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    
    fetchUser()
  }, [userId])  // Re-fetch when userId changes
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  if (!user) return <div>User not found</div>
  
  return <div>{user.name}</div>
}

// Pattern 2: Event listeners
function WindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  })
  
  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }
    
    window.addEventListener('resize', handleResize)
    
    // Cleanup: remove listener on unmount
    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])  // Empty array = only set up once
  
  return <div>{size.width} x {size.height}</div>
}

// Pattern 3: Timers
function Timer() {
  const [seconds, setSeconds] = useState(0)
  
  useEffect(() => {
    const intervalId = setInterval(() => {
      setSeconds(s => s + 1)
    }, 1000)
    
    // Cleanup: clear interval on unmount
    return () => clearInterval(intervalId)
  }, [])
  
  return <div>Seconds: {seconds}</div>
}

// Pattern 4: Document title
function PageTitle({ title }) {
  useEffect(() => {
    document.title = title
    
    // Optional: restore original title
    return () => {
      document.title = 'My App'
    }
  }, [title])
}

// Pattern 5: localStorage sync
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const stored = localStorage.getItem(key)
    return stored ? JSON.parse(stored) : initialValue
  })
  
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value))
  }, [key, value])
  
  return [value, setValue]
}

// Usage
function App() {
  const [user, setUser] = useLocalStorage('user', null)
}
```

#### useRef - Persistent References

```javascript
import { useRef } from 'react'

// 1. Access DOM elements
function FocusInput() {
  const inputRef = useRef(null)
  
  const handleClick = () => {
    inputRef.current.focus()
  }
  
  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>Focus Input</button>
    </>
  )
}

// 2. Store mutable values (doesn't cause re-render)
function Timer() {
  const [seconds, setSeconds] = useState(0)
  const intervalRef = useRef(null)
  
  const start = () => {
    intervalRef.current = setInterval(() => {
      setSeconds(s => s + 1)
    }, 1000)
  }
  
  const stop = () => {
    clearInterval(intervalRef.current)
  }
  
  return (
    <div>
      <p>Seconds: {seconds}</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  )
}

// 3. Previous value
function usePrevious(value) {
  const ref = useRef()
  
  useEffect(() => {
    ref.current = value
  }, [value])
  
  return ref.current
}

// Usage
function Counter() {
  const [count, setCount] = useState(0)
  const prevCount = usePrevious(count)
  
  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

#### useContext - Global State

```javascript
import { createContext, useContext, useState } from 'react'

// 1. Create context
const ThemeContext = createContext()

// 2. Provider component
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// 3. Custom hook for easy access
function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// 4. Usage
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Main />
    </ThemeProvider>
  )
}

function Header() {
  const { theme, toggleTheme } = useTheme()
  
  return (
    <header className={theme}>
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'dark' : 'light'}
      </button>
    </header>
  )
}
```

#### useMemo - Memoization

```javascript
import { useMemo } from 'react'

function ExpensiveComponent({ items, filter }) {
  // Only recalculate when items or filter change
  const filteredItems = useMemo(() => {
    console.log('Filtering items...')
    return items.filter(item => 
      item.name.includes(filter)
    )
  }, [items, filter])
  
  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}

// When to use useMemo:
// ✅ Expensive calculations
// ✅ Prevent unnecessary re-renders
// ❌ Simple operations (overhead not worth it)
```

#### useCallback - Memoize Functions

```javascript
import { useCallback } from 'react'

function Parent() {
  const [count, setCount] = useState(0)
  
  // Without useCallback: new function on every render
  const handleClick = () => {
    console.log('Clicked')
  }
  
  // With useCallback: same function reference
  const handleClickMemoized = useCallback(() => {
    console.log('Clicked')
  }, [])  // No dependencies = never changes
  
  // With dependencies
  const incrementBy = useCallback((amount) => {
    setCount(c => c + amount)
  }, [])  // setCount is stable, so [] is fine
  
  return <Child onClick={handleClickMemoized} />
}
```

#### Custom Hooks

**Create Reusable Logic:**

```javascript
// Custom hook for data fetching
function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)
        const response = await fetch(url)
        const json = await response.json()
        setData(json)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [url])
  
  return { data, loading, error }
}

// Usage
function UserList() {
  const { data: users, loading, error } = useFetch('/api/users')
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// Custom hook for form handling
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues)
  
  const handleChange = (e) => {
    setValues({
      ...values,
      [e.target.name]: e.target.value
    })
  }
  
  const reset = () => {
    setValues(initialValues)
  }
  
  return { values, handleChange, reset }
}

// Usage
function LoginForm() {
  const { values, handleChange, reset } = useForm({
    email: '',
    password: ''
  })
  
  const handleSubmit = (e) => {
    e.preventDefault()
    console.log(values)
    reset()
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        name="email"
        value={values.email}
        onChange={handleChange}
      />
      <input 
        name="password"
        type="password"
        value={values.password}
        onChange={handleChange}
      />
      <button type="submit">Login</button>
    </form>
  )
}
```

#### Learning Resources

**Documentation:**
- React Hooks documentation
- React useEffect guide

**Practice:**
- Build hooks from scratch
- Create custom hooks for common patterns
- Refactor class components to hooks

#### Practice Project: Weather Dashboard

**Objective:** Build a weather dashboard with API integration

**Requirements:**
- ✅ Search weather by city name
- ✅ Display current weather conditions
- ✅ Show 5-day forecast
- ✅ Save favorite cities (localStorage)
- ✅ Auto-refresh every 5 minutes
- ✅ Loading and error states
- ✅ Temperature unit toggle (°C/°F)

**Skills Practiced:**
- useEffect for data fetching
- useState for complex state
- Custom hooks (useFetch, useLocalStorage)
- Timers and cleanup
- Error handling
- API integration

**API:** OpenWeatherMap (free tier)

**Deliverable:** Working weather dashboard

---

<a name="phase-3"></a>
## 6. Phase 3: State Management & API Integration

### Overview
Connect your React frontend to backend APIs, handle authentication, and manage complex application state.

---

### API Integration & Authentication

#### Creating an API Client

**Think of this as your Python `requests` library for frontend:**

```javascript
// src/api/client.js

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000'

class APIError extends Error {
  constructor(message, status, data) {
    super(message)
    this.status = status
    this.data = data
  }
}

async function request(endpoint, options = {}) {
  // Get token from localStorage
  const token = localStorage.getItem('token')
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  }
  
  // Add body if present
  if (options.body) {
    config.body = JSON.stringify(options.body)
  }
  
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config)
    
    // Handle different response types
    const contentType = response.headers.get('content-type')
    let data
    
    if (contentType?.includes('application/json')) {
      data = await response.json()
    } else {
      data = await response.text()
    }
    
    if (!response.ok) {
      throw new APIError(
        data.message || 'Request failed',
        response.status,
        data
      )
    }
    
    return data
  } catch (error) {
    if (error instanceof APIError) {
      throw error
    }
    throw new APIError('Network error', 0, { message: error.message })
  }
}

// Export API methods (similar to Python API client)
export const api = {
  // Users
  users: {
    list: (params) => request('/users' + buildQueryString(params)),
    get: (id) => request(`/users/${id}`),
    create: (data) => request('/users', { method: 'POST', body: data }),
    update: (id, data) => request(`/users/${id}`, { method: 'PUT', body: data }),
    delete: (id) => request(`/users/${id}`, { method: 'DELETE' }),
  },
  
  // Auth
  auth: {
    login: (credentials) => request('/auth/login', { 
      method: 'POST', 
      body: credentials 
    }),
    logout: () => request('/auth/logout', { method: 'POST' }),
    refresh: () => request('/auth/refresh', { method: 'POST' }),
    me: () => request('/auth/me'),
  },
  
  // Posts
  posts: {
    list: (params) => request('/posts' + buildQueryString(params)),
    get: (id) => request(`/posts/${id}`),
    create: (data) => request('/posts', { method: 'POST', body: data }),
    update: (id, data) => request(`/posts/${id}`, { method: 'PUT', body: data }),
    delete: (id) => request(`/posts/${id}`, { method: 'DELETE' }),
  },
}

// Helper function
function buildQueryString(params) {
  if (!params) return ''
  const query = new URLSearchParams(params).toString()
  return query ? `?${query}` : ''
}

// Usage examples:
// const users = await api.users.list({ page: 1, limit: 10 })
// const user = await api.users.get(123)
// const newUser = await api.users.create({ name: 'John', email: 'john@example.com' })
```

#### Authentication Context

**Global Authentication State:**

```javascript
// src/contexts/AuthContext.jsx

import { createContext, useContext, useState, useEffect } from 'react'
import { api } from '../api/client'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  
  // Check if user is logged in on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token')
      
      if (token) {
        try {
          // Verify token and get user data
          const userData = await api.auth.me()
          setUser(userData)
        } catch (error) {
          // Token invalid or expired
          localStorage.removeItem('token')
        }
      }
      
      setLoading(false)
    }
    
    initAuth()
  }, [])
  
  const login = async (email, password) => {
    try {
      const data = await api.auth.login({ email, password })
      
      // Save token
      localStorage.setItem('token', data.token)
      
      // Save refresh token if provided
      if (data.refreshToken) {
        localStorage.setItem('refreshToken', data.refreshToken)
      }
      
      setUser(data.user)
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }
  
  const logout = () => {
    // Call logout endpoint (optional)
    api.auth.logout().catch(() => {})
    
    // Clear local data
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    setUser(null)
  }
  
  const updateUser = (updates) => {
    setUser(prev => ({ ...prev, ...updates }))
  }
  
  const value = {
    user,
    loading,
    login,
    logout,
    updateUser,
    isAuthenticated: !!user,
  }
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

**Usage in App:**

```javascript
// src/App.jsx

import { AuthProvider } from './contexts/AuthContext'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Your routes */}
        </Routes>
      </Router>
    </AuthProvider>
  )
}
```

**Login Component:**

```javascript
// src/components/LoginForm.jsx

import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    
    const result = await login(email, password)
    
    if (result.success) {
      navigate('/dashboard')
    } else {
      setError(result.error)
    }
    
    setLoading(false)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      
      <input 
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      
      <input 
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
```

#### Protected Routes

```javascript
// src/components/PrivateRoute.jsx

import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div>Loading...</div>
  }
  
  return user ? children : <Navigate to="/login" />
}

// Usage
<Route 
  path="/dashboard" 
  element={
    <PrivateRoute>
      <Dashboard />
    </PrivateRoute>
  } 
/>
```

#### Token Refresh Pattern

```javascript
// src/api/client.js (enhanced)

let isRefreshing = false
let refreshSubscribers = []

function subscribeTokenRefresh(callback) {
  refreshSubscribers.push(callback)
}

function onRefreshed(token) {
  refreshSubscribers.forEach(callback => callback(token))
  refreshSubscribers = []
}

async function request(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config)
    
    // Handle 401 (unauthorized)
    if (response.status === 401) {
      if (!isRefreshing) {
        isRefreshing = true
        
        try {
          const refreshToken = localStorage.getItem('refreshToken')
          const data = await fetch(`${API_BASE}/auth/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refreshToken })
          }).then(r => r.json())
          
          localStorage.setItem('token', data.token)
          isRefreshing = false
          onRefreshed(data.token)
          
          // Retry original request
          return request(endpoint, options)
        } catch (error) {
          isRefreshing = false
          // Refresh failed, logout user
          localStorage.clear()
          window.location.href = '/login'
          throw error
        }
      }
      
      // Wait for token refresh
      return new Promise((resolve) => {
        subscribeTokenRefresh((token) => {
          resolve(request(endpoint, options))
        })
      })
    }
    
    return data
  } catch (error) {
    throw error
  }
}
```

---

### State Management with React Query

#### Why React Query?

Think of React Query as an **ORM for API data**:
- Automatic caching (like Redis)
- Background refetching
- Optimistic updates
- Deduplication
- Pagination support
- Infinite scrolling

#### Setup

```bash
npm install @tanstack/react-query
```

```javascript
// src/main.jsx or src/App.jsx

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      cacheTime: 1000 * 60 * 10, // 10 minutes
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        {/* Your app */}
      </AuthProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

#### Fetching Data

```javascript
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'

// Simple fetch
function UserList() {
  const { data: users, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.users.list(),
  })
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// With parameters
function UserList({ page, filter }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users', { page, filter }],  // Key includes params
    queryFn: () => api.users.list({ page, filter }),
  })
  
  // ...
}

// Dependent query
function UserPosts({ userId }) {
  // Only fetch posts if userId exists
  const { data: posts } = useQuery({
    queryKey: ['posts', userId],
    queryFn: () => api.posts.list({ userId }),
    enabled: !!userId,  // Only run if userId is truthy
  })
  
  // ...
}
```

#### Mutations (Create/Update/Delete)

```javascript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function CreateUserForm() {
  const queryClient = useQueryClient()
  
  const mutation = useMutation({
    mutationFn: (newUser) => api.users.create(newUser),
    onSuccess: () => {
      // Invalidate and refetch users
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
  
  const handleSubmit = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    
    mutation.mutate({
      name: formData.get('name'),
      email: formData.get('email'),
    })
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <input name="email" type="email" required />
      
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create User'}
      </button>
      
      {mutation.isError && (
        <div className="error">{mutation.error.message}</div>
      )}
      
      {mutation.isSuccess && (
        <div className="success">User created!</div>
      )}
    </form>
  )
}

// Update mutation
function EditUserForm({ user }) {
  const queryClient = useQueryClient()
  
  const mutation = useMutation({
    mutationFn: (updates) => api.users.update(user.id, updates),
    onSuccess: (updatedUser) => {
      // Update specific user in cache
      queryClient.setQueryData(['users', user.id], updatedUser)
      
      // Or invalidate list
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
  
  // ...
}

// Delete mutation
function DeleteUserButton({ userId }) {
  const queryClient = useQueryClient()
  
  const mutation = useMutation({
    mutationFn: () => api.users.delete(userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
  
  return (
    <button onClick={() => mutation.mutate()}>
      Delete
    </button>
  )
}
```

#### Optimistic Updates

```javascript
function LikeButton({ post }) {
  const queryClient = useQueryClient()
  
  const likeMutation = useMutation({
    mutationFn: () => api.posts.like(post.id),
    
    // Optimistically update UI
    onMutate: async () => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['posts', post.id] })
      
      // Snapshot previous value
      const previousPost = queryClient.getQueryData(['posts', post.id])
      
      // Optimistically update
      queryClient.setQueryData(['posts', post.id], (old) => ({
        ...old,
        likes: old.likes + 1,
        isLiked: true,
      }))
      
      // Return context with snapshot
      return { previousPost }
    },
    
    // If mutation fails, rollback
    onError: (err, variables, context) => {
      queryClient.setQueryData(
        ['posts', post.id],
        context.previousPost
      )
    },
    
    // Always refetch after error or success
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['posts', post.id] })
    },
  })
  
  return (
    <button onClick={() => likeMutation.mutate()}>
      {post.isLiked ? 'Unlike' : 'Like'} ({post.likes})
    </button>
  )
}
```

#### Pagination

```javascript
function PaginatedUserList() {
  const [page, setPage] = useState(1)
  
  const { data, isLoading, isPreviousData } = useQuery({
    queryKey: ['users', page],
    queryFn: () => api.users.list({ page, limit: 10 }),
    keepPreviousData: true,  // Keep old data while fetching new page
  })
  
  return (
    <div>
      <ul>
        {data?.users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
      
      <div>
        <button 
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        
        <span>Page {page}</span>
        
        <button 
          onClick={() => setPage(p => p + 1)}
          disabled={isPreviousData || !data?.hasMore}
        >
          Next
        </button>
      </div>
    </div>
  )
}
```

#### Infinite Scroll

```javascript
import { useInfiniteQuery } from '@tanstack/react-query'

function InfiniteUserList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['users'],
    queryFn: ({ pageParam = 1 }) => api.users.list({ page: pageParam }),
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.hasMore ? allPages.length + 1 : undefined
    },
  })
  
  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.users.map(user => (
            <div key={user.id}>{user.name}</div>
          ))}
        </div>
      ))}
      
      {hasNextPage && (
        <button 
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  )
}
```

#### Practice Project: Task Management App

**Objective:** Build a full-featured task manager connected to your backend

**Requirements:**
- ✅ User authentication (login/logout)
- ✅ CRUD operations for tasks
- ✅ Categories/tags for tasks
- ✅ Filter by status (all, pending, completed)
- ✅ Search tasks
- ✅ Pagination
- ✅ Optimistic updates
- ✅ Real-time updates (polling every 30s)
- ✅ Error handling with retry
- ✅ Loading states

**Skills Practiced:**
- React Query for all API operations
- Authentication context
- Protected routes
- Form handling
- Optimistic UI updates
- Error handling
- Loading states

**Backend Integration:**
- Connect to your team's existing API
- Or build a simple FastAPI/Express backend

**Deliverable:** Production-ready task manager

---

<a name="phase-4"></a>
## 7. Phase 4: Modern React & Tooling

### React Router & Navigation

#### Installation

```bash
npm install react-router-dom
```

#### Basic Setup

```javascript
// src/main.jsx or src/App.jsx

import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/users">Users</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<UserList />} />
        <Route path="/users/:id" element={<UserDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}
```

#### Navigation Patterns

```javascript
import { Link, NavLink, useNavigate, useParams, useSearchParams } from 'react-router-dom'

// 1. Link (basic navigation)
<Link to="/users">View Users</Link>

// 2. NavLink (with active state)
<NavLink 
  to="/dashboard"
  className={({ isActive }) => isActive ? 'active' : ''}
>
  Dashboard
</NavLink>

// 3. Programmatic navigation
function LoginForm() {
  const navigate = useNavigate()
  
  const handleLogin = async () => {
    await login()
    navigate('/dashboard')  // Redirect after login
    // navigate(-1)  // Go back
    // navigate('/users', { replace: true })  // Replace history
  }
}

// 4. URL parameters
function UserDetail() {
  const { id } = useParams()  // Get :id from URL
  
  const { data: user } = useQuery({
    queryKey: ['users', id],
    queryFn: () => api.users.get(id),
  })
  
  return <div>{user?.name}</div>
}

// 5. Query parameters
function SearchResults() {
  const [searchParams, setSearchParams] = useSearchParams()
  
  const query = searchParams.get('q')
  const page = searchParams.get('page') || 1
  
  const updateSearch = (newQuery) => {
    setSearchParams({ q: newQuery, page: 1 })
  }
  
  return (
    <div>
      <input 
        value={query}
        onChange={(e) => updateSearch(e.target.value)}
      />
    </div>
  )
}
```

#### Nested Routes

```javascript
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        
        <Route path="users" element={<UsersLayout />}>
          <Route index element={<UserList />} />
          <Route path=":id" element={<UserDetail />} />
          <Route path="new" element={<CreateUser />} />
        </Route>
      </Route>
    </Routes>
  )
}

// Layout component
import { Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div>
      <Header />
      <Outlet />  {/* Nested routes render here */}
      <Footer />
    </div>
  )
}
```

#### Route Protection

```javascript
function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) return <div>Loading...</div>
  
  return user ? children : <Navigate to="/login" replace />
}

// Usage
<Route 
  path="/dashboard" 
  element={
    <PrivateRoute>
      <Dashboard />
    </PrivateRoute>
  } 
/>

// Role-based protection
function AdminRoute({ children }) {
  const { user } = useAuth()
  
  if (!user) return <Navigate to="/login" />
  if (user.role !== 'admin') return <Navigate to="/unauthorized" />
  
  return children
}
```

---

### Styling with Tailwind CSS

#### Why Tailwind for Backend Developers?

- **No CSS to write** - Use utility classes
- **Responsive design** built-in
- **Consistent spacing** and colors
- **Fast development** - No switching between files

#### Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### Basic Usage

```javascript
// Simple button
<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Click me
</button>

// Card layout
<div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
  <h2 className="text-2xl font-bold mb-4">User Profile</h2>
  <p className="text-gray-600">Backend Developer</p>
  <button className="mt-4 w-full py-2 bg-green-500 text-white rounded">
    Edit Profile
  </button>
</div>

// Flexbox layout
<div className="flex items-center justify-between p-4">
  <h1 className="text-xl font-bold">Dashboard</h1>
  <button className="px-3 py-1 bg-gray-200 rounded">Settings</button>
</div>

// Grid layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div className="bg-white p-4 rounded shadow">Card 1</div>
  <div className="bg-white p-4 rounded shadow">Card 2</div>
  <div className="bg-white p-4 rounded shadow">Card 3</div>
</div>

// Responsive design
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

// Form
<form className="max-w-md mx-auto space-y-4">
  <div>
    <label className="block text-sm font-medium mb-1">Email</label>
    <input 
      type="email"
      className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>
  
  <div>
    <label className="block text-sm font-medium mb-1">Password</label>
    <input 
      type="password"
      className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>
  
  <button 
    type="submit"
    className="w-full py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
  >
    Login
  </button>
</form>
```

#### Common Patterns

```javascript
// Container
<div className="container mx-auto px-4">
  {/* Content */}
</div>

// Centered content
<div className="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>

// Navbar
<nav className="bg-white shadow-md">
  <div className="container mx-auto px-4 py-3 flex items-center justify-between">
    <div className="text-xl font-bold">Logo</div>
    <div className="space-x-4">
      <a href="#" className="text-gray-700 hover:text-blue-500">Home</a>
      <a href="#" className="text-gray-700 hover:text-blue-500">About</a>
    </div>
  </div>
</nav>

// Card
<div className="bg-white rounded-lg shadow-md overflow-hidden">
  <img src="image.jpg" className="w-full h-48 object-cover" />
  <div className="p-4">
    <h3 className="text-lg font-semibold mb-2">Title</h3>
    <p className="text-gray-600 text-sm">Description</p>
  </div>
</div>

// Loading spinner
<div className="flex items-center justify-center">
  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
</div>
```

#### Component Library Alternative

If you prefer pre-built components:

```bash
# shadcn/ui (recommended)
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input

# Material-UI
npm install @mui/material @emotion/react @emotion/styled

# Chakra UI
npm install @chakra-ui/react @emotion/react @emotion/styled
```

---

<a name="phase-5"></a>
## 8. Phase 5: Production-Ready Skills

### Testing

#### Setup

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
```

```javascript
// src/test/setup.js
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom'

afterEach(() => {
  cleanup()
})
```

#### Component Testing

```javascript
// src/components/Counter.test.jsx
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Counter from './Counter'

describe('Counter', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={5} />)
    expect(screen.getByText('Count: 5')).toBeInTheDocument()
  })
  
  it('increments count on button click', () => {
    render(<Counter initialCount={0} />)
    
    const button = screen.getByText('Increment')
    fireEvent.click(button)
    
    expect(screen.getByText('Count: 1')).toBeInTheDocument()
  })
  
  it('decrements count', () => {
    render(<Counter initialCount={5} />)
    
    const button = screen.getByText('Decrement')
    fireEvent.click(button)
    
    expect(screen.getByText('Count: 4')).toBeInTheDocument()
  })
})
```

#### Testing with User Events

```javascript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

it('submits form with user input', async () => {
  const user = userEvent.setup()
  const handleSubmit = vi.fn()
  
  render(<LoginForm onSubmit={handleSubmit} />)
  
  // Type in inputs
  await user.type(screen.getByLabelText('Email'), 'test@example.com')
  await user.type(screen.getByLabelText('Password'), 'password123')
  
  // Click submit
  await user.click(screen.getByText('Login'))
  
  // Assert
  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  })
})
```

#### Mocking API Calls

```javascript
import { vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import UserList from './UserList'
import * as api from '../api/client'

it('displays users from API', async () => {
  // Mock API response
  const mockUsers = [
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' },
  ]
  
  vi.spyOn(api, 'getUsers').mockResolvedValue(mockUsers)
  
  render(<UserList />)
  
  // Wait for users to load
  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument()
    expect(screen.getByText('Bob')).toBeInTheDocument()
  })
})

it('displays error message on API failure', async () => {
  vi.spyOn(api, 'getUsers').mockRejectedValue(new Error('Failed to fetch'))
  
  render(<UserList />)
  
  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument()
  })
})
```

#### E2E Testing with Playwright

```bash
npm init playwright@latest
```

```javascript
// tests/login.spec.js
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:3000/login')
  
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')
  
  await expect(page).toHaveURL('http://localhost:3000/dashboard')
  await expect(page.locator('h1')).toContainText('Dashboard')
})

test('displays error for invalid credentials', async ({ page }) => {
  await page.goto('http://localhost:3000/login')
  
  await page.fill('input[name="email"]', 'wrong@example.com')
  await page.fill('input[name="password"]', 'wrongpass')
  await page.click('button[type="submit"]')
  
  await expect(page.locator('.error')).toContainText('Invalid credentials')
})
```

---

### Build Tools & Performance

#### Environment Variables

```bash
# .env.development
VITE_API_URL=http://localhost:8000
VITE_API_KEY=dev_key_123

# .env.production
VITE_API_URL=https://api.production.com
VITE_API_KEY=prod_key_456
```

```javascript
// Usage
const API_URL = import.meta.env.VITE_API_URL
const API_KEY = import.meta.env.VITE_API_KEY
```

#### Code Splitting

```javascript
import { lazy, Suspense } from 'react'

// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'))
const Settings = lazy(() => import('./Settings'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  )
}
```

#### Performance Optimization

```javascript
import { memo, useMemo, useCallback } from 'react'

// 1. Memoize components
const UserCard = memo(function UserCard({ user }) {
  return <div>{user.name}</div>
})

// 2. Memoize expensive calculations
function SearchResults({ items, query }) {
  const filteredItems = useMemo(() => {
    return items.filter(item => 
      item.name.toLowerCase().includes(query.toLowerCase())
    )
  }, [items, query])
  
  return <ul>{/* render filtered items */}</ul>
}

// 3. Memoize callbacks
function Parent() {
  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])
  
  return <Child onClick={handleClick} />
}
```

#### Image Optimization

```javascript
// Lazy loading
<img 
  src="large-image.jpg" 
  loading="lazy"
  width="400"
  height="300"
/>

// Responsive images
<img 
  srcSet="
    image-small.jpg 400w,
    image-medium.jpg 800w,
    image-large.jpg 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  src="image-large.jpg"
  alt="Description"
/>
```

#### Build Optimization

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'router-vendor': ['react-router-dom'],
          'query-vendor': ['@tanstack/react-query'],
        },
      },
    },
  },
})
```

---

<a name="phase-6"></a>
## 9. Phase 6: Team Project

### Full-Stack Team Project: Internal Admin Dashboard

#### Project Overview

**Objective:** Build a production-ready admin dashboard that connects to your team's backend API.

**Team Structure:**
- Backend team: Provide API endpoints
- Frontend team: Build React interface
- Collaborate on features and integration

#### Architecture

```
┌─────────────────────────────────────┐
│         React Frontend              │
│  ┌──────────────────────────────┐   │
│  │ Vite + React 18              │   │
│  │ React Query (data fetching)  │   │
│  │ React Router (navigation)    │   │
│  │ Tailwind CSS (styling)       │   │
│  │ Vitest (testing)             │   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               │ HTTP/REST API
               │ WebSocket (optional)
               │
┌──────────────▼──────────────────────┐
│      Backend API (Your Choice)      │
│  ┌──────────────────────────────┐   │
│  │ FastAPI / Django / Express   │   │
│  │ PostgreSQL / MongoDB         │   │
│  │ JWT Authentication           │   │
│  │ RESTful endpoints            │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```
==================================================================================
#### Core Features

** Project Setup & Authentication**

**Backend Tasks:**
- Set up API endpoints
- Implement JWT authentication
- User CRUD endpoints
- Database schema

**Frontend Tasks:**
- Initialize Vite + React project
- Set up folder structure
- Install dependencies
- Create API client
- Build authentication flow
- Login/logout functionality

**Deliverables:**
- Working authentication
- Protected routes
- Basic dashboard layout

---

** Core CRUD Operations**

**Backend Tasks:**
- Resource CRUD endpoints (users, products, orders, etc.)
- Pagination and filtering
- Search functionality
- Validation

**Frontend Tasks:**
- User management interface
  - List users with pagination
  - Create new user form
  - Edit user form
  - Delete user confirmation
- Data tables with sorting
- Search and filter UI
- Form validation

**Deliverables:**
- Complete CRUD operations for at least 2 resources
- Working search and filter
- Pagination

---

** Advanced Features**

**Backend Tasks:**
- File upload endpoint
- Analytics/stats endpoints
- Real-time notifications (WebSocket)
- Bulk operations

**Frontend Tasks:**
- File upload with progress
- Dashboard with charts
- Real-time notifications
- Bulk actions (select multiple, delete)
- Export data (CSV)
- Dark mode toggle

**Deliverables:**
- Working file upload
- Dashboard with visualizations
- Real-time features

---

** Testing, Deployment & Polish**

**Backend Tasks:**
- API tests
- Performance optimization
- Docker setup
- Deploy to cloud (Heroku, Railway, etc.)

**Frontend Tasks:**
- Unit tests for components
- E2E tests for critical flows
- Performance optimization
- Accessibility audit
- Error handling polish
- Loading states
- Deploy to Vercel/Netlify

**Deliverables:**
- >70% test coverage
- Deployed application
- Documentation
- Demo video

---

#### Recommended Tech Stack

**Frontend:**
```
- React 18
- Vite
- React Router
- React Query
- Tailwind CSS
- Recharts (for charts)
- React Hook Form (forms)
- Vitest + Testing Library
- Playwright (E2E)
```

**Backend (Choose one):**
```
- FastAPI + PostgreSQL
- Django + DRF + PostgreSQL
- Express + MongoDB
- NestJS + PostgreSQL
```

#### Example Feature: User Management

**API Endpoints (Backend):**
```
GET    /api/users              # List users
GET    /api/users/:id          # Get user
POST   /api/users              # Create user
PUT    /api/users/:id          # Update user
DELETE /api/users/:id          # Delete user
GET    /api/users/search?q=... # Search users
```

**Frontend Components:**

```
src/
├── pages/
│   ├── LoginPage.jsx
│   ├── DashboardPage.jsx
│   └── users/
│       ├── UserListPage.jsx
│       ├── UserDetailPage.jsx
│       ├── CreateUserPage.jsx
│       └── EditUserPage.jsx
├── components/
│   ├── layout/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   └── Layout.jsx
│   ├── users/
│   │   ├── UserTable.jsx
│   │   ├── UserCard.jsx
│   │   ├── UserForm.jsx
│   │   └── DeleteUserModal.jsx
│   └── common/
│       ├── Button.jsx
│       ├── Input.jsx
│       ├── Modal.jsx
│       └── LoadingSpinner.jsx
├── contexts/
│   └── AuthContext.jsx
├── api/
│   └── client.js
├── hooks/
│   ├── useAuth.js
│   └── useUsers.js
└── utils/
    ├── formatDate.js
    └── validators.js
```

#### Evaluation Criteria

**Functionality (40%)**
- All features working
- Error handling
- Edge cases handled
- User experience

**Code Quality (30%)**
- Clean, readable code
- Proper component structure
- Reusable components
- No code smells

**Testing (15%)**
- Unit tests
- Integration tests
- E2E tests
- >70% coverage

**Performance (10%)**
- Fast load times
- Optimized rendering
- Efficient API calls
- Proper caching

**Documentation (5%)**
- README with setup instructions
- Code comments where needed
- API documentation
- User guide

---

