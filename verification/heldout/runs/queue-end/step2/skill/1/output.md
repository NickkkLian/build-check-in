```text
# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Ari built Queue Board, a small waiting list that should serve the earliest arrival first.
2. Fixed or explained: Ari wrote, "It gave blue even though red arrived first."
3. The AI: The AI wrote the check file and changed the serving line twice, once at version 2 and again at version 3. The record shows the check failing at versions 1 and 2, then reporting one example passing at version 3.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- Q1: Own answer. It matches the failing check Ari saw at version 1, "FAIL expected 'red', got 'blue'" [result:test-1]. It is the quote used in family note line 2.
- Q2: Own answer, no flag. Its description of version 2 (it reads the last item and does not remove it) matches the change from `items.pop()` to `items[-1]` [snapshot:2:queue.py]. The AI made that edit [tool:edit-2][result:edit-2]. No AI explanation of the cause is recorded, so nothing here credits one.
- Q3: Contradicted by the history, so check with Ari.
  - "The AI made the last edit" is supported [snapshot:3:queue.py][tool:edit-3][result:edit-3].
  - "I asked it to check the two names again" does not match the recorded request. Prompt 3 reads "Please make the next change for version 3." [prompt:3]. No request to check the two names is recorded.
  - The answer also does not say what changed at version 3 (`items[-1]` became `items.pop(0)`), which the question asked for.
  - It is left out of the family note.
- Version 3 "PASS" is a recorded tool report, not an independent rerun [result:test-3]. Who ran each test command is not shown in the record [tool:test-1][tool:test-2][tool:test-3].
- The line 1 author of `queue.py` at version 1 is unknown [snapshot:1:queue.py]. The AI wrote the check file [tool:test-write], but the record does not show a successful write [result:test-write].
- Consent: the history records family consent for public drafts as missing. Keep this note and the page below private until consent is confirmed.

## For you (the student)
Hold: go over answers A3 with the student before giving them this page.
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:queue.py]
AI did: wrote a check file for `serve(['red', 'blue'])` [tool:test-write]. The record shows a check run that failed with "FAIL expected 'red', got 'blue'" [result:test-1].
Answer A1, copied unchanged:
> It gave blue even though red arrived first.

### Version 2 [snapshot:2:queue.py]
AI did: changed line 2 of `queue.py` from `items.pop()` to `items[-1]` [tool:edit-2][result:edit-2]. A later recorded run reports "FAIL version 2 still does not meet the expected result." [result:test-2]
Answer A2, copied unchanged:
> The second version only reads an item and leaves the list alone.

### Version 3 [snapshot:3:queue.py]
AI did: changed line 2 of `queue.py` from `items[-1]` to `items.pop(0)` [tool:edit-3][result:edit-3]. A later recorded run reports "PASS one fictional example, exit code 0" [result:test-3].
Answer A3, copied unchanged:
> The AI made the last edit. I asked it to check the two names again.
(Flagged for the instructor: the history shows otherwise. Prompt 3 asked for "the next change for version 3", not a check of the two names.)
```
