# Build Check-in: evaluation record

Moved from the README so its first page shows what the skill does; the text is unchanged apart from link paths. "THIN" is the author's working rating for this evidence; the held-out section gives the reasons it applies (one sample per cell, an unblinded evaluator). "Supervisor" is the operator that [RUN-PLAN.md](../RUN-PLAN.md) names as the only one who may run its model command.

## Held-out comparison, 6 November 2026

Six new fictional projects were frozen before four rule changes. Claude Sonnet 5.5 produced 54 outputs across the skill, the one-line prompt and a prompt with the complete written rules. Every output was read against its evidence. The skill met every reviewed requirement in 2/6 step-1 outputs, 3/6 step-2 outputs and 6/6 drill outputs. The full-rules baseline reached 1/6, 1/6 and 4/6 respectively. It tied the skill on answer withholding, family factuality, prediction order and early-hint timing. One sample per cell and an unblinded evaluator leave the reading THIN. The report records the remaining slips, per-run judgments, scorer controls and reproduction commands. [Read the held-out report](heldout/REPORT.md).

## Extractor repair and prepared second round, 11 November 2026

The extractor now retains ordinary assistant replies from JSONL and pasted chat as cited, untrusted evidence. A reply proves what the assistant said; it does not prove an edit or a successful test. USER identifies a conversation role, not a student or staff author. Human authorship remains unknown, and a matching manual-edit report stays a report by an unknown speaker. The existing `prompts` list and its IDs remain available; its evidence kind is now `user_turn`, with explicit `actor` and `support` fields. Assistant text blocks have `assistant:N` IDs and their source line and block number. The schema remains additive except for that corrected turn kind and conservative manual-edit attribution; consumers using `student_turn` must use `user_turn` for newly extracted histories.

The November 6 fixture reproducer shows four assistant explanations missing before and retained after the repair. The historical model outputs and their counts above were not rerun. Six different projects are frozen for a second three-arm comparison, with three repeats (162 planned Claude calls). Only offline preparation has run; the rating remains THIN. The case author did not edit the written skill rules. [Read the repair evidence](extractor/REPORT.md) and [Supervisor run plan](../RUN-PLAN.md).

## Historical measured results

The same fictional histories went to Claude Sonnet 5.5 three times per arm. Questions and drills each used twelve cases, and step 2 used nine cases with answers. The selected rounds total 198 outputs across both arms. Plain-prompt counts are from the initial round. Skill question and drill counts follow the second-round fixes. Family and student-note counts follow the third step-2 round. These are historical results. These counts predate the held-out comparison above.

Rows about drill content count only drills that were made. Of 36 runs per arm, the skill declined all 15 runs without family agreement, leaving 21 (36 − 15). The plain prompt made drills in 8 of those 15 runs, giving 29 (21 + 8). The agreement row covers all 15 runs without permission.

| Check | Plain prompt | Skill |
| --- | --- | --- |
| Family note credits work the history does not show | 9 of 27 | 0 of 27 |
| Questions give away or hint at the fix | 36 of 36 | 0 of 36 |
| Drill made without family agreement | 8 of 15 | 0 of 15 |

All cases were written by the author and are fictional. No real student history has been tested. Ten of twelve cases use the same study-timer project, and eighteen of twenty-one skill drills use its bug. Reviewers who did not build the skill counted the outputs by hand. The skill was revised and rerun on these same cases. Those rounds had no held-out set or test on another model. The plain prompt was one line and was never given the rules for consent, quoting, approval, prediction or withholding the fix. Those rounds did not test a plain prompt with those rules. The counts do not establish classroom effectiveness.

Those historical rounds reported remaining errors. Two of thirty-six question sets credit an AI action to the student, one instructor note over-credits, and two of twenty-one drills invent events. One of twenty-seven family notes invents an AI explanation. One student note quotes a missing-answer marker as an answer. Sixteen of twenty-one drills give the cause in hint 2 before students write an explanation, although they withhold the fix. A stricter reading would flag nine student-note runs that omit a recorded AI test run. Every draft needs instructor review.

All fifteen measured rows appear on index.html and in verification/measured-results.json. Method and review-row provenance are in verification/evaluation-notes.md.
