# Find Your AI Model - API Specification

## 1. Overview

**Base URL:** `https://findyouraimodel.com/api`  
**Version:** 1.0  
**Format:** JSON  
**Authentication:** None (public API)  
**Rate Limit:** 100 requests per IP per hour

---

## 2. Endpoints

### POST /api/recommend

**Purpose:** Get AI tool recommendation for a task

#### Request
POST /api/recommend
Content-Type: application/json
{
"taskType": "content-creation",
"taskDescription": "I need to write a 5000-word research blog post with citations, data, and case studies. Conversational but authoritative tone. SEO optimized. Deadline: 2 days."
}

#### Request Parameters

| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| taskType | string | No | Optional category |
| taskDescription | string | Yes | 10-5000 characters |

#### Response (200 Success)

```json
{
  "status": "success",
  "recommendation": {
    "primary_tool": {
      "name": "Claude Sonnet",
      "provider": "Anthropic",
      "match_score": 92,
      "pricing": "$20/month",
      "context_window": 200000,
      "why_best": [
        "200K context window handles full research + citations",
        "Excellent at research synthesis and accuracy",
        "Perfect for long-form content with data"
      ],
      "capabilities": {
        "text": true,
        "image": true,
        "vision": true,
        "tool_use": true,
        "streaming": true,
        "json_mode": true
      },
      "official_link": "https://claude.ai",
      "api_link": "https://docs.anthropic.com",
      "free_tier": false,
      "maturity": "stable"
    },
    "alternatives": [
      {
        "name": "ChatGPT Plus",
        "provider": "OpenAI",
        "match_score": 78,
        "pricing": "$20/month",
        "why_alternative": "Faster responses, creative hooks, but less consistent with citations"
      },
      {
        "name": "Perplexity Pro",
        "provider": "Perplexity",
        "match_score": 65,
        "pricing": "$20/month",
        "why_alternative": "Great for research phase, but not ideal for final content creation"
      }
    ],
    "free_alternatives": [
      {
        "name": "Claude Haiku",
        "description": "Free tier, limited context (10K tokens)"
      },
      {
        "name": "GPT-4 Turbo API",
        "description": "Free credits for new users"
      }
    ],
    "cost_estimate": {
      "primary_tool": 20,
      "total_monthly": 20,
      "notes": "Other tools optional"
    },
    "workflow": {
      "step_1": "Sign up to Claude at https://claude.ai",
      "step_2": "Paste your research notes and outline",
      "step_3": "Use this prompt: 'Write a 5000-word blog post...'",
      "step_4": "Get draft in 5-10 minutes",
      "step_5": "Edit and refine (30-60 minutes)"
    },
    "decision_confidence": 95,
    "decision_time": "2 minutes"
  },
  "metadata": {
    "models_analyzed": 847,
    "processing_time": "18.5 seconds",
    "timestamp": "2024-12-28T10:30:45Z",
    "api_version": "1.0"
  }
}
```

#### Response (400 Bad Request)

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_INPUT",
    "message": "Task description too short",
    "field": "taskDescription",
    "constraint": "Minimum 10 characters required"
  }
}
```

#### Response (429 Rate Limited)

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 3600,
    "limit": "100 requests per hour per IP"
  }
}
```

#### Response (500 Server Error)

```json
{
  "status": "error",
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Failed to process recommendation",
    "request_id": "req_12345678"
  }
}
```

---

### GET /api/health

**Purpose:** Health check endpoint

#### Request
GET /api/health

#### Response (200)

```json
{
  "status": "healthy",
  "timestamp": "2024-12-28T10:30:45Z",
  "uptime_percentage": 99.9,
  "services": {
    "api": "operational",
    "airtable": "operational",
    "openrouter": "operational"
  }
}
```

---

## 3. Error Codes

| Code | HTTP | Description | User Action |
|------|------|-------------|-------------|
| INVALID_INPUT | 400 | Bad request format | Fix input and retry |
| TASK_TOO_SHORT | 400 | Task < 10 characters | Provide more details |
| TASK_TOO_LONG | 400 | Task > 5000 characters | Shorten description |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Wait and retry |
| SERVICE_UNAVAILABLE | 503 | Backend down | Try again later |
| TIMEOUT | 504 | Request too long | Retry simpler task |

