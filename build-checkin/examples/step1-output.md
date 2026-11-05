# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. In your second prompt, you told the AI the score went from 5 to 51 instead of 6. What did you see on the screen, and how did you know it was wrong?
2. At version 2, the AI changed the score line and ran the test again. The test still failed with the same message. Why do you think that change didn't help?
3. In your third prompt, you wrote "Don't change the code. Just tell me where to look." Why did you ask the AI for that, and not for another fix?
4. In your fourth prompt, you said you changed one line in game.js by hand. Walk me through how you picked that line.
5. The AI ran the test at the end and reported that it passed. What would you check to be sure Continue works when someone really plays the game?

## Instructor key
Q1 [prompt:2][result:test-1]: A good answer mentions what the student saw: the score showed 51 after Continue, when a saved 5 plus one hop should give 6. The test message was "expected 6 got 51". The history does not show what the student saw on screen, so this is the student's own account.
Q2 [git:ce3d07aec6e2:game.js][tool:edit-2][result:test-2]: A good answer mentions that the AI changed how one point is added (`state.score = state.score + 1` became `state.score += 1`). It then notes that the problem was somewhere else, in how the saved score was loaded before the point was added. The same "expected 6 got 51" message came back.
Q3 [prompt:3][result:test-2]: A good answer mentions that the student had seen the AI's fix fail ("Still 51") and wanted to find the problem themselves instead of getting another edit. The history does not show the AI's reply to prompt 3, so any reason is the student's own.
Q4 [prompt:4][git:37d62952a1d5:game.js]: A good answer mentions how the student found the line that loads the saved score (`resumeGame`, line 7). It also covers what they changed on that line (the saved value is wrapped in `Number(...)`) and why. The history shows only that the student reported this edit. How they found the line is not in the history.
Q5 [result:test-3][tool:write-test]: A good answer mentions a check beyond the test: play the game, reach a score, press Continue, hop once and look at the number. It may also mention trying other saved scores. The test was written by the AI and uses one saved score ("5"). The pass at the end is a recorded report, not a rerun.

## Private AI contribution note
AI contribution: The AI wrote game.js and test_game.js in version 1, including the line that loaded the saved score [tool:write-game][tool:write-test][git:d8e855fe79bb:game.js]. The AI ran the test, which failed with "expected 6 got 51" [result:test-1]. At version 2 the AI changed the `+ 1` line to `+= 1`, and the test failed again [git:ce3d07aec6e2:game.js][tool:edit-2][result:test-2]. The student reported the version 3 hand edit to the saved-score line, and the diff matches the report [prompt:4][git:37d62952a1d5:game.js]. A passing run was then recorded [result:test-3]. Unknown: who ran the test at version 3, since the history shows the student saying they ran it, and what the AI replied to prompt 3 (no reply is recorded). The README lines at version 1 are unknown or conflicting [git:d8e855fe79bb:README.md].
Instructor check: The version 3 hand edit is self-reported; the diff proves the text, not who typed it [prompt:4][git:37d62952a1d5:game.js]. The final pass is a recorded report, not an independent rerun [result:test-3]. Commit messages such as "Read the saved score as a number" are author claims, not evidence [git:37d62952a1d5:game.js]. There are no staff claims in the context. Consent for public use is missing, so nothing from this history should be used publicly. The student's surname is in the context and must stay off the printed page.
