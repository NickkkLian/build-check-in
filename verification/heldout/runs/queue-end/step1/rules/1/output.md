# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. At version 1, a test run was recorded in your AI session. It said "FAIL expected 'red', got 'blue'". Walk me through what that message told you about your waiting list.
2. Your second prompt said "Please try a change for version 2." Why did you ask for it that way, and what did you want the AI to do?
3. At version 2, the AI changed a line in the queue file and the test still failed. Why do you think that change didn't help?
4. After your third prompt, the AI changed that same line again. What did you see happen, and what did you do next?
5. A pass was reported for one example, ['red', 'blue']. How would you check that your waiting list really works, and which other example would you try?

## Instructor key
Q1 [prompt:1][result:test-1]: A good answer mentions that the check expected the first arrival ("red") but the code gave back the last one ("blue"). It should show Ari saw the order was backwards. Version 1 used `items.pop()`, and the writer of that line is unknown.
Q2 [prompt:2][tool:edit-2]: A good answer mentions what Ari expected the AI to do. The prompt names no cause and no specific change, so the answer shows whether Ari had an idea of their own or was leaving it to the AI. No AI reply is recorded for this prompt.
Q3 [snapshot:2:queue.py][result:test-2]: A good answer mentions that version 2 swapped one way of taking the last item for another way of taking the last item, so "blue" still came out first. The recorded failure says only "version 2 still does not meet the expected result."
Q4 [snapshot:3:queue.py][tool:edit-3][result:test-3]: A good answer mentions the third change, which takes the first item, and the reported pass. Ari should say what they saw and what they did next. The history records no student action after the pass.
Q5 [result:test-3]: A good answer mentions that the pass covers one example only. Ari should name another list, such as three or more items or a one-item list, and what the right first result would be. The history shows no test beyond the one example.

## Private AI contribution note
AI contribution: The AI session records writing the check file [tool:test-write], running the test twice with failures [result:test-1][result:test-2] and a reported pass [result:test-3]. It records two edits to `queue.py`, at version 2 and version 3, and the diffs match both [snapshot:2:queue.py][tool:edit-2][result:edit-2][snapshot:3:queue.py][tool:edit-3][result:edit-3]. Ari's three prompts are recorded [prompt:1][prompt:2][prompt:3]. The history records no hand edits by Ari. The author of the version 1 code is unknown [snapshot:1:queue.py].
Instructor check: The pass is a recorded report of one fictional example, not a rerun [result:test-3]. The version order comes from folder names that staff supplied, and timestamps do not prove it [snapshot:1:queue.py]. The record shows no AI replies or explanations. Prompts 2 and 3 are generic and name no cause [prompt:2][prompt:3], so Q2 and Q4 may get "I don't know"; treat that as information, not a fault. Consent for public drafts is missing [consent], so keep the step 2 showcase notes private.

**Not produced here:** The weekly parent update is step 2. It has to quote Ari's own answers, so I haven't written it. Paste Ari's answers back to me and I'll draft it. Its "Next" line will use the context step: "Ask the instructor to select the next example."
