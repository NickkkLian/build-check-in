# Exercise: "The total is too low" (10 minutes)

The student consented to classroom use if the exercise is anonymised, so it names no student and no project. Show students only the code, the failing output, and the first two questions. The answer key at the end is for you.

## Setup (1 min)

Put this on the board:

```python
# receipt.py
def total(prices, fee):
    return sum(prices) - fee
```

Requirement: *a receipt total must include a fixed service fee.*

A check was run on `total([4, 6], 2)`. It printed:

```
FAIL expected 12, got 8
```

## Round 1: Find it (3 min, pairs)

1. Work out by hand what `sum([4, 6])` is, then what the function returns for `fee = 2`. Does that match the "got 8" line?
2. Which single character is wrong, and why does the failure message have the numbers it has?

Ask each pair to say the bug in one sentence before they type anything.

## Round 2: The tempting non-fix (3 min)

A student, or an AI assistant, tries this change:

```python
    return sum(prices) + 0
```

The check now fails again, this time with a vaguer message: `FAIL version 2 still does not meet the expected result.`

3. Work out what `total([4, 6], 2)` returns now. Is it closer to 12 than before?
4. This change got rid of the minus sign. Why was it still a guess and not a fix?
5. What should you have done between "the check failed" and "make an edit"?

The point to land on: removing the symptom is not the same as understanding the cause. The fee was never used in the second version.

## Round 3: Fix it and doubt the fix (3 min)

6. Write the correct line yourself.
7. The check now prints `PASS` for `total([4, 6], 2)`. Name one other input where the function could still be wrong. Try `total([], 2)`, `total([4, 6], 0)` and `total([0.1, 0.2], 2)`.
8. How many examples did "PASS" actually cover?

## Debrief (the last minute)

Pick one question per pair: *What is the one thing you checked before you changed the code?*

## Answer key (instructor only)

- **Q1–2:** `sum([4, 6])` is 10, and `10 - 2` is 8. The `-` should be `+`. Expected is 10 + 2 = 12.
- **Q3:** The version 2 function returns 10 (`10 + 0`). That is still wrong, and the fee is ignored entirely.
- **Q4–5:** Read the failure numbers and compute by hand before editing. The gap of 4 between 8 and 12 is exactly `2 × fee`. That points to a sign error, not a missing fee.
- **Q6:** `return sum(prices) + fee`
- **Q7–8:** The PASS covers one example. Ideas for more cases:
  - An empty list should give just the fee.
  - A zero fee should give just the sum.
  - Floating-point amounts may show rounding noise, e.g. 0.30000000000000004 + 2.
  - Whether the fee should be charged once per receipt, or not at all on an empty one, is a requirements question the code can't answer.

## Notes on the source material

- The log has three versions: a subtraction bug, a `+ 0` non-fix, then the correct `+ fee`. The exercise follows that order.
- **Caveat on the evidence:** the log's `test_case.py` write contains only a comment line. `test_case.py` is also missing from the project folder, so I couldn't read it. The `FAIL expected 12, got 8` and `PASS` lines are recorded tool output, not something I reran. The arithmetic in this exercise is checkable by hand, but I haven't run the original check. I could only open `receipt.py` directly, because I had no way to list the project folder. If it holds other files, I haven't seen them.
- **Version order:** the snapshot order comes from folder names, which the history file notes don't prove chronology. The edit prompts in the session log match that order.
