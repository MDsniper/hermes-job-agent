# Architecture: Hermes Autonomous Job Agent

## System Overview

The Hermes Autonomous Job Agent is a cron-driven AI pipeline that automates the full job search lifecycle: discovery → filtering → assessment → resume/cover letter generation → application submission → storage → notification.

It runs on the Hermes Agent platform, a CLI-based AI agent framework by Nous Research. Each cron tick spawns a fresh agent session with a self-contained prompt and loaded skills.

## Component Architecture

```
                        ┌──────────────────────┐
                        │   Hermes Cron Engine  │
                        │   (systemd timer)     │
                        └──────────┬───────────┘
                                   │ fires every 6 hours
                        ┌──────────▼───────────┐
                        │   Agent Session       │
                        │   ┌────────────────┐  │
                        │   │ Prompt (6-step) │  │
                        │   │ Skill: job-     │  │
                        │   │ search-toolkit  │  │
                        │   │ Model: MiniMax  │  │
                        │   └────────────────┘  │
                        └──────────┬───────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
  ┌───────▼────────┐    ┌─────────▼──────────┐   ┌─────────▼──────────┐
  │  PHASE 1       │    │  PHASE 2-4         │   │  PHASE 5-6         │
  │  Discovery     │    │  Processing        │   │  Storage & Notify  │
  │                │    │                    │   │                    │
  │ • web_search   │    │ • web_extract      │   │ • Nextcloud WebDAV │
  │ • AnySearch    │    │ • web_search       │   │ • AgentMail email  │
  │   fallback     │    │   (company info)   │   │ • Telegram digest  │
  │ • Rotate query │    │ • Fit evaluation   │   │ • Application log  │
  │   patterns     │    │ • Resume generation│   │                    │
  │                │    │ • Cover letter     │   │                    │
  │                │    │ • WeasyPrint PDF   │   │                    │
  └────────────────┘    └────────────────────┘   └────────────────────┘
```

## Phase 1: Discovery

### Search Strategy

The agent runs 8-10 web search queries per run, rotating through different title-location combinations to avoid seeing the same postings repeatedly.

**Title rotation (any of these per query):**
- CIO / Chief Information Officer
- IT Director / Director of Information Technology
- VP of IT / VP Technology / Vice President Technology
- Senior Director IT / Senior Director Technology
- Assistant CIO / Associate CIO
- Director AI / Head of AI / AI Director
- Director Digital Transformation
- Data Center Director / Director Data Center Operations
- Director of Infrastructure / Infrastructure Engineering Director
- Senior Manager IT Operations / IT Engineering Manager

**Location rotation (one per query):**
- Washington DC / DC metro
- Baltimore MD / Baltimore metro
- Northern Virginia (Tysons, Reston, Ashburn, McLean, Fairfax)
- Frederick MD / Hagerstown MD
- Bethesda / Rockville / Silver Spring MD
- Harrisburg PA / York PA / Lancaster PA
- Annapolis MD / Columbia MD
- Remote (DC/Baltimore preference)

### Search Tool Stack

```
Primary:    web_search  →  Tavily API (aggregates LinkedIn, Indeed, Glassdoor, etc.)
Fallback:   AnySearch CLI → python3 anysearch_cli.py search "<query>"
Extraction: web_extract → reads job posting page content (LinkedIn blocked)
            browser     → Chrome DevTools Protocol for LinkedIn (dismiss sign-in, extract via JS)
```

### Deduplication

The agent tracks previously processed URLs across runs by checking Nextcloud folder names. Jobs already in `Job-Applications/<company>_<role>/` are skipped.

## Phase 2: Filtering

### Hard Exclusions (Blocked)

| Category | Reason |
|----------|--------|
| Federal/USAJobs.gov | Requires login.gov + lengthy process |
| Active security clearance | Candidate doesn't hold any |
| Contract/1099-only | W-2 preferred |
| Below $160K salary | Below target band |
| Outside 80-mile radius | From Frederick, MD |
| WordPress positions | Not relevant |
| Pure software engineering | Code-heavy, not leadership |

