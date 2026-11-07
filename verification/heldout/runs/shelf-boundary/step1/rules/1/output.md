# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. Look at version 1 of Shelf Slots. The saved note says "expected True, got False". What did you expect the shelf to say, and why?
2. Version 2 changed the comparison line in `shelf.py`, and the saved note says the same failure was still there. Walk me through who made that change and what you hoped it would do.
3. Why do you think the failure stayed the same at version 2?
4. Version 3 has a new comparison, and no test run was saved for it. How would you check whether version 3 works, and what would you try first?

## Instructor key
Q1 [prompt:1][snapshot:1:shelf.py]: A good answer mentions that the idea says a shelf is full when used slots equal capacity, so a shelf with used equal to capacity should give True. The version 1 line is `return used > capacity`, so it gives False when they are equal. The student may name the equal case in their own words.
Q2 [prompt:2][snapshot:2:shelf.py]: A good answer says who edited the line (the history does not say) and what the student hoped, such as making the check catch the full shelf. The version 2 line is `return used >= capacity + 1`.
Q3 [prompt:2][snapshot:2:shelf.py]: A good answer mentions that adding 1 to capacity moves the point where the shelf counts as full. Used equal to capacity still gives False. The student may trace this with a number.
Q4 [prompt:3][snapshot:3:shelf.py]: A good answer names a concrete check, such as running `full` with used equal to capacity and expecting True. They should also say what they would try next, such as used just below capacity expecting False. No run is recorded for version 3, so this is the student's plan, not a recorded result.

## Private AI contribution note
AI contribution: Not recorded. No AI reply, edit record or tool call was saved [prompt:1][prompt:2]. The writer and runner of version 1 are unknown [prompt:1]. The writers of the version 1, 2 and 3 edits are unknown [snapshot:1:shelf.py][snapshot:2:shelf.py][snapshot:3:shelf.py]. The student reported no hand edits. All 4 changed-line attributions are `unknown_or_conflicting`.
Instructor check: The "prompts" here are staff notes, not messages the student wrote [prompt:1][prompt:2][prompt:3]. None of them shows the student or an AI doing anything. Because no AI step is recorded, no question says the AI did anything. If you want one, ask the student directly who made each change. Version order comes from folder names that staff supplied, and timestamps do not prove chronology [snapshot:1:shelf.py]. The version 1 failure ("expected True, got False") is a saved note, not a rerun [prompt:1]. Version 2 still failing is also only a saved note [prompt:2]. Version 3 has no saved run, so whether it passes is unknown [prompt:3]. Do not treat the version 3 line as the student's fix, or as the AI's, without asking.
