import { useEffect, useMemo, useRef, useState } from 'react';
import {
  filterAlternatives,
  normalizeRecommendation,
} from './lib/phase2';

const CATEGORIES = [
  { id: 'writing', icon: '✍️', label: 'Writing & Content' },
  { id: 'coding', icon: '💻', label: 'Coding & Development' },
  { id: 'image', icon: '🎨', label: 'Image Generation' },
  { id: 'audio', icon: '🎙️', label: 'Audio & Music' },
  { id: 'video', icon: '🎬', label: 'Video & Animation' },
  { id: 'data', icon: '📊', label: 'Data & Analytics' },
  { id: 'research', icon: '🔬', label: 'Research & Learning' },
  { id: 'productivity', icon: '⚡', label: 'Productivity' },
];

const TRUST_BRANDS = ['MeadowOps'];

const STATS = [
  { value: '800+', label: 'AI tools indexed' },
  { value: '90%+', label: 'Match accuracy' },
  { value: '30 sec', label: 'Average time' },
  { value: 'Free', label: 'To start using' },
];

const DRAFT_KEY = 'fyaim.draft.v2';
const UI_KEY = 'fyaim.uiState.v2';

const BUTTON_TEXTS = [
  "Schedule Your Diagnostic",
  "Get Your Strategic Report",
  "Let's Diagnose Your Situation",
  "See Your Implementation Roadmap"
];

const CTA_VERSIONS = [
  {
    title: "YOU FOUND THE TOOL. NOW WHAT?",
    tagline: "Knowing which AI tool to use is one thing. Knowing if it's actually right for YOUR business is another.",
    preBulletsText: "A lot of founders get the tool recommendation and then:",
    bullets: [
      "Build it wrong (wastes weeks)",
      "Build the wrong thing first (costs money)",
      "Build it alone and it fails (costs time)"
    ],
    postBulletsText: "That's exactly what the AI Audit prevents.",
    mainParagraph: "One 60-minute call. We diagnose your operations. You get clarity on exactly what to build, what it costs, and what it saves.",
    decideText: "Then you decide: build with us, build yourself, or wait.",
    footer: "Ready to know if this is the right move for your business?"
  },
  {
    title: "BEFORE YOU BUILD THIS, WAIT.",
    tagline: "That tool recommendation? It's solid. But here's what most founders miss:",
    preBulletsText: "They implement it wrong because they don't know:",
    bullets: [
      "Where to start (which problem first?)",
      "What it will actually cost (budget surprised?)",
      "What results to expect (how many hours saved?)",
      "How to hand it off to their team (so it actually works)"
    ],
    postBulletsText: "One call changes that.",
    mainParagraph: "We audit your specific situation. You get a detailed report showing: Exactly what to build, the investment range, what success looks like, your 90-day roadmap.",
    decideText: "It's the difference between \"we tried AI once and it failed\" and \"we implemented AI and it changed how we work.\"",
    footer: "Ready?"
  },
  {
    title: "I BUILT THIS TOOL BECAUSE I WAS YOU.",
    tagline: "I found the right AI tool for my task. Then I realized: I had no idea how to actually implement it for my specific business.",
    preBulletsText: "So I either:",
    bullets: [
      "Wasted time trying things that didn't work",
      "Paid someone who didn't understand my operations",
      "Gave up thinking \"AI isn't for us\""
    ],
    postBulletsText: "Now I help founders avoid that.",
    mainParagraph: "One conversation. You tell me what you do, how you work, what's breaking. I tell you exactly what to build first.",
    decideText: "No long-term contracts. No pressure. Just clarity.",
    extraBulletsText: "Most founders who do this end up either:",
    extraBullets: [
      "Building with us (because they see it's the right move)",
      "Building themselves (because they have the roadmap)",
      "Waiting (because it's not the right time)"
    ],
    extraFooter: "All three are the right answer. The wrong answer is guessing."
  },
  {
    title: "YOU PICKED THE RIGHT TOOL. WRONG QUESTION IS NEXT.",
    tagline: "Before you implement, ask yourself:",
    bullets: [
      "Will this actually save me time or create more work?",
      "What's the real ROI for my business?",
      "Am I building the right system first?",
      "How do I make sure my team actually uses this?"
    ],
    postBulletsText: "Most founders answer these wrong. That costs them weeks and money. The AI Audit answers them right.",
    mainParagraph: "One call. We map your operations, identify what's broken, show you what to fix first. You get a strategic report showing exact numbers: hours saved, money freed, revenue impact.",
    decideText: "Then you build with confidence or realize it's not the move yet."
  }
];