### AI Preference (Soft Filter)

Roles with AI responsibilities are ranked HIGHER in the digest. Roles without AI that otherwise fit are still included but ranked lower. AI keywords watched for:

- AI strategy, AI governance, AI adoption, AI transformation
- Machine learning, ML, generative AI, GenAI
- Agentic systems, automation, intelligent automation
- Copilot, LLM, large language model, neural network
- Data science, predictive analytics, cognitive computing

## Phase 3: Assessment

### Job Posting Extraction

LinkedIn blocks web_extract. The agent falls back to browser-based extraction:

```javascript
// 1. Navigate to LinkedIn job URL
// 2. Dismiss sign-in dialog
// 3. Extract via console
document.querySelector('main')?.innerText
```

For non-LinkedIn sources, web_extract is tried first.

### Company Research

Before assessing fit, the agent researches the company:
1. web_search for funding, leadership, Glassdoor reviews
2. web_extract on company About page
3. Note: PE firms, consulting practices, healthcare systems each have different signals

### Fit Evaluation Framework

Five-tier rating system:

| Rating | Criteria |
|--------|----------|
| EXCEPTIONAL | Perfect title match, comp in band, AI-heavy, strong industry alignment |
| VERY STRONG | Title matches, comp good, core competencies align, proximity within 60 min |
| STRONG | Good match on most axes, minor gaps (stretch title, comp at low end) |
| MODERATE | Several mismatches but worth watching |
| WEAK | Entry-level or severe mismatch, included for awareness only |

### Experience Weighting

The skill enforces specific experience weighting:

- **Accenture (9 years)** → Big 4 consulting delivery. IS consulting experience for PE/advisory roles.
- **Lockheed Martin (8.5 years)** → Enterprise programs, rigorous delivery. Defense = consulting muscle.
- **CNH current role** → Internal IT leadership, infrastructure ops, global team management
- **AI/automation hands-on (Digital Ethnicity, Hermes)** → Real differentiator, not "side project"
- **Healthcare IT** → Vertical expertise for PE healthcare portfolio companies

## Phase 4: Resume & Cover Letter Generation

### Resume Structure

```
> Apply here: [Job Posting URL]

PROFESSIONAL SUMMARY
[2-3 sentences targeting the role]

CORE COMPETENCIES
[Keywords from job posting]

PROFESSIONAL EXPERIENCE
Children's National Hospital | Senior Manager, DC&I/Ops | Present
Accenture | Business & Technology Delivery Manager | 9 years
Lockheed Martin | [Title] | 8.5 years
US Navy | Disbursing Clerk (de facto IT) | 12 years

AI PORTFOLIO
[If role has AI requirements]

EDUCATION & CERTIFICATIONS
```

### Critical Resume Constraints (Non-Negotiable)

These appear in the agent's memory and are enforced by the skill:

- CNH: "Senior Manager, Data Center & Infrastructure Operations"
- CNH scope: "oversees infrastructure representing $10M+ in assets" (NEVER "manages a $10M budget")
- Accenture: "Business & Technology Delivery Manager" (NEVER "Senior Manager")
- Navy: "Disbursing Clerk who served as de facto IT" (NEVER "Systems Administrator")
- NO active security clearance listed
- NO WordPress experience
- Digital Ethnicity = central brand, not side project

### PDF Generation

Markdown resumes are converted to PDF via WeasyPrint on Linux:

```python
from weasyprint import HTML
HTML('/tmp/resume.html').write_pdf('/tmp/resume.pdf')
```

Uses a professional CSS template with letter-size margins, section headers, and page numbers.

### Cover Letter

```text
[Header matching resume]
[Date]
[Hiring Team], [Company]
Re: [Exact Job Title]

Dear [Hiring Team],
[2-3 sentences: State role, connect background to needs]
[Achievements mapped to requirements - quantified]
[Company-specific priorities]
[Call to action]
Respectfully,
Bennie Williams
```

