#!/usr/bin/env python3
"""Private, deterministic class list from extracted histories; no project code runs.

Usage: python3 scripts/class_list.py class-list.json [--json]
The manifest's paths are relative to itself. No directory discovery or model calls.
"""
import argparse
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
import re


def read_file(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("Expected a regular supplied file")
    if path.stat().st_size > 20_000_000:
        raise ValueError("Supplied file exceeds 20 MB")
    return path.read_text(encoding="utf-8")


def version_list(history):
    return [v for v in history.get("versions", [])
            if v["id"] != "worktree" or v.get("evidence")]


def answer_count(text):
    blocks = re.findall(r"(?ms)^A\d+\.[ \t]*(.*?)(?=^[QA]\d+\.|\Z)", text)
    return sum(bool(b.strip()) and not b.strip().startswith("[")
               and b.strip().casefold() not in {"(no answer)", "no answer"} for b in blocks)


def summarise(student, base):
    history = json.loads(read_file(base / student["history"]))
    versions = version_list(history)
    last = versions[-1] if versions else {}
    date = last.get("recorded_date")
    if date:
        try:
            datetime.fromisoformat(date.replace("Z", "+00:00"))
        except ValueError:
            date = None
    evidence = history.get("evidence", [])
    by_id = {e["id"]: e for e in evidence}
    # Only a pass of the identical recorded command clears its earlier failure.
    # Missing command identity remains unresolved; no guessed link from prose.
    failed = {}
    for event in evidence:
        if event.get("kind") != "tool_result":
            continue
        tool = by_id.get(event.get("tool_evidence"), {})
        command = tool.get("command")
        key = command or event["id"]
        if event.get("outcome") == "failed":
            failed.setdefault(key, []).append(event["id"])
        elif event.get("outcome") in {"passed", "reported_pass"} and command:
            failed.pop(key, None)
    # Repetition is literal: same entire error report or same quoted error string.
    repeated = defaultdict(list)
    failure_ids = set(history.get("failure_evidence", []))
    for prompt in history.get("prompts", []):
        if prompt["evidence"] not in failure_ids:
            continue
        value = prompt["text"].strip()
        quotes = re.findall(r'`([^`\n]+)`|"([^"\n]+)"', value)
        signatures = [a or b for a, b in quotes] or [value]
        for signature in set(" ".join(s.casefold().split()) for s in signatures):
            repeated[signature].append(prompt["evidence"])
    repeats = [ids for ids in repeated.values() if len(ids) > 1]
    baseline = student.get("last_checkin_version")
    known_ids = {v["id"] for v in versions}
    unchanged = None if not baseline or baseline == "worktree" or baseline not in known_ids else last.get("id") == baseline
    answers_path = student.get("answers")
    count = answer_count(read_file(base / answers_path)) if answers_path else 0
    return {"label": student["label"], "last_version": last.get("id"), "last_date": date,
            "version_citations": last.get("evidence", []), "version_count": len(versions),
            "unresolved": list(failed.values()), "repeated": repeats,
            "no_new_version": unchanged, "baseline": baseline, "answer_count": count,
            "answers_returned": bool(count)}


def safe(value):
    # Do not echo arbitrary history text, names, paths, instructions or metric words.
    return re.sub(r"[^A-Za-z0-9_.:@/+ -]", "_", str(value)).replace("|", "_")


def refs(ids, index):
    return "".join(f"[student-{index}:{safe(id_)}]" for id_ in ids)


def table(rows):
    lines = ["Private instructor class list — recorded facts only.",
             "Dates are recorded metadata. Missing records stay unknown.", "",
             "| Student | Last version date | Failure with no later same-command pass | No new version since check-in | Same error in prompts | Step-1 answers |",
             "| --- | --- | --- | --- | --- | --- |"]
    first = []
    for index, row in enumerate(rows, 1):
        history_ref = f"[student-{index}:history]"
        version = f"{row['last_date'] or 'Not recorded'}; {row['version_count']} versions " + (refs(row["version_citations"], index) or history_ref)
        unresolved = row["unresolved"]
        failure = f"{len(unresolved)} failing records " + (refs([id_ for group in unresolved for id_ in group], index) or history_ref)
        state = row["no_new_version"]
        unchanged = ("Unknown" if state is None else "Yes" if state else "No") + f" [class:student-{index}:last_checkin_version]"
        repeat = f"{len(row['repeated'])} repeated reports " + (refs([id_ for group in row["repeated"] for id_ in group], index) or history_ref)
        answers = (f"Returned; {row['answer_count']} answers" if row["answers_returned"] else "Not returned; 0 answers") + f" [class:student-{index}:answers]"
        lines.append("| " + " | ".join([safe(row["label"]), version, failure, unchanged, repeat, answers]) + " |")
        reasons = []
        if unresolved:
            reasons.append("recorded failure " + refs([id_ for group in unresolved for id_ in group], index))
        if state:
            reasons.append(f"unchanged version [class:student-{index}:last_checkin_version]")
        if row["repeated"]:
            reasons.append("repeated report " + refs([id_ for group in row["repeated"] for id_ in group], index))
        if not row["answers_returned"]:
            reasons.append(f"answers missing [class:student-{index}:answers]")
        if reasons:
            first.append(safe(row["label"]) + " (" + "; ".join(reasons) + ")")
    lines += ["", "Talk to first (manifest order): " + ("; ".join(first) if first else "No recorded contact flags.")]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true", help="machine-readable facts")
    args = parser.parse_args()
    try:
        manifest = json.loads(read_file(args.manifest))
        rows = [summarise(s, args.manifest.parent) for s in manifest["students"]]
        if re.search(r"%|\b(?:percent(?:age)?|scores?)\b", json.dumps(rows), re.I):
            raise ValueError("Disallowed metric in supplied label or evidence ID")
        output = json.dumps(rows, indent=2) + "\n" if args.json else table(rows)
        # Output invariant, including untrusted labels/IDs: no percentages or scores.
        if re.search(r"%|\b(?:percent(?:age)?|scores?)\b", output, re.I):
            raise ValueError("Disallowed metric in supplied label or evidence ID")
        print(output, end="")
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(2, f"Class list could not be produced ({type(exc).__name__}); check supplied files.\n")


if __name__ == "__main__":
    main()
