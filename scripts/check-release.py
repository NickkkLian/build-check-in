#!/usr/bin/env python3
"""Audit this release folder and its archive without network access or dependencies."""
from pathlib import Path
from zipfile import ZipFile
from html.parser import HTMLParser
import argparse
import hashlib
import io
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--denylist', type=Path, help='Optional private JSON with a terms array; keep it outside the release.')
args = parser.parse_args()
terms = json.loads(args.denylist.read_text())['terms'] if args.denylist else []
checks, issues = [], []
counts = {'text': 0, 'binary': 0}
def check(ok, name):
    checks.append({'passed': bool(ok), 'check': name})
def inspect(name, data):
    # Dropping invalid bytes can join unrelated compressed bytes into fake emails.
    # Scan literal terms and key signatures in every byte; email syntax needs text.
    try:
        text = data.decode('utf-8')
        is_text = True
    except UnicodeDecodeError:
        text = data.decode('latin-1')
        is_text = False
    counts['text' if is_text else 'binary'] += 1
    # Only report the rule and filename, never the value of a possible secret.
    for i, term in enumerate(terms):
        if re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', text, re.I):
            issues.append({'file': name, 'rule': 'private denylist rule ' + str(i+1)})
    if ('/' + 'Users' + '/').lower() in text.lower():
        issues.append({'file': name, 'rule': 'absolute personal path'})
    for email in re.findall(r'\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b', text) if is_text else []:
        if not email.lower().endswith('.example'):
            issues.append({'file': name, 'rule': 'email outside reserved example domain'})
    for pattern in [r'\b(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{16,}', r'\bsk-(?:ant-|proj-)?[a-zA-Z0-9_-]{24,}', r'\bgh[pousr]_[a-zA-Z0-9]{30,}', r'\bAKIA[A-Z0-9]{16}\b', r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----']:
        if re.search(pattern, text):
            issues.append({'file': name, 'rule': 'possible credential pattern'})
    if name.endswith('.zip'):
        with ZipFile(io.BytesIO(data)) as archive:
            for item in archive.infolist():
                if not item.is_dir():
                    inspect(name + ':' + item.filename, archive.read(item))

files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts)
for p in files:
    rel = p.relative_to(ROOT).as_posix()
    if p.name == 'release-check.json':
        continue
    inspect(rel, p.read_bytes())
check(not issues, 'No private terms, personal paths, non-example emails or credential patterns, including ZIP members')
check(not any(p.name == '.git' for p in ROOT.rglob('.git')), 'Release has no inherited Git history')
check(all((ROOT / p).is_file() for p in ['index.html', 'README.md', 'LICENSE', '.nojekyll']), 'Root demo, README, MIT licence and Pages marker exist')
check('MIT License' in (ROOT / 'LICENSE').read_text(), 'MIT licence is present')

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags=[]
    def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)
html=(ROOT/'index.html').read_text();page=Page();page.feed(html)
csp=[a.get('content','') for t,a in page.tags if t=='meta' and a.get('http-equiv','').lower()=='content-security-policy']
check(len(csp)==1 and "connect-src 'none'" in csp[0] and "default-src 'none'" in csp[0], 'Demo CSP blocks external connections by default')
refs=[(t,k,v) for t,a in page.tags for k,v in a.items() if k in ('src','href','poster','action')]
readme_url = 'https://github.com/NickkkLian/build-check-in#readme'
check(all((t == 'a' and k == 'href' and v == readme_url) or v.startswith(('data:','#')) or (not re.match(r'^(?:[a-z][a-z\d+.-]*:|//|/)',v,re.I) and (ROOT/v).is_file()) for t,k,v in refs), 'Every demo reference is local or the approved GitHub README navigation link')
scripts=re.findall(r'<script\b[^>]*>(.*?)</script>',html,re.S|re.I)
js='\n'.join(scripts)
check(not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|importScripts|Worker|SharedWorker)\s*\(|\bimport\s*\(',js), 'Demo code has no network or dynamic-import API calls')
check(not re.search(r'@import|url\s*\(\s*[\'\"]?https?:',html,re.I), 'Demo CSS loads no remote resources')
result=subprocess.run(['node','--check','--input-type=commonjs'],input=js,text=True,capture_output=True)
check(result.returncode==0,'Inline demo JavaScript parses')
for p in sorted(ROOT.rglob('*.mjs')):
    result=subprocess.run(['node','--check',str(p)],text=True,capture_output=True)
    check(result.returncode==0,'JavaScript parses: '+p.relative_to(ROOT).as_posix())
passed=all(c['passed'] for c in checks)
report={'passed':passed,'checks':checks,'issues':issues,'files_scanned':len(files),'content_counts':counts,'email_scope':'UTF-8 text and ZIP text members; compressed media needs visual review','private_rules':len(terms),'demo_sha256':hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest()}
(ROOT/'verification').mkdir(exist_ok=True)
(ROOT/'verification/release-check.json').write_text(json.dumps(report,indent=2)+'\n')
for c in checks: print(('PASS ' if c['passed'] else 'FAIL ')+c['check'])
for issue in issues: print('FAIL '+issue['file']+': '+issue['rule'])
raise SystemExit(0 if passed else 1)
