# Workflow: Step-by-Step Execution

## Cron Trigger

```
Schedule: 0 */6 * * *
Tools:    web, terminal, file
Skills:   job-search-toolkit
Deliver:  telegram
```

Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC), the Hermes cron engine spawns a fresh agent session.

## Execution Flow (per tick)

### 1. Session Initialization

```
Agent boot → Load prompt → Load job-search-toolkit skill →
Read /root/.hermes/scripts/job-search-criteria.md →
Read /root/.hermes/scripts/job-auto-apply-config.md →
Read skill baseline resume from references/
```

### 2. Discovery Phase (~30-60s)

```
FOR each query in rotation (8-10 queries):
  web_search("<title> <location> $160k-$300k")
  IF empty: fallback to AnySearch CLI

AGGREGATE: deduplicate by URL
FILTER OUT: previously processed (check Nextcloud folder names)
```

### 3. Extraction Phase (~2-5 min per job)

```
FOR each candidate (target: 30+ raw → 20 qualified):
  web_extract(job_url)
  IF empty/LinkedIn → browser → dismiss sign-in → console extract
  
  web_search("<company> funding leadership reviews")
  
  BUILD: assessment, resume, cover letter
  CONVERT: markdown → PDF via WeasyPrint
```

### 4. Application Phase (~30s per job)

```
FOR each job:
  INSPECT: application page for form type
  
  IF simple form (no CAPTCHA, no login):
    curl POST form fields
    → LOG as "auto-applied"
  
  IF complex form (CAPTCHA, login, wizard):
    → LOG as "materials prepared, manual submission required"
  
  ALWAYS:
    agentmail inboxes:messages send → bennie.williams36@gmail.com
    curl MKCOL + curl PUT → Nextcloud WebDAV
```

### 5. Delivery Phase

```
BUILD: HTML digest
  - Run summary
  - Top 5 picks with ★ ratings
  - Full job table
  - Apply priority
  - Exclusion audit
  - Nextcloud links

UPLOAD: digest HTML to Nextcloud
DELIVER: final response → Telegram
```

## Tool Call Budget (Typical Run)

| Phase | Tool | Calls | Time |
|-------|------|-------|------|
| Discovery | web_search | 8-10 | ~30s |
| Discovery | AnySearch (fallback) | 0-5 | ~15s |
| Extraction | web_extract | 3-5 | ~10s |
| Extraction | browser | 3-5 | ~30s |
| Research | web_search | 3-5 | ~10s |
| Generation | write_file | 15-30 | ~20s |
| PDF | terminal (weasyprint) | 3-5 | ~30s |
| Upload | terminal (curl) | 20-40 | ~60s |
| Email | terminal (agentmail) | 3-5 | ~15s |
| **Total** | | **~60-100** | **~5-8 min** |

## State Management

The agent is **stateless between runs** — each tick is a fresh session. State is maintained externally:

- **Nextcloud:** Application folders and logs persist across runs
- **Running comparison:** Stored at `Job-Applications/_meta/running-comparison.md`
- **Application log:** Stored at `Job-Applications/_applications-log/`
- **Deduplication:** Check existing Nextcloud folder names

## Empty Run Handling

If no new jobs are found (all searches empty, or all results are duplicates):
- Respond with exactly `[SILENT]`
- Hermes suppresses delivery — no Telegram notification
- Prevents spam on quiet days
