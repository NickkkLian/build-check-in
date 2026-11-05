# Build Check-in

For instructors who teach teens to code.

Build Check-in helps a coding instructor who teaches teens turn a student's build history (project versions and their AI chat log) into questions about specific moments in the work, a cited instructor key, and a private account of what the AI did. After the instructor supplies the student's answers, it drafts a five-line family note and returns the student's own words in build order for a project showcase. It also makes classroom debugging drills when the family has agreed, and a class list of each student's unresolved errors.

For instructors of teen coding courses who have project versions and a build log. Outputs stay drafts until an instructor reviews them.

## Install for Claude Code

Download build-checkin.zip from this project and unzip it. Copy the enclosed build-checkin folder into your Claude Code skills directory, typically ~/.claude/skills/. Invoke /build-checkin and specify step 1, step 2, debug drill, or class list. The same skill folder is also included directly in this repository.

Python 3.9 or newer is needed for the helpers, with git available for git histories. Helpers use the standard library. Run commands from the installed build-checkin folder. Fill context-template.json with adult-runner confirmation, project context and classroom agreement (the family's permission to use a bug in class). Supply only paths you intend the extractor to read. Keep histories and outputs in a private working directory.

```sh
python3 scripts/extract_history.py PROJECT --context CONTEXT.json --session SESSION.jsonl --out PRIVATE/history.json
```

A pasted USER/ASSISTANT chat or ordered snapshots can be supplied instead. SKILL.md documents the arguments. The extractor skips symlinks, dependencies and credential-like files, and redacts common token patterns. Review records before sharing them. Recorded tests are reports. The extractor never executes project code.

## Worked fictional example

Leo's fictional Pixel Hop game restores a score of 5, then displays 51 after a hop. The history records an AI edit that failed and Leo's report of a later hand edit. Step 1 gives the instructor this question from a recorded model run on the fictional fixture.

> At version 2, the AI changed the score line and ran the test again. The test still failed with the same message. Why do you think that change didn't help?

The instructor key links it to the recorded edit and failing result. Leo writes his own answer. The bundled step2-answers.md and step2-output.md illustrate how an instructor supplies answers and receives a family note draft. Step-2 and drill examples were written by hand. The questions and key are real model output on this fictional history. All example people and projects are fictional.

Read build-checkin/examples/. For the class list, fill build-checkin/class-list-template.json and run scripts/class_list.py with its path. It prints cited unresolved failures, unchanged versions, repeated errors and returned-answer counts in manifest order.

## Measured results

The same fictional histories went to Claude Sonnet 5.5 three times per arm. Questions and drills each used twelve cases, and step 2 used nine cases with answers. The selected rounds total 198 outputs across both arms. Plain-prompt counts are from the initial round. Skill question and drill counts follow the second-round fixes. Family and student-note counts follow the third step-2 round. These are historical results. The public wording changes have not had a new model evaluation.

Rows about drill content count only drills that were made. Of 36 runs per arm, the skill declined all 15 runs without family agreement, leaving 21 (36 − 15). The plain prompt made drills in 8 of those 15 runs, giving 29 (21 + 8). The agreement row covers all 15 runs without permission.

| Check | Plain prompt | Skill |
| --- | --- | --- |
| Family note credits work the history does not show | 9 of 27 | 0 of 27 |
| Questions give away or hint at the fix | 36 of 36 | 0 of 36 |
| Drill made without family agreement | 8 of 15 | 0 of 15 |

All cases were written by the author and are fictional. No real student history has been tested. Ten of twelve cases use the same study-timer project, and eighteen of twenty-one skill drills use its bug. Reviewers who did not build the skill counted the outputs by hand. The skill was revised and rerun on these same cases. There is no held-out set or test on another model. The plain prompt was one line and was never given the rules for consent, quoting, approval, prediction or withholding the fix. A plain prompt with those rules was never tested. The counts do not establish classroom effectiveness.

Errors remain. Two of thirty-six question sets credit an AI action to the student, one instructor note over-credits, and two of twenty-one drills invent events. One of twenty-seven family notes invents an AI explanation. One student note quotes a missing-answer marker as an answer. Sixteen of twenty-one drills give the cause in hint 2 before students write an explanation, although they withhold the fix. A stricter reading would flag nine student-note runs that omit a recorded AI test run. Every draft needs instructor review.

All fifteen measured rows appear on index.html and in verification/measured-results.json. Method and review-row provenance are in verification/evaluation-notes.md.

## Review and consent

An adult operates the skill. Students write their own answers. The instructor reviews drafts and approves family notes. Classroom drills require the family's agreement and remove identifying details. Suspected pasted answers prompt an instructor conversation. Attribution follows recorded evidence, with self-reports and unknown authorship kept explicit.

## Local checks

Run python3 scripts/check.py for archive and helper checks. Run python3 scripts/check-release.py --denylist PATH for the privacy and offline audit, using a private policy kept outside the release. Run sh verify-local.sh for browser interactions and 390/1440 layouts with installed headless Chromium. Reports are in verification/.

## Licence

MIT. See LICENSE.
