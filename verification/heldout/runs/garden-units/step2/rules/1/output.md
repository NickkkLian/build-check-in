# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Bea made a watering planner that turns litres into millilitres.
2. Fixed or explained: Bea wrote, "Ten made the answer even smaller."
3. The AI: The AI wrote a small check for the planner and ran it, and the check failed. It then changed the multiplier to 10, and the check still failed. Bea told the AI she then changed the multiplier by hand to 1000 and asked it to check. The AI's recorded run reported a pass on one example.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- Q1: Own answer, consistent with the history. It matches the test's expected 2000 [result:test-1]. Version 1's water.py has an unknown writer [snapshot:1:water.py]. Version order comes from staff folder names, not timestamps.
- Q2: Own answer, consistent with the history. The AI's edit changed `* 100` to `* 10` [snapshot:2:water.py][tool:edit-2][result:edit-2], and the test still failed [result:test-2].
- Q3: Bea's claim to have changed the multiplier by hand is self-reported. The diff matches it [snapshot:3:water.py][prompt:3], but a diff does not show who typed it. The answer does not address the "what does the history show about who did it" part. The "why" it gives is consistent with the history. Ask Bea how she decided on that number.
- Q3: The pass was one fictional example. It is a recorded report, not a rerun [result:test-3].
- No answers read as pasted AI text. None contain personal details, other students' names or instructions. No answers are missing.

## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:water.py]
AI did: wrote a check for millilitres(2) and ran it. The recorded result was "FAIL expected 2000, got 200" [tool:test-write][result:test-1].
Answer A1, copied unchanged:
> Two litres should fill two thousand millilitres.

### Version 2 [snapshot:2:water.py]
AI did: edited water.py to `return litres * 10` [tool:edit-2][result:edit-2]. The recorded test run failed [result:test-2].
Answer A2, copied unchanged:
> Ten made the answer even smaller.

### Version 3 [snapshot:3:water.py]
AI did: ran the check, and the recorded result was a pass on one example [tool:test-3][result:test-3]. The hand edit to `* 1000` is the student's own report [prompt:3].
Answer A3, copied unchanged:
> I changed the multiplier by hand because each litre is a thousand millilitres.
