# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. Your first prompt asked the AI to write a check for a receipt of 4 and 6 with a fee of 2. The AI ran that check on version 1 and it said "expected 12, got 8". How do you think the number 12 was worked out?
2. Look at version 1 when the check failed. What did you think was wrong, and where in the file did you look?
3. Your second prompt said "Please try a change for version 2." The AI changed the total line and the check still failed. Why do you think that change didn't help?
4. For your third prompt you asked the AI to "make the next change for version 3." What did you expect the AI to do, and why did you ask it that way?
5. The AI's record says the check passed after version 3. How would you make sure the total is right for a receipt that is not 4 and 6?

## Instructor key
Q1 [prompt:1][result:test-1]: A good answer mentions that 4 + 6 = 10 and the fee of 2 is added to get 12. The check is one example [tool:test-write] (the AI wrote it; whether the student chose the numbers is unknown, since the prompt supplies them). The student may say they are not sure how the AI picked 12.
Q2 [result:test-1][snapshot:1:receipt.py]: A good answer mentions the total came out lower than expected (8 instead of 12) and that the student looked at the total line or the fee. Who wrote version 1 is unknown, so do not assume the student wrote the line. An answer like "I didn't look, I asked the AI" is honest and fits the history.
Q3 [tool:edit-2][result:test-2][snapshot:2:receipt.py]: A good answer mentions the fee still was not counted in the total, so the result stayed wrong. The AI made this edit; the student only asked for "a change". Listen for whether the student can say what the line did differently, or only that the test still failed.
Q4 [prompt:3][tool:edit-3][snapshot:3:receipt.py]: A good answer mentions what the student hoped would happen, such as that the fee would be added. The prompt names no cause or fix, so the student may say they were guessing or trusting the AI. Both are fine to hear.
Q5 [result:test-3]: A good answer mentions trying other prices or fees, and checking by adding up by hand. The pass is a recorded report of one example [result:test-3], not a rerun. Listen for whether the student sees that one passing example is not proof for every receipt.

## Private AI contribution note
AI contribution: The AI wrote the check file [tool:test-write] and the record shows it ran the check, which failed at version 1 [result:test-1] and version 2 [result:test-2]. The AI made the edit at version 2 [snapshot:2:receipt.py][tool:edit-2][result:edit-2] and the edit at version 3 [snapshot:3:receipt.py][tool:edit-3][result:edit-3]. The student's recorded part is three prompts [prompt:1][prompt:2][prompt:3]. Who wrote the original total function in version 1 is unknown [snapshot:1:receipt.py]. No student hand edits are reported.
Instructor check: The pass after version 3 is one recorded report on one example, not an independent rerun [result:test-3]. The test file's content was not captured beyond one comment line [tool:test-write], and its write result is unknown [result:test-write]. Version order comes from folder names supplied by staff, and timestamps do not prove the order [snapshot:1:receipt.py]. The history has no AI explanation text. Prompts 2 and 3 name no cause or fix, so the history does not show whether the student understood why the first two versions failed. Family consent for public drafts is missing, so keep any later notes private.
