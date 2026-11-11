# Extractor repair evidence

11 November 2026. Status: deterministic repair verified; second model evaluation not run. Rating remains THIN.

## Dropped assistant prose

The November 6 extractor's `session()` assembled text blocks but emitted text evidence only for USER messages. Its block loop handled tool calls and results, never ordinary assistant text. That discarded each of the four recorded explanations before the skill read the derived history. The raw logs were also available to the earlier models, so the bug is an established input omission, not proof that it alone caused every model mistake.

| Old case | Raw assistant wording at `session.jsonl:6` | Before | After |
| --- | --- | --- | --- |
| queue-end | The code selects the last item instead of the first. | Dropped | Retained as `assistant:1` |
| garden-units | The multiplier is 100 although one litre contains 1000 millilitres. | Dropped | Retained as `assistant:1` |
| gallery-case | The comparison is case-sensitive and the stored literal uses different case. | Dropped | Retained as `assistant:1` |
| receipt-total | The initial code subtracts the fee instead of adding it. | Dropped | Retained as `assistant:1` |

`reproduction.json` contains exact source wording and old/new evidence records. `november6/before/` and `november6/after/` hold all six full extracted histories. The USER-only map-offset and shelf-boundary histories still contain zero assistant replies. The baseline source in `evals/frozen/extract_history_before.py` is copied unchanged from `f10857f`.

The repair retains each ordinary text block in order, including mixed text/tool messages, with its role, source line, block number and unique citation ID. String and text-block JSONL replies, nested message roles and multiline pasted chat are covered. Secret-pattern redaction and untrusted-data labels still apply. Thinking/image blocks are not ordinary assistant prose and are not copied. An assistant saying it ran a test is not promoted to a tool result or a successful edit.

## Invented staff authorship

Shelf-boundary's first USER message says, “The instructor supplied snapshots 1, 2 and 3 in order.” It never identifies who wrote the messages. Both earlier rule-bearing step-1 outputs nevertheless say the prompts are staff notes. The skill output at `verification/heldout/runs/shelf-boundary/step1/skill/1/output.md` says: “The \"prompts\" are staff notes, not words the student typed”. Its step-2 flag says, “The note comes from you.” These are unsupported identity inferences.

The likely contributing ambiguity is the combination of an adult-operated skill, staff-supplied snapshot metadata and an extractor that labels every USER message `student_turn`. The model's internal cause cannot be established without new model evidence. The deterministic defect is that the extractor infers human identity from a transport role.

The code fix emits `user_turn`, `role: user`, `actor: unknown` and a local support statement separating snapshot submission from message authorship. The prompt list and IDs stay intact. Matching manual-edit text remains cited with `self_report_matches_diff`; its author stays unknown rather than automatically becoming the student. AI tool attribution is unchanged. The SKILL.md rules are byte-identical to November 6; no rule was tuned by the new case author.

This fixes misleading evidence, not a proven model recurrence rate. Whether Claude now avoids the unsupported staff claim must be measured in the held-out rerun.

## Checks and scope

`evals/check_extractor.py` runs 12 regression tests. Before the repair, 10 test methods fail (13 failures including the four old-case subtests); two negative/preservation controls pass. After the repair all 12 pass. The full offline gate includes these tests, archive/helper checks, the original scorer controls and the historical evaluation audit. Old outputs and old frozen hashes are preserved.

The second set is frozen in `746ee88`: six different projects, three JavaScript and three Python, 52 hashed files including unchanged written rules. The existing runner now accepts a separate frozen suite without replacing old fixtures. The prepared round has 162 work copies and zero model outputs. The auditor checks every input copy, complete task/arm/repeat coverage, expected-answer isolation, unchanged helper/rule copies and reply preservation. Mutation controls confirm it rejects a changed input and an expectation file placed in model input. The scorer recognises new assistant citations, including invalid references.

The downloadable ZIP is rebuilt from the repaired package. No UI files changed. Browser rendering was not rerun. The clean-export release audit and repository public-candidate scan check public files, including ZIP members. No push, deployment, external data write or model execution occurred.

See [RUN-PLAN.md](../../RUN-PLAN.md) for exact model commands, counts, failure handling, hand-counting and rating criteria. Synthetic fixtures, unblinded implementation work, unknown human speakers and no new model outcomes remain explicit limitations.