---

## 4. Status Codes

| Code | Description |
|------|-------------|
| 200 | Success - recommendation returned |
| 400 | Bad request - invalid input |
| 429 | Rate limited - too many requests |
| 500 | Server error - internal error |
| 503 | Service unavailable - backend down |
| 504 | Gateway timeout - request too slow |

---

## 5. Request/Response Examples

### Example 1: Simple Task

```bash
curl -X POST https://findyouraimodel.com/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "taskType": "code-generation",
    "taskDescription": "Write Python function to sort list of dictionaries by multiple fields"
  }'
```

**Response:**
```json
{
  "status": "success",
  "recommendation": {
    "primary_tool": {
      "name": "Claude Sonnet",
      "match_score": 88,
      "why_best": ["Excellent code explanation", "Handles complex algorithms"]
    }
  }
}
```

### Example 2: Complex Task

```bash
curl -X POST https://findyouraimodel.com/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "taskDescription": "I need to create a 10,000-word comprehensive guide about AI tools for non-technical founders. Include comparison tables, case studies, pricing analysis, implementation checklists. Target: startup founders with 0 AI experience. Tone: friendly professional. Format: blog post with TOC. Deadline: 1 week."
  }'
```

**Response:**
```json
{
  "status": "success",
  "recommendation": {
    "primary_tool": {
      "name": "Claude Opus",
      "match_score": 96,
      "why_best": ["100K+ context for full guide", "Excellent structured writing", "Best reasoning for explanations"]
    }
  }
}
```

---

## 6. Rate Limiting

### Limits
Public API:
├─ 100 requests per IP per hour
├─ Resets hourly (UTC)
└─ Header: X-RateLimit-Remaining

### Response Headers
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1703757600

### Handling Rate Limits
When you receive 429:

Check X-RateLimit-Reset header
Wait specified number of seconds
Implement exponential backoff
Retry after delay


---

## 7. CORS Policy

### Allowed Origins
Production:
├─ https://findyouraimodel.com
Development:
├─ http://localhost:3000
Custom:
├─ On request (contact support)

### Allowed Methods
├─ POST (for /recommend)
├─ GET (for /health)
└─ OPTIONS (for preflight)

### Allowed Headers
├─ Content-Type
├─ Accept
└─ Authorization (future)

---

## 8. Caching Strategy

### Frontend Caching
Recommendations:
├─ Cache: 5 minutes
├─ Header: Cache-Control: public, max-age=300
└─ Browser storage: sessionStorage
Static assets:
├─ Cache: 1 hour
├─ Header: Cache-Control: public, max-age=3600
└─ CDN: Vercel global CDN

### Backend Caching
Airtable models:
├─ Cache: 5 minutes in-memory
├─ Reduces API calls
└─ Fallback: Stale cache if API fails
Recent recommendations:
├─ Deduplication: 5 minute window
├─ Same task = same recommendation
└─ Saves OpenRouter API calls

---

## 9. API Client Libraries

### JavaScript Example

```javascript
async function getRecommendation(task) {
  const response = await fetch('https://findyouraimodel.com/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      taskDescription: task
    })
  });
  
  const data = await response.json();
  return data;
}
```

### Python Example

```python
import requests

def get_recommendation(task):
    response = requests.post(
        'https://findyouraimodel.com/api/recommend',
        json={'taskDescription': task}
    )
    return response.json()
```

---

## 10. Deprecation Policy

### Version Management
Current: v1 (active)
Deprecated: None
Sunset: Future versions after 6 months notice

### Process
When deprecating endpoint:

Announce 6 months before sunset
Provide migration guide
Support both versions during overlap
Retire old version
Archive documentation


---

## 11. SLA & Support

### Service Level Agreement
Uptime: 99.9% (36 min downtime/month)
Response Time:
├─ 95th percentile: < 30 seconds
├─ 99th percentile: < 60 seconds
└─ Average: < 20 seconds
Support:
├─ Issues: GitHub Issues
├─ Email: support@findyouraimodel.com
└─ Response: Within 24 hours

---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026