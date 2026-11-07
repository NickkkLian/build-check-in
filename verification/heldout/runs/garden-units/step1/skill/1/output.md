# Build Check-in · Step 1
Status: Draft for the instructor. Print only the Student questions part for the student.

## Student questions
Answer in your own words. No AI for this page. Short answers are fine.
1. Your first prompt asked the AI to write a small check for your project. The AI ran it and it printed "FAIL expected 2000, got 200". What did you think that message was telling you?
2. At version 2 you wrote, "Please try a change for version 2." Why did you ask it that way, and what did you hope the AI would do?
3. The AI changed one line in water.py at version 2, and then the AI ran the test again. It still failed. Why do you think that change didn't help?
4. At version 3 you reported changing water.py by hand. Walk me through how you chose what to change.
5. After version 3, the AI's run reported a pass on one example. What else would you check before you trust it?

## Instructor key
Q1 [result:test-1][prompt:1]: A good answer mentions that the check wanted 2000 for 2 litres and the code gave 200, so the number coming out was too small. The answer may also mention that the AI wrote and ran the check. The history records the AI writing the test file [tool:test-write] and running it [tool:test-1], but the write result is `unknown` [result:test-write]. The student only asked for it [prompt:1].
Q2 [prompt:2]: A good answer mentions that the prompt did not say what to change, and gives the student's own reason for leaving it open (for example, trusting the AI to pick, or not knowing yet). There is no single right answer. Note whether the student had a plan of their own.
Q3 [tool:edit-2][result:test-2][snapshot:2:water.py]: A good answer mentions that the AI's edit moved the multiplier from 100 to 10. That made the output smaller, further from the 2000 the check wanted. Any answer that compares the new output with the expected number is a strong one. The edit result is `unknown` [result:edit-2], and the failure message is only a recorded report [result:test-2].
Q4 [prompt:3][snapshot:3:water.py]: A good answer mentions comparing the expected number with the output seen earlier [result:test-1], or knowing the litres-to-millilitres relationship, and arriving at the new line. This is the student's report that they made the edit by hand, and the diff matches it. It is not observed. The student may also say the AI's version 2 attempt helped them see which way to go.
Q5 [result:test-3][prompt:3]: A good answer mentions trying other inputs, such as 0, 1 or a decimal, or running the test themselves rather than relying on the AI's report. The run is a recorded report of one fictional example and not a rerun [result:test-3].

## Private AI contribution note
AI contribution: The AI wrote a check file [tool:test-write] and proposed running it, with a recorded failure [tool:test-1][result:test-1]. The AI edited the water.py line at version 2 [tool:edit-2][snapshot:2:water.py], and a recorded failure followed [result:test-2]. The student reported changing the line by hand at version 3, and the diff matches [prompt:3][snapshot:3:water.py]. The AI's run then recorded one reported pass [tool:test-3][result:test-3]. Who wrote version 1 of water.py is unknown [snapshot:1:water.py].
Instructor check: There is no `.git` directory, and version order comes from staff's folder names, not timestamps [snapshot:1:water.py]. The version 3 hand edit is self-reported. The pass at version 3 is a recorded report of one example, not an independent rerun [result:test-3]. The write and edit results are `unknown` [result:test-write][result:edit-2]. The record does not show which version the first test run was against [tool:test-1]. Consent state is `missing`, so no public drafts should come from this history.
