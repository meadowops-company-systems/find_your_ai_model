# Find Your AI Model - Development Guide

## 1. Project Overview

**Project:** Find Your AI Model (FYAIM)  
**Purpose:** Web app helping users choose the right AI tool  
**Type:** Full-stack web application  
**Status:** Ready for development  
**Scope:** Frontend + Backend only (no agent)

---

## 2. Tech Stack

### Frontend
React 18
Tailwind CSS
JavaScript/JSX
Node.js
npm
Vercel (hosting)

### Backend
Python 3.10+
Vercel Serverless Functions
requests library
JSON format
.env variables

### Database & APIs
Airtable (read-only)
OpenRouter API (Llama 2 70B)
Google Analytics
Calendly
GitHub

---

## 3. Project Structure
find-your-ai-model/
├─ frontend/
│  ├─ public/
│  │  ├─ index.html
│  │  └─ favicon.ico
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ Header.jsx
│  │  │  ├─ TaskForm.jsx
│  │  │  ├─ RecommendationDisplay.jsx
│  │  │  ├─ PrimaryRecommendation.jsx
│  │  │  ├─ AlternativesList.jsx
│  │  │  ├─ CostBreakdown.jsx
│  │  │  └─ Footer.jsx
│  │  ├─ pages/
│  │  │  └─ HomePage.jsx
│  │  ├─ api/
│  │  │  └─ client.js
│  │  ├─ styles/
│  │  │  └─ globals.css
│  │  ├─ App.jsx
│  │  └─ index.js
│  ├─ package.json
│  ├─ .env.example
│  └─ README.md
│
├─ api/
│  ├─ recommend.py
│  ├─ airtable_client.py
│  ├─ openrouter_client.py
│  ├─ recommendation_engine.py
│  ├─ utils/
│  │  ├─ validators.py
│  │  ├─ formatters.py
│  │  └─ logger.py
│  ├─ vercel.json
│  ├─ requirements.txt
│  ├─ .env.example
│  └─ README.md
│
├─ docs/
│  ├─ README.md
│  ├─ PRD.md
│  ├─ SRS.md
│  ├─ ARCHITECTURE.md
│  ├─ DATABASE.md
│  ├─ API.md
│  ├─ CLAUDE.md (this file)
│  ├─ UI-UX.md
│  ├─ TESTING.md
│  ├─ DEPLOYMENT.md
│  ├─ DECISIONS.md
│  ├─ CHANGELOG.md
│  └─ ROADMAP.md
│
├─ tests/
│  ├─ frontend/
│  │  └─ components.test.jsx
│  └─ backend/
│     ├─ test_recommend.py
│     ├─ test_airtable.py
│     └─ test_openrouter.py
│
├─ .github/
│  └─ workflows/
│     └─ deploy.yml
│
├─ .gitignore
├─ .env.example
└─ README.md

---

## 4. Key Commands

### Frontend

```bash
# Install dependencies
npm install

# Start dev server (localhost:3000)
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (requires Vercel CLI)
vercel dev

# Test API
curl -X POST http://localhost:3000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"taskDescription":"Write a blog post"}'

# Run tests
pytest tests/backend/

# Lint
pylint api/

# Format
black api/
```

### Deployment

```bash
# Deploy to production
git push origin main

# Manual deployment
vercel deploy --prod

# Check status
vercel ls
```

---

## 5. Architecture & Design Rules

### 🔴 CRITICAL RULES (Must Follow)

**1. NO AGENT CODE**
- Agent is separate project
- Never include agent in FYAIM repo
- FYAIM only reads from Airtable
- Agent updates Airtable independently

**2. STATELESS BACKEND**
- No user sessions
- No stored state
- Every request independent
- Enables easy scaling

**3. AIRTABLE AS SOURCE OF TRUTH**
- All model data in Airtable
- FYAIM reads only
- Never hardcode model data
- Cache only for performance

**4. API-FIRST DESIGN**
- Frontend talks to API only
- No direct database calls
- Enables future mobile apps
- Clear separation

