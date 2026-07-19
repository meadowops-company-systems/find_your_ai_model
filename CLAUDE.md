# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Find Your AI Model (FYAIM)** - A web application helping users choose the right AI tool for their specific tasks. Built with React frontend + Python backend (Vercel Serverless), using Airtable as the database and OpenRouter Llama 2 70B for AI recommendations.

## Key Commands

### Frontend (React 18 + Tailwind CSS)
```bash
cd frontend
npm install
npm start        # Dev server at localhost:3000
npm run build   # Production build
npm test        # Run tests
```

### Backend (Python + Vercel Serverless)
```bash
cd api
pip install -r requirements.txt
vercel dev                              # Local development
pytest tests/backend/                   # Run backend tests
curl -X POST http://localhost:3000/api/recommend -H "Content-Type: application/json" -d '{"taskDescription":"Write a blog post"}'
```

### Deploy
```bash
git push origin main  # Auto-deploys to Vercel
```

## Architecture

```
Frontend (React) ──HTTPS POST──> Backend (Python/Vercel)
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                                       ▼
              Airtable (DB)                           OpenRouter
              800+ models                              Llama 2 70B
              Read-only                                Free API
```

- **Frontend**: React 18, Tailwind CSS, JavaScript/JSX
- **Backend**: Python 3.10+, Vercel Serverless Functions
- **Database**: Airtable (800+ AI models, read-only)
- **AI**: OpenRouter Llama 2 70B (free tier)

## Critical Rules

1. **NO AGENT CODE** - Agent is a separate project. FYAIM only reads from Airtable.
2. **STATELESS BACKEND** - No user sessions, no stored state. Every request is independent.
3. **AIRTABLE AS SOURCE OF TRUTH** - All model data in Airtable, never hardcode model data.
4. **ZERO COST FIRST** - Use free tiers (OpenRouter free Llama 2, Airtable free 1000 records, Vercel free tier).
5. **All secrets in .env** - Never hardcode API keys or secrets.

## Project Structure

```
find-your-ai-model/
├── frontend/          # React app (src/components/, src/pages/, src/api/)
├── api/               # Python serverless functions
│   ├── recommend.py   # Main API endpoint
│   ├── airtable_client.py
│   ├── openrouter_client.py
│   └── utils/
├── docs/              # Full documentation (README, PRD, SRS, ARCHITECTURE, etc.)
├── tests/
└── .github/workflows/
```

## Full Documentation

Detailed documentation is in the `docs/` folder:
- `docs/README.md` - Project overview
- `docs/CLAUDE.md` - Complete development guide (comprehensive version)
- `docs/architecture.md` - System design details
- `docs/api.md` - API specification
- `docs/database.md` - Airtable schema
- `docs/ui-ux.md` - Design system
- `docs/testing.md` - Testing strategy
- `docs/deployment.md` - Deployment guide
