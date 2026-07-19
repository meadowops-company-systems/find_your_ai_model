# Find Your AI Model - Architecture Document

## 1. Introduction

Technical architecture for Find Your AI Model (FYAIM). Describes system design, components, and technology choices.

**Audience:** Architects, senior developers, DevOps  
**Scope:** Frontend, backend, database, external APIs

---

## 2. System Overview

### High-Level Architecture
┌──────────────────────────────────────────┐
│         Frontend (React 18)              │
│  Input form + Results display            │
│  Tailwind CSS + Responsive               │
└────────────────┬─────────────────────────┘
│ HTTPS REST API
│ JSON requests/responses
▼
┌──────────────────────────────────────────┐
│    Backend (Python + Vercel Serverless)  │
│  • Input validation                      │
│  • Airtable queries                      │
│  • OpenRouter AI integration             │
│  • Response formatting                   │
│  • Caching layer                         │
└────────────────┬───────────┬─────────────┘
│           │
┌───────┘           └────────┐
│                            │
▼                            ▼
Airtable                     OpenRouter
(Database)                   (AI Model)
800+ models                  Llama 2 70B
Read-only                    Free API
Cloud                        Cloud

---

## 3. Components

### Frontend Architecture
Components:
├─ App (root)
├─ Header
├─ TaskForm
│  ├─ CategorySelector
│  ├─ TaskInput
│  └─ SubmitButton
├─ RecommendationDisplay
│  ├─ PrimaryRecommendation
│  ├─ AlternativesList
│  ├─ FreeOptionsList
│  ├─ CostBreakdown
│  ├─ WorkflowSteps
│  └─ BookingButton
└─ Footer
State Management:
├─ task (string)
├─ category (string)
├─ loading (boolean)
├─ recommendation (object)
└─ error (string)
API Client:
└─ functions/
└─ recommendTool(task, category)

### Backend Architecture
Entry Points:
└─ api/recommend.py
├─ Vercel serverless function
├─ Receives POST request
└─ Returns JSON response
Core Modules:
├─ airtable_client.py
│  ├─ fetch_models() → 800+ models
│  └─ cache layer (5 min TTL)
├─ openrouter_client.py
│  ├─ call_llama_2(prompt)
│  └─ error handling
├─ recommendation_engine.py
│  ├─ analyze_task()
│  ├─ generate_scores()
│  └─ rank_tools()
└─ utils/
├─ validators.py
├─ formatters.py
└─ logger.py

---

## 4. Data Flow

### Request Flow

User enters task (Frontend)
└─ Task: "Write blog post about AI"
Frontend validates
└─ Check length (10-5000)
└─ Sanitize input
Frontend calls backend
└─ POST /api/recommend
└─ Body: {taskDescription: "..."}
Backend receives request
├─ Validate input
├─ Check rate limit
└─ Log request
Backend queries Airtable
├─ Check cache (5 min)
├─ If miss: Fetch all 800+ models
├─ Parse fields
└─ Cache result
Backend calls OpenRouter
├─ Prepare prompt
├─ Include all models
├─ Call Llama 2 70B
├─ Parse JSON response
└─ Timeout: 30 seconds
Backend formats response
├─ Add metadata
├─ Add processing time
└─ Validate structure
Backend returns JSON
└─ HTTP 200 + recommendation
Frontend receives response
└─ Parse JSON
└─ Update state
Frontend displays results
├─ Primary tool
├─ Match score
├─ Alternatives
├─ Cost
└─ Booking button

Total Time: ~15-30 seconds

---

## 5. Technology Choices

### Frontend: React 18 + Tailwind CSS

**Why?**
- Large ecosystem
- Easy hiring
- Fast development
- Excellent tooling
- Good performance

**Alternatives considered:**
- Vue (smaller community)
- Svelte (steeper learning curve)
- Next.js (overkill for MVP)

---

### Backend: Python + Vercel Serverless

**Why?**
- Python great for AI/ML work
- Vercel: zero DevOps
- Auto-scaling
- Integrated with frontend
- Pay-per-use pricing

**Alternatives considered:**
- Node.js (less ideal for AI)
- AWS Lambda (more complex)
- Traditional server (expensive)

---

### Database: Airtable

**Why?**
- Zero infrastructure
- REST API included
- 1000+ records free
- Non-technical updates
- Perfect for startup

**Why NOT PostgreSQL?**
- Requires DevOps
- More infrastructure work
- Overkill for current scale

---

