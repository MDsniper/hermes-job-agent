---
name: job-search-toolkit
description: 'Comprehensive toolkit for job seekers: evaluate recruiting outreach legitimacy, tailor resumes to job postings, compare opportunities, and prepare application materials. Class-level skill covering the full job application lifecycle.'
---

# Job Search Toolkit

A comprehensive skill for job seekers that covers evaluating recruiting messages, tailoring resumes, comparing opportunities, and preparing complete application packages.

## Recruiting Outreach Review

Review LinkedIn messages, emails, and other recruiting outreach to assess legitimacy and job fit.

### Evaluation Framework

#### Red Flags (Scam Indicators)
- Won't disclose company name AND job posting doesn't exist
- Requests personal info early (SSN, bank details, "background check" before interview)
- Pushes to move off-platform immediately (WhatsApp, personal email, text)
- Pay range is suspiciously high for role/requirements
- Vague job description with no specific responsibilities
- Recruiter has no LinkedIn history or very new account
- Grammar/spelling errors in professional outreach
- Generic greeting not using your name

#### Acceptable Practices (Not Necessarily Red Flags)
- Won't name client before screening call — standard for third-party recruiters
- Staffing firm posts job under their own name (e.g., PSI, Robert Half, TEKsystems)
- Job posting exists on company LinkedIn page or recruiter's company page
- Recruiter has verifiable LinkedIn profile with employment history

#### Legitimacy Checks
1. Search the job posting URL — does it resolve to a real LinkedIn/company posting?
2. Check the recruiter's LinkedIn profile — tenure, connections, employment history
3. Verify the staffing firm exists (Google "company name + reviews" or check Glassdoor)
4. Ask for: industry vertical, team size, comp range, role origin (new vs replacement)

### Company Deep-Dive (Before Writing Assessment)
Before writing any assessment, research the company beyond the outreach email:
1. **web_search** the company name + co-founders + funding — find press coverage (CRN, TechCrunch, WSJ, etc.)
2. **web_extract** the company's own site (About page) and any press articles found
3. Synthesize: funding rounds, investors, acquisitions, leadership bios, product/platform details, engineering team composition
4. This research often reveals far more than the recruiter shared — actual revenue, team size, client verticals, AI platform capabilities, and advisory board members
5. Use this enriched profile to assess fit more accurately and generate better questions for the user

Without this step, assessments are based on the recruiter's pitch alone, which is always incomplete.

### Response Template

When reviewing a message, provide:

1. **Legitimacy assessment**: Likely legitimate / Questionable / Likely scam
2. **Key details extracted**: Role, location, comp, company (if known), recruiter firm
3. **Red flags**: List any concerns
4. **Green flags**: What looks normal/legitimate
5. **Recommended questions to ask**: If the user wants to pursue
6. **Verdict**: Take the call / Proceed with caution / Pass

### Context Gathering

Ask for or extract:
- User's role/seniority level they're targeting
- Geographic constraints
- Current compensation (to evaluate offers)
- Industry preferences
- Any specific concerns about the outreach

### Experience Weighting Rules

When assessing fit against job requirements, weight the user's background as follows:
- **Accenture (9 years)** = Big 4 consulting delivery. This IS consulting experience for any PE/advisory role. Don't discount it.
- **Lockheed Martin (8.5 years)** = Enterprise-scale programs, rigorous delivery, complex stakeholder environments. Strong credibility for any senior technology leadership role.
- **CNH current role** = Internal IT leadership, infrastructure operations, global team management.
- **AI/automation hands-on work (Digital Ethnicity, Hermes)** = Real differentiator for AI-focused roles. Not "side project" — treat as production experience.
- **Healthcare IT** = Vertical expertise that translates well to PE healthcare portfolio companies.

When the job asks for "consulting experience" and the user has Accenture on their resume, that box is checked. Don't frame it as a gap.

### Company Identification (When Client Is Undisclosed)

Third-party recruiters often won't name the client before a screening call. To help the user evaluate the opportunity:

1. **Access the job posting URL directly** — Even without being logged in, LinkedIn job postings often show the full description, including the staffing firm name and sometimes subtle clues about the actual client (industry hints, size, tech stack mentioned).

2. **Analyze job requirements for company signals:**
   - Specific certifications (e.g., BICSI) point to structured cabling integrators
   - "Hyperscale" vs "enterprise" vs "colocation" narrows the market
   - Team size, reporting structure, and growth language indicate company stage
   - Equipment mentioned (specific brands, liquid cooling, etc.) may indicate client type

3. **Research the staffing firm:**
   - Search "<firm name> + clients + data center" or "<firm name> + Glassdoor reviews"
   - Staffing firms often specialize in certain verticals — their website may list industries served

4. **Generate candidate companies based on:**
   - Industry vertical + geography + company stage ("growing rapidly" = mid-market, not hyperscaler)
   - Known major players in the region (maintain a mental list for common tech hubs like Ashburn, Dallas, Phoenix)

