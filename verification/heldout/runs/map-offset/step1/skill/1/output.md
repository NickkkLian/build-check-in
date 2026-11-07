# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. At version 1, you reported getting "hill" instead of "lake". Which spot did you pick, and what did you expect to get back?
2. Version 2 looks a little different from version 1, but you wrote that it still gave the same point. Who made that change, and why did you think it would help?
3. In your second prompt you asked the AI to explain the bug before you changed anything. Why did you want an explanation first, and what did you do next?
4. Version 3 now looks different again. Walk me through how you decided it was right, and what you saw or tried.

## Instructor key
Q1 [prompt:1][snapshot:1:map.py]: A good answer mentions the spot or number the student picked, and that they expected "lake" at that spot (zero-based index: the first spot is 0). The history records only the report "got hill instead of lake". It does not record which index was used.
Q2 [prompt:2][snapshot:2:map.py]: A good answer says who made the version 2 change (the history does not record this) and what they hoped it would do. The student's own prompt says it "still gives the same point". The change only rearranged the same addition, so an answer that notices the result could not change is a strong one. Ask them to say it in their own words.
Q3 [prompt:2]: A good answer gives a real reason for asking before editing (wanting to understand first, not wanting to guess again after version 2) and says what they did next. The history records the request only. No AI reply is recorded, so do not accept "the AI told me X" as confirmed. Ask what the reply said.
Q4 [prompt:3][snapshot:3:map.py]: A good answer says how they checked version 3, for example by picking the same spot again and seeing "lake". Prompt 3 says nobody recorded who made the change or any test run, so the check itself is unrecorded. An answer that names a specific spot and result is the student's own account. It is not confirmed by the history.

## Private AI contribution note
AI contribution: No AI action is recorded. There are no AI replies, edit records or test runs in the history. The student asked the AI to explain the bug [prompt:2], and that proves only the request. Who made the changes in versions 1, 2 and 3 is unknown [snapshot:1:map.py][snapshot:2:map.py][snapshot:3:map.py]. No student-reported hand edit is recorded either.
Instructor check: All four changed lines are unknown_or_conflicting, so do not credit the student or the AI for any version. Version order is folder-name order that staff supplied, and timestamps do not prove the sequence [snapshot:1:map.py]. Prompt 3 says nobody recorded the version 3 author or any test run [prompt:3]. There is no recorded evidence that version 3 returns "lake". The history is a snapshot set with no git or session log, so the questions rely on the student's own account.
