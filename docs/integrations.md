# Integrations

## Nextcloud (WebDAV)

Primary storage for all application materials.

**Endpoint:** `https://nc.bwai.us/remote.php/dav/files/admin/`

**Commands:**
```bash
# Create folder
curl -X MKCOL 'https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<folder>' \
  -u 'admin:<password>'

# Upload file
curl -T /tmp/file.pdf \
  'https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<folder>/file.pdf' \
  -u 'admin:<password>'

# List folder
curl -X PROPFIND 'https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<folder>' \
  -u 'admin:<password>' -H "Depth: 1"

# Read file
curl 'https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<folder>/file.md' \
  -u 'admin:<password>'
```

**Directory structure:**
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

**Folder naming:** lowercase, hyphens. Example: `alvarez-marsal_director-pepi-cio-domain/`

## AgentMail

Email service for application notifications and recruiter responses.

**Inbox:** `srv838555@digital-ethnicity.com`
**API Key:** Stored in `~/.hermes/secrets/agentmail.env`
**Documentation:** https://docs.agentmail.to

**Key commands:**
```bash
# Send email
agentmail inboxes:messages send \
  --inbox-id "srv838555@digital-ethnicity.com" \
  --to "bennie.williams36@gmail.com" \
  --subject "Job Application Prepared: <position> - <company>" \
  --text "Application details..."

# Check inbox for recruiter responses
agentmail inboxes:messages list \
  --inbox-id "srv838555@digital-ethnicity.com"
```

**Notification template:**
```
Subject: Job Application Prepared: <position> - <company>

Bennie,

Your Hermes Agent prepared an application:

POSITION: <title>
COMPANY: <company>
LOCATION: <location>
SALARY: <salary>
FIT RATING: <rating>

APPLY HERE: <url>
APPLICATION LOG: https://nc.bwai.us/Job-Applications/_applications-log/
AGENTMAIL INBOX: srv838555@digital-ethnicity.com

---
Sent by Hermes Agent via AgentMail
```

## Telegram

Digest delivery platform. The cron job delivers its final response to the user's Telegram chat via Hermes' built-in delivery system.

**Platform:** Telegram
**Delivery target:** User's configured Telegram chat

## Notion (Optional)

When enabled, job search digests can be posted to a Notion page as structured blocks.

**API:** `https://api.notion.com/v1/blocks/<page_id>/children`
**Auth:** Bearer token via `NOTION_API_KEY`

**Block structure for job entries:**
- heading_2 → Date/run label
- callout → Search summary
- heading_3 → Job title
- paragraph → Salary, location, fit rating, AI status
- bookmark → Job posting URL
- numbered_list_item → Apply priority

**Shell escaping pitfall:** URLs with `&` in JSON cause shell backgrounding errors. Always write payload to file first:
```bash
cat > /tmp/notion-blocks.json << 'EOF'
{"children": [...]}
EOF
curl -X PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d @/tmp/notion-blocks.json
```

## AnySearch CLI

Fallback search engine when Tavily-backed web_search returns empty results.

```bash
python3 /root/.hermes/skills/search/anysearch/scripts/anysearch_cli.py \
  search "IT Director job Maryland" --max_results 5
```

## WeasyPrint

PDF generation from HTML on Linux:

```python
from weasyprint import HTML
HTML('/tmp/resume.html').write_pdf('/tmp/resume.pdf')
```

Requires: `uv pip install weasyprint`
