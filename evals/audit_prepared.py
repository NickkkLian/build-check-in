#!/usr/bin/env python3
"""Audit a full frozen three-arm round, dry or completed, without any model call."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import re

from frozen_inputs import verify
from runner_checkin import ARMS, TASKS, SKILL, command_for, prompt_for

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(runroot):
    manifest = json.loads((runroot / 'manifest.json').read_text())
    suite = ROOT / manifest['suite_root']
    assert suite.resolve().is_relative_to(ROOT / 'evals'), 'Suite must be repository-local'
    assert verify(suite / 'FROZEN.txt') == manifest['frozen_files']
    assert sha(suite / 'FROZEN.txt') == manifest['freeze_sha256']
    assert sha(SKILL / 'SKILL.md') == manifest['skill_sha256']
    assert sha(SKILL / 'scripts/extract_history.py') == manifest['extractor_sha256']
    cases = json.loads((suite / 'checkin/manifest.json').read_text())
    assert set(manifest['arms']) == set(ARMS) and set(manifest['tasks']) == set(TASKS)
    grid = set(itertools.product([c['case'] for c in cases], TASKS, ARMS, range(1, manifest['runs_per_case'] + 1)))
    rows = manifest['runs']
    assert len(rows) == len(grid) == manifest['expected_total'], 'Incomplete or duplicated round'
    assert {(r['case'], r['task'], r['arm'], r['repeat']) for r in rows} == grid
    assert len({r['relative_dir'] for r in rows}) == len(rows)
    identical = {}
    counts, models = Counter(), Counter()
    verified = []
    for row in rows:
        expected_relative = f"{row['case']}/{row['task']}/{row['arm']}/{row['repeat']}"
        assert row['relative_dir'] == expected_relative
        target = runroot / expected_relative
        work, inputs = target / 'work', target / 'work/input'
        hashes = {p.relative_to(inputs).as_posix(): sha(p) for p in sorted(inputs.rglob('*')) if p.is_file()}
        key = (row['case'], row['task'])
        assert hashes == identical.setdefault(key, hashes), 'Arms or repeats received different evidence'
        assert 'expected.json' not in hashes and ('answers.md' in hashes) == (row['task'] == 'step2')
        assert sha(target / 'expected.json') == sha(suite / 'checkin' / row['case'] / 'expected.json')
        assert sha(target / 'history.json') == sha(inputs / 'history.json')
        for p in (suite / 'fixtures' / row['case']).rglob('*'):
            if p.is_file():
                assert sha(p) == sha(inputs / p.relative_to(suite / 'fixtures' / row['case']))
        assert sha(inputs / 'context.json') == sha(suite / 'checkin' / row['case'] / 'context.json')
        if row['task'] == 'step2':
            assert sha(inputs / 'answers.md') == sha(suite / 'checkin' / row['case'] / 'answers.md')
        assert (target / 'prompt.txt').read_text() == prompt_for(row['task'], row['arm'], inputs) + '\n'
        invocation = json.loads((target / 'invocation.json').read_text())
        assert invocation['argv'] == command_for(row['arm'], work)
        assert invocation['cwd'] == str(work)
        assert invocation['will_execute'] == (manifest['kind'] == 'claude')
        staged = work / '.claude/skills/build-checkin'
        if row['arm'] == 'skill':
            shipped = {p.relative_to(SKILL).as_posix(): sha(p) for p in SKILL.rglob('*')
                       if p.is_file() and 'examples' not in p.relative_to(SKILL).parts and '__pycache__' not in p.parts and p.suffix != '.pyc'}
            installed = {p.relative_to(staged).as_posix(): sha(p) for p in staged.rglob('*') if p.is_file()}
            assert installed == shipped, 'Staged skill differs or exposes worked examples'
        else:
            assert not staged.exists()
        history = json.loads((target / 'history.json').read_text())
        expected = json.loads((target / 'expected.json').read_text())
        replies = [e for e in history['evidence'] if e['kind'] == 'assistant_turn']
        assert bool(replies) == expected['ai_reply_recorded'], 'Recorded replies missing or invented in preparation'
        assert all(p.get('actor') == 'unknown' for p in history['prompts'])
        meta = json.loads((target / 'meta.json').read_text())
        assert meta['kind'] == manifest['kind'] and not meta.get('error')
        assert all(meta[k] == row[k] for k in ('task', 'arm', 'repeat'))
        record = {**row, 'input_hashes': hashes}
        if manifest['kind'] == 'dry-run':
            assert not (target / 'output.md').exists() and not (target / 'envelope.json').exists()
        else:
            assert manifest['kind'] == 'claude'
            envelope = json.loads((target / 'envelope.json').read_text())
            assert envelope.get('subtype') == 'success' and not envelope.get('is_error') and not envelope.get('permission_denials')
            assert (target / 'output.md').read_text() == envelope['result'] + '\n'
            assert envelope['result'].strip()
            assert len(envelope.get('modelUsage', {})) == 1, 'Expected one resolved model per output'
            models.update(envelope['modelUsage'].keys())
            record['output_sha256'] = sha(target / 'output.md')
        counts[(row['task'], row['arm'])] += 1
        verified.append(record)
    assert len(models) <= 1, 'Different models across the round; do not pool results'
    return dict(passed=True, kind=manifest['kind'], prepared=len(rows),
                completed=len(rows) if manifest['kind'] == 'claude' else 0,
                frozen_files=manifest['frozen_files'], skill_sha256=manifest['skill_sha256'],
                extractor_sha256=manifest['extractor_sha256'], resolved_models=dict(models),
                counts=[dict(task=t, arm=a, count=n) for (t, a), n in sorted(counts.items())],
                matched_case_task_inputs=len(identical), runs=verified)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.run_id):
        parser.error('run-id must be simple')
    result = audit(ROOT / 'evals/runs' / args.run_id)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(f"PASS {result['kind']}: {result['prepared']} entries; {result['completed']} model outputs; "
          f"{result['frozen_files']} frozen hashes; {result['matched_case_task_inputs']} matched input groups")


if __name__ == '__main__':
    main()
