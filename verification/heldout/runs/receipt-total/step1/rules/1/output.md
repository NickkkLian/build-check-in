# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. In your first prompt, you asked the AI to write a check for total([4, 6], 2). What did you expect that check to give, and why?
2. The check ran and the screen said "expected 12, got 8". Walk me through what you thought when you saw that.
3. At version 2, the AI changed one line and ran the check again, and it still failed. Why do you think that change didn't help?
4. Your third prompt was "Please make the next change for version 3." How did you decide what to ask for, and what did you look at afterward?
5. Imagine the service fee on a receipt was 5 instead of 2. What would you check to be sure the total is right?

## Instructor key
Q1 [prompt:1][tool:test-write]: A good answer mentions that the student's prompt gives prices 4 and 6 and a fee of 2. The student should be able to say how the expected total is made from those. The history records the expected value only in the failure message, "expected 12" [result:test-1]. The check file's content beyond a comment line is not recorded, so do not assume what the AI wrote in it. The AI's record shows it wrote the check file [tool:test-write].
Q2 [result:test-1]: A good answer mentions what the student noticed about the gap between 12 and 8, and what they tried or thought next. The history does not record what they did after seeing it. The failing run is a recorded report, not a rerun.
Q3 [snapshot:2:receipt.py][tool:edit-2][result:test-2]: A good answer mentions that the version 2 edit replaced the fee-related part of the return line with 0, so the fee was still not added. The student should say in their own words why that left the total wrong. The AI edit record matches the diff. The test result is a recorded report, and it does not say why the test failed.
Q4 [prompt:3][snapshot:3:receipt.py][result:test-3]: A good answer mentions how the student chose what to ask. The history shows the prompt did not name a change, so they may say they trusted the AI or looked at the failure. For "afterward", the student may mention the AI's recorded pass, "PASS one fictional example". That pass is a recorded report, not an independent rerun, and only one example was checked.
Q5 [prompt:1][result:test-3]: A good answer mentions trying another example with a different fee and working out the expected total by hand first. This is a transfer question and has no single recorded answer. The recorded pass covers only one example [result:test-3].

## Private AI contribution note
AI contribution: The AI's record shows it wrote the check file [tool:test-write], and a failing run was recorded after it [result:test-1]. The AI's edit record matches the diff at version 2 [snapshot:2:receipt.py][tool:edit-2] and at version 3 [snapshot:3:receipt.py][tool:edit-3]. A pass was recorded after version 3 [result:test-3]. The student's prompts [prompt:2][prompt:3] ask for a change but do not say what to change. The writer of the version 1 `receipt.py` is unknown [snapshot:1:receipt.py]. No hand edits by the student are reported.
Instructor check: Version order comes from staff-supplied folder names, and timestamps do not prove chronology [snapshot:1:receipt.py]. Test results are recorded reports, not reruns [result:test-1][result:test-2][result:test-3]. The write result for the check file is "File written." with no recorded outcome [result:test-write]. No recorded AI reply explains any cause or fix, so Q3 and Q4 depend on the student's own account. The context has no staff claims. Consent for public drafts is missing [context:brief], so keep everything here private.
