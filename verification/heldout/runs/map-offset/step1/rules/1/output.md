# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. Your first prompt says you got "hill" instead of "lake". Walk me through what you did and what you expected to see.
2. At version 2 the line in `map.py` looked different, but you told the AI it "still gives the same point". Why do you think that change did not help?
3. In your second prompt you asked the AI to explain the bug before you changed anything. Why did you want an explanation first?
4. Version 3 looks different from version 2. Who made that change, and how did you find out it was the right one?
5. How would you check that the route picker returns the right point for any chosen number?

## Instructor key
Q1 [prompt:1][snapshot:1:map.py]: A good answer mentions the student picking one position in the list and expecting the "lake" point. The history shows the student got "hill" instead. The code at version 1 is `return points[index + 1]`, so the answer may mention that the result was one place off in the list.
Q2 [prompt:2][snapshot:2:map.py]: A good answer mentions that the version 2 line `points[1 + index]` only swaps the order of the same addition, so it picks the same point. Who made this edit is not recorded.
Q3 [prompt:2]: A good answer mentions wanting to understand the cause before editing, or not wanting to guess again after the first change failed. Whether the AI replied is not recorded, so the answer should not claim what the AI said.
Q4 [prompt:3][snapshot:3:map.py]: A good answer says honestly who made the version 3 change and how they checked it. The student's own prompt says they did not record who changed it or any test run, so a confident claim of a test or of doing it themselves is unsupported. The change itself is `points[index]`, which matches the zero-based idea in [context:brief].
Q5 [snapshot:3:map.py][context:brief]: A good answer mentions trying a known position (such as the first one, 0, or the lake point) and comparing the result with the point they expect. Zero-based counting from the brief is a good thing to hear.

## Private AI contribution note
AI contribution: No AI action is recorded. The history has no AI reply, no AI edit record and no tool result [prompt:1][prompt:2][prompt:3]. The student asked an AI to explain the bug at version 2 [prompt:2], but the reply is not recorded. Who wrote each line of `map.py` at versions 1, 2 and 3 is unknown [snapshot:1:map.py][snapshot:2:map.py][snapshot:3:map.py].
Instructor check:
- Version 3's author is unknown. The student wrote that they did not record who changed it or any test run [prompt:3]. Do not credit the fix to the student or to the AI.
- The folder order of the versions was supplied by staff, and timestamps do not prove the order [snapshot:1:map.py].
- "Got hill instead of lake" and "still gives the same point" are the student's reports. No test or run result is recorded [prompt:1][prompt:2].
- No git history is present, so all four attribution entries are unknown or conflicting.
- Consent for public drafts is missing. Keep all of this private.