5. **If browser searches are blocked by CAPTCHAs:**
   - Try accessing the LinkedIn job posting directly via its URL
   - Use curl with browser-like User-Agent headers
   - Fall back to asking the user to search from their logged-in browser

#### Browser Session Limitation
The agent's browser is a separate isolated session — it cannot see tabs or sessions the user is logged into. If the user says "I'm logged in, look at my LinkedIn," ask them to paste the message content directly rather than trying to navigate to their session.

### Example Output

```
Role: VP of Operations (Data Center / Structured Cabling)
Recruiter: John Usher, "Talent Acquisition | AI Business Consulting"
Posted by: PSI (Proteam Solutions) — staffing firm
Location: Ashburn, VA (hybrid)
Company: Undisclosed until screening (common for third-party recruiters)

Assessment: LIKELY LEGITIMATE
- PSI/Proteam Solutions is a known staffing firm in data center/cabling space
- Job posting exists and resolves on LinkedIn
- Recruiter's request to connect before naming client is standard practice

Red flags: None significant
Green flags: Real job posting, known staffing firm, role matches user's background

Recommended questions:
- Is the client a contractor/integrator, operator, or enterprise?
- How many direct reports?
- Comp range? (Don't give yours first)
- Why is the role open — new or replacement?

Verdict: Worth taking the screening call.
```

## Resume Tailoring

Create customized resumes that map a user's experience directly to job posting requirements.

### Workflow

#### Phase 1: Extract Job Requirements

**LinkedIn extraction — web_extract is BLOCKED by LinkedIn.** Use the browser tool instead:

1. `browser_navigate` to the LinkedIn job URL
2. Dismiss the sign-in dialog (click the "Dismiss" button — usually the first interactive element)
3. Extract full text via `browser_console` with expression:
   ```javascript
   document.querySelector('main')?.innerText
   ```
   This returns the complete job posting including title, company, description, qualifications, salary, and similar jobs section.

4. `web_extract` does NOT work on LinkedIn — it returns "Website Not Supported". Do not try it; go straight to the browser approach.

**Other job boards** (company sites, Indeed, etc.) — try `web_extract` first; fall back to browser if blocked.

**Extract these fields from the posting text:**
- Job title and company
- Location and travel requirements
- Salary range (if posted)
- Required qualifications
- Preferred qualifications
- Key responsibilities
- Application deadline
- Any special requirements (citizenship, clearance, etc.)

#### Phase 2: Map User Experience
Draw from memory/session context for:
- Current role and seniority level
- Years of experience in relevant domains
- Technical skills and certifications
- Team leadership scope
- Budget/project scale
- Industry background
- Target compensation range

#### Phase 3: Generate Tailored Resume
Structure the resume to emphasize alignment:

**Sections to include:**
1. Header (Name, contact info, LinkedIn)
2. Apply link (the job posting URL, right under the header as a blockquote)
3. Professional Summary (2-3 sentences targeting the role)
4. Core Competencies (keywords from job posting)
5. Professional Experience (quantified accomplishments)
6. Education
7. Certifications (prioritize those mentioned in job posting)

**Apply link rule:** EVERY resume and document must include the job posting
URL near the top so the user can go back and apply without searching for it.
Format: `> Apply here: <URL>`

**Tailoring principles:**
- Mirror job posting language and keywords
- Lead with experience that matches their "must-haves"
- Quantify accomplishments (team size, budget, uptime %, cost savings)
- Address their specific requirements explicitly
- Note any gaps or missing certifications honestly in the output

#### Phase 4: Customization Checklist
Remind user to:
- Replace placeholder company names with actual employers
- Update contact information
- Adjust numbers to match actual experience
- Remove certifications not held
- Convert to requested format (DOCX, PDF, etc.)

### Job Posting Extraction Notes

The proven LinkedIn extraction is `document.querySelector('main')?.innerText`
via browser_console after dismissing the sign-in dialog. See Phase 1 above.

For salary extraction from raw text:
```javascript
document.body.innerText.match(/pay range|salary|compensation|wage range/i)
```

### Extracting from LinkedIn

LinkedIn blocks `web_extract`. Use the browser tool + console extraction pattern documented in `references/linkedin-extraction.md`.

### Resume Structure Template

```
[NAME]
[Title] | [Location] | [Email] | [Phone] | LinkedIn

> Apply here: [Job Posting URL]

PROFESSIONAL SUMMARY
[Targeted summary emphasizing relevant experience]
PROFESSIONAL SUMMARY
[Targeted summary emphasizing relevant experience]

CORE COMPETENCIES
[Keywords mapped from job requirements]

PROFESSIONAL EXPERIENCE
[RELEVANT TITLE]
[Company] | [Dates]

Key Accomplishments:
• [Achievement matching their requirement 1]
• [Achievement matching their requirement 2]
...

EDUCATION
[Degree] | [University]

CERTIFICATIONS
[Relevant certs, prioritizing those mentioned in posting]
```

### Tailoring for Stretch Roles

