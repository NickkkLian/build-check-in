#!/usr/bin/env python3
"""Earlier CLI runner adapted for six frozen cases and three matched-input arms.

--dry-run does file handling only and never invokes Claude.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
sys.dont_write_bytecode = True
from runner import ignore, raw_evidence  # noqa: E402  (shared with the Build Story suite)
from frozen_inputs import verify as verify_frozen  # noqa: E402

FIXTURES = ROOT / "evals/fixtures"
CHECKIN = ROOT / "evals/checkin"
SKILL = ROOT / "build-checkin"
TASKS = ("step1", "step2", "drill")
PLAIN_CHECKIN = "Here is a student's build log. Write 3-5 questions to check they understand their project, a note for their instructor about how much the AI did, and a short weekly update for their parents."
PLAIN_DRILL = "Here is a student's build log. Turn one bug from it into a 10-minute debugging exercise for their class."
SKILL_MODE = {"step1": "check-in step 1", "step2": "check-in step 2", "drill": "debug drill"}
ARMS = ("skill", "plain", "rules")


def extract(name, out, fixtures=FIXTURES, checkin=CHECKIN):
    source = fixtures / name
    command = [sys.executable, "-B", str(SKILL / "scripts/extract_history.py"), str(source / "project"), "--context", str(checkin / name / "context.json"), "--out", str(out)]
    if (source / "session.jsonl").exists():
        command += ["--session", str(source / "session.jsonl")]
    if (source / "chat.txt").exists():
        command += ["--chat", str(source / "chat.txt")]
    if (source / "snapshots").exists():
        command += ["--snapshots", str(source / "snapshots")]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(out.read_text())


def prompt_for(task, arm, inputs):
    """Absolute input paths: in round 2, 5 of 30 plain runs guessed a wrong path and were refused."""
    log = inputs / ("chat.txt" if (inputs / "chat.txt").exists() else "session.jsonl")
    answers = f"\nThe student's answers to the questions, pasted by the instructor: {inputs / 'answers.md'}" if task == "step2" else ""
    evidence = (f"\nRead {inputs / 'context.json'}, {inputs / 'history.json'}, {inputs / 'raw-diffs.md'}, "
                f"the files in {inputs / 'project'}, and {log}.")
    if arm == "skill":
        return (f"/build-checkin\nMode: {SKILL_MODE[task]}.\nThe history.json was already produced by the bundled extractor."
                f"{evidence}{answers}\nProduce the skill's complete output directly in your reply.")
    plain = PLAIN_DRILL if task == "drill" else PLAIN_CHECKIN
    if arm == "rules":
        rules = (SKILL / "SKILL.md").read_text()
        return (f"{plain}\nMode: {SKILL_MODE[task]}. Follow the complete written rules below for this mode.\n"
                f"{rules}\nThe history.json was already produced by the bundled extractor."
                f"{evidence}{answers}\nProduce the complete output for the requested mode directly in your reply.")
    return f"{plain}{answers}{evidence}\nProduce the output directly in your reply."


def command_for(arm, work):
    absolute = "/" + str(work)  # Claude Code reads "//path" as an absolute path rule.
    command = ["claude", "-p", "--model", "sonnet", "--output-format", "json", "--no-session-persistence", "--max-turns", "10",
               "--permission-mode", "dontAsk", "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", str(work / "empty-mcp.json")]
    command += ["--tools", "Read,Skill" if arm == "skill" else "Read", "--allowedTools", "Read(./input/**)", f"Read({absolute}/input/**)"]
    if arm == "skill":
        command += ["Read(./.claude/skills/build-checkin/**)", f"Read({absolute}/.claude/skills/build-checkin/**)", "Skill(build-checkin)"]
    else:
        command += ["--disable-slash-commands"]
    return command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--suite-root", type=Path, default=ROOT / 'evals', help="directory containing fixtures/ and checkin/ (default: original suite)")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ"))
    parser.add_argument("--repeats", type=int, default=3, choices=range(1, 6))
    parser.add_argument("--tasks", default=",".join(TASKS), help="comma list of step1,step2,drill")
    parser.add_argument("--arms", default=",".join(ARMS), help="comma list of skill,plain,rules")
    args = parser.parse_args()
    tasks = [t for t in args.tasks.split(",") if t]
    arms = [a for a in args.arms.split(",") if a]
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id) or not tasks or any(t not in TASKS for t in tasks) or len(tasks) != len(set(tasks)) or not arms or any(a not in ARMS for a in arms) or len(arms) != len(set(arms)):
        parser.error("run-id must be simple; tasks from step1,step2,drill; distinct arms from skill,plain,rules")
    suite = args.suite_root.resolve()
    if not suite.is_relative_to(ROOT / 'evals'):
        parser.error('suite-root must be inside this repository\'s evals directory')
    fixtures, checkin = suite / 'fixtures', suite / 'checkin'
    freeze = suite / 'FROZEN.txt'
    if suite != ROOT / 'evals' and not freeze.is_file():
        parser.error('A separate suite requires FROZEN.txt')
    frozen_count = verify_frozen(freeze) if freeze.is_file() else None
    cases = json.loads((checkin / 'manifest.json').read_text())
    names = [item['case'] for item in cases]
    if not names or len(names) != len(set(names)) or any(not re.fullmatch(r'[a-z0-9-]+', name) for name in names):
        parser.error('Cases must have unique simple names')
    runroot = ROOT / "evals/runs" / args.run_id
    if runroot.exists():
        parser.error("run directory exists; refusing to overwrite outputs")
    runroot.mkdir(parents=True)
    planned = sum(len(arms) * args.repeats for item in cases for task in tasks if task != "step2" or item["answers"])
    manifest = {"suite": "build-checkin", "kind": "dry-run" if args.dry_run else "claude", "model": "sonnet", "runs_per_case": args.repeats, "tasks": tasks, "arms": arms, "expected_total": planned, "runs": []}
    manifest.update(suite_root=suite.relative_to(ROOT).as_posix(), frozen_files=frozen_count,
                    freeze_sha256=hashlib.sha256(freeze.read_bytes()).hexdigest() if freeze.is_file() else None,
                    skill_sha256=hashlib.sha256((SKILL / 'SKILL.md').read_bytes()).hexdigest(),
                    extractor_sha256=hashlib.sha256((SKILL / 'scripts/extract_history.py').read_bytes()).hexdigest())
    for case_index, item in enumerate(cases):
        name = item["case"]
        history = extract(name, runroot / f"{name}-history.json", fixtures, checkin)
        expected = checkin / name / "expected.json"
        for task_index, task in enumerate(tasks):
            if task == "step2" and not item["answers"]:
                continue
            for repeat in range(1, args.repeats + 1):
                offset = (case_index + task_index + repeat - 1) % len(ARMS)
                order = ARMS[offset:] + ARMS[:offset]
                for arm in [a for a in order if a in arms]:
                    relative = Path(name) / task / arm / str(repeat)
                    target = runroot / relative
                    work = (target / "work").resolve()
                    inputs = work / "input"
                    inputs.mkdir(parents=True)
                    shutil.copytree(fixtures / name / "project", inputs / "project", ignore=ignore)
                    shutil.copytree(fixtures / name / "snapshots", inputs / "snapshots", ignore=ignore)
                    for file in ("session.jsonl", "chat.txt"):
                        if (fixtures / name / file).exists():
                            shutil.copy2(fixtures / name / file, inputs / file)
                    shutil.copy2(checkin / name / "context.json", inputs / "context.json")
                    if task == "step2":
                        shutil.copy2(checkin / name / "answers.md", inputs / "answers.md")
                    (inputs / "raw-diffs.md").write_text(raw_evidence(history))
                    if arm == "skill":
                        # The worked examples come from the pixel-hop eval case; they stay out of the model's copy.
                        shutil.copytree(SKILL, work / ".claude/skills/build-checkin", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "examples"))
                    (inputs / "history.json").write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
                    (work / "empty-mcp.json").write_text('{"mcpServers":{}}\n')
                    prompt = prompt_for(task, arm, inputs)
                    command = command_for(arm, work)
                    # Frozen copies outside the model-visible input folder, for the scorer.
                    (target / "history.json").write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
                    shutil.copy2(expected, target / "expected.json")
                    (target / "prompt.txt").write_text(prompt + "\n")
                    (target / "invocation.json").write_text(json.dumps({"argv": command, "cwd": str(work), "stdin": "../prompt.txt", "will_execute": not args.dry_run}, indent=2, ensure_ascii=False) + "\n")
                    meta = {"kind": manifest["kind"], "model": "sonnet", "task": task, "arm": arm, "repeat": repeat}
                    manifest["runs"].append({"case": name, "task": task, "arm": arm, "repeat": repeat, "relative_dir": relative.as_posix()})
                    (runroot / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
                    if not args.dry_run:
                        # Supervisor only: no retries; stop on the first CLI failure or refused read.
                        try:
                            result = subprocess.run(command, input=prompt, cwd=work, capture_output=True, text=True, timeout=240)
                            (target / "stderr.txt").write_text(result.stderr)
                            (target / "envelope.json").write_text(result.stdout)
                            envelope = json.loads(result.stdout)
                            output = envelope.get("result", "")
                            if envelope.get("permission_denials"):
                                raise ValueError(f"permission denied: {json.dumps(envelope['permission_denials'])[:300]}")
                            if result.returncode or envelope.get('subtype') != 'success' or envelope.get("is_error") or not isinstance(output, str) or not output.strip():
                                raise ValueError(f"Claude CLI failed (exit {result.returncode}); inspect envelope/stderr")
                            (target / "output.md").write_text(output + "\n")
                            meta["usage"] = envelope.get("usage")
                            meta["model_usage"] = envelope.get("modelUsage")
                        except (OSError, ValueError, subprocess.SubprocessError) as exc:
                            meta["error"] = str(exc)
                            (target / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
                            raise SystemExit(f"Stopped at {relative}: {exc}")
                    (target / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    done = len(manifest["runs"])
    assert done == planned, (done, planned)
    print(f"{'DRY RUN: no Claude executed.' if args.dry_run else 'Claude run complete.'} {done} isolated work copies under {runroot.relative_to(ROOT)} ({', '.join(tasks)}; {args.repeats} repeats per arm)")


if __name__ == "__main__":
    main()
