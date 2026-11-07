## Questions for Ari

1. `serve(['red', 'blue'])` should return `'red'`. Your first version used `items.pop()`, and the check failed with "expected 'red', got 'blue'". Why did it return `'blue'`?
2. Version 2 changed that line to `items[-1]`, and the check still failed. What does `items[-1]` give you, and why didn't it fix the problem?
3. Version 3 uses `items.pop(0)`. What does the `0` change? Besides the return value, what else happens to the list after `serve` runs?
4. Suppose `serve` is called on an empty list. What happens, and what would you want it to do on a waiting list?
5. The only check you ran was one example, `['red', 'blue']`. What other inputs would you try before trusting this, for example one name or three?

## Note for the instructor

**Scope:** The log has 3 prompts and 3 versions of one two-line file, `queue.py`. The record doesn't show that Ari wrote any code.

- **AI-authored changes:** The AI made both edits (versions 2 and 3). Each edit matches its diff, so the record supports this.
- **Version 1:** The origin of the original `items.pop()` code is unknown. The log has no AI record of it, and it also has no student record.
- **Ari's prompts:** All three were short and gave no direction. Prompt 2 was "Please try a change for version 2" and prompt 3 was "Please make the next change for version 3". The log shows no sign that Ari diagnosed the bug or chose the fix. The AI said "the code selects the last item instead of the first" after the first failure, so the diagnosis came from the AI.
- **Version 2:** It was a guess that didn't change behaviour. `items[-1]` still returns the last item.
- **Tests:**
  - The AI wrote the check (`test_case.py`), and it contains only a comment line in the log.
  - The final "PASS" is a recorded report of one example. Nobody independently reran it.
  - `test_case.py` isn't in the project folder I was given, so I couldn't confirm the check does what the log says.
- **Not shown:** There is no live link, and no consent for public drafts is on file. I can't say how much Ari understands. The questions above are the way to find out.
- **Classroom drill:** Consent for it is recorded as "yes".

## Weekly update for parents

*Not for sending yet. The record shows no consent for public or parent-facing drafts, so check that first.*

This week Ari worked on Queue Board, a small program for a waiting list that should serve whoever arrived first. Ari ran a check, saw it fail because the program picked the last person instead of the first, tried a fix that didn't work, and then tried another that did. The final check passed on one example. Ari used an AI assistant for the code changes. Next, Ari will ask the instructor to pick the next example, and will go over how the fix works and test a few more cases.
