# Find Your AI Model - Deployment Guide

## 1. Deployment Overview

**Platform:** Vercel (Frontend + Backend)  
**Database:** Airtable (Cloud)  
**Target:** Production  
**Uptime:** 99.9%

---

## 2. Prerequisites
Required:
├─ GitHub account
├─ Vercel account (free)
├─ Airtable account (configured)
├─ All tests passing
└─ Environment variables ready
Optional:
├─ Custom domain
├─ CDN (Vercel included)
└─ Monitoring tools

---

## 3. Environment Setup

### Production Variables

**Backend (.env.production)**
AIRTABLE_API_KEY=your_airtable_key
AIRTABLE_BASE_ID=your_base_id
OPENROUTER_API_KEY=optional_if_paying
DEBUG=False
LOG_LEVEL=INFO

**Frontend (.env.production)**
REACT_APP_API_URL=https://findyouraimodel.com/api
REACT_APP_CALENDLY_URL=https://calendly.com/your-name

### Configure Vercel

Go to Vercel Dashboard
Select Project
Settings → Environment Variables
Add variables (from .env.production)
Select: Production environment
Save


---

## 4. Deployment Steps

### Step 1: Frontend Deployment

```bash
# Push code
git add .
git commit -m "Deploy frontend v1.0"
git push origin main

# Vercel auto-deploys (2-5 minutes)
# Check: https://findyouraimodel.com
```

### Step 2: Backend Deployment

```bash
# Deployed automatically with frontend
# Test endpoint:
curl -X POST https://findyouraimodel.com/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"taskDescription":"Write a blog post"}'

# Should return recommendation within 30 seconds
```

### Step 3: Verify Production

```bash
# Frontend loads
curl https://findyouraimodel.com

# API responds
curl https://findyouraimodel.com/api/health

# End-to-end test
Visit https://findyouraimodel.com
Enter task → Get recommendation
Book audit works
```

---

## 5. CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: cd frontend && npm install && npm test
      - uses: actions/setup-python@v2
      - run: cd api && pip install -r requirements.txt && pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          production: true

  verify:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - run: curl -f https://findyouraimodel.com/api/health
      - run: curl -f -X POST https://findyouraimodel.com/api/recommend \
              -H "Content-Type: application/json" \
              -d '{"taskDescription":"Test"}'
```

---

## 6. Database Setup (Airtable)

### Initial Setup

Create Airtable Base
Visit: airtable.com
Create base: "AI Models Database"
Create Table: "AI Models"
See DATABASE.md for field details
Generate API Key
Account Settings → Tokens
Create token with data.records:read
Get Base ID
Share → Copy base link
Extract: appXXXXXXXXXXXXXX


### Load Data

```bash
# Option 1: Manual (slow)
# Airtable UI → Add records

# Option 2: Script (fast)
python scripts/load_models.py

# Option 3: CSV Import
# 1. Prepare CSV
# 2. Airtable → Import
# 3. Map columns
```

---

## 7. Monitoring & Alerts

### Uptime Monitoring
Service: UptimeRobot (free)
Setup:

Visit: uptimerobot.com
Add monitor
URL: https://findyouraimodel.com/api/health
Interval: 5 minutes
Alert: Email if down > 5 min


### Error Logging
Service: Sentry (free tier)
Setup:

Create account
Create project
Add to backend:
import sentry_sdk
sentry_sdk.init("YOUR_DSN")
Errors auto-tracked


### Performance Monitoring
Vercel Analytics (built-in):

Dashboard → Analytics
Monitor:
├─ Response times
├─ Error rates
├─ Function usage
└─ Bandwidth


---

## 8. Scaling

### Current Capacity
Users: 1,000+ concurrent
Requests: 1,000+ per minute
Daily: 10,000+ recommendations
Cost: < $100/month

### Scaling Path
10K daily:
├─ Monitor metrics
├─ Upgrade Airtable if needed
└─ Cost: ~$20/month
100K daily:
├─ Add cache layer
├─ Database optimization
└─ Cost: ~$100-500/month
1M+ daily:
├─ Multi-region deployment
├─ Full infrastructure overhaul
└─ Cost: $1,000+/month

---

## 9. Rollback Procedure

### Quick Rollback
Option A: Revert commit

git revert <commit-hash>
git push origin main
Vercel auto-redeploys

Option B: Vercel dashboard

Vercel Dashboard
Deployments
Click previous deployment
Promote to Production


---

## 10. Post-Deployment Checklist

### Immediate (5 min)
☐ Homepage loads
☐ No console errors
☐ API health check passes
☐ Recommendation works
☐ Booking redirects to Calendly

### Short-term (1 hour)
☐ Monitor error logs
☐ Check analytics
☐ Monitor Airtable quota
☐ Verify uptime monitor

### Long-term (24 hours)
☐ Review performance
☐ Check user feedback
☐ Verify no data issues
☐ Monitor costs

---

## 11. Security Checklist
Before Deployment:
☐ No secrets in code
☐ All .env files excluded
☐ API keys rotated
☐ Database access restricted
☐ HTTPS enabled
☐ Rate limiting configured
☐ Input validation enabled
☐ CORS properly set
☐ Error messages safe
☐ Monitoring enabled
☐ Logs configured
☐ Alerts set up
☐ Database backed up
☐ No PII stored
☐ GDPR compliant

---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026