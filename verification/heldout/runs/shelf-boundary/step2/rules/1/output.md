# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Faye worked on Shelf Slots, a function that says whether a shelf is full once its used slots reach its capacity.
2. Fixed or explained: Faye wrote, "At three out of three there is no room left."
3. The AI: The saved history records no AI replies or AI edits, so what the AI did is not recorded.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- Q1 [prompt:1][snapshot:1:shelf.py]: A1 is consistent with the idea, which says full means used equals capacity. The history records a failure for version 1 (expected True, got False). That failure comes from a staff note, not a rerun, and the writer and runner are not recorded. The answer is short and plain, so it reads as the student's own.
- Q2 [prompt:2][snapshot:2:shelf.py]: A2 is consistent with the history. Version 2 changed the line to `capacity + 1`, and the saved note says the failure remained. No test run, AI reply or tool call is saved, so who made that edit is unknown.
- Q3 [prompt:3][snapshot:3:shelf.py]: A3 says the student does not know who made the edits. That matches the history, where the writer of all three versions is unknown. A3 does not say what changed at version 3, so you could ask Faye to describe the change in their own words. There is no saved run for version 3.
- Attribution: every changed line is `unknown_or_conflicting` [snapshot:1:shelf.py][snapshot:2:shelf.py][snapshot:3:shelf.py]. Do not credit Faye or the AI with any edit, test or fix.
- Consent: the family's consent and classroom-drill consent are both missing, so public use is not permitted. Keep the showcase notes private until the family agrees.
- No answer looks pasted from an AI, none is contradicted by the history, and none contains personal details or other students' names.

## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:shelf.py]
AI did: not recorded
Answer A1, copied unchanged:
> At three out of three there is no room left.

### Version 2 [snapshot:2:shelf.py]
AI did: not recorded
Answer A2, copied unchanged:
> The second version still misses the exact boundary.

### Version 3 [snapshot:3:shelf.py]
AI did: not recorded
Answer A3, copied unchanged:
> I looked at the three versions. I do not know who made the edits.