When the user's background is adjacent to but not a perfect match for the role (e.g., infrastructure leader applying for a software engineering role, ops manager applying for consulting):

1. **Reframe, don't fabricate.** Operational automation and scripting becomes "AI engineering." Team leadership becomes "client engagement and technical consulting." Budget management becomes "program delivery."
2. **Add a Portfolio section.** For AI/tech roles, add a dedicated section listing production deployments, tools used, and contributions — this shows hands-on depth that the experience section alone may not convey.
3. **Be honest about gaps in the assessment notes.** The notes.md file should clearly state which requirements are a stretch so the user can prepare for interview questions on those areas. Don't hide gaps in the resume itself.
4. **Mirror their language aggressively.** Pull exact phrases from the job posting ("agentic platforms," "forward deployed," "pod-based delivery") and weave them into the summary and bullet points.
5. **Lead with the strongest match.** If healthcare experience is the bridge, put "Healthcare IT" in the professional summary's first sentence.

## Cover Letter Integration

When creating resumes, offer to also review or generate cover letters. A complete application package includes both.

### Cover Letter Review Checklist
If user submits a cover letter for review, evaluate:
- **Opening**: Does it state the specific role and company? Is it direct?
- **Value proposition**: Does it connect user's experience to the role's needs?
- **Quantified examples**: Are there specific achievements (team size, budget, metrics)?
- **Company-specific elements**: Does it reference the company's stated priorities (e.g., AI focus)?
- **Tone**: Confident without arrogance; professional without being stiff
- **Closing**: Clear call to action, not passive

### Cover Letter Structure
```
[Header matching resume]

[Date]

[Hiring Team / Hiring Manager]
[Company]

Re: [Exact Job Title]

Dear [Hiring Team],

[2-3 sentences: State the role, connect your background to their needs]

[1-2 paragraphs: Specific achievements that map to their requirements - quantify]

[1 paragraph: Address any unique requirements or company-specific priorities]

[Closing: Express interest, call to action]

Respectfully,
[Name]
```

## Multi-Job Comparison

When user is evaluating multiple opportunities, create and maintain a
RUNNING comparison table that grows with each new job assessed. This is
the single most valuable artifact for the user — keep it updated and
include it in every assessment summary.

### Running Ranking Table Format

Include this at the bottom of every assessment (notes.md) and in the
chat summary:

```
| Rank | Opportunity | Fit | Comp | Key Factor |
|------|------------|-----|------|------------|
| 1. ★ | Company VP | EXCEPTIONAL | $225K | VP title, perfect match |
| 2. | Company Dir | VERY STRONG | $410K | Partner track, travel |
| 3. | Company Lead | STRONG | $195K | Federal, no travel |
```

Fit levels: EXCEPTIONAL > VERY STRONG > STRONG > MODERATE > WEAK
Star (★) the top pick(s). Re-rank after every new opportunity.

### Apply Priority Recommendation

After the comparison table, give a clear "APPLY PRIORITY" section:
- Numbered list of which jobs to apply to first
- Brief reason for each priority level
- Note any time-sensitive postings (high applicant count, old posting)

### Detailed Comparison Table

When user asks or when comparing 2-3 top candidates, create a detailed
side-by-side table:

| Factor | Job A | Job B |
|--------|-------|-------|
| Title | ... | ... |
| Company | ... | ... |
| Base salary | ... | ... |
| Bonus/OTE | ... | ... |
| Type (W-2/1099) | ... | ... |
| Location | ... | ... |
| Travel | ... | ... |
| Key requirements | ... | ... |
| Your match strength | ... | ... |
| Comp vs current | ... | ... |

## Application Materials Organization

**Storage: Nextcloud at https://nc.bwai.us** (WebDAV API)

For EVERY job application worked on, create a folder via WebDAV:
  https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<company>_<role>/

Folder naming: lowercase, hyphens for spaces. Examples:
  - alvarez-marsal_director-pepi-cio-domain/
  - oracle_director-datacenter-ops/
  - swooped_technology-operations-manager/

**WebDAV commands:**
```bash
# Create folder
curl -s -o /dev/null -w "%{http_code}" -X MKCOL 'https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<folder>' -u 'admin:<password>'

# Upload file
curl -s -o /dev/null -w "%{http_code}" -T /path/to/file.md 'https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications/<folder>/filename.md' -u 'admin:<password>'
```

Inside each folder, name files WITH the company name so they're identifiable standalone:
  - <company>-assessment.md — fit analysis, red/green flags, questions to ask, salary analysis
  - <company>-resume.md — tailored resume for this role
  - <company>-resume.docx — ATS-ready Word version
  - <company>-cover-letter.md — cover letter (if generated)
  - <company>-cover-letter.docx — ATS-ready Word version
  - <company>-job-posting.md — raw extracted job posting text

Example filenames in alvarez-marsal_director-pepi-cio-domain/:
  - alvarez-marsal-assessment.md
  - alvarez-marsal-resume.md / .docx
  - alvarez-marsal-cover-letter.md / .docx

