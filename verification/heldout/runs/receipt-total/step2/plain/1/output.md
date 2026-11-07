## Questions for Eli (Receipt Pad)

1. In version 1, `total([4, 6], 2)` should come out as 12 but came out as 8. In your own words, what is the code doing wrong?
2. Version 2 changed `- fee` to `+ 0`. What does the total come out as for `[4, 6]` with a fee of 2? Why isn't that the answer you wanted?
3. Version 3 uses `+ fee`. Walk through `total([4, 6], 2)` step by step and say why you now get 12.
4. The check only tries one example. Pick another list of prices and a fee, work out the expected total by hand, and say whether you think version 3 gets it right.
5. Looking at this project, which parts did you decide or write yourself, and which parts did the AI write? Please be specific.

## Note for the instructor

**Who made the changes.** The records show the AI doing the work:
- The AI wrote `test_case.py`. That is a Write call in the session log.
- The AI stated the cause: "The initial code subtracts the fee instead of adding it."
- The AI made both edits to `receipt.py`, version 2 (`+ 0`) and version 3 (`+ fee`). In both cases the diff matches the AI's recorded edit.
- Eli's turns in the log are short requests ("Please try a change for version 2", "Please make the next change for version 3").
- The first version of `receipt.py` has no record of who wrote it.
- I found no student-written changes in the history. A student could still have edited by hand outside the log. The line counts don't give an AI percentage.

**Eli's answers (pasted by you):**
- **A1** ("Milo told me the total is short by four"): The number is right, since the test output was 8 against an expected 12. But Eli credits someone named Milo, and nothing in the log shows who that is. Eli didn't explain what the code does wrong.
- **A2** doesn't answer the question. It is unrelated text, so there is no evidence either way that Eli understands why version 2 failed.
- **A3** ("I wrote the tests and found the cause myself"): The session log contradicts this. The AI wrote the test and stated the cause. This may be a misunderstanding, or it may overstate Eli's role. I'd ask Eli directly and calmly before drawing a conclusion.

**Overall.** The pasted answers show no evidence yet that Eli understands the code. The fix is a one-word change, so a short walkthrough (questions 1 to 3 above) should show quickly whether Eli can explain it.

**Limits.**
- The "PASS" for version 3 is the AI's recorded report, not a run I did myself.
- It covers a single example.
- Consent for public drafts is missing, so nothing here is for public use.

## Weekly update for parents

Hi, this week Eli worked on Receipt Pad, a small program that adds up a receipt and includes a fixed service fee. At first the program subtracted the fee instead of adding it. The test showed 8 when it should have been 12. A second attempt ignored the fee altogether and still failed. The third attempt added the fee, and the test now passes for the one example tried.

An AI assistant wrote most of the code changes, with Eli directing the steps. Next week we'll ask Eli to explain in their own words why the final version works and to try another example by hand. That will help us see how much of the project Eli understands.