function readStorageObject(key, fallback) {
  if (typeof window === 'undefined') return fallback;

  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return fallback;
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : fallback;
  } catch {
    return fallback;
  }
}

function writeStorageObject(key, value) {
  if (typeof window === 'undefined') return;

  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Ignore storage failures.
  }
}

function BrandMark() {
  return (
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" aria-hidden="true">
      <rect x="4" y="21" width="7" height="15" rx="2" fill="url(#b1)" />
      <rect x="15" y="13" width="7" height="23" rx="2" fill="url(#b2)" />
      <rect x="26" y="7" width="7" height="29" rx="2" fill="url(#b3)" />
      <defs>
        <linearGradient id="b1" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#7c3aed" />
          <stop offset="100%" stopColor="#c4b5fd" />
        </linearGradient>
        <linearGradient id="b2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#8b5cf6" />
          <stop offset="100%" stopColor="#ede9fe" />
        </linearGradient>
        <linearGradient id="b3" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#a78bfa" />
          <stop offset="100%" stopColor="#fff" />
        </linearGradient>
      </defs>
    </svg>
  );
}

function ScoreRing({ score }) {
  const ringRef = useRef(null);
  const numberRef = useRef(null);
  const circumference = 2 * Math.PI * 38;
  const offset = circumference - (Math.max(0, Math.min(score || 0, 100)) / 100) * circumference;

  useEffect(() => {
    const ring = ringRef.current;
    if (!ring) return undefined;

    ring.style.strokeDashoffset = `${circumference}`;
    const timer = window.setTimeout(() => {
      ring.style.strokeDashoffset = `${offset}`;
    }, 50);

    const labelTimer = window.setTimeout(() => {
      const target = Math.max(0, Math.min(score || 0, 100));
      let current = 0;
      const interval = window.setInterval(() => {
        current = Math.min(current + 3, target);
        if (numberRef.current) numberRef.current.textContent = String(current);
        if (current >= target) window.clearInterval(interval);
      }, 18);
    }, 220);

    return () => {
      window.clearTimeout(timer);
      window.clearTimeout(labelTimer);
    };
  }, [circumference, offset, score]);

  return (
    <div className="score-ring" aria-label={`Match score ${score}%`}>
      <svg width="94" height="94" viewBox="0 0 94 94" fill="none">
        <circle cx="47" cy="47" r="38" stroke="rgba(255,255,255,0.12)" strokeWidth="8" />
        <circle
          ref={ringRef}
          cx="47"
          cy="47"
          r="38"
          stroke="url(#score-grad)"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          transform="rotate(-90 47 47)"
          style={{ transition: 'stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1)' }}
        />
        <defs>
          <linearGradient id="score-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#7c3aed" />
            <stop offset="55%" stopColor="#a78bfa" />
            <stop offset="100%" stopColor="#06b6d4" />
          </linearGradient>
        </defs>
      </svg>
      <div className="score-ring__label">
        <span ref={numberRef}>0</span>
        <small>/100</small>
      </div>
    </div>
  );
}

