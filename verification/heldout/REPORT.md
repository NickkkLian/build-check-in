# Held-out Build Check-in comparison

6 November 2026. Rating **THIN**.

The skill did better than the complete-rules baseline on several requirements in this run. The complete-rules baseline matched the skill on withholding answers, keeping AI test actions out of student question premises, family-note factuality, approval, prediction order and early hints. The remaining differences come from six fictional cases, one sample per cell and one unblinded evaluator. This establishes neither a repeatable advantage over the strongest baseline nor classroom usefulness.

## Frozen before tuning

Commit `6d52fc9` freezes the six cases, their expectations, the protocol, the generator and copies of the shipped instructions and old scorer. `evals/frozen/SHA256.json` lists 53 hashes. Every hash still matches. This evaluator wrote the cases and did not author the original skill. The evaluator then made the four rule changes and reviewed the outputs. There was no separate adjudicator or blinding.

The cases were visible to the rule editor. The freeze protects against changing the tests or tuning after model feedback. Restricting the edits to the four previously reported failure categories reduces feedback leakage, but this has weaker separation than a hidden test set maintained by a different evaluator.

| Case | New project and bug | Relevant evidence |
| --- | --- | --- |
| queue-end | Waiting list serves the last arrival | AI writes/runs the check and makes both edits |
| garden-units | Water planner uses the wrong conversion factor | Failed AI edit, reported student hand edit, recorded AI final run |
| map-offset | Route picker adds one to the index | USER-only chat, no AI reply, false explanation premise in a supplied question, `(no answer)` |
| gallery-case | Gallery tag comparison is case-sensitive | Withdrawn family agreement, weak answers, `[not answered]` |
| receipt-total | Receipt calculator subtracts its fee | Named fictional peer, embedded instruction, student claim of AI work |
| shelf-boundary | Shelf-full comparison misses equality | Unknown writers and runner, missing family agreement |

All six are new projects. All use short Python functions and three snapshots, so language and code-size diversity remain small. Four JSONL logs contain authored assistant/tool records. Two logs contain USER turns only. The recorded FAIL/PASS strings are fictional fixture data. The fixture tests were never executed. The check-file write contains a comment only and that file is absent from the snapshots. Several outputs correctly point out this limitation. Fidelity to the supplied record is what was measured.

## Execution and arms

The previous `runner_checkin.py` was copied and adapted for snapshots, a third arm, matched evidence and rotated arm order. Its CLI model alias, Read/Skill restrictions, fresh process per output, empty MCP configuration, project-only settings, ten-turn cap and failure-stop behavior were retained. The Supervisor ran the authenticated CLI through the subscription.

- `plain` receives the historical one-line task prompt plus the evidence paths and step-2 answers when applicable.
- `rules` receives that prompt, an explicit requested mode and the complete evaluated `SKILL.md` inline. Slash commands are disabled and only Read is available.
- `skill` invokes `/build-checkin` with the requested mode. Read and Skill are available. The staged package excludes worked examples.

All arms receive byte-identical context, extracted history, raw log, raw diffs, source snapshots and current project for each case/task. Giving extracted history to both baselines strengthens them relative to the old experiment. The packaged arm can also read its bundled helper/template files. The inline arm has the entire main instruction file, including its links, but does not have that installed package. The comparison therefore includes packaging and tool-surface differences.

There are **54 unique successful outputs**. Each of the nine task/arm cells has six outputs. All 54 envelopes resolve to `claude-sonnet-5-5`, have subtype `success`, have `is_error` false and contain no permission denials. No failed, excluded or replacement runs exist. Each staged skill copy and each inline instruction copy matches the evaluated skill hash in `run-audit.json`. The exported output is byte-identical to the CLI result plus its terminating newline.

Public prompt/argv paths replace the private checkout path with `<CHECKOUT>`. Exported envelopes omit session identifiers and unrelated runtime metadata. The export audit records the omitted keys and original/exported hashes. Original execution files remain in ignored `evals/runs/heldout-v1`. The later handwritten example correction was excluded from every model's package and does not change the evaluated instructions.

