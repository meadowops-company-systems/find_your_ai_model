# Find Your AI Model - Database Schema

## 1. Database Information

| Property | Value |
|----------|-------|
| **Type** | Airtable (Cloud Database) |
| **Purpose** | Store 800+ AI models with complete specifications |
| **Access** | REST API (read-only from FYAIM) |
| **Records** | 800+ AI models |
| **Storage** | ~5-10 MB |
| **Update** | External agent (daily) |
| **FYAIM Role** | Read-only queries |

---

## 2. Entity-Relationship Overview
Airtable Base: "AI Models Database"
└─ Table: "AI Models" (800+ records)
├─ Primary Key: Model Name
├─ All fields read-only from FYAIM
└─ Updated daily by external agent

---

## 3. AI Models Table - Field Definitions

### Core Information Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Model Name | Text | Yes | Primary key (e.g., "Claude Sonnet") |
| Provider | Text | Yes | Company (e.g., "Anthropic", "OpenAI") |
| Status | Single Select | Yes | active, beta, deprecated, coming_soon |

### Capability Fields

| Field | Type | Description |
|-------|------|-------------|
| Primary Category | Single Select | Text, Image, Video, Code, Audio, Search |
| Supported Modalities | Multi-Select | text, image, audio, video, tool_use, vision |
| Capabilities | Multi-Select | streaming, json_mode, vision, tool_use |
| Vision Capability | Checkbox | Can process images |
| Audio Capability | Checkbox | Can process audio |
| Tool Use | Checkbox | Supports function calling |
| Streaming Support | Checkbox | Supports streaming responses |
| JSON Mode | Checkbox | Can force JSON output |
| Custom Instructions | Checkbox | Supports system prompts |

### Pricing Fields

| Field | Type | Description |
|-------|------|-------------|
| Pricing Type | Single Select | free, freemium, paid, open_source |
| Monthly Price USD | Number | Cost per month (null if free) |
| Input Token Price | Number | Cost per 1M input tokens |
| Output Token Price | Number | Cost per 1M output tokens |
| Free Tier Limit | Text | Limitations of free tier |

### Technical Specifications

| Field | Type | Description |
|-------|------|-------------|
| Context Window | Number | Max input tokens (e.g., 200000) |
| Max Output Size | Number | Max output tokens (e.g., 4096) |
| Input Format | Text | Accepted formats |
| Output Format | Text | Response formats |
| Rate Limit | Text | Requests per minute/hour |
| Authentication Type | Text | api_key, oauth, service_account |
| API Stability | Single Select | experimental, beta, stable, legacy |
| Supported Parameters | Text | temperature, top_p, etc. |

### Performance & Quality

| Field | Type | Description |
|-------|------|-------------|
| Benchmark Score | Number | Performance on benchmarks (0-100) |
| Speed Rating | Single Select | very_fast, fast, medium, slow |
| Quality Rating | Single Select | very_high, high, medium, low |
| Accuracy Percentage | Percent | Benchmark accuracy (0-100%) |
| Latency ms | Number | Average response time in milliseconds |

### Business Logic

| Field | Type | Description |
|-------|------|-------------|
| Best For | Multi-Select | content_writing, code, image_gen, research |
| Strengths | Long Text | Key advantages (comma-separated) |
| Weaknesses | Long Text | Key limitations (comma-separated) |
| Maturity | Single Select | new, beta, stable, mature, legacy |
| For Enterprise | Checkbox | Suitable for enterprise use |
| For Startups | Checkbox | Good for bootstrapped teams |

### Data Management

| Field | Type | Description |
|-------|------|-------------|
| Data Source | Single Select | openrouter, huggingface, official, custom |
| Source URL | URL | Link to official source |
| Official API Docs | URL | API documentation |
| GitHub Repository | URL | Open-source repository |
| Launch Date | Date | Release date (YYYY-MM-DD) |
| Last Updated | Date | Auto-updated timestamp |
| Notes | Long Text | Additional information |

---

## 4. Sample Record

```json
{
  "Model Name": "Claude Sonnet",
  "Provider": "Anthropic",
  "Status": "active",
  "Primary Category": "Text",
  "Supported Modalities": ["text", "image", "vision"],
  "Pricing Type": "paid",
  "Monthly Price USD": 20,
  "Input Token Price": 0.003,
  "Output Token Price": 0.015,
  "Context Window": 200000,
  "Max Output Size": 4096,
  "Strengths": "Long-form reasoning, citations, code explanation, data synthesis",
  "Weaknesses": "No real-time data, slightly slower than GPT-4",
  "Best For": ["content_writing", "code_review", "analysis", "research"],
  "Capabilities": ["streaming", "json_mode", "vision", "tool_use"],
  "Maturity": "stable",
  "For Enterprise": true,
  "For Startups": true,
  "Benchmark Score": 92,
  "Speed Rating": "fast",
  "Quality Rating": "very_high",
  "Accuracy Percentage": 92,
  "Latency ms": 800,
  "Data Source": "openrouter",
  "Launch Date": "2024-06-20",
  "Last Updated": "2024-12-28",
  "Vision Capability": true,
  "Audio Capability": false,
  "Tool Use": true,
  "JSON Mode": true,
  "Streaming Support": true,
  "Custom Instructions": true
}
```