**5. ZERO COST FIRST**
- Use free tiers
- OpenRouter free (Llama 2)
- Airtable free (1000 records)
- Vercel free tier
- Upgrade only if needed

**6. SECURITY DEFAULTS**
- All secrets in .env
- Never in code
- Input validation everywhere
- Rate limiting enabled
- No sensitive logs

---

## 6. Coding Conventions

### Frontend (JavaScript/React)

```javascript
// File naming
components/TaskForm.jsx     // ✅ PascalCase
components/taskForm.jsx     // ❌ camelCase

// Component structure
export default function TaskForm() {
  const [state, setState] = useState(null);
  
  const handleClick = () => {
    // logic
  };
  
  return (
    <div>{/* JSX */}</div>
  );
}

// Props destructuring
function Button({ label, onClick, disabled = false }) {
  return <button disabled={disabled}>{label}</button>;
}

// Functional components only (no class components)

// Imports at top
import React, { useState } from 'react';
import { formatCost } from '../utils/formatters';

// Comments only for complex logic
// Self-documenting code preferred

// Spacing and formatting
const x = 1;        // ✅ Spaces around operators
const y=2;          // ❌ No spaces

// Semicolons
const name = "John";  // ✅
const age = 25        // ❌
```

### Backend (Python)

```python
# File naming
recommend.py            # ✅ snake_case
recommendationEngine.py # ❌ camelCase

# Function naming
def get_recommendation():  # ✅ snake_case
def getRecommendation():   # ❌ camelCase

# Class naming
class AirtableClient:   # ✅ PascalCase
class airtable_client:  # ❌ snake_case

# Constants
MAX_DESCRIPTION_LENGTH = 5000
DEFAULT_CACHE_TTL = 300

# Type hints (recommended)
def validate_input(task: str, length: int = 10) -> bool:
    return len(task) >= length

# Docstrings
def recommend(task_description: str) -> dict:
    """
    Generate AI tool recommendation for given task.
    
    Args:
        task_description: User's detailed task description
        
    Returns:
        Dictionary with recommendation data
        
    Raises:
        ValueError: If task description is invalid
    """
    pass

# Error handling
try:
    response = airtable.get_models()
except requests.RequestException as e:
    logger.error(f"Airtable error: {e}")
    return cached_models()

# Import organization
import os  # stdlib
from typing import Dict  # stdlib

import requests  # third-party

from .utils import logger  # local
```

---

## 7. IMPORTANT: Rules & Constraints

### Environment Variables
✅ DO:
├─ Store in .env file
├─ Load with os.getenv()
├─ Exclude .env from git (.gitignore)
├─ Provide .env.example
❌ DON'T:
├─ Hardcode secrets
├─ Commit .env file
├─ Print secrets to logs
├─ Share in messages

### Input Validation
✅ DO:
├─ Validate all user input
├─ Check length (10-5000)
├─ Check format
├─ Return clear errors
❌ DON'T:
├─ Trust user input
├─ Allow injection attacks
├─ Skip validation
├─ Generic error messages

### Error Handling
✅ DO:
├─ Handle all exceptions
├─ Return user-friendly errors
├─ Log errors with context
├─ Implement fallbacks
❌ DON'T:
├─ Let exceptions crash
├─ Expose internal errors
├─ Log sensitive data
├─ Fail silently

### Rate Limiting
✅ DO:
├─ Enforce 100 req/hour
├─ Return 429 on limit
├─ Provide retry info
├─ Track per IP
❌ DON'T:
├─ Allow unlimited requests
├─ Silently reject
├─ Allow DoS attacks
├─ Track per user

### Caching
✅ DO:
├─ Cache Airtable (5 min)
├─ Cache recommendations
├─ Implement TTL
├─ Fallback to stale cache
❌ DON'T:
├─ Use stale data permanently
├─ Cache sensitive data
├─ Make unnecessary calls
├─ Cache errors