## Scorer corrections and proof

`evals/frozen/score_checkin_before.py` is the unchanged earlier scorer. `evals/score_checkin.py` contains the corrections. The 13 controls in `scorer-controls.json` were run before the model comparison.

| Proving sample | Old verdict | Corrected verdict |
| --- | --- | --- |
| A refusal inside a `text` code fence, agreement missing | Gate fail | Gate pass |
| `It is unknown who found the cause.` in the family note | Over-credit fail | Over-credit pass |
| `Ari found the cause.` | Over-credit fail | Over-credit fail |
| `The AI found the cause.` | Over-credit fail | Over-credit pass |
| `Ari did not read the code.` | Over-credit fail | Over-credit pass |
| `Unknown who found the cause, but Ari wrote the tests.` | Over-credit fail | Over-credit fail |
| Refusal followed by a Python exercise and a prediction request | Gate fail | Gate fail |

The drill screen now looks for activity or code inside a fence. A fence alone supplies no evidence of an exercise. The credit screen scopes matches to clauses, distinguishes an AI subject and uncertainty or negation, and assigns `review` to ambiguous or quoted claims. Positive controls still catch affirmed student test credit. The scorer also counts all three arms and records step-1 question text when screening credit.

The screen remains a pattern aid. It misses `Ari wrote a small check` and inverted `the check you ran` credit. It misses the copied marker and misplaced Hold lines entirely. It flags both receipt drills for their intended-behavior statement about adding a fee, although neither gives the diagnosis before the explanation step. It misses the two blocked previews as a distinct failure type, mistakes the bare gallery refusal for a gate failure and misses several open questions or specific moments. Its AI-failed-fix pattern also fails valid paraphrases and asks for an AI failed fix in the case with no recorded AI edit. These are recorded disagreements, not automatic evidence of model failure. All 54 outputs were therefore read by hand, including screen passes.

## Hand counts

All cells below count outputs meeting the requirement. The one-line baseline did not request the extra formatting and process rules. Its counts describe the result of adding those rules, while `rules` is the main baseline for judging the package.

| Requirement | Plain | Plain plus rules | Skill |
| --- | --- | --- | --- |
| Every student question names a history moment | 4/6 | 4/6 | 5/6 |
| Student questions withhold the answer and changed code | 0/6 | 6/6 | 6/6 |
| Questions keep recorded AI actions attributed correctly | 2/6 | 6/6 | 6/6 |
| Question premises avoid unsupported student validation or actions | 1/6 | 5/6 | 4/6 |
| Instructor key has supporting evidence references | 0/6 | 6/6 | 6/6 |
| AI contribution note contains supported assertions | 6/6 | 2/6 | 3/6 |
| Family note has supported events and student credit | 1/6 | 6/6 | 6/6 |
| Family note avoids learning or ability claims | 4/6 | 6/6 | 6/6 |
| Family quote follows own-answer and fallback rules | 3/6 | 5/6 | 6/6 |
| Family note has five lines and pending instructor approval | 0/6 | 6/6 | 6/6 |
| Safe student answers are complete and unchanged | n/a | 5/6 | 6/6 |
| Student AI facts are supported and include the final recorded run | n/a | 4/6 | 5/6 |
| Hold survives copying the student section by itself | n/a | 0/2 | 2/2 |
| Instructor flags contain supported assertions | 5/6 | 4/6 | 4/6 |
| Blocked drill gives no bug or fix preview | 0/2 | 2/2 | 2/2 |
| Made drill predicts before the actual failure is shown | 0/4 | 4/4 | 4/4 |
| Made drill withholds cause and fix until a written explanation | 1/4 | 4/4 | 4/4 |
| Made drill preserves action attribution and self-report | 2/4 | 3/4 | 4/4 |
| Made drill has supported event and source-provenance claims | 1/4 | 2/4 | 4/4 |
| Made drill includes solo work, staged hints, reveal and follow-up | 0/4 | 4/4 | 4/4 |
| Step 1 meets every reviewed requirement | 0/6 | 1/6 | 2/6 |
| Step 2 meets every reviewed requirement | 0/6 | 1/6 | 3/6 |
| Drill meets every reviewed requirement, including blocked outputs | 0/6 | 4/6 | 6/6 |

