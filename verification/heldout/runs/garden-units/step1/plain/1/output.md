## Check-in questions for Bea

1. Your first check asked for `millilitres(2)`. What number should come back, and how did you work that out before running anything?
2. At version 1 the test said "expected 2000, got 200". Using only those two numbers, what was wrong with the function?
3. At version 2 you changed the multiplier from 100 to 10, and the test still failed. Why was the answer always going to be wrong with 10? What would you check before changing a number next time?
4. In version 3 you wrote `litres * 1000`. Why is 1000 the right number? Say it in your own words, without the word "multiplier".
5. The passing test only checks one example. What other litre amounts, such as 0, 0.5 or 10, would you try to be more sure it works? What should come back for each?

## Note for the instructor

**Who did what (from the log, not a percentage):**
- **AI:** Wrote the test file, which was a one-line placeholder comment. Made the version 2 edit (100 → 10) and ran the tests. The AI also said the multiplier "is 100 although one litre contains 1000 millilitres." That pointed to the right fix, but the log doesn't show Bea acting on it straight away.
- **Bea:** Says in the session that she changed `water.py` by hand to `litres * 1000` for version 3. The file change matches what she said, but nobody saw her do it. The log can't confirm it.
- **Unknown:** The version 1 code (`litres * 100`) has no recorded source.

**Caveats:**
- The version 3 pass ("PASS one fictional example") is the log's own record, not a rerun by anyone independent.
- The test file isn't in the project folder, and the log shows it only as a one-line comment. I couldn't read what it checks. Please run it, or look at it, before trusting the pass.
- Snapshot order comes from folder names, so timestamps don't prove the sequence.
- The final code is one line and correct. The risk is that Bea reached the fix after the AI told her the answer. The questions above are meant to find out whether she understands why 1000 is right.
- No parent consent is on file, so the parent update below is a draft for you to review. It isn't cleared to send.

## Weekly update for parents (draft, not cleared to send)

Hi! This week Bea worked on Water Planner, a small tool that turns litres of water into millilitres. Her first version gave the wrong answer: 2 litres came out as 200 instead of 2000. A first attempt at a fix still didn't work. Then Bea changed the number herself to 1000, and the check now passes. She is practising how to test her code and how to spot why an answer is wrong. Next, she'll test a few more amounts to be sure it works.
