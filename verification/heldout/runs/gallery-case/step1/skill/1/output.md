# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. In your first prompt, you asked the AI for a small check for `is_photo('photo')`. The AI ran it and the screen said "FAIL expected True, got False". What did you think that message meant?
2. At version 2, the AI changed a line in `gallery.py` and ran the check again. It still failed. Why do you think that change didn't help?
3. Your second prompt was "Please try a change for version 2." What were you hoping the AI would try, and why did you word it that way?
4. Before you wrote your third prompt, what did you look at or think about?
5. At version 3, the recorded run says one example passed. Which other examples would you try to be sure it works, and why?

## Instructor key
Q1 [prompt:1][result:test-1]: A good answer mentions what the student saw on screen and what they took it to mean: the check wanted a true answer and the code gave a false one for `'photo'`. The student's own reading may be partial or wrong.
Q2 [tool:edit-2][result:test-2][snapshot:2:gallery.py]: A good answer mentions that version 2 changed the text the tag is compared to, but the compared word is still one fixed spelling, so `'photo'` still does not match. The student may only say it "didn't work", which shows weak understanding.
Q3 [prompt:2]: A good answer mentions what the student expected the AI to do, or admits they did not know what to ask. The prompt gives no detail, so the student's own thinking about the cause is not in the record.
Q4 [prompt:3][result:test-2]: A good answer mentions something the student looked at, such as the failed result, the code, or the idea that capital and small letters should both work. "Nothing" or "I just asked again" is an honest answer that the instructor should note.
Q5 [result:test-3][snapshot:3:gallery.py]: A good answer names other spellings of the tag, such as all capitals, a mix of capitals and small letters, or the original capitalised form, and says why. Only one fictional example is recorded as tested.

## Private AI contribution note
AI contribution: The AI wrote the test file `test_case.py` [tool:test-write][result:test-write]. The AI's recorded edit matches the version 2 change to line 2 of `gallery.py` [snapshot:2:gallery.py][tool:edit-2][result:edit-2], and the version 3 change to line 2 [snapshot:3:gallery.py][tool:edit-3][result:edit-3]. The record shows the check failing at version 1 and version 2 [result:test-1][result:test-2], and a reported pass at version 3 [result:test-3]. The student wrote three prompts [prompt:1][prompt:2][prompt:3]. No hand edits by the student are reported. The origin of the version 1 code in `gallery.py` is unknown [snapshot:1:gallery.py].
Instructor check:
- The pass at version 3 is a recorded tool report, not a rerun, and covers one fictional example [result:test-3].
- Prompts 2 and 3 name no cause and no fix [prompt:2][prompt:3], so the record doesn't show whether the student understood the problem.
- Only a one-line comment of `test_case.py` is recorded [tool:test-write], so its full content is unverified.
- Version order comes from folder names supplied by staff, and timestamps don't prove the order [snapshot:1:gallery.py]. There is no git history in the folder.
- Family consent is recorded as missing, so no public drafts are permitted. The classroom drill agreement is withdrawn, so no drill can be made from this history.
