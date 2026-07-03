#!/usr/bin/env python3
"""Convert job application markdown files to PDF and upload to Nextcloud.

Usage:
    python3 convert_resumes_to_pdf.py

Reads all *-resume.md and *-cover-letter.md files from /tmp/,
converts to styled PDF via weasyprint, uploads to Nextcloud.

Requires: uv pip install weasyprint
"""

import os
import subprocess
import re

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

NC_URL = "https://nc.bwai.us/remote.php/dav/files/admin/Job-Applications"
NC_AUTH = "admin:22e146a6954b1ee6876d884a"

# ═══════════════════════════════════════════════════════════════════
# PDF TEMPLATE (HTML + CSS)
# ═══════════════════════════════════════════════════════════════════
# Professional letter-size PDF with:
#   - 0.75in top/bottom margins, 0.85in left/right
#   - Uppercase section headers with navy underline
#   - Page numbers at bottom center
#   - Blockquote styling for the apply link

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: letter;
    margin: 0.75in 0.85in;
    @bottom-center {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 9pt;
      color: #666;
    }}
  }}
  body {{
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.45;
    color: #1a1a1a;
  }}
  h1 {{ font-size: 20pt; margin: 0 0 4px 0; color: #1a3a5c; letter-spacing: 1px; }}
  h2 {{ font-size: 12pt; color: #1a3a5c; border-bottom: 1.5px solid #1a3a5c; padding-bottom: 3px; margin: 16px 0 8px 0; text-transform: uppercase; letter-spacing: 0.5px; }}
  h3 {{ font-size: 11pt; color: #2c5282; margin: 12px 0 4px 0; }}
  p {{ margin: 4px 0; }}
  ul {{ margin: 4px 0 8px 0; padding-left: 18px; }}
  li {{ margin-bottom: 3px; font-size: 10pt; }}
  blockquote {{ border-left: 3px solid #1a3a5c; padding: 6px 12px; margin: 8px 0; background: #f0f4f8; font-size: 9.5pt; color: #333; }}
  strong {{ color: #1a3a5c; }}
  hr {{ border: none; border-top: 1.5px solid #1a3a5c; margin: 12px 0; }}
</style>
</head>
<body>
{content}
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════════
# MARKDOWN → HTML CONVERTER
# ═══════════════════════════════════════════════════════════════════
# Converts a simplified subset of markdown to HTML for weasyprint.
# Supports: h1/h2/h3, bullet lists, blockquotes, bold, horizontal rules.

def md_to_html_simple(md_text):
    lines = md_text.split('\\n')
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
            continue
        if stripped.startswith('# ') and not stripped.startswith('## '):
            if in_list: html_lines.append('</ul>'); in_list = False
            html_lines.append(f'<h1>{stripped[2:]}</h1>')
            continue
        if stripped.startswith('## '):
            if in_list: html_lines.append('</ul>'); in_list = False
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
            continue
        if stripped.startswith('### '):
            if in_list: html_lines.append('</ul>'); in_list = False
            html_lines.append(f'<h3>{stripped[4:]}</h3>')
            continue
        if stripped in ('---', '***', '___'):
            if in_list: html_lines.append('</ul>'); in_list = False
            html_lines.append('<hr>')
            continue
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list: html_lines.append('<ul>'); in_list = True
            item = stripped[2:]
            item = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', item)
            html_lines.append(f'<li>{item}</li>')
            continue
        if stripped.startswith('> '):
            if in_list: html_lines.append('</ul>'); in_list = False
            text = stripped[2:]
            text = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', text)
            html_lines.append(f'<blockquote>{text}</blockquote>')
            continue
        if in_list: html_lines.append('</ul>'); in_list = False
        text = stripped
        text = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', text)
        html_lines.append(f'<p>{text}</p>')
    if in_list: html_lines.append('</ul>')
    return '\\n'.join(html_lines)

# ═══════════════════════════════════════════════════════════════════
# FILE PROCESSING PIPELINE
# ═══════════════════════════════════════════════════════════════════
# One file → markdown → HTML → PDF → Nextcloud upload

def process_file(md_path, nc_folder):
    # 1. Read markdown source
    with open(md_path, 'r') as f:
        md_content = f.read()
    # 2. Convert markdown to HTML
    html_content = md_to_html_simple(md_content)
    full_html = HTML_TEMPLATE.format(content=html_content)
    html_path = md_path.replace('.md', '.html')
    with open(html_path, 'w') as f:
        f.write(full_html)
    # 3. Convert HTML to PDF via weasyprint
    pdf_path = md_path.replace('.md', '.pdf')
    try:
        subprocess.run(['python3', '-c',
            f"from weasyprint import HTML; HTML('{html_path}').write_pdf('{pdf_path}')"],
            check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {e.stderr.decode()}")
        return False
    # 4. Upload PDF to Nextcloud via WebDAV
    filename = os.path.basename(pdf_path)
    nc_path = f"{NC_URL}/{nc_folder}/{filename}"
    result = subprocess.run([
        'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
        '-T', pdf_path, nc_path, '-u', NC_AUTH
    ], capture_output=True, text=True)
    status = result.stdout.strip()
    print(f"  {filename}: {status}")
    # 5. Cleanup temp HTML
    os.remove(html_path)
    return status == '201'


# ═══════════════════════════════════════════════════════════════════
# BATCH PROCESSING — File Manifest
# ═══════════════════════════════════════════════════════════════════
# Add (local_path, nc_folder) entries here for each batch run.
# Example:
#   ("/tmp/mccormick-resume.md", "mccormick_director-infrastructure"),
#   ("/tmp/mccormick-cover-letter.md", "mccormick_director-infrastructure"),

FILES = [
    # ("/tmp/company-resume.md", "company_folder"),
    # ("/tmp/company-cover-letter.md", "company_folder"),
]

# ═══════════════════════════════════════════════════════════════════
# MAIN — Batch Runner
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    success = failed = 0
    for md_path, nc_folder in FILES:
        if not os.path.exists(md_path):
            print(f"SKIP: {md_path}"); continue
        # Ensure Nextcloud folder exists
        subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
            '-X', 'MKCOL', f"{NC_URL}/{nc_folder}", '-u', NC_AUTH], capture_output=True)
        if process_file(md_path, nc_folder):
            success += 1
        else:
            failed += 1
    print(f"\\nDone: {success} PDFs uploaded, {failed} failed")
