# Pitfalls & Lessons Learned

## LinkedIn Extraction

**Problem:** `web_extract` returns "Website Not Supported" for all LinkedIn URLs.

**Solution:** Use the browser tool (CDP) instead:
1. `browser_navigate` to LinkedIn job URL
2. Dismiss sign-in dialog (click the "Dismiss" button)
3. Extract via `browser_console`: `document.querySelector('main')?.innerText`

**Pitfall:** The browser is an isolated session — it cannot see the user's logged-in LinkedIn. For content behind auth walls, ask the user to paste the posting text.

## web_search Emptiness

**Problem:** `web_search` (Tavily-backed) frequently returns empty results in cron environments.

**Solution:** Fall back to AnySearch CLI:
```bash
python3 /root/.hermes/skills/search/anysearch/scripts/anysearch_cli.py search "query" --max_results 5
```

AnySearch uses a different API and often succeeds when Tavily fails.

## Resume Constraints

**Problem:** The agent occasionally generates incorrect titles or phrases that violate the user's strict resume constraints.

**Solution:** The skill enforces these non-negotiable rules:
- CNH: "Senior Manager, Data Center & Infrastructure Operations" (NEVER "manages a $10M budget")
- Accenture: "Business & Technology Delivery Manager" (NEVER "Senior Manager")
- Navy: "Disbursing Clerk who served as de facto IT" (NEVER "Systems Administrator")
- NO active security clearance listed
- NO WordPress experience

These are embedded in the skill and the cron prompt loads them as "CRITICAL" rules.

## Auto-Apply Limitations

**Problem:** Most job sites have anti-bot protections — Dice, LinkedIn, Workday, Greenhouse all require authenticated sessions.

**Reality:** Auto-apply works for ~10% of postings (simple WordPress forms, some company career pages). The agent correctly falls back to "materials prepared, manual submission required" for the remaining 90%.

**What works:** Simple HTML forms without CAPTCHA (WP Job Manager, WPForms, Contact Form 7 on WordPress sites).

**What doesn't:** LinkedIn Easy Apply, Dice, Indeed, Workday, Greenhouse, Lever, any site with Cloudflare Turnstile or reCAPTCHA.

## Shell Escaping with Notion API

**Problem:** URLs containing `&` in JSON passed to `curl -d` are interpreted as shell background operators.

**Wrong:**
```bash
curl -d '{"url": "https://example.com?a=1&b=2"}'
# Shell interprets &b=2 as background command
```

**Right:**
```bash
echo '{"url": "https://example.com?a=1&b=2"}' > /tmp/payload.json
curl -d @/tmp/payload.json
```

## PDF Generation

**Linux:** WeasyPrint works well after `uv pip install weasyprint`.

**macOS:** WeasyPrint fails without homebrew pango/gobject. Use Chrome headless instead:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --print-to-pdf="/tmp/resume.pdf" \
  "file:///tmp/resume.html"
```

## Browserbase Configuration

**Problem:** Setting `browser.engine = browserbase` mid-session doesn't take effect.

**Solution:** Requires `/reset` or starting a new session. The browser continues using local Chromium until a fresh session is started.

## Experience Weighting

**Problem:** The agent initially undervalued defense consulting experience when assessing PE/advisory roles.

**Fix:** The skill now enforces:
- Accenture (9 years) = Big 4 consulting delivery → IS consulting experience
- Lockheed Martin (8.5 years) = Enterprise-scale programs → IS consulting muscle
- Don't frame these as "gaps" — they're direct qualifications

## Empty Run Handling

**Problem:** Cron jobs delivering empty "nothing found" messages are noise.

**Solution:** When no new jobs are found, respond with exactly `[SILENT]`. Hermes suppresses delivery — no Telegram notification, no spam.

## Mac Python (Hermes-Master)

**Problem:** `python3` on the Mac is miniconda 3.13. Pip-installed packages go to Python 3.12 site-packages and are invisible.

**Fix:** Use system Python explicitly:
```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 script.py
```

## Config File Location

The cron prompt references files at absolute paths:
- `/root/.hermes/scripts/job-search-criteria.md`
- `/root/.hermes/scripts/job-auto-apply-config.md`

These must exist on the host running the cron scheduler. If migrating to a different host, update paths.

## Model Selection

The cron job uses the default model configured in Hermes. Currently MiniMax-M3. Model choice affects:
- Job assessment quality (reasoning depth)
- Resume tailoring accuracy (constraint adherence)
- Digest formatting (HTML quality)

No model override is pinned on the job — it uses whatever the scheduler's default model is.