Always create the folder at the start of working on a job, even if only doing an initial assessment. Files get added as the work progresses.

## Browser & Search Configuration

This skill relies on Browserbase and Tavily for reliable job posting extraction:

- **Browserbase** (browser.engine = browserbase): Use for ALL browser automation —
  LinkedIn job postings, company career pages, and any bot-protected sites.
  Residential proxies bypass bot detection. No CAPTCHA issues.
- **Tavily** (TAVILY_API_KEY): Use `web_search` for researching companies,
  recruiters, and salary data. Preferred over generic search for depth and accuracy.

### Workflow for Job Posting Extraction
1. First try `web_extract` on the URL — fast, no browser needed.
2. If web_extract fails (LinkedIn blocks it, empty content), fall back to browser.
3. Browser automatically uses Browserbase after `/reset` in a new session.
4. For company research, use `web_search` (backed by Tavily) to find funding,
   leadership, reviews, and news before writing the assessment.

### LinkedIn-Specific Notes
- LinkedIn blocks web_extract — always use browser for job postings.
- Dismiss the sign-in dialog (click Dismiss button) then extract via console:
  `document.querySelector('main')?.innerText`
- The browser is a separate session — it cannot see the user's logged-in LinkedIn.
  If content is behind auth, ask user to paste the posting text directly.

## Document Formatting & Submission

- **No Raw Markdown for Final Deliverables**: When generating resumes or cover letters intended for submission, DO NOT output raw Markdown syntax (e.g., `#`, `**`) as the final formatted document. It looks unprofessional in word processors.
- **Clean Text Output**: Provide clean, plain-text formatting (e.g., ALL CAPS for section headers, standard `•` bullet points) if generating text for copy-pasting.
- **Master Template Handoff**: Explicitly instruct the user to copy the generated clean text into their own pre-formatted master resume template (Word or formatted Google Doc) for final styling, fonts, and margins.
- **Google Docs Creation**: If creating Google Docs programmatically, ensure the content is stripped of Markdown syntax before insertion, or provide a separate "Clean Text" version to avoid rendering issues.

## PDF Generation

Two approaches depending on environment:

### Linux/Server (Weasyprint — preferred on srv838555)
```bash
uv pip install weasyprint
```

Convert markdown → HTML → PDF with professional styling:
```python
from weasyprint import HTML
HTML('/tmp/resume.html').write_pdf('/tmp/resume.pdf')
```

See `references/html-resume-template.md` for the CSS template (letter-size margins, section headers, professional fonts, page numbers).

### macOS (Chrome headless)
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --print-to-pdf="/path/to/output.pdf" \
  --no-margins --print-to-pdf-no-header \
  "file:///path/to/resume.html"
