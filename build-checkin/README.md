# Build Check-in

For instructors who teach teens to code. Point it at one student's project
folder and build log. This build history means the project versions and their AI chat log. It reads how the project was actually built and gives you:

- **Check-in step 1:** 3 to 5 questions for the student, each about a moment in their own
  history (a version, a failing test, a prompt, a hand edit), with an instructor key that
  says what a good answer mentions, and a private AI contribution note that cites the history.
- **Check-in step 2:** after you paste the student's answers in their own words, a
  five-line family note that quotes the student, says what the AI did, and stays a draft
  until you approve it. Answers that are missing, "I don't know", read like pasted AI
  text or claim the AI's work are flagged for you, not passed to the family. A private
  project showcase section returns the student's own answers unchanged, in build order, for
  that student after your review. Weekly or once at project showcase: your call.
- **Debug drill:** a 10-minute class exercise from one real bug: predict, try alone,
  write why it broke, then the reveal of what the classmate and the AI really did. Only
  if you collect the family's agreement for class use, and anonymised.
- **Class list:** `python3 scripts/class_list.py class-list.json` reads several extracted
  histories and prints cited facts about unresolved tests, unchanged versions, repeated
  error reports and returned answers, plus who to talk to first. Fill
  [class-list-template.json](class-list-template.json); no model is used.

It never writes the student's answers, never talks to students, never gives an AI-use
percentage, and never claims what a student learned.

## Install

1. **Claude.ai:** upload `build-checkin.zip` in the Skills settings and enable it. Folder
   access, Python and git may be unavailable there: run the extractor locally and upload
   the private `history.json`.
2. **Claude Code:** copy the folder to `~/.claude/skills/build-checkin/` and invoke
   `/build-checkin`, saying which mode you want.

## Extract locally

Python 3.9+ standard library; git on PATH for git histories. Nothing in the project is run.

```sh
python3 scripts/extract_history.py /path/to/project --context context.json --session session.jsonl --out /private/output/history.json
```

Fill a copy of [context-template.json](context-template.json): adult runner confirmed,
first and last name (the last name is only used to keep it out), project name, and
`classroom_drill_consent` for the drill. The check-in and family note do not need class-use agreement: the family note goes only
to that child's own family, after your approval.

The extractor is the one from Build Story (the earlier skill), plus the drill agreement and a list of failure
records and recorded git version dates. It reads only the supplied paths, skips symlinks, dependencies, binaries and
credential-like files, redacts common key and token patterns, and never loads git hooks
or configs. Use a private output folder outside the project.

## What the history can and cannot show

An AI edit record that matches a diff shows the AI made that change. A student's report
that they changed a line by hand, matching a diff, is still the student's report. Lines
with no matching record are unknown, whatever git says about the author. A recorded test
pass is a report, not a rerun. The student's answers show what they can explain this
week; they are not proof of learning, and the family note does not claim any.

## Limits

Tested so far only on fictional cases written by the author; no real student history has been run. The check for "reads like pasted AI
text" is a prompt for the instructor to ask, not a detector. Staff still check every line
before anything reaches a student, a class or a family.
