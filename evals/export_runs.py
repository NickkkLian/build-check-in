#!/usr/bin/env python3
"""Audit the completed comparison and export review evidence without local paths.

The original execution files stay in ignored evals/runs. Public prompts and argv use
<CHECKOUT> in place of the absolute checkout path. Envelope session identifiers are
omitted. Output text is retained byte for byte and checked against the envelope.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run-id', required=True)
args = parser.parse_args()
source = ROOT / 'evals/runs' / args.run_id
target = ROOT / 'verification/heldout/runs'
if target.exists():
    raise SystemExit('Refusing to overwrite exported evidence')
manifest = json.loads((source / 'manifest.json').read_text())
assert manifest['kind'] == 'claude' and manifest['expected_total'] == 54
assert len(manifest['runs']) == len({row['relative_dir'] for row in manifest['runs']}) == 54
frozen = json.loads((ROOT / 'evals/frozen/SHA256.json').read_text())
assert all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest for name, digest in frozen.items())
rules = (ROOT / 'build-checkin/SKILL.md').read_bytes()
counts = Counter()
models = Counter()
audit = []
input_hashes = {}
envelope_keys = ('type', 'subtype', 'is_error', 'result', 'permission_denials', 'modelUsage', 'usage',
                 'num_turns', 'total_cost_usd', 'duration_ms', 'duration_api_ms', 'stop_reason', 'terminal_reason')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


for entry in manifest['runs']:
    directory = source / entry['relative_dir']
    envelope = json.loads((directory / 'envelope.json').read_text())
    meta = json.loads((directory / 'meta.json').read_text())
    output = (directory / 'output.md').read_bytes()
    assert envelope.get('subtype') == 'success' and not envelope.get('is_error')
    assert not envelope.get('permission_denials') and not meta.get('error')
    assert output.decode() == envelope['result'] + '\n' and output.strip()
    assert meta['arm'] == entry['arm'] and meta['task'] == entry['task']
    counts[(entry['task'], entry['arm'])] += 1
    models.update(envelope['modelUsage'].keys())
    inputs = directory / 'work/input'
    hashes = {p.relative_to(inputs).as_posix(): sha(p.read_bytes()) for p in sorted(inputs.rglob('*')) if p.is_file()}
    key = (entry['case'], entry['task'])
    assert hashes == input_hashes.setdefault(key, hashes)
    assert (directory / 'expected.json').read_bytes() == (ROOT / 'evals/checkin' / entry['case'] / 'expected.json').read_bytes()
    prompt = (directory / 'prompt.txt').read_text()
    if entry['arm'] == 'skill':
        staged = directory / 'work/.claude/skills/build-checkin'
        assert (staged / 'SKILL.md').read_bytes() == rules and not (staged / 'examples').exists()
    if entry['arm'] == 'rules':
        assert rules.decode() in prompt
    exported = target / entry['relative_dir']
    exported.mkdir(parents=True)
    for name in ('output.md', 'history.json', 'expected.json', 'meta.json', 'stderr.txt'):
        shutil.copyfile(directory / name, exported / name)
    for name in ('prompt.txt', 'invocation.json'):
        (exported / name).write_text((directory / name).read_text().replace(str(ROOT), '<CHECKOUT>'))
    save(exported / 'envelope.json', {key: envelope[key] for key in envelope_keys if key in envelope})
    audit.append({**entry, 'output_sha256': sha(output), 'original_envelope_sha256': sha((directory / 'envelope.json').read_bytes()),
                  'exported_envelope_sha256': sha((exported / 'envelope.json').read_bytes()),
                  'omitted_envelope_keys': sorted(set(envelope) - set(envelope_keys)),
                  'input_hashes': hashes})
assert set(counts.values()) == {6} and len(counts) == 9
save(target / 'manifest.json', manifest)
save(ROOT / 'verification/heldout/run-audit.json', {
    'passed': True, 'expected': 54, 'completed': len(audit), 'errors': [], 'excluded': [],
    'resolved_models': dict(models), 'frozen_files_verified': len(frozen), 'skill_sha256': sha(rules),
    'counts': [{'task': task, 'arm': arm, 'count': count} for (task, arm), count in sorted(counts.items())],
    'export_policy': 'Only prompt/argv checkout paths and non-result envelope metadata differ. Output text is byte-identical to the original result plus newline.',
    'runs': audit})
print('Audited and exported 54 successful outputs. Nine task/arm cells each contain six runs.')
print('All arms have byte-identical case/task inputs. All skill and inline-rule copies match the evaluated instructions.')
