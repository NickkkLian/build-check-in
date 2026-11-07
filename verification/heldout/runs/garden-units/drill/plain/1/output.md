# 10-minute debugging exercise: "The Number That Moved the Wrong Way"

This is anonymised. It uses no name, and the student's project is called "a watering planner". The bug comes from one student's three-version log, and the students get a fresh copy of the code.

**Instructor note:** The student's log has three versions. Version 1 multiplied by 100 and failed with "expected 2000, got 200". An AI edit in version 2 changed it to 10, and it still failed. The student then typed 1000 by hand at version 3, and the log reports a pass. That pass is the log's own report. Nobody reran it independently, and the check in the log covers one example, `millilitres(2)`. The test file wasn't in the project folder, so I rebuilt the check below from the logged failure message.

## Hand-out (students see this)

```python
def millilitres(litres):
    return litres * 100

# check
assert millilitres(2) == 2000, f"expected 2000, got {millilitres(2)}"
```

Running it prints: `AssertionError: expected 2000, got 200`

A helper suggests changing `100` to `10`.

## Timeline

**0:00–2:00 – Predict (solo, on paper)**
1. Before running anything: what will the check say if we use the helper's `10`?
2. Which direction does the number need to move, and by how much?

**2:00–5:00 – Read the failure (pairs)**
The failure message gives two numbers, 2000 and 200.
- What is the ratio between them?
- 2 litres is how many millilitres? So how many millilitres is 1 litre?
- Does the helper's suggestion move the answer toward 2000 or away from it? Check by working out `2 * 10` by hand.

**5:00–7:00 – Fix and run (pairs)**
Apply your fix and run the check.

**7:00–10:00 – Is one passing check enough? (whole class)**
The check only tests `millilitres(2)`.
1. Name one other input that a wrong formula could still get right. (Hint: what does `litres * 1000` return for `0`? Is there any other formula that also gives 2000 for an input of 2?)
2. Write one more check with a different input, such as `millilitres(0.5)`.
3. The last question is the one to talk through: if a helper says "fixed, it passes", what would you do before you believe it?

## Answer key (instructor only)

- **Root cause:** The multiplier is 100, but 1 litre = 1000 ml. The failure shows the answer is 10 times too small (200 vs 2000).
- **Trap:** Changing to `10` makes the output smaller, so it moves further from 2000. Students should predict this in the first step. The real log shows exactly this failed attempt.
- **Fix:** `return litres * 1000`.
- **Discussion point:** A single passing example is weak evidence. `litres * 1000` is right, but so would be a wrong formula like `litres ** 3 * 250` for the input 2. Extra inputs (0, 0.5, 10) make the check stronger. Also, "it passes" from a helper's output is a report, so students should rerun it themselves.
- **Common mistakes:**
  - Students blame the test rather than the code.
  - They guess a number without using the ratio from the message.
  - They treat the first pass as proof.

## Before you use this
- The consent on file for this student allows anonymised classroom drills only. Don't mention the student, the project name, or the version history out loud.
- I couldn't see the original test file, so the check above is my reconstruction. Run the hand-out once yourself before class.