---

## 5. Field Validation Rules

### Required Fields
Must always be populated:
├─ Model Name (unique, primary key)
├─ Provider (company name)
├─ Status (active/beta/deprecated)
├─ Primary Category (for filtering)
├─ Pricing Type (free/paid/freemium)
├─ Data Source (where data came from)
└─ Last Updated (timestamp)

### Conditional Rules
If Pricing Type = "free":
├─ Monthly Price = 0 or null
├─ Input Token Price = 0 or null
└─ Output Token Price = 0 or null
If Pricing Type = "paid":
├─ Monthly Price > 0 OR (Input Token Price > 0)
└─ Must have pricing info
If Status = "deprecated":
├─ Mark why (in Notes)
└─ May hide from recommendations
If Context Window populated:
├─ Must be > 0
├─ Must be < 1,000,000
└─ Represents token count

### Format Validation
Date fields:
├─ Format: YYYY-MM-DD
├─ Must be valid date
└─ Cannot be future date
URL fields:
├─ Must start with http:// or https://
├─ Must be accessible
└─ Should link to official source
Number fields:
├─ Input Token Price: 0.0001 - 1.0
├─ Context Window: 1 - 1,000,000
└─ Accuracy %: 0 - 100

---

## 6. Data Access Patterns

### FYAIM Access Pattern
Read Operation:
GET all 800+ models from Airtable
├─ Include all fields
├─ No filtering (backend does filtering)
├─ Cache result (5 min TTL)
└─ Handle API failures gracefully
Query Example:
SELECT * FROM "AI Models"
WHERE Status = "active"
ORDER BY Last Updated DESC

### Backend Processing

Check cache (5 min TTL)
If hit: Return cached data
If miss:
├─ Query Airtable API
├─ Parse all fields
├─ Cache for 5 minutes
└─ Return to caller


---

## 7. Data Consistency

### No Duplicates
Unique constraints:
└─ Model Name must be unique
├─ "Claude Sonnet" only once
├─ Case-sensitive
└─ Primary key enforcement

### Data Integrity
Referential integrity:
├─ All URLs must be valid (if populated)
├─ Dates must be valid
├─ Numbers must be positive (if applicable)
└─ Selects must match predefined options

### Business Logic Consistency
Price consistency:
├─ If free: price = 0
├─ If paid: price > 0
└─ If freemium: both free + paid options
Capability consistency:
├─ If Vision = true: modalities include "image"
├─ If Audio = true: modalities include "audio"
└─ If Tool Use = true: capabilities include "tool_use"
Status consistency:
├─ Only active tools in recommendations
├─ Beta tools shown with warning
└─ Deprecated tools excluded

---

## 8. Backend Query Implementation

### Python Example

```python
def fetch_models_from_airtable():
    """
    Fetch all models from Airtable
    Implements caching (5 min TTL)
    """
    cache_key = "airtable_models"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Query Airtable
    response = requests.get(
        f"https://api.airtable.com/v0/{BASE_ID}/AI%20Models",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    if response.status_code != 200:
        # Use stale cache if available
        return cache.get(cache_key, stale=True)
    
    models = response.json()['records']
    
    # Cache for 5 minutes
    cache.set(cache_key, models, ttl=300)
    
    return models
```

---

## 9. Data Lifecycle

### Creation
External agent creates records:
├─ Fetches from 4 sources
├─ Deduplicates
├─ Creates new Airtable records
└─ Sets Last Updated timestamp

### Updates
External agent updates records:
├─ Checks pricing changes
├─ Updates benchmarks
├─ Adds new capabilities
└─ Updates Last Updated timestamp

### Deletion
Records marked deprecated, not deleted:
├─ Status → "deprecated"
├─ Kept for historical record
├─ Excluded from recommendations
└─ Last Updated → current date

---

## 10. Disaster Recovery

### Data Backup
Airtable built-in:
├─ Automatic daily snapshots
├─ Version history (30 days)
├─ Manual exports available
└─ Recoverable at any time
FYAIM backup:
├─ GitHub repository
├─ Weekly export of Airtable data
└─ Stored as CSV or JSON

### Recovery Procedure
If data is corrupted:

Identify issue
Use Airtable version history
Restore to known good state
Update FYAIM cache
Verify recommendations

If Airtable unavailable:

Use 5-min cache if available
Show warning to users
Alert ops team
Monitor for recovery


---

## 11. Performance Optimization

### Indexing Strategy
Critical indexes:
├─ Model Name (primary key)
├─ Status (frequent filtering)
├─ Primary Category (recommendations)
└─ Last Updated (caching invalidation)

### Query Optimization
Best practices:
├─ Fetch all at once (not paginated)
├─ Cache aggressively (5 min)
├─ Filter in backend (not Airtable)
├─ No N+1 queries
└─ Batch updates (not per-record)

---

**Document Version:** 1.0  
**Status:** Final  
**Last Updated:** May 31, 2026
