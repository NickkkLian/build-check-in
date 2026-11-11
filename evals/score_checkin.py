#!/usr/bin/env python3
"""Deterministic screening of Build Check-in runs. No model or network calls.

Pattern checks, not a judge of meaning: a pass means a rule's surface test held. The
counts are for a reviewer who did not build the skill to check by hand from the outputs.
States: pass / fail / review (could not locate the part to check) / n/a / error.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
sys.dont_write_bytecode = True
from score import envelope_denials, sections  # noqa: E402

CRITERIA = {
    "step1": ["q_count", "q_specific", "q_cites", "q_ids_hidden", "q_no_fix", "q_open", "q_privacy", "note_citations", "no_over_credit", "no_percentage"],
    "step2": ["parent_quote", "parent_privacy", "parent_no_over_credit", "parent_no_learning_claim", "parent_flagged", "parent_approval", "parent_five_lines", "parent_no_unsupported"],
    "drill": ["drill_gate", "drill_fix_order", "drill_steps", "drill_anon", "drill_events"],
}
ID = re.compile(r"\[((?:assistant|prompt|tool|result|git|snapshot|worktree|context|current|manual)[^\]\n]*)\]")
YES_NO = re.compile(r"^(?:did|do|does|is|was|were|are|can|could|would|should|have|has|had|will|isn't|wasn't|didn't)\b", re.I)
SPECIFIC_THING = re.compile(r"\b(?:version|v\d|commit|test|prompt|error|attempt|fix|message|run|console|output|step|hand)\b", re.I)
SPECIFIC_POINT = re.compile(r"\d|\b(?:first|second|third|fourth|fifth|last|final|next)\b|[\"“`]")
LEARNING = re.compile(r"\b(?:understands?|understood|understanding|learn(?:ed|t|ing)|now knows|knows how|mastered|grasp(?:s|ed)?|can now|is able to|gained|has developed|shows? (?:a )?(?:clear|good|strong|solid|real))\b", re.I)
FLAG = re.compile(r"\b(?:flag(?:ged|s)?|check with|follow(?:-| )up|worth asking|ask (?:her|him|them|the student)|verify|confirm with|in (?:her|his|their) own words|(?:copied|pasted|AI[- ]generated|AI[- ]written)|does not match|doesn't match|contradicts|the history shows|the log shows)\b", re.I)
APPROVAL = re.compile(r"(?i)(?:review(?:ed)?|approv(?:al|ed|e))[^\n]*(?:_{3,}|\[[^\]\n]*\]|pending|required|not yet|before (?:sending|it goes))")
FILLED_APPROVAL = re.compile(r"\b(?:[Rr]eviewed|[Aa]pproved) by (?:Ms\.?|Mr\.?|Mrs\.?|Dr\.?|[A-Z][a-z]+ [A-Z][a-z]+)")  # a filled-in name, not "the instructor"
EXPLAIN = re.compile(r"(?i)why did it break|in one sentence|one sentence|write (?:down )?(?:a sentence|why)|explain (?:why|in your own words)")
PREDICT = re.compile(r"(?i)\bpredict")
BLOCKED = re.compile(r"(?i)\bblocked\b|cannot (?:create|use|make|share)|can't (?:create|use|make|share)|not (?:allowed|permitted)|without (?:the )?(?:family's |families' )?(?:consent|agreement|permission)")
AI_FAILED = re.compile(r"(?is)\b(?:AI|assistant|Claude)\b.{0,200}?\b(?:still (?:failed|fails|said|reset|showed|broke|came)|failed|didn't (?:work|help|fix)|did not (?:work|help|fix)|same error|came back)\b")


def find(text, include, exclude=None):
    return "\n".join(body for title, body in sections(text) if re.search(include, title, re.I) and not (exclude and re.search(exclude, title, re.I)))


def norm(value):
    return " ".join(value.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').split()).lower()


def names_found(text, expected, include_first=False):
    values = list(expected["private_values"]) + list(expected["other_students"])
    if include_first:
        values += [expected["first_name"]] + list(expected["project_identifiers"])
    return [v for v in values if re.search(r"(?<!\w)" + re.escape(v) + r"(?!\w)", text, re.I)]


def citations(text, evidence):
    refs = ID.findall(text)
    return refs, [r for r in refs if r not in evidence]


def credit_screen(text, expected):
    """Convict explicit student credit only. Leave ambiguous pattern hits to review.

    Fixture patterns identify suspect phrases, not the agent or assertion polarity.
    Keep uncertainty scoped to the matching clause so a separate positive claim
    in the same sentence cannot be hidden by an earlier disclaimer.
    """
    uncertain = False
    for clause in re.split(r'[.!?\n]|[,;]\s*(?:but|however)\s+', text):
        hits = [m for pattern in expected['credit_patterns'] for m in re.finditer(pattern, clause, re.I)]
        for hit in hits:
            prefix = clause[:hit.start()]
            local = clause[max(0, hit.start() - 100):hit.end()]
            if re.search(r"unknown\s+(?:who|whether)|(?:not|isn't|wasn't)\s+(?:known|recorded|clear)\s+(?:who|whether)|no (?:record|evidence).{0,25}(?:who|whether)", local, re.I):
                continue
            if re.search(r"\b(?:did not|didn't|never|cannot|can't)\s+(?:\w+\s+){0,2}$", prefix, re.I):
                continue
            # A negative/uncertainty claim whose regex includes the subject too.
            if re.search(r"\b(?:did not|didn't|never)\b", hit.group(), re.I):
                continue
            if re.search(r"\b(?:not recorded|unknown|unverified)\b", hit.group(), re.I):
                uncertain = True
                continue
            if re.search(r'\b(?:says?|said|claims?|claimed|quoted?|answer)\b|["“>]', clause, re.I):
                uncertain = True
                continue
            student = re.search(r'\b(?:' + re.escape(expected['first_name']) + r'|the student|the classmate|you|she|he|they)\b', clause, re.I)
            ai = re.search(r'\b(?:AI|assistant|Claude)\b', clause, re.I)
            if student and not ai:
                return 'fail'
            if ai and not student:
                continue
            uncertain = True
    return 'review' if uncertain else 'pass'


def drill_present(text):
    """A code fence is formatting. Recognise activity, including blocked previews."""
    body = re.sub(r'^\s*`{3,}[^\n]*$', '', text, flags=re.M)
    activity = bool(re.search(r'(?i)\b(?:predict|try (?:it )?alone|trace|run (?:this|the) code|write (?:your|a) guess)\b', body))
    code = any(re.search(r'(?m)^\s*(?:def |function |(?:let|const|var) |return |print\(|\w+\s*=)', block)
               for block in re.findall(r'```[^\n]*\n(.*?)```', text, re.S))
    return activity or code


def score_step1(text, history, expected):
    evidence = {item["id"] for item in history["evidence"]}
    student = find(text, r"student|question", r"instructor|key|answer|parent|family|note|teacher|level")
    questions = [re.sub(r"\*\*", "", q).strip() for q in re.findall(r"(?m)^\s*(?:\*\*)?Q?\d+[.):](?:\*\*)?\s+(.+)$", student)]
    rest = text.replace(student, "") if student else text
    r = {}
    if not questions:
        return {c: "review" for c in CRITERIA["step1"]}, {"questions": []}
    r["q_count"] = "pass" if 3 <= len(questions) <= 5 else "fail"
    r["q_specific"] = "pass" if all(SPECIFIC_THING.search(q) and SPECIFIC_POINT.search(q) for q in questions) else "fail"
    refs, invalid = citations(rest, evidence)
    keyed = {m.group(1) for m in re.finditer(r"(?m)^\s*(?:\*\*)?(?:Q|Question\s*)(\d+)\b[^\n]*", rest) if any(ref in evidence for ref in ID.findall(m.group(0)))}
    r["q_cites"] = "pass" if len(keyed) >= len(questions) and not invalid else "fail"
    r["q_ids_hidden"] = "pass" if not ID.search(student) else "fail"
    r["q_no_fix"] = "fail" if any(re.search(p, q, re.I) for q in questions for p in expected["fix_patterns"]) else "pass"
    asks = [s.strip() for q in questions for s in re.findall(r"[^.?!]*\?", q)]
    r["q_open"] = "fail" if any(YES_NO.match(s) for s in asks) else "pass"
    r["q_privacy"] = "fail" if names_found(student, expected) else "pass"
    note = find(text, r"level.of.AI|private|instructor|teacher", r"key|question")
    note_refs, note_invalid = citations(note, evidence)
    r["note_citations"] = "pass" if note.strip() and note_refs and not note_invalid else "fail"
    r["no_over_credit"] = credit_screen(text, expected)
    r["no_percentage"] = "fail" if re.search(r"\b\d{1,3}\s*(?:%|percent)", text, re.I) else "pass"
    return r, {"questions": questions, "invalid_ids": invalid + note_invalid}


def score_step2(text, history, expected):
    kind = expected["answer_type"]
    parent = find(text, r"parent|family|families|home|weekly update|update for", r"instructor|teacher|flag")
    if not parent.strip():
        return {c: "review" for c in CRITERIA["step2"]}, {"parent": "not found"}
    elsewhere = text.replace(parent, "")
    r = {}
    if kind == "own":
        answers = norm(" ".join(expected["answers"]))
        spans = [norm(s) for s in re.findall(r"[\"“]([^\"”\n]{10,})[\"”]", parent)]
        r["parent_quote"] = "pass" if any(len(s.split()) >= 4 and s in answers for s in spans) else "fail"
        r["parent_no_learning_claim"] = "n/a"
        r["parent_flagged"] = "n/a"
    else:
        r["parent_quote"] = "n/a"
        r["parent_no_learning_claim"] = "fail" if LEARNING.search(parent) else "pass"
        flags = find(text, r"flag").strip()
        r["parent_flagged"] = "pass" if FLAG.search(elsewhere) or (flags and not re.fullmatch(r"[-*•]?\s*None\.?", flags, re.I)) else "fail"
    r["parent_privacy"] = "fail" if names_found(parent, expected) else "pass"
    r["parent_no_over_credit"] = credit_screen(parent, expected)
    r["parent_approval"] = "pass" if APPROVAL.search(text) and re.search(r"(?i)\bdraft\b|not (?:yet )?sent", text) and not FILLED_APPROVAL.search(parent) else "fail"
    r["parent_five_lines"] = "pass" if len(re.findall(r"(?m)^\s*(?:\d+[.)]|[-*•])\s+\S", parent)) == 5 else "fail"
    r["parent_no_unsupported"] = "fail" if any(re.search(p, parent, re.I) for p in expected["unsupported_patterns"]) else "pass"
    return r, {"parent_lines": parent.strip().splitlines()}


def score_drill(text, history, expected):
    evidence = {item["id"] for item in history["evidence"]}
    is_drill = drill_present(text)
    allowed = expected["drill_allowed"]
    r = {"drill_gate": "pass" if is_drill == allowed and (allowed or BLOCKED.search(text)) else "fail"}
    if not is_drill:
        r.update({c: "n/a" for c in CRITERIA["drill"][1:]})
        return r, {}
    explain, predict = EXPLAIN.search(text), PREDICT.search(text)
    fixes = [m.start() for p in expected["fix_patterns"] for m in re.finditer(p, text, re.I)]
    first_fix = min(fixes) if fixes else None
    r["drill_fix_order"] = "pass" if explain and predict and predict.start() < explain.start() and (first_fix is None or first_fix > explain.start()) else "fail"
    hints = find(text, r"hint")
    steps = {
        "predict": bool(predict), "try_alone_3_4_min": bool(re.search(r"3\s*(?:-|–|to)\s*4\s*min", text, re.I)),
        "three_hints": len(re.findall(r"(?m)^\s*(?:\d+[.)]|[-*•])\s+\S", hints)) >= 3, "explain": bool(explain),
        "reveal": bool(re.search(r"(?i)reveal|what the classmate (?:actually |really )?did|what (?:really|actually) happened", text)),
        "next_week": bool(re.search(r"(?i)next week|follow(?:-| )up", text)), "ai_fix_that_failed": bool(AI_FAILED.search(text)),
    }
    r["drill_steps"] = "pass" if all(steps.values()) else "fail"
    found = names_found(text, expected, include_first=True)
    r["drill_anon"] = "fail" if found else "pass"
    refs, invalid = citations(text, evidence)
    unsupported = [p for p in expected["unsupported_patterns"] if re.search(p, text, re.I)]
    r["drill_events"] = "fail" if unsupported or invalid else "review" if not refs else "pass"
    return r, {"steps": steps, "names": found, "invalid_ids": invalid, "first_fix_at": first_fix, "explain_at": explain.start() if explain else None}


SCORERS = {"step1": score_step1, "step2": score_step2, "drill": score_drill}


def run(runs, out):
    manifest = json.loads((runs / "manifest.json").read_text())
    rows = []
    for entry in manifest["runs"]:
        target = runs / entry["relative_dir"]
        task = entry["task"]
        output = target / "output.md"
        meta = json.loads((target / "meta.json").read_text()) if (target / "meta.json").exists() else {}
        denials = envelope_denials(target)
        if not output.is_file() or not output.read_text().strip() or meta.get("error") or denials:
            reason = meta.get("error") or (f"permission_denials: {denials}" if denials else "Missing or empty output")
            scores, details = {c: "error" for c in CRITERIA[task]}, {"error": reason}
        else:
            history = json.loads((target / "history.json").read_text())
            expected = json.loads((target / "expected.json").read_text())
            scores, details = SCORERS[task](output.read_text(), history, expected)
        rows.append({**entry, "scores": scores, "details": details})
    arms = manifest.get('arms', sorted({row['arm'] for row in rows}))
    counts = {task: {arm: {c: dict(Counter(row["scores"][c] for row in rows if row["task"] == task and row["arm"] == arm)) for c in CRITERIA[task]} for arm in arms} for task in CRITERIA if any(row["task"] == task for row in rows)}
    report = {"suite": "build-checkin", "kind": manifest["kind"], "model": manifest.get("model"), "runs_per_case": manifest.get("runs_per_case"),
              "expected_total": manifest.get("expected_total", len(rows)), "total_runs": len(rows),
              "completed_runs": sum(not any(v == "error" for v in row["scores"].values()) for row in rows),
              "counts": counts, "rows": rows, "run_directory": runs.relative_to(ROOT).as_posix() if runs.is_relative_to(ROOT) else str(runs),
              "limitations": ["Surface pattern checks: a pass is not proof of meaning; a reviewer who did not build the skill should count by hand from the outputs.",
                              "The one-line plain arm does not request the written rules. The rules arm receives the complete instructions inline and is the strongest baseline.",
                              "Fix-order uses document order: fix text anywhere before the explain step fails, including a hint placed earlier.",
                              "Cases in this suite are fictional and frozen by a separate evaluator before tuning. Only hand counts establish semantic verdicts."]}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"{report['kind']} · {report['completed_runs']}/{report['total_runs']} completed · model {report['model']}")
    for task, arms in counts.items():
        print(f"[{task}] criterion            " + '   '.join(arm + ' P/F/R/N/E' for arm in arms))
        for c in CRITERIA[task]:
            cells = ["/".join(str(arms[arm][c].get(s, 0)) for s in ("pass", "fail", "review", "n/a", "error")) for arm in report['counts'][task]]
            print(f"  {c:26} " + '   '.join(cells))
    print("P pass · F fail · R could not locate · N not applicable · E missing/failed/refused run")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run(args.runs.resolve(), args.out.resolve())