```

**Pitfall:** WeasyPrint fails on macOS without homebrew pango/gobject. On macOS, go straight to Chrome headless.

### Bulk PDF Conversion
See `scripts/convert_resumes_to_pdf.py` for a reusable script that processes all resume/cover-letter markdown files in a directory, converts to styled PDF, and uploads to Nextcloud.

## File Format Notes

- **Binary .docx**: Use `python3 -c "from docx import Document..."` if python-docx available, otherwise extract text via zipfile/XML approach
- **Extracting text from .docx**: Use the zipfile + XML parsing pattern to read without external dependencies
- **User-submitted files**: Always read and summarize before providing feedback

## Salary & Contract Calculations

When user mentions hourly rates or contract terms, calculate:
- **Gross annual**: hourly × 40 hrs/week × 52 weeks
- **1099 considerations**: Self-employment tax (~15.3%), no benefits
- **W-2 vs 1099 comparison**: Show net estimates for both
- **Benefits value**: Health insurance, 401k, PTO typically worth $15K-$25K/year

### Notes
- For W-2 vs contract roles, adjust framing (stability vs flexibility)
- Healthcare/regulated industry experience translates well to legal/finance
- Leadership scope (team size, budget) matters for senior roles
- Always note citizenship requirements if mentioned
- CDW and similar services companies value "consultative delivery" language
- Fortune 500 consulting experience (Accenture, Deloitte, etc.) is a strong credibility marker
- AI fluency is increasingly a differentiator - highlight if user has hands-on AI experience
- **Defense/aerospace experience IS consulting-relevant.** Lockheed, Northrop, Raytheon, etc. deliver enterprise programs under rigorous compliance. When assessing PE or consulting roles, treat this as equivalent delivery muscle — do not downgrade it as "not consulting."
- **When the user pushes back on a fit assessment, recalibrate immediately.** They know their experience better than the model does. If they say "doesn't X count?", the answer is almost always yes — adjust the rating and explain what changed.

### PE / Consulting Jargon
When discussing roles with the user, always explain acronyms on first use:
- **PE = Private Equity** — investment firms that buy companies, improve them, sell for profit (Blackstone, KKR, Carlyle, etc.)
- **PEPI = Private Equity Performance Improvement** — A&M's PE advisory practice
- **Due diligence** = pre-buy assessment of a company's technology, operations, finances
- **Portfolio company** = a company owned by a PE firm
- **Value creation** = making portfolio companies more profitable before selling
- **Engagement** = a consulting project for a client
- **Deliverable** = the output of an engagement (report, assessment, roadmap)

## User-Specific Resume & Bio Constraints (CRITICAL)
When generating or tailoring resumes/bios for this user (Bennie "Ben" Williams), strictly enforce these rules:
- **Current Role (CNH)**: Phrase as "Senior Manager, Data Center & Infrastructure Operations" who "oversees infrastructure representing $10M+ in assets". NEVER say "manages a $10M budget" (budget authority sits with the director).
- **Accenture Title**: Must be exactly "Business & Technology Delivery Manager". NEVER "Senior Manager".
- **Navy Service**: Phrase as "Disbursing Clerk who served as de facto IT". NEVER "Systems Administrator".
- **Clearances**: NEVER list any active security clearance. He holds none currently.
- **CareerFlow**: Keep completely separate from any discussion of the user's personal career or job search.
- **Digital Ethnicity**: Treat as the central brand/venture, not a side project.
- **Location**: Frederick, MD (relocated from Hagerstown, MD in 2026; target geography is Baltimore / DC metro for IT infra and managed-services roles).
- **No WordPress**: Do not mention or include WordPress experience.

## User's CNH Title (for resume tailoring)

Memory only carries the framing rule ("oversees infrastructure representing $10M+ in assets") — the exact CNH title string itself is NOT recorded. When tailoring a resume, ask the user for the verbatim CNH title rather than guessing. The "Senior Manager, Data Center & Infrastructure Operations" wording in the older constraint block above may be stale; do not use it without confirming.

## Output format when user wants both editable + ATS-friendly

Some users (this one) want a resume + cover letter as BOTH a Word .docx (for ATS upload) and a Google Doc (for easy editing). When asked for both:
- Build the .docx with `python-docx` (see "macOS Python pitfall" below).
- Upload via direct Google Drive + Docs API (CLI only supports `docs get` and `drive search`, NOT create). See `google-workspace` skill's `references/docs-create-via-api.md` for the working pattern.
- Folder layout: Nextcloud at `Job-Applications/<company>_<role>/` via WebDAV (see Application Materials Organization section). Google Docs live in Drive root, named "Bennie Williams — <Doc> (Company, Year)".

## macOS Python pitfall (this profile)

`python3` on this Mac is the miniconda 3.13 binary, NOT the system Python. Anything installed via `pip3 install --user` writes to `/Users/bwilliams/Library/Python/3.12/lib/python/site-packages` and is INVISIBLE to the default `python3`. If you need to use pip3-installed packages (python-docx, google-api-python-client, notebooklm, etc.), invoke the system 3.12 explicitly:

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 script.py
```

Symptom: `pip3 list` shows the package, but `python3 -c "import X"` ModuleNotFoundErrors. Always test your script before declaring done.

## Pitfalls

1. **Don't undervalue Big 4 / defense consulting experience for PE roles.** The user has 9 years at Accenture and 8.5 years at Lockheed Martin. When assessing PE consulting roles (PEPI, diligence, portfolio value creation), treat this as STRONG fit, not moderate. Big 4 consulting delivery IS the skill PE firms want — client-facing engagements, executive communications, scoping, team management. Defense contracting shows you can operate in high-stakes, structured environments. Don't frame these as "gaps" — frame them as direct qualifications. The only real gap is PE deal-specific diligence (buy-side IT assessments), and that's a narrow technicality, not a fundamental mismatch.

2. **Define jargon on first use.** Don't assume the user knows consulting acronyms. PE = Private Equity, PEPI = Private Equity Performance Improvement, OTE = On-Target Earnings, etc. Define once, then use the acronym freely.

3. **Browserbase config changes require `/reset` or new session.** Setting
   `browser.engine = browserbase` or updating `BROWSERBASE_API_KEY` in `.env`
   does NOT take effect mid-session. The browser will continue using local
   Chromium until the user runs `/reset` or starts a new hermes session.
   Tell the user this when configuring Browserbase for the first time.

2. **Apply link must appear in EVERY file, not just README.** User explicitly
   requested the job posting URL be in README.md, job-posting.md, AND
   resume.md (near the top as `> Apply here: [URL]`). They don't want to
   hunt through files to find where to apply. This is non-negotiable.

3. **LinkedIn web_extract always fails.** Don't waste a tool call trying it.
   Go straight to browser → dismiss dialog → `document.querySelector('main')?.innerText`.

4. **Don't skip company research.** After extracting the posting, always run
   web_search for the company before writing the assessment. The recruiter's
   email or job posting alone is never enough to assess legitimacy or fit.

5. **Browserbase may show "Running WITHOUT residential proxies" warning** if
   `BROWSERBASE_PROXIES=true` is not set in `.env` or the plan doesn't include
   proxy support. The browser still works but bot detection is more aggressive.

