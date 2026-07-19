# Find Your AI Model - Architecture Decision Records

## ADR-001: Use OpenRouter Free Models Over Claude API

**Status:** Accepted  
**Date:** 2024-12-28

### Context

Need AI for recommendations. Options:
1. Claude API ($0.01-0.05/request)
2. OpenRouter free (Llama 2 70B, $0)

Cost matters for MVP.

### Decision

Use OpenRouter Llama 2 70B (free)

### Rationale

- $0 vs $150-500/month
- Llama 2 70B is capable
- Supports MVP growth
- Can upgrade later

### Consequences

**Positive:**
- Zero API costs
- Faster profitability
- Easier investor pitch

**Negative:**
- Slightly less intelligent
- May upgrade post-launch
- Depends on OpenRouter free tier

---

## ADR-002: Airtable Over PostgreSQL

**Status:** Accepted  
**Date:** 2024-12-28

### Context

Need database for 800+ models. Options:
1. Airtable (cloud, no setup)
2. PostgreSQL (traditional DB)
3. MongoDB (document DB)

Early-stage with limited DevOps.

### Decision

Use Airtable

### Rationale

- Zero infrastructure
- REST API included
- Non-technical updates possible
- Perfect for startup
- Simple upgrade path

### Consequences

**Positive:**
- Instant setup
- No DB administration
- Anyone can manage data

**Negative:**
- Some vendor lock-in
- Not ideal for millions of records
- Pricing increases at scale

---

## ADR-003: Vercel Serverless Over Traditional Server

**Status:** Accepted  
**Date:** 2024-12-28

### Context

Need backend hosting. Options:
1. Vercel Serverless
2. AWS EC2
3. Heroku
4. DigitalOcean

No dedicated DevOps team.

### Decision

Use Vercel Serverless

### Rationale

- Auto-scaling
- Pay-per-use ($0-100/month)
- Zero server management
- Integrated with frontend
- Fast deployments

### Consequences

**Positive:**
- No infrastructure work
- Perfect scaling
- Low ops burden

**Negative:**
- Vendor lock-in to Vercel
- Cold starts (acceptable)

---

## ADR-004: React + Tailwind For Frontend

**Status:** Accepted  
**Date:** 2024-12-28

### Context

Need frontend framework. Options:
1. React + Tailwind
2. Vue + Tailwind
3. Next.js
4. Svelte

Need fast development.

### Decision

React 18 + Tailwind CSS

### Rationale

- Largest ecosystem
- Easiest hiring
- Well-documented
- Rapid development

### Consequences

**Positive:**
- Fast development
- Large community
- Good tooling

---

## ADR-005: Read-Only Access to Airtable

**Status:** Accepted  
**Date:** 2024-12-28

### Context

FYAIM needs model data. Options:
1. Read-only from Airtable
2. Read/write access
3. Cache locally

Data populated by external agent.

### Decision

Read-only from Airtable

### Rationale

- External agent updates data
- FYAIM only reads
- No conflicts
- Clean separation
- Enables independent scaling

### Consequences

**Positive:**
- Simple architecture
- Agent independent
- No data conflicts

**Negative:**
- Can't write from FYAIM
- Daily updates sufficient

---

## ADR-006: Rate Limiting at 100 req/hour

**Status:** Accepted  
**Date:** 2024-12-28

### Context

Need API protection. Options:
1. No limits (open to abuse)
2. 100 req/hour (generous)
3. 10 req/hour (restrictive)

Balance accessibility with protection.

### Decision

100 requests per IP per hour

### Rationale

- Fair usage
- Prevents scraping
- Allows power users
- Scalable

### Consequences

**Positive:**
- Protects API
- Fair for all

**Negative:**
- Can be circumvented
- Affects power users

---

## ADR-007: No User Accounts in MVP

**Status:** Accepted  
**Date:** 2024-12-28

### Context

Users want recommendations. Options:
1. No accounts (stateless)
2. Optional accounts
3. Required accounts

MVP should be simple.

### Decision

No user accounts

### Rationale

- Reduces complexity
- No login friction
- Stateless = scales easily
- No PII = simpler privacy
- Phase 2 feature

### Consequences

**Positive:**
- Simple UX
- No auth infrastructure
- Better scaling

**Negative:**
- No saved history
- No personalization
- Users can't track usage

---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026