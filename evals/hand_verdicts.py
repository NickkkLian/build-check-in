#!/usr/bin/env python3
"""Materialise the evaluator's hand judgments and count them without model calls.

The P/F/N matrices and quotations below were written after reading all 54 outputs
against the frozen inputs. This is a transcription of human-style close reading,
not an automatic semantic scorer. Re-running it reproduces the counts only.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'verification/heldout/runs'
ARMS = ('plain', 'rules', 'skill')
CRITERIA = {
    'step1': ('shape', 'moments', 'open', 'withholds_answer', 'action_attribution', 'supported_premises', 'key_citations', 'contribution_supported', 'privacy'),
    'step2': ('family_supported', 'family_no_learning', 'family_quote_rule', 'family_format_approval', 'flags', 'student_section', 'student_answers', 'student_ai_facts', 'student_hold', 'privacy', 'instructor_supported'),
    'drill': ('gate', 'refusal_no_preview', 'predict_before_failure', 'withholds_cause_fix', 'attribution', 'events_supported', 'anonymous', 'workflow'),
}
# Each line is one explicit manual judgment matrix, in CRITERIA order.
MATRICES = {
    'step1': {
        'queue-end':      {'skill':'P P P P P P P F P', 'rules':'P P P P P P P F P', 'plain':'P F P F F F F P P'},
        'garden-units':   {'skill':'P P P P P P P P P', 'rules':'P P P P P P P P P', 'plain':'P P P F F F F P P'},
        'map-offset':     {'skill':'P P P P P F P P P', 'rules':'P F P P P F P P P', 'plain':'P P P F P F F P P'},
        'gallery-case':   {'skill':'P P P P P P P P P', 'rules':'P P P P P P P F P', 'plain':'P F F F F F F P P'},
        'receipt-total':  {'skill':'P P P P P P P F P', 'rules':'P F P P P P P F P', 'plain':'P P P F F F F P P'},
        'shelf-boundary': {'skill':'P F P P P F P F P', 'rules':'P P P P P P P F P', 'plain':'P P F F P P F P P'},
    },
    'step2': {
        'queue-end':      {'skill':'P P P P P P P P P P F', 'rules':'P P P P P P P P F P P', 'plain':'F F F F P F N N N P P'},
        'garden-units':   {'skill':'P P P P N P P P N P P', 'rules':'P P P P N P P P N P P', 'plain':'F F F F N F N N N P F'},
        'map-offset':     {'skill':'P P P P P P P P N P P', 'rules':'P P F P P P P P N P P', 'plain':'F P P F P F N N N P P'},
        'gallery-case':   {'skill':'P P P P P P P F N P P', 'rules':'P P P P P P F F N P F', 'plain':'F P P F P F N N N P P'},
        'receipt-total':  {'skill':'P P P P P P P P P P P', 'rules':'P P P P P P P F F P P', 'plain':'P P P F P F N N N P P'},
        'shelf-boundary': {'skill':'P P P P N P P P N P F', 'rules':'P P P P N P P P N P F', 'plain':'F P F F N F N N N P P'},
    },
    'drill': {
        'queue-end':      {'skill':'P N P P P P P P', 'rules':'P N P P P F P P', 'plain':'P N F F P P F F'},
        'garden-units':   {'skill':'P N P P P P P P', 'rules':'P N P P F F P P', 'plain':'P N F F F F P F'},
        'map-offset':     {'skill':'P N P P P P P P', 'rules':'P N P P P P P P', 'plain':'P N F F P F P F'},
        'gallery-case':   {'skill':'P P N N N N N N', 'rules':'P P N N N N N N', 'plain':'P F N N N N N N'},
        'receipt-total':  {'skill':'P N P P P P P P', 'rules':'P N P P P P P P', 'plain':'P N F P F F P F'},
        'shelf-boundary': {'skill':'P P N N N N N N', 'rules':'P P N N N N N N', 'plain':'P F N N N N N N'},
    },
}

# Failure explanations are grounded in exact spans. Cross-cutting format failures
# use the whole relevant section so the reviewer can inspect the absent structure.
FINDINGS = {
    'queue-end/step1/skill': [('contribution_supported', 'The history shows no AI explanation text', 'The raw session contains an assistant explanation after test-1. The extractor drops assistant prose.')],
    'queue-end/step1/rules': [('contribution_supported', 'The record shows no AI replies or explanations.', 'The raw session contains the AI explanation. The additional [consent] token is not a valid evidence ID.')],
    'queue-end/step1/plain': [('moments', 'Suppose `serve` is called on an empty list.', 'Q4 is a generic hypothetical without a recorded moment.'), ('withholds_answer', 'Version 3 uses `items.pop(0)`.', 'Gives the final fix in the student copy.'), ('action_attribution', 'The only check you ran', 'The assistant ran the check. Also fails supported_premises.')],
    'garden-units/step1/plain': [('withholds_answer', 'In version 3 you wrote `litres * 1000`.', 'Supplies the final fix and flattens the hand-edit self-report.'), ('action_attribution', 'At version 2 you changed the multiplier from 100 to 10', 'The AI made version 2. Also fails supported_premises.')],
    'map-offset/step1/skill': [('supported_premises', 'Walk me through how you decided it was right', 'Presupposes student validation of version 3. The source says no author or run was recorded. This is the strict premise reading.')],
    'map-offset/step1/rules': [('supported_premises', 'how did you find out it was the right one?', 'Presupposes student validation. The source records neither a check nor a correct result.'), ('moments', 'How would you check that the route picker returns the right point for any chosen number?', 'Q5 is generic transfer, without a named history moment.')],
    'map-offset/step1/plain': [('withholds_answer', 'Version 3 is `points[index]`.', 'Supplies the final fix.'), ('supported_premises', 'If you asked for index 2 and the points were hill, ridge, lake, what would it return', 'Version 1 indexes position 3 and raises IndexError. It cannot match the hill/lake report as the rest of Q1 presupposes.')],
    'gallery-case/step1/rules': [('contribution_supported', 'No AI replies or explanations are recorded', 'The raw session contains the AI explanation of case sensitivity.')],
    'gallery-case/step1/plain': [('moments', 'what should `is_photo` return for', 'Q1 is a generic truth-table question without a history moment.'), ('open', 'would you have predicted that?', 'Q3 asks a yes/no question.'), ('withholds_answer', 'why does comparing against lowercase', 'Q4 supplies the normalization mechanism and fix.'), ('action_attribution', 'Before you ran it', 'The assistant ran the check. Also fails supported_premises.')],
    'receipt-total/step1/skill': [('contribution_supported', 'The history has no AI explanation text.', 'The raw session contains the explanation that the fee is subtracted.')],
    'receipt-total/step1/rules': [('moments', 'Imagine the service fee on a receipt was 5 instead of 2.', 'Q5 is transfer without a named history moment.'), ('contribution_supported', 'No recorded AI reply explains any cause or fix', 'The raw session contains the AI explanation of subtraction.')],
    'receipt-total/step1/plain': [('withholds_answer', 'the line became `return sum(prices) + 0`', 'Supplies the changed code as part of the answer to why version 2 failed.'), ('action_attribution', 'The check you ran', 'The assistant ran it. Also fails supported_premises.')],
    'shelf-boundary/step1/skill': [('moments', 'Your idea says a shelf is full as soon as used slots equal capacity.', 'Q4 asks from the idea without a history moment.'), ('supported_premises', 'how did you decide what to try?', 'The writer and decision-maker for version 3 are unknown. Strict premise reading.'), ('contribution_supported', 'The "prompts" are staff notes, not words the student typed', 'The supplied chat labels these turns USER. No source establishes they were typed by staff.')],
    'shelf-boundary/step1/rules': [('contribution_supported', 'staff notes, not messages the student wrote', 'The raw chat labels these USER messages. The model invents staff authorship.')],
    'shelf-boundary/step1/plain': [('open', 'Does the "expected True, got False" failure still happen?', 'Q3 asks yes/no.'), ('withholds_answer', 'The final version is `return used >= capacity`.', 'Supplies the final fix.')],
    'queue-end/step2/skill': [('instructor_supported', 'Who ran each test command is not shown in the record', 'Each Bash call is in an assistant turn. Also says the file write has no successful record although File written is a non-error result. Adds a public-consent gate to the private family note.')],
    'queue-end/step2/rules': [('student_hold', 'Hold: go over answers A3', 'Hold is above the student section heading. It is lost when that section is handed over alone.')],
    'queue-end/step2/plain': [('family_supported', 'Ari wrote a small check', 'The AI wrote it.'), ('family_no_learning', 'Ari could explain what went wrong', 'Asserts ability instead of quoting the answer.')],
    'garden-units/step2/plain': [('family_supported', 'Bea then worked out herself', 'The AI stated the conversion first. Neither the log nor answer shows independent discovery. Also states the project is unpublished without evidence.'), ('family_no_learning', 'She can explain why the answer should be 2000.', 'Asserts ability beyond the quote. The family rule prohibits this claim.'), ('instructor_supported', "She doesn't say who made the edit", 'A3 explicitly says I changed the multiplier by hand.')],
    'map-offset/step2/rules': [('family_quote_rule', '"I am not sure what that change did."', 'Quotes an I-do-not-know answer where the rules require the factual fallback.')],
    'map-offset/step2/plain': [('family_supported', "Cleo also hasn't run a test yet", 'Absence of a recorded run is turned into a claim that none occurred.')],
    'gallery-case/step2/skill': [('student_ai_facts', '### Version 2', 'Student section stops at version 2. It omits the recorded version-3 AI edit and test. This is the protocol\'s strict factual-completeness reading.')],
    'gallery-case/step2/rules': [('student_answers', 'Your three answers are', 'Drops the period from I do not know., omits unchanged A1/A2 blocks, and calls [not answered] one of the student\'s answers.'), ('student_ai_facts', 'No answers can be shown yet.', 'No versioned AI facts, including the recorded final test.'), ('instructor_supported', "the record doesn't say who ran it", 'The Bash call is in an assistant turn.')],
    'gallery-case/step2/plain': [('family_supported', 'the one example check we ran', 'Transfers the AI run to an unspecified we. The record shows an assistant tool call.')],
    'receipt-total/step2/rules': [('student_hold', 'Hold: go over answers A3', 'Hold is outside the student section.'), ('student_ai_facts', 'AI did: Changed line 2', 'Student section mentions the final edit but omits the recorded AI test and pass.')],
    'shelf-boundary/step2/skill': [('instructor_supported', 'The note comes from you.', 'The source labels it USER, with no established staff authorship.')],
    'shelf-boundary/step2/rules': [('instructor_supported', 'a staff note, not a rerun', 'No source establishes staff authorship of the USER message.')],
    'shelf-boundary/step2/plain': [('family_supported', 'the class looked at three versions', 'No class activity is recorded.')],
    'queue-end/drill/rules': [('events_supported', 'The record shows no explanation of the cause from the AI.', 'The raw session contains the AI explanation.')],
    'queue-end/drill/plain': [('predict_before_failure', 'expected', 'The introductory source recap shows the actual failure before prediction.'), ('withholds_cause_fix', 'Version 3 used `items.pop(0)`', 'The introductory recap gives the fix before any written explanation.'), ('anonymous', 'Queue Board', 'The introduction names the source project.')],
    'garden-units/drill/rules': [('attribution', 'the history does not show who ran it', 'The last Bash call is recorded in an assistant turn. Also fails events_supported.')],
    'garden-units/drill/plain': [('attribution', 'The student then typed 1000 by hand', 'Turns a self-report into an established action. Also fails events_supported.'), ('predict_before_failure', 'Running it prints', 'Shows the failure before prediction.'), ('withholds_cause_fix', 'The student then typed 1000 by hand', 'Introductory note supplies the final fix before a written explanation.')],
    'map-offset/drill/plain': [('predict_before_failure', 'Running it prints `hill`.', 'Actual output precedes prediction.'), ('withholds_cause_fix', 'The Off-by-One Pick', 'The title names the causal mechanism before a written explanation. Round 2 also says every answer is one place too far.'), ('events_supported', 'Names and code are not copied from the student', 'The two-line function is verbatim snapshot code, despite the denial. This is a source-provenance error, not an invented student event.')],
    'gallery-case/drill/plain': [('refusal_no_preview', "**The fix:** `tag.lower() == 'photo'`.", 'Refuses a full drill but exposes the source bug and fix. It also asks for the student to re-consent, although family agreement is required.')],
    'receipt-total/drill/plain': [('predict_before_failure', 'It printed:', 'Shows the failure without a prediction step.'), ('attribution', 'A student, or an AI assistant, tries this change', 'The source establishes the AI made version 2. Also fails events_supported. The introduction incorrectly attributes consent to the student.')],
    'shelf-boundary/drill/plain': [('refusal_no_preview', '**The bug:**', 'Refuses a full drill but provides the bug, failed edit and final fix. It asks for the student\'s consent rather than the family\'s agreement.')],
}


def section(text, start, end=None):
    match = re.search(start, text, re.I | re.M)
    if not match:
        return text.strip()
    tail = text[match.start():]
    stop = re.search(end, tail[1:], re.I | re.M) if end else None
    return tail[:stop.start() + 1].strip() if stop else tail.strip()


manifest = json.loads((RUNS / 'manifest.json').read_text())
rows = []
for entry in manifest['runs']:
    name, task, arm = entry['case'], entry['task'], entry['arm']
    output = (RUNS / entry['relative_dir'] / 'output.md').read_text()
    labels = MATRICES[task][name][arm].split()
    assert len(labels) == len(CRITERIA[task])
    findings = FINDINGS.get('/'.join((name, task, arm)), [])
    assert all(quote in output for _, quote, _ in findings), (name, task, arm)
    quotes = {criterion: (quote, reason) for criterion, quote, reason in findings}
    decisions = {}
    for criterion, code in zip(CRITERIA[task], labels):
        verdict = {'P':'pass', 'F':'fail', 'N':'n/a'}[code]
        if task == 'step1':
            evidence = section(output, r'^##.*(?:Student questions|Questions for|Questions for|1\. Questions)', r'^## ') if criterion not in ('key_citations', 'contribution_supported') else section(output, r'^##.*(?:Instructor key|Private AI contribution|Note for the instructor|2\. Note)')
        elif task == 'step2':
            evidence = section(output, r'^##.*(?:Family note|Weekly update|3\. Weekly)') if criterion.startswith('family') else section(output, r'^##.*(?:For you|Instructor flags|Note for the instructor|Reading the answers)')
        else:
            evidence = output.strip()
        quote, reason = quotes.get(criterion, (evidence, 'Read the quoted section against the frozen inputs using PROTOCOL.md. The explicit manual matrix records the verdict.'))
        if verdict == 'n/a':
            reason = 'Not applicable to this output. See the denominator rules in REPORT.md.'
        decisions[criterion] = {'verdict': verdict, 'quote': quote, 'reason': reason}
    rows.append({**entry, 'output_sha256': hashlib.sha256(output.encode()).hexdigest(), 'decisions': decisions,
                 'all_requirements': all(value != 'F' for value in labels),
                 'findings': [{'criterion': c, 'quote': q, 'reason': r} for c, q, r in findings]})
counts = {}
for task in CRITERIA:
    counts[task] = {}
    for arm in ARMS:
        relevant = [row for row in rows if row['task'] == task and row['arm'] == arm]
        counts[task][arm] = {criterion: dict(Counter(row['decisions'][criterion]['verdict'] for row in relevant)) for criterion in CRITERIA[task]}
        counts[task][arm]['all_requirements'] = dict(Counter('pass' if row['all_requirements'] else 'fail' for row in relevant))
report = {'method': 'One evaluator read all 54 outputs in full. Matrices are manually assigned. This script only transcribes evidence and counts verdicts.',
          'reviewer_limit': 'The evaluator also wrote the new cases, changed the four skill rules, and fixed the scorer. This review is not blinded or independently adjudicated.',
          'counts': counts, 'rows': rows}
(ROOT / 'verification/heldout/hand-review.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
lines = ['| Task and requirement | Plain | Plain plus rules | Skill |', '| --- | --- | --- | --- |']
for task in CRITERIA:
    for criterion in (*CRITERIA[task], 'all_requirements'):
        cells = []
        for arm in ARMS:
            counter = counts[task][arm][criterion]
            denominator = counter.get('pass', 0) + counter.get('fail', 0)
            cells.append(f"{counter.get('pass', 0)}/{denominator}" if denominator else 'n/a')
        lines.append('| ' + task + ' / ' + criterion + ' | ' + ' | '.join(cells) + ' |')
(ROOT / 'verification/heldout/hand-table.md').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines))