## Autonomous Job Search (Cron-Based)

Set up a recurring cron job to automatically search for jobs, assess fit, generate materials, and notify the user.

### User's Active Search Criteria
- **Titles:** CIO, Assistant CIO, IT Director, Associate IT Director, Senior Manager, Senior IT Manager, senior IT leadership
- **Location:** 80-mile driving radius from 13534 Pulaski Dr, Hagerstown, MD 21742
  - Covers: DC Metro (Arlington, Bethesda, Rockville, Tysons, Reston, Herndon, Ashburn, McLean, Fairfax, Alexandria, Silver Spring, Columbia, Gaithersburg), Baltimore Metro (Baltimore, Towson, Ellicott City, Annapolis), Frederick/Shenandoah (Frederick, Leesburg, Winchester, Martinsburg WV), PA South (Harrisburg, York, Chambersburg, Gettysburg, Lancaster)
- **Salary:** $160K–$300K
- **Industries:** Any
- **Batch size:** 20 jobs per day
- **Notification:** Email digest (once configured) or Telegram

### Search Strategy
Since LinkedIn blocks automation, use web_search as the primary discovery tool:

1. **Rotate search queries** across title/location combinations:
   - `"CIO" OR "Chief Information Officer" Washington DC OR Baltimore OR Frederick`
   - `"IT Director" OR "Director of IT" Northern Virginia OR Fairfax OR Tysons`
   - `"VP Technology" OR "Vice President IT" Maryland OR "DC metro"`
   - `"Senior Manager IT" OR "Senior IT Manager" Bethesda OR Rockville OR Arlington`

2. **Source mix:** web_search catches LinkedIn, Indeed, ZipRecruiter, Glassdoor, and company career pages via Google indexing

3. **Extract details:** Try web_extract on each URL. LinkedIn often fails — fall back to searching the company + title for more context

4. **Filter:** Only process jobs matching salary range ($160K+) and geographic radius

5. **Deduplicate:** Track processed URLs to avoid re-analyzing the same posting

### Per-Job Processing
For each qualifying job:
1. Extract posting details (web_extract or web_search fallback)
2. Research company (funding, leadership, Glassdoor)
3. Assess fit against user's background
4. Generate tailored resume + cover letter
5. Create Nextcloud folder and upload all files
6. Add to running comparison table

### Cron Job Prompt Pattern
```
Search for [N] new senior IT leadership jobs matching the user's criteria.
For each new job found:
1. Extract posting details via web_extract (fall back to web_search if blocked)
2. Research the company via web_search
3. Assess fit using the job-search-toolkit evaluation framework
4. Generate tailored resume and cover letter
5. Upload to Nextcloud at Job-Applications/<company>_<role>/
Report a summary of all jobs processed with fit ratings.
```

### Delivery
- Batch all jobs into a single digest notification
- Include: company, title, location, salary, fit rating, and Nextcloud link
- Mark top picks with ★ for priority

### Notion Delivery (Secondary Target)

When the user wants job search results posted to Notion in addition to Telegram:

1. **Write digest as Notion blocks**, not markdown. Use the block types from the `notion` skill's `references/block-types.md`.
2. **For large block payloads**, write JSON to `/tmp/notion-blocks.json` first, then use `curl -d @file`. Passing URLs with `&` directly via `-d` causes shell backgrounding errors.
3. **Page structure**: heading_1 for title, heading_2 for each date/run, heading_3 for each job, callout for search summary, bookmark blocks for clickable links, numbered_list_item for apply priority.
4. **Extract page ID from Notion URL**: The 32-char hex string at the end of the URL is the page_id. Format: `https://app.notion.com/p/Page-Title-<hex-id>`.
5. **Internal integrations** need `parent.page_id` — cannot create workspace-level pages with `workspace: true`.

#### Notion Block Template for Job Entry
```json
{"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "1. Company — Title, Location"}}]},
{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [
  {"type": "text", "text": {"content": "💰 $XXX | 📍 Location | 🎯 "}},
  {"type": "text", "text": {"content": "FIT_RATING"}, "annotations": {"italic": true}},
  {"type": "text", "text": {"content": " | 🤖 AI: Yes/No"}}
]}},
{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "One-line reason"}, "annotations": {"italic": true}}]}},
{"object": "block", "type": "bookmark", "bookmark": {"url": "https://job-posting-url"}}
```

#### Shell Escaping Pitfall
URLs containing `&` in JSON passed to `curl -d` are interpreted as shell background operators. Always write to file first:
```bash
# Write JSON to file
cat > /tmp/notion-blocks.json << 'PAYLOAD_EOF'
{"children": [...]}
PAYLOAD_EOF
# Then use -d @file
curl -s -X PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d @/tmp/notion-blocks.json
```

## Notion Integration for Job Search Results

When the user wants job search digests posted to Notion (in addition to Telegram/Nextcloud):

