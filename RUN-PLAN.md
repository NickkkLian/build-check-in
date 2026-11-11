# Supervisor run plan: second held-out round

Status: prepared offline only. No new Claude outputs or new performance claims. The rating stays THIN. Only the Supervisor may run the model command below, using the existing Claude subscription. Do not install credentials, copy settings from another account, publish output, or run project code.

## Fixed design

The cases were frozen in commit `746ee88` before extractor or runner edits. `evals/heldout-v2/FROZEN.txt` covers 52 files, including the written SKILL.md. Its author is this case-preparation agent; the written rules remain those of the November 6 editor. The case author also changed the extractor, so this is not a blind study. No model feedback informed these repairs. See the frozen [protocol](evals/heldout-v2/PROTOCOL.md) for every criterion, applicability rule and limitation.

- Six cases, three tasks (`step1`, `step2`, `drill`), three arms (`plain`, `rules`, `skill`), three repeats: **162 independent Claude CLI processes**.
- Each arm has 54 outputs; each task/arm cell has 18. Four allowed drills per repeat give 12 allowed opportunities per arm; two blocked cases give 6.
- The `rules` arm is plain+rules: the historical plain prompt plus the complete unchanged written SKILL.md. Both plain arms have Read only; skill has Read and Skill. All receive identical raw logs, snapshots, current source, context, diffs and extracted history. Skill additionally has the helper/template package; worked examples are excluded.
- The runner retains the earlier `--model sonnet` alias and records the actual resolved model. The November 6 run resolved to `claude-sonnet-5-5`; do not assume today's alias does. The post-run audit requires one identical resolved model throughout. Record any model-version change and do not pool it with old counts.

## Completed preparation and checks

From the repository root, this exact dry run was prepared:

```sh
python3 -B evals/runner_checkin.py --suite-root evals/heldout-v2 --dry-run --run-id heldout-v2-dry-20261111 --repeats 3 --tasks step1,step2,drill --arms plain,rules,skill
python3 -B evals/audit_prepared.py --run-id heldout-v2-dry-20261111 --out verification/extractor/dry-run-audit.json
python3 -B evals/check_preparation.py --run-id heldout-v2-dry-20261111
```

The existing run directory is intentionally protected from overwrite. To repeat preparation, use a new run ID and pass that ID to both audits. Work copies are ignored under `evals/runs/`; public-safe hashes are in `verification/extractor/dry-run-audit.json`. Local raw logs are in the job folder's `evidence/` directory. A temporary local `claude` tripwire was first on PATH during preparation; calling it would fail the round and leave a marker. No marker was created.

The repository offline gate is `python3 -B evals/check.py`. The release audit must run on a clean candidate export without `.git` or ignored execution files; running `scripts/check-release.py` directly on a checkout correctly rejects inherited Git history and private execution paths. The local candidate was assembled from explicit Git tracked/unignored candidate paths. A configured global public-push-guard also applies. Run its underlying publish gate against the final commit range; retain the raw result in the job's evidence folder. Its exact local path and result belong in the private handback, not this public repository. This job does not write a global gate stamp or push. Do not use the old `export_runs.py` or `hand_verdicts.py` for this round: those intentionally describe the historical 54-output study.

## Actual model run: Supervisor only

Start in this repository, with the reviewed commits present. Verify the local evidence directory exists (`../evidence`). This command consumes **162 model calls**. It is deliberately absent from local check scripts.

```sh
python3 -B evals/runner_checkin.py --suite-root evals/heldout-v2 --run-id heldout-v2-claude-20261111 --repeats 3 --tasks step1,step2,drill --arms plain,rules,skill > ../evidence/heldout-v2-claude.log 2>&1
```

Inspect the exit status and log immediately. The runner stops on the first failed CLI call, empty result, non-success envelope or read denial. Do not discard a failed directory or retry individual cells until they pass. Retain error metadata and partial envelopes. If a whole fresh attempt is necessary, choose a new run ID, document its reason, retain the failed attempt and state exclusion counts. Never combine selective replacement successes with the original matrix.

After a complete successful run, run these read-only audits and screen:

```sh
python3 -B evals/audit_prepared.py --run-id heldout-v2-claude-20261111 --out ../evidence/heldout-v2-run-audit.json > ../evidence/heldout-v2-run-audit.log 2>&1
python3 -B evals/score_checkin.py --runs evals/runs/heldout-v2-claude-20261111 --out ../evidence/heldout-v2-screen.json > ../evidence/heldout-v2-screen.log 2>&1
```

The audit must show 162 completed outputs, nine cells of 18, 52 frozen hashes, one resolved model, byte-identical case/task evidence across arms/repeats, unchanged rules, correct helper staging, no envelope errors or permission denials, and outputs matching envelope results. The screen is a search aid: read every output, including passes. Its generic drill check expects a failed AI attempt even in reply-absent cases; use the protocol's applicability rule when hand-counting.

## Hand-count and re-rate

1. Prefer a reviewer other than the case author or rule editor. Read the protocol first. If feasible, give outputs opaque IDs, hide their arm labels until verdicts are written, and ask a second reviewer to adjudicate disagreements. Record whether blinding actually occurred.
2. For each of the 162 outputs, read its raw log, snapshots, extracted history, supplied answers and `expected.json`. Keep `expected.json` outside model-visible input. Record the output hash from the audit and one `pass`, `fail` or `n/a` per applicable protocol criterion, with an exact output quote and plain reason. For a missing required section, record a failure and the empty quote with reason `required section absent`. Flag unsupported staff authorship anywhere, including instructor-only notes. A USER speaker is unknown even when an instructor supplied the snapshots.
3. Read the actual assistant reply before judging whether an explanation was recorded. Distinguish its wording from whether its claims are true. Denying a present explanation and inventing an absent explanation are separate failures. Keep a human claim of a manual edit separate from verified identity and from the assistant's recorded final run. Do not let an accurate family note conceal a false instructor flag.
4. For each task/arm, tally criterion passes over applicable outputs and whole-output passes over 18. A whole-output pass requires every required criterion to pass; n/a never excuses a missing section. Count made and blocked drills separately. Report the 12 explanation-present and 6 reply-absent outputs per task/arm, plus the 3 label-escape staff-authorship targets per task/arm. Include all failures and all screen/hand-review disagreements with quotations.
5. Show the three repeat verdicts per case alongside aggregate counts. Compare skill to rules first, then plain. Count case-level wins/ties/losses; do not present 18 outputs as 18 independent projects. Report excluded attempts, failed reads and unresolved judgments. Reviewers should independently recompute the table from the per-output rows before acceptance.
6. Keep THIN for a tie with rules, inconsistent gains, critical attribution/consent regressions, insufficient review or dry-run-only evidence. Any proposed upgrade needs repeatable practical advantage over rules and separate evidence of usefulness outside synthetic exercises. This evaluation cannot establish classroom learning or adoption. Record the strongest reason for the final rating, including evidence against upgrading it.

Do not commit raw execution work folders: they contain local paths and runtime metadata. If the Supervisor later approves a public evidence export, copy only fictional inputs/outputs and necessary metadata into a new `verification/heldout-v2/` directory, replace checkout paths in prompt/invocation copies, omit session identifiers, verify output bytes against envelopes, and run the public candidate gate again. Preserve the original private execution files and export hashes. Publishing or pushing remains a separate Supervisor decision.
