# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. Look at version 1 of Shelf Slots. The saved note says the check showed "expected True, got False". Walk me through what you thought the shelf should say, and what it said instead.
2. At version 2, the line that decides if the shelf is full was changed. The saved note says the same failure was still there. Why do you think the change did not help?
3. Between version 2 and version 3, the line was changed again. Who changed it, and how did you decide what to try?
4. Your idea says a shelf is full as soon as used slots equal capacity. Which numbers would you pick to test that, and what answer would you expect for each?
5. Nobody saved a test run for version 3. How would you check that version 3 works? Which test would you run, and what would tell you it is fixed?

## Instructor key
Q1 [prompt:1][snapshot:1:shelf.py]: A good answer mentions that the student expected the shelf to count as full, and that version 1 said not full. The code at version 1 is a strict "greater than" comparison. The test numbers are not recorded, so the student has to supply them. The writer and runner of that test are not recorded.
Q2 [prompt:2][snapshot:2:shelf.py]: A good answer mentions that the version 2 comparison still does not treat "used equals capacity" as full, because it now needs one more than capacity. The saved note says the failure stayed the same. The writer of this change is unknown, and no AI reply or tool call was saved.
Q3 [prompt:3][snapshot:3:shelf.py]: A good answer names who made the version 3 change (the history says this is unknown) and gives the student's own reason for trying it. It may mention the change from "greater than or equal to capacity plus one" to "greater than or equal to capacity", which now matches the idea. Any claim of authorship is the student's report only.
Q4 [context:brief][snapshot:3:shelf.py]: A good answer picks examples where used equals capacity and expects "full". It may also pick used below and above capacity, with expected answers that fit the idea. This is the student's own plan, not a recorded step.
Q5 [prompt:3][snapshot:3:shelf.py]: A good answer says the student would run a test with used equal to capacity and check for True. It may mention also trying other numbers. No run for version 3 is saved, so this shows what they would check, not what they did.

## Private AI contribution note
AI contribution: Not established. No AI reply, edit record or tool call is saved [prompt:2]. All four changed-line records are `unknown_or_conflicting` [snapshot:1:shelf.py][snapshot:2:shelf.py][snapshot:3:shelf.py]. No student-reported hand edit is recorded either. The writer of the version 1 test and the version 3 change are both unknown [prompt:1][prompt:3].
Instructor check: The history has no recorded AI step, so none of the questions credits the AI. Ask the student who changed each version. The "prompts" are staff notes, not words the student typed [prompt:1][prompt:2][prompt:3]. The folder order was supplied by staff and timestamps do not prove the order [snapshot:1:shelf.py]. The failure at version 1 and the repeat at version 2 are saved notes, not reruns [prompt:1][prompt:2]. Version 3 has no saved run [prompt:3]. Any answer that claims who wrote or ran something stays a self-report.