### AI Model: OpenRouter Llama 2 70B (Free)

**Why?**
- Completely free
- Powerful (70B parameters)
- Good reasoning ability
- Low cost vs Claude/GPT-4
- Simple API

**Why NOT Claude API?**
- Costs $0.01-0.05/request
- Adds $150-500/month
- Overkill for MVP

---

### Hosting: Vercel

**Why?**
- Frontend + Backend in one place
- Auto-deploys from GitHub
- Auto-scaling
- Global CDN
- Free tier available

---

## 6. Caching Strategy
Frontend Caching:
├─ Static assets: 1 year
├─ API responses: 5 minutes
└─ Form state: localStorage
Backend Caching:
├─ Airtable models: 5 min in-memory
├─ Recommendation results: Deduplication
└─ Failures: Circuit breaker (1 min)
Cache Invalidation:
├─ TTL expiration (5 min)
├─ Manual on deployment
└─ Graceful fallback on miss

---

## 7. Scalability

### Current Capacity
Users: 1,000+ concurrent
Requests: 1,000+ per minute
Recommendations: 10,000+ daily
Cost: < $100/month

### Scaling Path
10K daily:
├─ Monitor CPU
├─ Upgrade Airtable if needed
└─ Cost: ~$20/month
100K daily:
├─ Add Redis cache layer
├─ Database optimization
├─ Load balancing
└─ Cost: ~$100-500/month
1M+ daily:
├─ Full infrastructure overhaul
├─ Multiple regions
├─ Advanced caching
└─ Cost: $1,000+/month

---

## 8. Security

### Data Security
HTTPS:
├─ All traffic encrypted (TLS 1.3)
├─ Vercel manages certificates
└─ Auto-renewal
API Keys:
├─ Stored in environment variables
├─ Never in code
├─ Never in logs
└─ Rotated quarterly
Input Validation:
├─ Length checks
├─ Character validation
├─ No injection prevention needed
└─ Rate limiting (100 req/hour)

### Privacy
NO PII Collected:
├─ No user accounts
├─ No email storage
├─ No task descriptions logged
└─ GDPR compliant
Analytics:
├─ Google Analytics (anonymized)
├─ Event tracking (no PII)
├─ Retention: 24 months

---

## 9. Deployment

### Pipeline
Developer pushes to main
↓
GitHub Actions runs tests
├─ Frontend tests
├─ Backend tests
└─ Linting
↓
If all pass:
├─ Deploy frontend to Vercel
├─ Deploy backend to Vercel
└─ E2E tests
↓
If all pass: LIVE! ✅
If fail: ROLLBACK ❌

### Environments

| Environment | Purpose | Auto-Deploy |
|-------------|---------|------------|
| Development | Local testing | No |
| Staging | Pre-production | On PR |
| Production | Live | On main |

---

## 10. Architecture Decisions

### ADR-001: Stateless Backend

**Decision:** No sessions, no user state  
**Benefit:** Easy horizontal scaling  
**Trade-off:** No saved recommendations (Phase 2)

### ADR-002: Read-Only Database

**Decision:** FYAIM only reads Airtable  
**Benefit:** No data conflicts, agent independent  
**Trade-off:** No real-time model updates (daily is enough)

### ADR-003: Free Models First

**Decision:** Use OpenRouter free tier  
**Benefit:** $0 API costs  
**Trade-off:** Slightly less intelligence than paid models

---

## 11. Monitoring & Observability

### Uptime Monitoring

- Service: UptimeRobot
- Endpoint: /api/health
- Interval: 5 minutes
- Alert: Email if down > 5 min

### Error Tracking

- Service: Sentry (optional)
- Captures: Errors, exceptions
- Alerts: Critical errors only

### Performance Monitoring

- Vercel Analytics (built-in)
- Metrics:
  - Response times
  - Error rates
  - Function usage
  - Bandwidth

---

## 12. Disaster Recovery

### Backup Strategy
Frontend:
├─ GitHub repo (version control)
├─ Vercel backups (deployments)
└─ Code backup in repo
Backend:
├─ GitHub repo (code)
├─ Vercel logs (history)
└─ Requirements.txt (deps)
Database:
├─ Airtable backup (built-in)
├─ Weekly manual exports
└─ GitHub archive

### Recovery Procedures
Frontend Down:

Vercel usually auto-recovers
If not: Manual redeploy

Backend Down:

Check API logs
Check Airtable connection
Redeploy if needed

Database Down:

Use Airtable recovery
Restore from backup


---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026
