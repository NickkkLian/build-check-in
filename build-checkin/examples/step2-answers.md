# Student answers
Pasted by the instructor in the student's own words. Fictional example.
Student first name: Leo

Q1. In your second prompt, you told the AI the score went from 5 to 51 instead of 6. What did you see on the screen, and how did you know it was wrong?
A1. It showed 51 after Continue and one hop. I had 5 saved so I expected 6.

Q2. At version 2, the AI changed the score line and ran the test again. The test still failed with the same message. Why do you think that change didn't help?
A2. Because += 1 is the same as + 1. It was still adding to text.

Q3. In your third prompt, you wrote "Don't change the code. Just tell me where to look." Why did you ask the AI for that, and not for another fix?
A3. It had already tried a fix and it still said 51. I wanted to find the line myself.

Q4. In your fourth prompt, you said you changed one line in game.js by hand. Walk me through how you picked that line.
A4. The saved score comes back as text so I put Number() around it. Then 5 + 1 is 6 and the test passed.

Q5. The AI ran the test at the end and reported that it passed. What would you check to be sure Continue works when someone really plays the game?
A5. I would save a different number, press Continue and hop once to see if it adds one.