### Setup
1. Ensure `NOTION_API_KEY` is set in `~/.hermes/.env`
2. User must connect the integration to the target page: page menu `...` → **Connections** → select integration
3. Extract page ID from URL: the 32-char hex string at the end of `https://app.notion.com/p/Page-Title-<hex-id>`

### Writing Digest to Notion
1. Write JSON payload to `/tmp/notion-blocks.json` first (shell `&` in URLs causes backgrounding errors with `curl -d`)
2. Use `curl -d @/tmp/notion-blocks.json` to POST
3. Block structure: heading_1 (title), heading_2 (date/run), heading_3 (each job), callout (summary), bookmark (links), numbered_list_item (priority)
4. **Cannot insert before a specific block** — Notion API only appends. To reorder, delete all blocks and re-add in desired order.
5. Internal integrations require `parent.page_id` — cannot create workspace-level pages with `workspace: true`

### Shell Escaping Pitfall
URLs with `&` in JSON passed to `curl -d` are interpreted as shell background operators. Always write to file first:
```bash
# WRONG — & causes shell backgrounding
curl -d '{"url": "https://example.com?a=1&b=2"}'

# RIGHT — write to file, then use @file
echo '{"url": "https://example.com?a=1&b=2"}' > /tmp/payload.json
curl -d @/tmp/payload.json
```

## AgentMail Integration for Job Applications

AgentMail gives the agent its own email inbox for receiving verification emails, application confirmations, and recruiter responses.

**Setup:** See `references/agentmail-setup.md` for API key, CLI install, and commands.

**Usage pattern:**
1. Use the AgentMail inbox address (e.g., `srv838555@digital-ethnicity.com`) as the contact email on all job applications
2. After submitting an application, check the inbox for confirmations, interview invitations, and verification emails
3. Forward important emails to the user's personal email if needed

**Key commands:**
```bash
export AGENTMAIL_API_KEY="am_..."
agentmail inboxes:messages list --inbox-id "inbox@domain.com"
agentmail inboxes:messages send --inbox-id "inbox@domain.com" --to "recipient@example.com" --subject "Subject" --text "Body"
```

## Direct Application Submission

When the job application is on a simple web form (no CAPTCHA, no account required), submit directly via curl instead of using browser automation.

**Identify the form type** by looking at field names in the page HTML:

| Plugin | Field Pattern | Submit Endpoint |
|--------|--------------|-----------------|
| WP Job Manager | `awsm_applicant_*` | `POST /wp-admin/admin-ajax.php` with `action=awsm_applicant_form_submission` |
| WPForms | `wpforms[<id>]` | `POST /wp-json/wpforms/v1/forms/<id>/submit` |
| Contact Form 7 | `your-name`, `your-email` | `POST /wp-json/contact-form-7/v1/contact-forms/<id>/feedback` |

**Full curl patterns:** See `references/wordpress-form-submission.md`

**When to use direct submission:**
- Form has no CAPTCHA
- No account/login required
- Simple fields (name, email, phone, cover letter, resume upload)
- WordPress site with identifiable form plugin

**When to fall back to browser:**
- CAPTCHA present
- Multi-step wizard
- JavaScript-only form (no HTML form action)
- Requires authentication

## Auto-Apply with Exclusions (Full Auto Mode)

When user selects "full auto with exclusions," apply automatically to jobs with simple HTML forms while skipping excluded categories.

### Exclusion List (Default)
- Federal/USAJobs.gov jobs (requires login.gov, lengthy process)
- Contract/1099-only roles
- Anything requiring active security clearance
- Salary below $160,000
- Outside 80-mile radius from Frederick, MD
- WordPress-related positions
- Pure software engineering / code-heavy roles

### Auto-Apply Decision Tree
1. Extract form fields from job posting page
2. If form has CAPTCHA, login requirement, or multi-step wizard → SKIP auto-apply, prepare for manual
3. If form has simple fields (name, email, phone, cover letter, resume) → AUTO-APPLY
4. Submit via curl with standard contact info
5. Log to `_applications-log/` on Nextcloud
6. Send email notification to bennie.williams36@gmail.com via AgentMail

### Notification Email Template (MANDATORY after every application)
```bash
export AGENTMAIL_API_KEY="<key from .env>"
agentmail inboxes:messages send \
  --inbox-id "srv838555@digital-ethnicity.com" \
  --to "bennie.williams36@gmail.com" \
  --subject "Job Application Submitted: <position> - <company>" \
  --text "Bennie,

Your Hermes Agent submitted a job application:

POSITION: <title>
COMPANY: <company>
LOCATION: <location>
SALARY: <salary>
FIT RATING: <fit rating>

APPLICATION DETAILS:
- Email: srv838555@digital-ethnicity.com
- Phone: 757-652-6922
- Resume: <filename>.pdf

APPLY HERE: <url>

APPLICATION LOG: Nextcloud > Job-Applications > _applications-log

---
Sent by Hermes Agent via AgentMail"
```

**CRITICAL:** Always send to bennie.williams36@gmail.com, NOT ben@benniewilliams.com.

