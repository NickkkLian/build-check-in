# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Ari is building Queue Board, a waiting list that should serve the earliest arrival first.
2. Fixed or explained: Ari wrote: "It gave blue even though red arrived first."
3. The AI: The AI wrote the check file, ran it, and made the edits at version 2 and version 3. The last recorded run reported a pass.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- Q3 (A3): The history contradicts part of this answer. "The AI made the last edit" is supported [snapshot:3:queue.py][tool:edit-3][result:edit-3]. But the third prompt reads "Please make the next change for version 3." [prompt:3]. It does not ask the AI to check two names, and no prompt in the history does. Ask Ari what they asked the AI at that step. A3 is not used in the family note.
- Q2 (A2): This looks like Ari's own answer. It matches version 2, where the AI replaced `items.pop()` with `items[-1]`, which reads an item and does not remove it [snapshot:2:queue.py][tool:edit-2]. The recorded failure at that step is only "version 2 still does not meet the expected result" [result:test-2]. You could ask Ari what the version 2 line returned for `['red', 'blue']`.
- Q1 (A1): This looks like Ari's own answer. It matches the recorded failure "FAIL expected 'red', got 'blue'" [result:test-1].
- The writer of the version 1 `queue.py` is unknown [snapshot:1:queue.py]. The note does not credit Ari or the AI with it.
- All test results are recorded reports, not reruns [result:test-1][result:test-2][result:test-3]. The "pass" is a recorded report only.
- Consent for public drafts is missing in the history. Do not publish the showcase notes below until the family's agreement is confirmed.

Hold: go over answers A3 with the student before giving them this page.
## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:queue.py]
AI did: wrote the check file `test_case.py` and ran it; the recorded result was a fail [tool:test-write][tool:test-1][result:test-1]. Who wrote the version 1 `queue.py` is unknown [snapshot:1:queue.py].
Answer A1, copied unchanged:
> It gave blue even though red arrived first.

### Version 2 [snapshot:2:queue.py]
AI did: changed the `queue.py` line to `return items[-1]`, then ran the check; the recorded result was a fail [tool:edit-2][result:edit-2][result:test-2].
Answer A2, copied unchanged:
> The second version only reads an item and leaves the list alone.

### Version 3 [snapshot:3:queue.py]
AI did: changed the `queue.py` line to `return items.pop(0)`, then ran the check; the recorded result was a pass [tool:edit-3][result:edit-3][result:test-3].
Answer A3, copied unchanged:
> The AI made the last edit. I asked it to check the two names again.

(Flagged for the instructor: the history shows otherwise.)