function App() {
  const [task, setTask] = useState(() => readStorageObject(DRAFT_KEY, { task: '', category: '' }).task || '');
  const [category, setCategory] = useState(() => readStorageObject(DRAFT_KEY, { task: '', category: '' }).category || '');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [recommendation, setRecommendation] = useState(null);
  const [alternativeQuery, setAlternativeQuery] = useState(() => readStorageObject(UI_KEY, {}).alternativeQuery || '');
  const [minimumScore, setMinimumScore] = useState(() => readStorageObject(UI_KEY, {}).minimumScore || 0);
  const [priceMode, setPriceMode] = useState(() => readStorageObject(UI_KEY, {}).priceMode || 'all');
  const [ctaIndex, setCtaIndex] = useState(0);
  const [ctaButtonText, setCtaButtonText] = useState('Schedule Your Diagnostic');

  const normalized = useMemo(() => normalizeRecommendation(recommendation), [recommendation]);
  const filteredAlternatives = useMemo(
    () => filterAlternatives(normalized.alternatives, { query: alternativeQuery, minScore: minimumScore, priceMode }),
    [normalized.alternatives, alternativeQuery, minimumScore, priceMode],
  );
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';
  const auditUrl = 'https://meadowops.tech/audit';
  const canSubmit = task.trim().length >= 10 && !loading;

  useEffect(() => {
    writeStorageObject(DRAFT_KEY, { task, category });
  }, [task, category]);

  useEffect(() => {
    writeStorageObject(UI_KEY, {
      alternativeQuery,
      minimumScore,
      priceMode,
    });
  }, [alternativeQuery, minimumScore, priceMode]);

  useEffect(() => {
    let interval = null;

    if (loading) {
      interval = window.setInterval(() => {
        setProgress((value) => Math.min(value + 7, 90));
      }, 220);
    }

    return () => {
      if (interval) window.clearInterval(interval);
    };
  }, [loading]);

  const handleSubmit = async () => {
    if (!canSubmit) return;

    setLoading(true);
    setError('');
    setRecommendation(null);
    setProgress(0);

    try {
      const response = await fetch(`${apiUrl}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          taskDescription: task.trim(),
          category,
        }),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(data?.message || 'Failed to get recommendation');
      }

      setProgress(100);
      setRecommendation(data);
      setCtaIndex((prev) => {
        let next = Math.floor(Math.random() * CTA_VERSIONS.length);
        while (next === prev && CTA_VERSIONS.length > 1) {
          next = Math.floor(Math.random() * CTA_VERSIONS.length);
        }
        return next;
      });
      setCtaButtonText((prev) => {
        const available = BUTTON_TEXTS.filter(t => t !== prev);
        if (available.length === 0) return prev;
        return available[Math.floor(Math.random() * available.length)];
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
      window.setTimeout(() => setProgress(0), 450);
    }
  };

  return (
    <>
      <div className="background">
        <div className="background__grid" />
        <div className="background__orb background__orb--one" />
        <div className="background__orb background__orb--two" />
        <div className="background__orb background__orb--three" />
      </div>

      <div className="shell">
        <header className="topbar">
          <div className="brand">
            <BrandMark />
            <div>
              <div className="brand__title">FYAIM</div>
              <div className="brand__subtitle">Find Your AI Model</div>
            </div>
          </div>
          <a className="ghost-button" href={auditUrl} target="_blank" rel="noreferrer">
            Get Clarity
          </a>
        </header>

        <main className="main-grid">
          <section className="hero-card panel">
            <div className="eyebrow">800+ AI models · live data · free to use</div>
            <h1>
              Find the perfect AI tool
              <span>for your task</span>
            </h1>
            <p className="hero-copy">
              Describe exactly what you need. We analyze the live model database and surface the best match with clear reasoning.
            </p>

            <div className="stats">
              {STATS.map((item) => (
                <div key={item.label} className="stat-card">
                  <strong>{item.value}</strong>
                  <span>{item.label}</span>
                </div>
              ))}
            </div>

            <div className="trust-row">
              <span>Trusted by teams at</span>
              {TRUST_BRANDS.map((brand) => (
                <strong key={brand}>{brand}</strong>
              ))}
            </div>
          </section>

          <section className="panel form-card">
            <div className="section-head">
              <div>
                <p className="section-label">Task Category</p>
                <h2>Refine your search</h2>
              </div>
              <span className="muted">Optional</span>
            </div>

            <div className="category-grid">
              {CATEGORIES.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  className={`category-pill${category === item.id ? ' is-active' : ''}`}
                  onClick={() => setCategory((current) => (current === item.id ? '' : item.id))}
                >
                  <span>{item.icon}</span>
                  {item.label}
                </button>
              ))}
            </div>

            <div className="divider" />

            <div className="section-head section-head--tight">
              <div>
                <p className="section-label">Describe Your Task</p>
                <h2>What do you want to achieve?</h2>
              </div>
              <span className={`count${task.trim().length >= 10 ? ' is-ready' : ''}`}>
                {task.trim().length} / 5000
              </span>
            </div>

            <textarea
              className="task-input"
              rows={8}
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="Example: I need a 5,000-word research blog post about AI productivity tools in 2025. Include real statistics, citations, SEO headings, and a conversational-yet-authoritative tone."
            />

            {task.trim().length > 0 && task.trim().length < 10 && (
              <div className="inline-error">Please enter at least 10 characters.</div>
            )}

            <button className="primary-button" type="button" onClick={handleSubmit} disabled={!canSubmit}>
              {loading ? 'Analyzing your task...' : 'Find My AI Tool'}
            </button>

            {loading && (
              <div className="progress-block">
                <div className="progress-copy">
                  <span>{progress < 35 ? 'Fetching models...' : progress < 70 ? 'Ranking matches...' : 'Finalizing recommendation...'}</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar__fill" style={{ width: `${progress}%` }} />
                </div>
              </div>
            )}

            {error && <div className="error-banner">{error}</div>}
          </section>
        </main>

        <section className="results-layout">
          <div className="panel results-panel">
            <div className="section-head">
              <div>
                <p className="section-label">Recommendation</p>
                <h2>Best match for your task</h2>
              </div>
              {normalized.processingTime !== null && (
                <span className="muted">Generated in {normalized.processingTime}ms</span>
              )}
            </div>

            {normalized.primary ? (
              <>
                <div className="primary-card">
                  <div className="primary-card__top">
                     <div className="primary-badge">Primary recommendation</div>
                    <ScoreRing score={normalized.primary.score} />
                  </div>

                  <div className="primary-info">
                    <div className="primary-logo">{normalized.primary.logo}</div>
                    <div>
                      <h3>{normalized.primary.name}</h3>
                      <p>{normalized.primary.provider}</p>
                    </div>
                  </div>

                  {normalized.primary.description && <p className="primary-description">{normalized.primary.description}</p>}

                  {normalized.primary.reasons.length > 0 && (
                    <div className="reason-list">
                      {normalized.primary.reasons.slice(0, 3).map((reason) => (
                        <div key={reason} className="reason-item">
                          <span>✓</span>
                          <p>{reason}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {normalized.primary.caps.length > 0 && (
                    <div className="cap-list">
                      {normalized.primary.caps.slice(0, 6).map((cap) => (
                        <span key={String(cap)} className="cap-chip">
                          {String(cap)}
                        </span>
                      ))}
                    </div>
                  )}

                  <div className="price-row">
                    <div>
                      <strong>{normalized.primary.price}</strong>
                      {normalized.primary.context ? <span>{normalized.primary.context}</span> : null}
                    </div>
                    {normalized.primary.website ? (
                      <a className="ghost-button" href={normalized.primary.website} target="_blank" rel="noreferrer">
                        Visit website
                      </a>
                    ) : null}
                  </div>
                </div>

                {normalized.primary.workflow.length > 0 && (
                  <div className="workflow-card">
                    <h4>How to use it</h4>
                    <ol>
                      {normalized.primary.workflow.slice(0, 5).map((step) => (
                        <li key={step}>{step}</li>
                      ))}
                    </ol>
                  </div>
                )}

                <div className="audit-card">
                  <div className="audit-content">
                    <p className="section-label">Tailored AI Audit</p>
                    <h3 className="audit-title">{CTA_VERSIONS[ctaIndex].title}</h3>
                    
                    <p className="audit-tagline">{CTA_VERSIONS[ctaIndex].tagline}</p>
                    
                    {CTA_VERSIONS[ctaIndex].preBulletsText && (
                      <p className="audit-pre-bullets">{CTA_VERSIONS[ctaIndex].preBulletsText}</p>
                    )}
                    
                    {CTA_VERSIONS[ctaIndex].bullets && (
                      <ul className="audit-bullets">
                        {CTA_VERSIONS[ctaIndex].bullets.map((b, idx) => (
                          <li key={idx}>{b}</li>
                        ))}
                      </ul>
                    )}
                    
                    {CTA_VERSIONS[ctaIndex].postBulletsText && (
                      <p className="audit-post-bullets">{CTA_VERSIONS[ctaIndex].postBulletsText}</p>
                    )}
                    
                    <p className="audit-paragraph">{CTA_VERSIONS[ctaIndex].mainParagraph}</p>
                    
                    {CTA_VERSIONS[ctaIndex].decideText && (
                      <p className="audit-decide">{CTA_VERSIONS[ctaIndex].decideText}</p>
                    )}
                    
                    {CTA_VERSIONS[ctaIndex].extraBulletsText && (
                      <p className="audit-pre-bullets">{CTA_VERSIONS[ctaIndex].extraBulletsText}</p>
                    )}
                    {CTA_VERSIONS[ctaIndex].extraBullets && (
                      <ul className="audit-bullets">
                        {CTA_VERSIONS[ctaIndex].extraBullets.map((b, idx) => (
                          <li key={idx}>{b}</li>
                        ))}
                      </ul>
                    )}
                    {CTA_VERSIONS[ctaIndex].extraFooter && (
                      <p className="audit-extra-footer">{CTA_VERSIONS[ctaIndex].extraFooter}</p>
                    )}
                    
                    {CTA_VERSIONS[ctaIndex].footer && (
                      <p className="audit-footer">{CTA_VERSIONS[ctaIndex].footer}</p>
                    )}
                  </div>
                  
                  <div className="audit-action">
                    <a className="primary-button" href={auditUrl} target="_blank" rel="noreferrer">
                      {ctaButtonText}
                    </a>
                  </div>
                </div>
              </>
            ) : (
              <div className="empty-state">
                <h3>Your result will appear here</h3>
                <p>Enter a detailed task and generate a recommendation to see the best AI tool, alternatives, and workflow steps.</p>
              </div>
            )}
          </div>

          <aside className="side-stack">
            <div className="panel side-panel">
              <div className="section-head section-head--tight">
                <div>
                  <p className="section-label">Alternatives</p>
                  <h2>Other strong options</h2>
                </div>
              </div>

              <div className="control-row">
                <input
                  className="mini-input"
                  value={alternativeQuery}
                  onChange={(e) => setAlternativeQuery(e.target.value)}
                  placeholder="Search models..."
                />
                <select className="mini-select" value={priceMode} onChange={(e) => setPriceMode(e.target.value)}>
                  <option value="all">All prices</option>
                  <option value="free">Free only</option>
                  <option value="paid">Paid only</option>
                </select>
                <select className="mini-select" value={minimumScore} onChange={(e) => setMinimumScore(Number(e.target.value))}>
                  <option value="0">All scores</option>
                  <option value="50">50+</option>
                  <option value="70">70+</option>
                  <option value="85">85+</option>
                </select>
              </div>

              {filteredAlternatives.length > 0 ? (
                <div className="alt-list">
                  {filteredAlternatives.slice(0, 3).map((alt, idx) => (
                    <div key={`${alt.name}-${alt.provider}-${idx}`} className="alt-card">
                      <div className="alt-card__row">
                        <div>
                          <h4>{alt.name}</h4>
                          <p>{alt.provider}</p>
                        </div>
                        <strong>{alt.score}%</strong>
                      </div>
                      <div className="progress-bar progress-bar--thin">
                        <div className="progress-bar__fill" style={{ width: `${Math.max(0, Math.min(alt.score, 100))}%` }} />
                      </div>
                      {alt.reason ? <p className="alt-reason">{alt.reason}</p> : null}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="muted">Alternatives will show after a recommendation is generated.</p>
              )}
            </div>

            <div className="panel side-panel side-panel--accent">
              <p className="section-label">Why FYAIM</p>
              <h2>Clear, fast, and data-backed</h2>
              <ul className="feature-list">
                <li>Live Airtable model database</li>
                <li>Transparent recommendation reasoning</li>
                <li>Free-tier-first AI selection</li>
                <li>Implementation support when needed</li>
              </ul>
            </div>
          </aside>
        </section>
      </div>
    </>
  );
}

export default App;
