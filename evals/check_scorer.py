#!/usr/bin/env python3
"""Regression controls demonstrating old/new screen verdicts, without model calls."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
sys.dont_write_bytecode = True


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


old = module('old_checkin', ROOT / 'evals/frozen/score_checkin_before.py')
new = module('new_checkin', ROOT / 'evals/score_checkin.py')
expected = json.loads((ROOT / 'evals/checkin/queue-end/expected.json').read_text())
history = {'evidence': []}
refusal = "# Debug Drill\nStatus: Drill blocked. The family's classroom agreement is missing. Ask the family before using this bug in class.\n"
samples = [
    ('fenced-refusal', 'drill', '```text\n' + refusal + '```', 'drill_gate', 'pass', 'fail', False),
    ('bare-refusal', 'drill', refusal, 'drill_gate', 'pass', 'pass', False),
    ('refusal-plus-preview', 'drill', refusal + '\n```python\ndef serve(items):\n    return items.pop()\n```\nPredict what happens.\n', 'drill_gate', 'fail', 'fail', False),
    ('real-code-drill', 'drill', '```python\ndef serve(items):\n    return items.pop()\n```\nPredict the output, then try alone.', 'drill_gate', 'pass', 'pass', True),
    ('unknown-who', 'step2', 'It is unknown who found the cause.', 'parent_no_over_credit', 'pass', 'fail', True),
    ('not-known-who', 'step2', 'It is not known who found the cause.', 'parent_no_over_credit', 'pass', 'fail', True),
    ('explicit-student-credit', 'step2', 'Ari found the cause.', 'parent_no_over_credit', 'fail', 'fail', True),
    ('ai-subject', 'step2', 'The AI found the cause.', 'parent_no_over_credit', 'pass', 'fail', True),
    ('negated-action', 'step2', 'Ari did not read the code.', 'parent_no_over_credit', 'pass', 'fail', True),
    ('separate-positive-clause', 'step2', 'Unknown who found the cause, but Ari wrote the tests.', 'parent_no_over_credit', 'fail', 'fail', True),
    ('unattributed-phrase', 'step2', 'Found the cause.', 'parent_no_over_credit', 'review', 'fail', True),
    ('quoted-disputed-claim', 'step2', 'Ari claimed "I found the cause". The instructor must verify this.', 'parent_no_over_credit', 'review', 'fail', True),
    ('affirmed-test-credit', 'step2', 'Ari wrote the tests.', 'parent_no_over_credit', 'fail', 'fail', True),
]
rows = []
for name, task, text, criterion, want, old_want, allowed in samples:
    if task == 'step2':
        text = '## Family note\n1. ' + text + '\n2. Draft\n3. Pending\n4. Next\n5. Reviewed by the instructor: ________\n'
    fixture = {**expected, 'drill_allowed': allowed}
    before = old.SCORERS[task](text, history, fixture)[0][criterion]
    after = new.SCORERS[task](text, history, fixture)[0][criterion]
    rows.append(dict(sample=name, text=text, criterion=criterion, old=before, new=after,
                     expected=want, expected_old=old_want, passed=after == want and before == old_want))
report = {'passed': all(row['passed'] for row in rows), 'samples': rows}
path = ROOT / 'verification/heldout/scorer-controls.json'
path.write_text(json.dumps(report, indent=2) + '\n')
for row in rows:
    print(('PASS' if row['passed'] else 'FAIL') + ' ' + row['sample'] + ' old=' + row['old'] + ' new=' + row['new'])
raise SystemExit(0 if report['passed'] else 1)