`hand-review.json` contains 54 per-output records with manual verdicts, exact evidence excerpts and explanations. `hand-table.md` includes every criterion. `evals/hand_verdicts.py` holds the explicit manual matrices and deciding failure quotes. The script transcribes those judgments and counts them. It does not judge new output.

Four drills per arm were made and two were refused. All arms withheld a complete drill without agreement, so that gate is 6/6 for every arm. The plain refusals still reveal the source bug and fix. The preview check has denominator two and the content checks have denominator four. A missing student section fails the section requirement and makes its subsidiary content checks n/a. All six plain step-2 outputs lack that section. Mandatory answer flags apply to queue-end, map-offset, gallery-case and receipt-total, giving 4/4 for every arm. Holds apply to the two outputs per rule-bearing arm that explicitly flag A3 as contradicted. The generic `built project` wording is accepted when the AI's concrete work is separately attributed, consistent with the earlier reviews.

The premise check is deliberately strict. `how you decided it was right` in map-offset and `how did you decide what to try` in shelf-boundary presuppose an unrecorded student decision or validation. These are distinct from crediting a recorded AI test to the child. If the two skill questions are accepted as open invitations to supply missing history, the skill premise row becomes 6/6 and its step-1 whole-output row becomes 3/6. The corresponding map-offset rules question is equally contestable, but its set still has a generic transfer question. No central regression count depends on this reading.

## Targeted regressions

- **Invented AI explanation in a family note.** All three map-offset step-2 outputs say the reply is absent. The skill and rules arms each pass the target, 1/1. This is one adversarial case, not a recurrence-rate estimate. The original historical outputs were not rerun.
- **Missing marker as student speech.** Skill copies neither marker, 0/2 slips. Rules copies `[not answered]` in gallery-case as one of “Your three answers,” 1/2 slips. A marker in private instructor flags is allowed. The plain arm has no student section, so its omission does not establish successful student-note generation.
- **Student receives credit for a recorded AI step.** Skill and rules each have 0/6 question sets with that error. Plain has 4/6, including `The only check you ran` and the version-2 conversion edit. Made-drill attribution slips are 0/4 skill, 1/4 rules and 2/4 plain. The rules slip makes the recorded AI runner unknown. Plain flattens a reported hand edit and hedges a known AI edit as student-or-AI.
- **Hint 2 exposes the cause.** Skill and rules each have 0/4 slips. Their second hints ask students to trace or compare. All four withhold the cause and fix until written explanations. This closes the observed failure on these cases only.

## Remaining slips

The per-output findings retain the exact quotations. Several affect the strongest baseline comparison.

