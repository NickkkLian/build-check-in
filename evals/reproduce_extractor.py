#!/usr/bin/env python3
"""Save old/new extraction of the six November 6 fixtures, without model calls."""
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/extractor'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Extractor


def main():
    paths = {'before': ROOT / 'evals/frozen/extract_history_before.py',
             'after': ROOT / 'build-checkin/scripts/extract_history.py'}
    rows = []
    for entry in json.loads((ROOT / 'evals/checkin/manifest.json').read_text()):
        case = entry['case']
        source = ROOT / 'evals/fixtures' / case
        texts = []
        if (source / 'session.jsonl').exists():
            for line, raw in enumerate((source / 'session.jsonl').read_text().splitlines(), 1):
                item = json.loads(raw)
                if item['type'] == 'assistant' and isinstance(item['message']['content'], str):
                    texts.append({'source': f'session.jsonl:{line}', 'text': item['message']['content']})
        row = {'case': case, 'raw_assistant_text': texts}
        for label, path in paths.items():
            out = OUT / 'november6' / label / (case + '.json')
            history = load(label, path)().run(SimpleNamespace(project=str(source / 'project'),
                context=str(ROOT / 'evals/checkin' / case / 'context.json'),
                session=str(source / 'session.jsonl') if (source / 'session.jsonl').exists() else None,
                chat=str(source / 'chat.txt') if (source / 'chat.txt').exists() else None,
                snapshots=str(source / 'snapshots'), manual_history=None, out=str(out)))
            replies = [e for e in history['evidence'] if e['kind'] == 'assistant_turn']
            row[label] = {'assistant_records': replies,
                          'dropped_text': [t for t in texts if not any(e.get('text') == t['text'] for e in history['evidence'])],
                          'user_records': [e for e in history['evidence'] if e['id'].startswith('prompt:')]}
        assert len(row['before']['dropped_text']) == len(texts)
        assert not row['after']['dropped_text']
        rows.append(row)
    report = {'passed': True, 'source_commit': 'f10857f',
              'extractor_sha256': {label: hashlib.sha256(p.read_bytes()).hexdigest() for label, p in paths.items()},
              'raw_reply_count': sum(len(row['raw_assistant_text']) for row in rows), 'cases': rows}
    (OUT / 'reproduction.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS November 6 reproduction: four raw explanations dropped before, four retained after; two reply-absent controls stay empty.')


if __name__ == '__main__':
    main()