## Phase 5: Auto-Apply

### Decision Tree

```
Job Application Page
    │
    ├─ CAPTCHA present? ──────► SKIP auto-apply
    ├─ Login required? ────────► SKIP auto-apply
    ├─ Multi-step wizard? ─────► SKIP auto-apply
    └─ Simple HTML form? ──────► AUTO-APPLY via curl
```

### Supported Form Plugins

| Plugin | Detection Pattern | Submit Endpoint |
|--------|------------------|-----------------|
| WP Job Manager | `awsm_applicant_*` | POST wp-admin/admin-ajax.php |
| WPForms | `wpforms[id]` | POST wp-json/wpforms/v1/forms/{id}/submit |
| Contact Form 7 | `your-name`, `your-email` | POST wp-json/contact-form-7/v1/contact-forms/{id}/feedback |

### Auto-Apply Limitations

In practice, most job sites have anti-bot protections. The agent auto-applies when possible but often falls back to preparing materials for manual submission. Common blockers: Dice/LinkedIn/Workday authentication, CAPTCHAs, JavaScript-only forms.

## Phase 6: Storage & Notification

### Nextcloud (WebDAV)

All application materials are stored at `https://nc.bwai.us` under `Job-Applications/`.

**Folder structure per job:**
```
Job-Applications/
├── <company>_<role>/
│   ├── <company>-assessment.md
│   ├── <company>-resume.md
│   ├── <company>-resume.pdf
│   ├── <company>-cover-letter.md
│   └── <company>-cover-letter.pdf
├── _applications-log/
│   └── <company>-<role>-<date>.md
├── _meta/
│   └── running-comparison.md
└── digest-<date>.html
```

### AgentMail

After every application (successful or prepared-for-manual), an email is sent:

```
From: srv838555@digital-ethnicity.com
To:   bennie.williams36@gmail.com
Subject: Job Application Prepared: <position> - <company>

POSITION: <title>
COMPANY: <company>
FIT RATING: <rating>
APPLY HERE: <url>
```

### Telegram Digest

The final output is an HTML-formatted digest delivered to Telegram with:
- Run summary (jobs searched/qualified/auto-applied)
- Top 5 picks with fit ratings, salary, and key factors
- Full job table with links
- Apply priority ranking
- Exclusion audit trail
- Nextcloud links

## Tool Dependency Graph

```
web_search (Tavily)
    ├── Primary: job discovery
    └── Secondary: company research

web_extract
    ├── Job posting extraction (non-LinkedIn)
    └── Company about pages

browser (CDP)
    └── LinkedIn job extraction (sign-in bypass)

terminal (shell)
    ├── AnySearch CLI (search fallback)
    ├── AgentMail CLI (email send)
    ├── Curl (WebDAV uploads, auto-apply submissions)
    └── WeasyPrint (PDF generation)
```

## Skill Dependency

The cron job loads the `job-search-toolkit` skill, which provides:

- **Evaluation Framework:** Legitimacy checks, red/green flags, company deep-dive pattern
- **Resume Tailoring Rules:** Structure, constraints, stretch-role handling, AI portfolio
- **Cover Letter Structure:** Template, review checklist
- **Multi-Job Comparison:** Running ranking table format, priority system
- **Auto-Apply Rules:** Form detection, exclusion list, notification template
- **Integration Patterns:** Nextcloud WebDAV, AgentMail, Notion, Google Workspace

## Error Handling

| Failure Mode | Recovery |
|--------------|----------|
| web_search returns empty | Fall back to AnySearch CLI |
| LinkedIn blocks web_extract | Use browser CDP + JS console |
| Company research URL broken | Search company name + "about" |
| Nextcloud upload fails | Log failure, include materials in digest |
| AgentMail send fails | Log error, continue with other notifications |
| AnySearch also fails | Report honestly: "0 jobs found this run" |
| All searches empty | Deliver [SILENT] to suppress empty notification |
