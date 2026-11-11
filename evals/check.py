#!/usr/bin/env python3
"""Offline release and held-out evidence gate. No model, browser or network calls."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZipFile
from frozen_inputs import verify as verify_frozen

ROOT = Path(__file__).resolve().parents[1]
checks = []


def check(ok, name):
    checks.append({'passed': bool(ok), 'check': name})
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


for script in ('scripts/check.py', 'evals/check_extractor.py', 'evals/check_scorer.py', 'evals/hand_verdicts.py'):
    result = subprocess.run([sys.executable, '-B', script], cwd=ROOT, capture_output=True, text=True)
    print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='')
    check(result.returncode == 0, script)

result = subprocess.run([sys.executable, '-B', 'evals/score_checkin.py', '--runs', 'verification/heldout/runs',
                         '--out', 'verification/heldout/screen.json'], cwd=ROOT, capture_output=True, text=True)
print(result.stdout, end='')
check(result.returncode == 0, 'Three-arm pattern screen completes')
frozen = json.loads((ROOT / 'evals/frozen/SHA256.json').read_text())
check(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest for name, digest in frozen.items()), 'All 53 pre-tuning frozen files match')
check(verify_frozen(ROOT / 'evals/heldout-v2/FROZEN.txt') == 52, 'Second-round cases and unchanged written rules match all 52 frozen hashes')
manifest = json.loads((ROOT / 'verification/heldout/runs/manifest.json').read_text())
audit = json.loads((ROOT / 'verification/heldout/run-audit.json').read_text())
check(audit['completed'] == len(manifest['runs']) == 54 and not audit['errors'] and not audit['excluded'], '54 unique completed outputs with no exclusions')
check(audit['skill_sha256'] == hashlib.sha256((ROOT / 'build-checkin/SKILL.md').read_bytes()).hexdigest(), 'Shipped instructions match the evaluated instructions')
check(audit['resolved_models'] == {'claude-sonnet-5-5': 54}, 'Every output used the same resolved model')
review = json.loads((ROOT / 'verification/heldout/hand-review.json').read_text())
check(len(review['rows']) == 54 and len({row['relative_dir'] for row in review['rows']}) == 54, 'Every output has one hand-review record')
valid = True
markers = {'skill': 0, 'rules': 0}
for row in review['rows']:
    directory = ROOT / 'verification/heldout/runs' / row['relative_dir']
    output = (directory / 'output.md').read_text()
    envelope = json.loads((directory / 'envelope.json').read_text())
    valid &= hashlib.sha256(output.encode()).hexdigest() == row['output_sha256']
    valid &= envelope.get('result', '') + '\n' == output
    valid &= envelope.get('subtype') == 'success' and not envelope.get('is_error') and not envelope.get('permission_denials')
    valid &= all(item['quote'] in output for item in row['decisions'].values())
    valid &= all(item['quote'] in output for item in row['findings'])
    valid &= row['all_requirements'] == all(item['verdict'] != 'fail' for item in row['decisions'].values())
    if row['task'] == 'step2' and row['arm'] in markers:
        student = output.split('## For you (the student)', 1)[1]
        markers[row['arm']] += bool(re.search(r'\(no answer\)|\[not answered\]', student))
check(valid, 'All verdict quotations, output hashes, envelope results and rollups match')
check(markers == {'skill': 0, 'rules': 1}, 'Residual marker failure is retained in the rules arm')
check(all(data.get('q_no_fix', {}).get('pass', 0) == 6 for arm, data in json.loads((ROOT / 'verification/heldout/screen.json').read_text())['counts']['step1'].items() if arm in ('skill', 'rules')), 'Both rule-bearing arms retain all six answer-withholding screen passes')
for path in sorted((ROOT / 'evals').glob('*.py')):
    ast.parse(path.read_text())
check(True, 'All evaluation Python parses')
with ZipFile(ROOT / 'build-checkin.zip') as archive:
    check(archive.read('build-checkin/SKILL.md') == (ROOT / 'build-checkin/SKILL.md').read_bytes(), 'ZIP ships the evaluated instructions')
    check(b'2. Trace or compare:' in archive.read('build-checkin/examples/drill-output.md'), 'Handwritten drill example uses a diagnostic hint 2')

# Audit only the public tracked/candidate files. Execution work copies stay ignored.
listed = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT,
                        capture_output=True, check=True).stdout.decode().split('\0')
issues = []
private_terms = ('Built' + ' Young', 'Nick' + ' Lian')
for name in sorted(set(filter(None, listed))):
    path = ROOT / name
    if not path.is_file():
        continue
    data = path.read_bytes()
    blobs = [(name, data)]
    if path.suffix == '.zip':
        with ZipFile(path) as archive:
            blobs += [(name + ' member ' + member, archive.read(member)) for member in archive.namelist()]
    for label, blob in blobs:
        text = blob.decode('utf-8', errors='replace')
        if ('/' + 'Users' + '/') in text or any(term.lower() in text.lower() for term in private_terms):
            issues.append({'file': label, 'rule': 'personal path or private name/organisation'})
        if re.search(r'https?://[^\s<>\x22\x27]*@[0-9]', text):
            issues.append({'file': label, 'rule': 'unencoded package version URL'})
        if re.search(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}|sk-(?:ant-|proj-)?[A-Za-z0-9_-]{24,})\b', text):
            issues.append({'file': label, 'rule': 'credential-like signature'})
check(not issues, 'Public candidates and ZIP omit private names, paths, credential-like data and unencoded version URLs')
for issue in issues:
    print('FAIL ' + issue['file'] + ' ' + issue['rule'])
report = {'passed': all(item['passed'] for item in checks), 'checks': checks, 'privacy_issues': issues,
          'public_files_scanned': len(set(filter(None, listed)))}
(ROOT / 'verification/heldout/check-results.json').write_text(json.dumps(report, indent=2) + '\n')
raise SystemExit(0 if report['passed'] else 1)