### Application Log Format
Create `Job-Applications/_applications-log/<company>-<role>-<date>.md` with:
- Position details (title, company, location, salary)
- Fit rating and assessment summary
- Materials submitted (resume, cover letter filenames)
- Application URL
- Status (submitted/pending manual)
- Expected next steps

## Search Fallback: AnySearch CLI

When `web_search` tool returns empty results (common in cron environments), fall back to AnySearch CLI:

```bash
python3 /root/.hermes/skills/search/anysearch/scripts/anysearch_cli.py search "IT Director job Maryland" --max_results 5
```

AnySearch uses a different API and often returns results when Tavily-backed web_search fails. Use for:
- Finding fresh job postings
- Company research
- Verifying job posting URLs

## Automated Job Applications — Limitations

**Reality check:** Most job application sites have anti-bot protections, CAPTCHAs, and require authenticated sessions. Fully automated applying is extremely difficult.

### What CAN be automated:
- **LinkedIn Easy Apply** — if user is logged in via browser session
- **Simple company career pages** — some accept direct submissions without heavy bot protection
- **USAJobs.gov** — federal applications have standardized process (but require login.gov auth)
- **Pre-filled application packages** — resume + cover letter + pre-filled form data ready for user to click submit

### What CANNOT be reliably automated:
- Sites with CAPTCHAs (Indeed, Glassdoor, most company portals)
- Sites requiring account creation
- Complex multi-step application flows
- Sites that block browser automation
- Federal jobs requiring login.gov authentication + online assessments

### User Preference (July 2026)
User prefers applying directly on company career sites, NOT through LinkedIn or job boards. When suggesting application approach, prioritize direct company career page URLs over aggregated job board links.

## Federal Resume Format

When applying to USAJobs.gov positions, the standard private-sector resume format will NOT work. Federal resumes require:

### Key Differences from Private Sector
- **Length**: 4-6 pages (not 1-2)
- **Hours per week**: Must include for each position
- **Supervisor info**: Name, phone, and whether they may be contacted
- **Salary**: For each position
- **Detailed duties**: Expand each role with specific duties mapped to the job announcement's specialized experience requirements
- **Competency narratives**: Address each of the 4 IT competencies (Attention to Detail, Customer Service, Oral Communication, Problem Solving)

### Federal Resume Structure
```
[NAME]
[Address] | [Phone] | [Email]

WORK EXPERIENCE

[Job Title]
[Agency/Company] | [City, State]
[Start Date] – [End Date] | [Hours per week: 40]
[Salary: $XXX,XXX/year]
Supervisor: [Name], [Phone] (May/May not contact)

Duties:
• [Duty mapped to specialized experience requirement 1]
• [Duty mapped to specialized experience requirement 2]
• [Duty mapped to IT competency: Attention to Detail]
• [Duty mapped to IT competency: Customer Service]
...

EDUCATION
[Degree] | [University] | [Year]

CERTIFICATIONS
[Cert name] | [Issuing body] | [Date]
```

### USAJobs Application Process
1. Create/login to USAJobs account (requires login.gov authentication)
2. Build federal resume in USAJobs resume builder OR upload PDF
3. Complete online assessments (must finish within 48 hours of applying)
4. Upload supporting documents (DD-214, transcripts, certifications)
5. Answer occupational questionnaire
6. Submit

## Related Files
- `references/agentmail-setup.md` - AgentMail API setup, CLI commands, inbox management for job application emails
- `references/wordpress-form-submission.md` - Direct form submission via curl for WP Job Manager, WPForms, Contact Form 7
## Related Files
- `references/agentmail-setup.md` - AgentMail API setup, CLI commands, inbox management for job application emails
- `references/wordpress-form-submission.md` - Direct form submission via curl for WP Job Manager, WPForms, Contact Form 7
- `references/pdf-generation-linux.md` - weasyprint setup, HTML resume template, markdown-to-HTML converter
- `references/docx-handling.md` - DOCX reading/writing techniques and LinkedIn extraction patterns
- `references/user-baseline-resume.md` - User's baseline resume for tailoring
- `references/linkedin-extraction.md` - LinkedIn job posting extraction workflow (dismiss dialog + console extract)
- `references/workflow-and-extraction.md` - Standard 4-file output, LinkedIn extraction JS, comparison tables, assessment structure
- `references/docx-generation.md` - python-docx setup, resume/cover letter DOCX formatting patterns, section border XML
- `references/autonomous-job-search-pattern.md` - Cron-based job search agent: search queries, filtering, WebDAV upload, digest format
- `references/federal-resume-format.md` - USAJobs.gov federal resume template, IT competencies, occupational questionnaire tips
- `scripts/convert_resumes_to_pdf.py` - Batch convert all markdown resumes/cover letters to styled PDF and upload to Nextcloud
- `scripts/convert_resumes_to_pdf.py` - Batch convert all markdown resumes/cover letters to styled PDF and upload to Nextcloud