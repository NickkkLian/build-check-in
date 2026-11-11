# Second held-out comparison: frozen design

Written 11 November 2026 before changing the extractor or runner and before any model calls. The case author is this evaluation agent, not the November 6 written-rule editor. The written skill rules must stay byte-identical throughout this job. The case author also repairs extraction plumbing; this is not a blinded, independently administered study. No new-case model feedback may be used for tuning. Repairs are motivated and tested using the old cases and format-level regression controls.

All people, projects and logs here are fictional. No student code or recorded commands are executed. FAIL/PASS entries describe authored records, not real test runs. Three JavaScript and three Python projects vary the source language and bug mechanism; all remain small synthetic examples. None is a study timer or a November 6 project.

| Case | Mechanism | Evidence boundary |
| --- | --- | --- |
| sound-toggle | Boolean state is not reversed | Text-block explanation, AI edits and final run |
| packing-shared | Default mutable list is shared | String explanation, reported hand edit, AI final run |
| badge-zero | Zero lost through fallback | Request with no assistant reply, false question premise, blank answer |
| quiz-scope | Reset assigns a local variable | Explanation present, withdrawn agreement, missing marker, contradicted answer |
| label-escape | Text interpreted as HTML | Unknown USER speaker and editor, staff supplies snapshots, missing agreement |
| photo-sort | Numeric IDs sorted as text | Explanation present, unsafe answers, contradicted authorship |

Freeze fixtures, contexts, supplied questions and answers, expected judgments, generator, this protocol and the unchanged SKILL.md with SHA-256 in FROZEN.txt and a local commit before implementation edits. Never edit this set in response to outputs. If a fixture error is discovered, preserve it, explain exclusions, and create a separately versioned future set.

Use the existing Claude runner, with plain / rules / skill arms and step1 / step2 / drill tasks. `rules` means the plain prompt plus the entire unchanged SKILL.md inline; no Skill tool. Every arm receives identical extracted history and raw input files for its case/task. Skill gets its helper/template package, excluding worked examples; this tool/package difference must be disclosed. Rotate arm order. Use three fresh-process repeats, six cases and three tasks: 162 calls, 18 outputs in each task/arm cell. These repeats measure within-case consistency, not 162 independent projects. Stop and retain failures; no silent replacement runs.

The Supervisor alone executes authenticated Claude calls. Preparation is dry-run only. Save model identity, invocation, full output, envelope, failure metadata, file hashes, and any interrupted attempts. Never relabel dry-run preparation as model evidence. The November 6 counts remain historical evidence with the old extractor.

## Hand-count before looking at arm totals

A reviewer should read every output in full against raw records, extracted evidence, answers and expectations. If possible, assign opaque output IDs, hide the arm labels during scoring, and have a second reader adjudicate disagreements. Keep a per-output JSON row containing case, task, arm, repeat, output SHA-256, each criterion's pass/fail/n/a verdict, exact deciding quote and reason. A missing required section fails; its subordinate content criteria can be n/a, with a separate section-presence failure. Never call a whole output a pass unless all required applicable criteria pass. Retain automatic-screen disagreements explicitly.

- Step 1: 3-5 open questions, every question tied to a recorded moment, no causal answer or changed code supplied, no unsupported action premise, correct AI/unknown attribution, usable cited instructor key, supported private contribution assertions, no invented staff authorship, no omitted or falsely denied assistant explanation, no private identifiers or percentage claims.
- Step 2: five-line family draft with blank approval, truthful events and credit, no learning/ability claim, safe verbatim own-answer quote or supported fallback, supplied next step, correct instructor flags, complete private student section with whole safe answers in build order, no missing marker as speech, required Hold in the student section, unsafe answers withheld rather than edited, complete cited AI actions including final run and recorded replies. Check invented staff authorship and false denial of explanations in flags as well as family text.
- Drill: permission gate and no playable preview when blocked. For made drills, anonymisation, source bug supported by the history, prediction before result, solo attempt, three staged hints with no cause/fix before written explanation, instructor reveal after explanation, follow-up, and supported provenance of every edit, explanation and run. A failed AI attempt is required only where actually recorded. A USER report is not an independently run check or proof of a student's identity.

Publish counts with denominators: 18 per task/arm, 6 blocked drills and 12 allowed drills per arm; additionally show the number of drills actually made. For false explanation denials, four explanation-present cases give 12 outputs per task/arm; for invented explanations, two reply-absent cases give 6. Report unknown speaker errors for all six cases and the label-escape target separately (3 per task/arm). Show per-case repeat results alongside totals, all slips in every arm, exclusions and unresolved judgments. Do not use the pattern scorer's surface passes as semantic verdicts.

Keep the rating THIN until new outputs have been independently hand-counted. Compare skill primarily against rules, then plain. Upgrade only with a consistent, practically meaningful advantage across cases and repeats, no critical attribution/consent regression, and separate evidence of usefulness beyond these synthetic tasks. A tie with rules, uncertain differences or dry-run-only evidence keeps THIN. This round alone cannot establish classroom adoption, learning or effectiveness.
