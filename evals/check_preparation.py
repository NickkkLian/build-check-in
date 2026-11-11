#!/usr/bin/env python3
"""Verify that the dry-run auditor rejects mismatched inputs and leaked answers."""
import argparse
from pathlib import Path

from audit_prepared import audit, ROOT
from score_checkin import citations

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run-id', required=True)
args = parser.parse_args()
runroot = ROOT / 'evals/runs' / args.run_id
report = audit(runroot)
assert report['kind'] == 'dry-run'
first = report['runs'][0]
inputs = runroot / first['relative_dir'] / 'work/input'
history = inputs / 'history.json'
original = history.read_bytes()
try:
    history.write_bytes(original + b'\n')
    try:
        audit(runroot)
    except AssertionError:
        print('PASS auditor rejects altered history in one arm')
    else:
        raise AssertionError('Auditor accepted unequal history')
finally:
    history.write_bytes(original)
leaked = inputs / 'expected.json'
assert not leaked.exists()
try:
    leaked.write_text('{}\n')
    try:
        audit(runroot)
    except AssertionError:
        print('PASS auditor rejects expectations leaked into model inputs')
    else:
        raise AssertionError('Auditor accepted expectation leakage')
finally:
    leaked.unlink()
assert citations('[assistant:1]', {'assistant:1'}) == (['assistant:1'], [])
assert citations('[assistant:999]', {'assistant:1'}) == (['assistant:999'], ['assistant:999'])
print('PASS scorer recognises valid and invalid assistant citations')
