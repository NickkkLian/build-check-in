# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Bea built Water Planner, a small watering planner that converts litres to millilitres.
2. Fixed or explained: Bea wrote, "Two litres should fill two thousand millilitres."
3. The AI: The AI wrote a small check for the planner and made one change to the multiplier, which did not pass the check. Bea reported making the next change by hand. The AI then ran the check again.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- None of the three answers looks pasted, and none contradicts the history. Q1 and Q2 match the recorded results: the check expected 2000 and got 200 [result:test-1], and the AI's change from 100 to 10 made the number smaller [snapshot:2:water.py][tool:edit-2].
- Q3: Bea says they changed the multiplier by hand. Only Bea's own message reports this [prompt:3], and the diff matches it [snapshot:3:water.py]. Treat it as the student reporting it, not as observed. The reported pass [result:test-3] is a recorded report, not a rerun.
- Version 1: the writer of `water.py` is unknown [snapshot:1:water.py]. Don't credit the starting code to Bea or to the AI.
- Version 1 check: the AI wrote the check file [tool:test-write]. The outcome of that write is recorded as "unknown", with only the text "File written." [result:test-write]. The AI ran the check and a failure was reported [tool:test-1][result:test-1].
- Version 2 failure: the recorded failure text is generic, "version 2 still does not meet the expected result" [result:test-2].
- Version order comes from folder names that staff supplied. Timestamps do not prove the order [snapshot:1:water.py].
- Consent: the history records public-draft consent as missing. Don't share the showcase notes publicly until the family agrees.

## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:water.py]
AI did: the AI wrote a small check for millilitres(2) [tool:test-write], then ran it. The run was reported as "FAIL expected 2000, got 200" [tool:test-1][result:test-1].
Answer A1, copied unchanged:
> Two litres should fill two thousand millilitres.

### Version 2 [snapshot:2:water.py]
AI did: the AI changed the multiplier line from `litres * 100` to `litres * 10` [tool:edit-2][snapshot:2:water.py]. The check was then reported as still failing [result:test-2].
Answer A2, copied unchanged:
> Ten made the answer even smaller.

### Version 3 [snapshot:3:water.py]
AI did: the AI ran the check after your message, and the run was reported as a pass [tool:test-3][result:test-3]. The student reported making the change to `litres * 1000` by hand [prompt:3].
Answer A3, copied unchanged:
> I changed the multiplier by hand because each litre is a thousand millilitres.
