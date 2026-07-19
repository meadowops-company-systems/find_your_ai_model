# Find Your AI Model (FYAIM)

> The fastest way to find the perfect AI tool for your specific task.

**Status:** Production Ready  
**Version:** 1.0  
**Last Updated:** December 28, 2024

---

## 🎯 What is FYAIM?

Find Your AI Model (FYAIM) is a web application that helps users choose the right AI tool in seconds instead of hours.

**User Flow:**
1. User enters detailed task description
2. System analyzes using Llama 2 AI
3. Shows best matching AI tool with alternatives
4. User can book $100 implementation audit

**Technology:**
- Frontend: React 18 + Tailwind CSS
- Backend: Python + Vercel Serverless
- Database: Airtable (800+ AI models)
- AI Model: OpenRouter Llama 2 70B (free)

---

## 📂 Documentation

Start with your role:

**For Product Managers:** [PRD.md](./PRD.md)  
**For Developers:** [CLAUDE.md](./CLAUDE.md)  
**For Architects:** [ARCHITECTURE.md](./ARCHITECTURE.md)  
**For Designers:** [UI-UX.md](./UI-UX.md)  
**For QA:** [TESTING.md](./TESTING.md)  
**For DevOps:** [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🚀 Quick Start

```bash
# 1. Clone repo
git clone https://github.com/yourname/find-your-ai-model.git
cd find-your-ai-model

# 2. Frontend setup
cd frontend
npm install
npm start

# 3. Backend setup (new terminal)
cd api
pip install -r requirements.txt
vercel dev

# 4. Visit http://localhost:3000
```

---

## 📚 Document Index

| Document | Purpose | Audience |
|----------|---------|----------|
| [PRD.md](./PRD.md) | Product vision & strategy | Product managers |
| [SRS.md](./SRS.md) | Detailed specifications | Developers, QA |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design | Architects, senior devs |
| [DATABASE.md](./DATABASE.md) | Airtable schema | Database engineers |
| [API.md](./API.md) | API specification | Backend, integrations |
| [openapi.yaml](./openapi.yaml) | Machine-readable API contract | Backend, integrations |
| [CLAUDE.md](./CLAUDE.md) | Development guide | All developers |
| [UI-UX.md](./UI-UX.md) | Design system | Frontend, designers |
| [TESTING.md](./TESTING.md) | Testing strategy | QA, developers |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Deployment guide | DevOps, infrastructure |
| [DECISIONS.md](./DECISIONS.md) | Architecture decisions | Architects |
| [CHANGELOG.md](./CHANGELOG.md) | Version history | Everyone |
| [ROADMAP.md](./ROADMAP.md) | Future features | Product managers |

---

## 🏗️ Architecture (High-Level)
┌──────────────────────────────────────┐
│         Frontend (React)             │
│  Input form + Results display        │
└────────────────┬─────────────────────┘
│ API calls
▼
┌──────────────────────────────────────┐
│    Backend API (Python/Vercel)       │
│  • Validate input                    │
│  • Query Airtable                    │
│  • Call OpenRouter AI                │
│  • Format response                   │
└────────────────┬─────────────────────┘
┌───────┴──────────┐
│                  │
▼                  ▼
Airtable (DB)    OpenRouter (AI)
800+ models      Llama 2 70B
Read-only        Free API

---

## 🎯 Core Features

✅ Task input form (10-5000 characters)  
✅ AI recommendation engine  
✅ Alternative tool suggestions (2-3)  
✅ Free tool alternatives  
✅ Monthly cost estimation  
✅ Implementation workflow guidance  
✅ $100 audit booking (Calendly)  
✅ Mobile responsive design  
✅ WCAG AA accessibility  

---

## 📊 Key Metrics

| Metric | Target |
|--------|--------|
| Page Load Time | < 3 seconds |
| Recommendation Time | 15-30 seconds |
| System Uptime | 99.9% |
| User Satisfaction | 90%+ |
| Audit Conversion | 2-5% |

---

## 🛠️ Tech Stack
Frontend:
├─ React 18
├─ Tailwind CSS
├─ JavaScript/JSX
└─ Vercel (hosting)
Backend:
├─ Python 3.10+
├─ Vercel Serverless
├─ requests library
└─ JSON format
Database:
├─ Airtable (cloud)
├─ 800+ AI models
└─ REST API
External APIs:
├─ Airtable API
├─ OpenRouter API
├─ Calendly (bookings)
└─ Google Analytics

---

## 📁 Project Structure
find-your-ai-model/
├─ frontend/
│  ├─ src/components/
│  ├─ src/pages/
│  ├─ src/api/
│  ├─ package.json
│  └─ .env.example
├─ api/
│  ├─ recommend.py
│  ├─ airtable_client.py
│  ├─ openrouter_client.py
│  ├─ utils/
│  ├─ requirements.txt
│  └─ .env.example
├─ docs/
│  ├─ PRD.md
│  ├─ SRS.md
│  ├─ ARCHITECTURE.md
│  └─ ... (other docs)
├─ tests/
├─ .github/workflows/
└─ README.md (this file)

---

## 🚀 Deployment

**Frontend & Backend:** Vercel (auto-deploy from GitHub)  
**Database:** Airtable (cloud)  
**Domain:** Custom domain via Vercel

Deploy new features: Push to `main` branch → Auto-deployed in 2-5 minutes

---

## 🔐 Security

✅ HTTPS encryption  
✅ Input validation  
✅ Rate limiting (100 req/hour)  
✅ No PII stored  
✅ GDPR compliant  
✅ API keys in environment variables  

---

## 📞 Getting Help

**Questions?** Check the relevant documentation file above.

**Bug reports:** GitHub Issues  
**Feature requests:** GitHub Discussions  
**Email:** support@findyouraimodel.com  

---

## 📄 License

Find Your AI Model © 2024. All rights reserved.

---

**Last Updated:** May 31, 2026  
**Next Review:** July 31, 2026