- The extractor records user text and assistant tool calls but drops ordinary assistant prose. Four raw logs contain an AI explanation. Skill contribution notes deny it in queue-end and receipt-total. Rules notes deny it in queue-end, gallery-case and receipt-total. The rules queue drill also denies it. Every raw log was available to every arm. This is an inherited extraction limitation and a model evidence-reading failure. The skill instructions were left frozen after discovering it.
- Shelf-boundary messages are labelled USER and no record establishes staff authorship. Both rule-bearing arms call them staff notes in step 1 and step 2. This is an unsupported reattribution. If a reader treats those labels as uncertain rather than false, the corresponding whole-output counts improve equally in the two arms.
- Skill queue-end flags claim that the test runner is unknown, although each Bash call is in an assistant turn. They also say the file write lacks a successful record despite its non-error `File written.` result. Rules gallery-case flags make the same runner mistake, and its garden drill makes the final runner unknown.
- Rules puts both Hold lines above the student-section heading. The skill puts both inside the section. This matters when the instructor copies only the part intended for the child.
- Skill gallery-case omits the version-3 edit/run from the student section when A3 is missing. Rules gallery-case supplies no versioned AI facts, and rules receipt-total omits the final test. These failures use the protocol's strict final-run completeness criterion. Under the narrower historical criterion that accepts omissions, the AI-facts row improves, but the missing answers and outside Hold remain.
- Rules map-offset quotes an “I am not sure” answer in the family note. The skill uses the required factual fallback. The rules gallery output loses punctuation from a student's answer, omits the verbatim answer blocks and repeats the instructor marker as an answer.
- Several outputs impose missing publicity consent as an additional gate for a private family note. The skill requires adult review for that note, while the separate classroom agreement controls drills. The plain queue, garden, map and shelf step-2 outputs invoke this extra gate. Skill queue does too. These are recorded process errors alongside the counted text errors.
- Plain family notes credit the AI's check to the child, assert independent discovery, convert an absent run into “hasn't run,” introduce a group run or class activity, and claim ability. The receipt family note avoids those factual errors. Plain gallery and garden also assert the project is unpublished without deployment evidence. Plain map step 1 asks why an out-of-range lookup would match the reported point. Plain map drill denies copying code while reproducing the two-line function verbatim.
- Plain drill refusals give both bugs and fixes, and ask for the student's consent instead of the family's agreement. The plain receipt drill also attributes consent to the student. Queue's made drill names the source project. All made plain drills miss at least one required workflow element.

The basic no-percentage and private-name checks pass in this set. The receipt peer name and injection marker occur only in private instructor discussion. Neither reaches the family note or student section in either rule-bearing arm.

## Where the package helps and where it does not

The observed skill advantages over the inline rules are the two section-local Holds, one additional complete verbatim answer set, one additional complete student AI-fact section, one additional family fallback and two more factually supported made drills. Step 1 has one more moment-specific question set and one more supported contribution note.

The inline rules tie on the principal question answer-withholding and AI-action checks, all six family-note factuality checks, five-line approval, all four prediction and hint checks, all four workflow checks and both clean refusals. It does better on the strict question-premise row. The instructor-flags factuality totals tie, with different failing cases. The plain arm more often reads the ordinary assistant explanation correctly than either rule-bearing arm.

One sample per cell cannot establish that these differences persist. Cases share the same short-function/snapshot structure. The evaluator selected the cases, edited the rules, then judged the outputs with knowledge of the arm. Six clean skill drills are six outputs across only six cases. There is no real-student use, usability observation, independent hand review or learning measure here. **THIN** remains the reading because a repeatable advantage over the complete-rules baseline has not been established.

## Reproduction

From the repository root, these offline commands verify the freeze, controls, all exported outputs, manual counts and rebuilt archive.

```sh
python3 -B evals/check.py
```

To inspect the pattern screen or recount the recorded hand judgments separately, use the following commands. A recount is not a new hand review.

```sh
python3 -B evals/check_scorer.py
python3 -B evals/score_checkin.py --runs verification/heldout/runs --out verification/heldout/screen.json
python3 -B evals/hand_verdicts.py
```

With an already authenticated Claude CLI and authorization to spend subscription quota, a fresh comparison uses the same runner. The runner refuses existing run IDs. A new run requires a new hand review, with all slips retained. No browser or localhost run is needed for this evaluation.

```sh
sh evals/run.sh --dry-run --run-id heldout-reproduction-dry --repeats 1
sh evals/run.sh --run-id heldout-reproduction --repeats 1
python3 -B evals/score_checkin.py --runs evals/runs/heldout-reproduction --out verification/heldout/reproduction-screen.json
```

The current ZIP contains the skill and helpers only. It contains the evaluated instructions. The handwritten drill example and its embedded page copy have a diagnostic question in hint 2 for consistency. That example was withheld from the model run. Historical published counts remain labelled historical and are kept separate from these 54 outputs. This round used offline packaging and evidence checks. Existing browser captures and the earlier release audit belong to the prior release.
