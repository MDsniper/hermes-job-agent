# Hermes Autonomous Job Agent

An AI-powered autonomous job search and application agent built on [Hermes Agent](https://nousresearch.com). Finds senior IT leadership positions, assesses fit, generates tailored resumes and cover letters, auto-applies where possible, uploads materials to Nextcloud, and sends digest notifications via Telegram — all on a 6-hour cron schedule.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 Hermes Scheduler                  │
│            cron: 0 */6 * * * (every 6h)          │
└─────────────────┬───────────────────────────────┘
                  │
          ┌───────▼───────┐
          │  Cron Prompt   │  ← Self-contained instructions
          │  + Skills      │  ← job-search-toolkit skill loaded
          └───────┬───────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
┌────▼────┐ ┌────▼────┐ ┌────▼────┐
│  SEARCH  │ │ ASSESS  │ │  APPLY  │
│  Layer   │ │  Layer  │ │  Layer  │
└────┬────┘ └────┬────┘ └────┬────┘
     │            │            │
┌────▼────┐ ┌────▼────┐ ┌────▼────┐
│web_search│ │Fit Eval │ │curl auto│
│AnySearch │ │Resume   │ │apply    │
│web_extract│ │Cover Ltr│ │form sub │
└────┬────┘ └────┬────┘ └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
     ┌────────────▼──────────────┐
     │     OUTPUT / DELIVERY      │
     ├────────────────────────────┤
     │ Nextcloud (WebDAV)         │
     │  └─ Job-Applications/*/    │
     │ AgentMail (notifications)  │
     │ Telegram (digest)          │
     └────────────────────────────┘
```

## How It Works

### 1. Search Layer

Every 6 hours, the agent runs 8-10 web search queries targeting senior IT leadership roles across DC/Baltimore/NoVA metro. Rotates title-location combinations to avoid duplicates.

**Search sources:** web_search (Tavily-backed), AnySearch CLI (fallback), direct web_extract on job posting URLs.

### 2. Filter & Exclude

Before processing any job, the agent checks exclusions:

- **Blocked:** Federal/USAJobs.gov, active security clearance required, contract/1099-only, below $160K salary, outside 80-mile radius, WordPress roles, pure software engineering
- **Preferred:** AI responsibilities (moves role up in ranking), healthcare/regulated industry, DC/Baltimore metro proximity

### 3. Assess & Generate

For each qualifying job (target: 20 per run):

1. Extract posting details via web_extract or browser console
2. Research company (funding, Glassdoor, leadership)
3. Assess fit using a 5-tier framework: EXCEPTIONAL → VERY STRONG → STRONG → MODERATE → WEAK
4. Generate tailored resume (mirrors job language, includes AI Portfolio section)
5. Generate tailored cover letter
6. Convert to PDF via WeasyPrint

### 4. Auto-Apply

For each job, the agent inspects the application page for a simple HTML form. If the form has no CAPTCHA and no login requirement, it auto-submits via curl with the candidate's details. Otherwise, it prepares materials and notifies for manual submission.

### 5. Store & Notify

- **Nextcloud (WebDAV):** Each job gets a folder at `Job-Applications/<company>_<role>/` with assessment, resume (.md + .pdf), cover letter (.md + .pdf)
- **AgentMail:** Email notification sent to the user after every application with position details, fit rating, and expectations
- **Telegram:** Digest summary with top picks, full table, and apply priority
- **Application log:** `_applications-log/<company>-<role>-<date>.md` tracks every application

## Skills & Configuration

| Component | Path | Description |
|-----------|------|-------------|
| Cron prompt | `prompts/cron-prompt.md` | The full self-contained prompt the cron job executes |
| Search criteria | `config/search-criteria.md` | Target roles, location, salary, industries, exclusions |
| Auto-apply config | `config/auto-apply-config.md` | Contact info, exclusions, notification rules |
| Hermes skill | `skill/job-search-toolkit.md` | Full skill: evaluation framework, resume rules, company research patterns |

## Cron Schedule

```
Schedule:  0 */6 * * * (every 6 hours)
Delivery:  Telegram digest
Tools:     web, terminal, file
Skills:    job-search-toolkit
```

## Resume Constraints (Non-Negotiable)

The skill enforces strict resume rules to keep the candidate's background accurate:

- CNH: "Senior Manager, Data Center & Infrastructure Operations" who "oversees infrastructure representing $10M+ in assets"
- Accenture: "Business & Technology Delivery Manager" — NEVER "Senior Manager"
- Navy: "Disbursing Clerk who served as de facto IT" — NEVER "Systems Administrator"
- NEVER list any active security clearance
- No WordPress experience
- Digital Ethnicity is the central brand, not a side project

## Integrations

| Service | Purpose | Auth |
|---------|---------|------|
| Nextcloud (WebDAV) | Store all application materials | Basic auth |
| AgentMail | Send application notification emails | API key |
| Telegram | Deliver digest summaries | Bot token |
| AnySearch CLI | Fallback job search when Tavily fails | API key |

## Project Structure

```
hermes-job-agent/
├── README.md                         ← You are here
├── ARCHITECTURE.md                   ← Deep-dive architecture docs
├── config/
│   ├── search-criteria.md            ← Job search parameters
│   ├── user-profile.md               ← Candidate background/bio
│   └── auto-apply-config.md          ← Auto-apply rules & contact info
├── prompts/
│   └── cron-prompt.md                ← Full autonomous agent prompt
├── skill/
│   └── job-search-toolkit.md         ← The complete Hermes skill
├── docs/
│   ├── workflow.md                   ← Step-by-step execution flow
│   ├── integrations.md               ← Nextcloud, AgentMail, Notion setup
│   └── pitfalls.md                   ← Lessons learned & gotchas
└── scripts/
    └── convert_resumes_to_pdf.py     ← Batch PDF generation
```

## Example Output

A typical digest includes:

- **Run Summary:** jobs searched, qualified, processed, auto-applied
- **Top Picks (★):** Ranked by fit with company, title, salary, location, key factor
- **Full Job Table:** All 20 jobs with fit ratings, comp ranges, links
- **Apply Priority:** Which to submit first and why
- **Exclusion Audit:** What was skipped and why
- **Nextcloud Inventory:** Direct links to every application folder

## License

MIT