### Logging
✅ DO:
├─ Log important events
├─ Log errors with context
├─ Use structured logging
├─ Log timestamps
❌ DON'T:
├─ Log sensitive data
├─ Log passwords
├─ Log API keys
├─ Log user data

---

## 8. Testing Strategy

### Unit Tests (Frontend)

```javascript
// tests/components/TaskForm.test.jsx
test('renders form with input', () => {
  render(<TaskForm />);
  expect(screen.getByPlaceholderText(/describe/i)).toBeInTheDocument();
});

test('disables button when empty', () => {
  render(<TaskForm />);
  expect(screen.getByText(/get recommendation/i)).toBeDisabled();
});

test('enables button when valid', () => {
  render(<TaskForm />);
  fireEvent.change(screen.getByPlaceholderText(/describe/i), {
    target: { value: 'Write a blog post' }
  });
  expect(screen.getByText(/get recommendation/i)).not.toBeDisabled();
});
```

### Unit Tests (Backend)

```python
# tests/backend/test_validators.py
def test_valid_input():
    assert validate_input("Write a blog post") == True

def test_input_too_short():
    with pytest.raises(ValueError):
        validate_input("short")

def test_input_too_long():
    with pytest.raises(ValueError):
        validate_input("a" * 5001)
```

### Integration Tests

```python
# tests/backend/test_recommend.py
def test_full_recommendation_flow():
    response = post('/api/recommend', {
        'taskDescription': 'Write a blog post'
    })
    assert response.status_code == 200
    assert 'recommendation' in response.json()
```

### Run Tests

```bash
# Frontend
npm test

# Backend
pytest tests/backend/

# All
npm test && pytest tests/
```

---

## 9. Environment Setup

### .env Template

```bash
# Frontend (.env in frontend/)
REACT_APP_API_URL=http://localhost:3000/api
REACT_APP_CALENDLY_URL=https://calendly.com/your-name

# Backend (.env in api/)
AIRTABLE_API_KEY=pat_your_key_here
AIRTABLE_BASE_ID=app_your_base_id
OPENROUTER_API_KEY=optional_if_paying
DEBUG=False
LOG_LEVEL=INFO
```

### Local Setup

```bash
# 1. Clone repo
git clone https://github.com/yourname/find-your-ai-model.git
cd find-your-ai-model

# 2. Frontend setup
cd frontend
npm install
cp .env.example .env
# Edit .env with your values
npm start

# 3. Backend setup (new terminal)
cd api
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
vercel dev

# 4. Visit http://localhost:3000
```

---

## 10. Common Tasks

### Add New Environment Variable

```bash
# 1. Add to .env file
MY_NEW_VAR=value

# 2. Update .env.example
MY_NEW_VAR=value_placeholder

# 3. Use in code
import os
value = os.getenv('MY_NEW_VAR')
```

### Update Dependencies

```bash
# Frontend
npm install package-name
npm update

# Backend
pip install new-package
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Deploy Changes

```bash
# 1. Commit changes
git add .
git commit -m "Describe your changes"

# 2. Push to main
git push origin main

# 3. Vercel auto-deploys
# Check deployment in Vercel dashboard
```

---

## 11. Debugging Tips

### Frontend Debugging

```javascript
// Console logging
console.log('Variable:', variable);

// React DevTools
// Install Chrome extension: React Developer Tools

// Network tab
// Check API calls in DevTools Network tab

// Performance
// DevTools → Performance tab → record
```

### Backend Debugging

```python
# Logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Variable: {variable}")

# Print statements
print("Debug:", variable)

# Breakpoints (with debugger)
import pdb
pdb.set_trace()

# Local testing
curl -X POST http://localhost:3000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"taskDescription":"test"}'
```

---

## 12. References

- [Architecture](./ARCHITECTURE.md)
- [API Spec](./API.md)
- [Database](./DATABASE.md)
- [UI/UX](./UI-UX.md)
- [Testing](./TESTING.md)
- [Deployment](./DEPLOYMENT.md)

---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026