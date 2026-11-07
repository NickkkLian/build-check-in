# 10-minute debugging exercise: "The Off-by-One Pick"

**Based on:** a bug in a route-picker project where choosing item 0 gave back item 1. The log says only that the result was "hill instead of lake". It doesn't show the real data or the test, so the exercise uses new made-up data. Names and code are not copied from the student, and the student's name isn't needed.

**Goal:** students find the bug by checking one case against what they expected before they touch any code.

## Hand-out (students see this)

```python
def pick(points, index):
    return points[index + 1]

stops = ["lake", "hill", "bridge", "cabin"]
print(pick(stops, 0))   # expected: lake
```

Prompt: "The picker is supposed to return the stop at the position you choose, counting from 0. Running it prints `hill`. Don't change anything yet."

## Timing

| Min | Step | What students do |
|---|---|---|
| 0–2 | Predict | Without running anything, write down what `pick(stops, 2)` returns. Then run it and compare. |
| 2–5 | Narrow it down | Fill in a table of index, expected and actual for 0, 1, 2 and 3. Students should see that every answer is one place too far. Ask what happens at index 3. |
| 5–7 | Explain before fixing | Each pair writes one sentence: "The bug is ___ because ___." The sentence has to name the line and say why the answer is shifted. They are not allowed to edit the code yet. |
| 7–9 | Fix and re-check | Make the one-line fix. Re-run all four indexes from the table, not only index 0. |
| 9–10 | Debrief | Use the discussion questions below. |

## Facilitator answer key

- **Bug:** `index + 1` shifts every pick one position along. Python lists start at 0, so `points[index]` is correct.
- **Index 3 crashes with an `IndexError`.** The shift also breaks the last item. The student's "wrong point" report is the quieter symptom. This is a good moment to point out that an error message is a free clue.
- **Common wrong fix:** rewriting `index + 1` as `1 + index`. It looks different but gives the same result. Students who do this are testing whether the code looks different, not whether the output is right. This is the most useful thing to catch in the room. The student's own history shows this exact step (version 1 to 2), followed by "it still gives the same point".
- **Another wrong fix:** `index - 1`. It passes index 1 but returns the wrong point for index 0, because it wraps to the last item. It only looks right when you check one case.

## Debrief questions

1. Why did swapping `index + 1` for `1 + index` change nothing?
2. Which single check would have told you the bug was a shift and not a one-off wrong answer?
3. The original report said only "got hill instead of lake." What else would you want written down so a classmate could reproduce it? (Aim for: the input, the expected output and the actual output.)

## Notes for the instructor

- **Consent:** the record says classroom drill use is allowed ("yes"). Permission for public drafts is missing, so don't post this exercise, or anything tracing back to the student, outside the class.
- **Who made which change is unknown.** The log has no record of who edited what or of any test run. The exercise uses only the bug's shape and doesn't say how the student found it.
- **Not checked:** I haven't run the hand-out code. The behaviour above follows from how Python indexing works. Run it once before class.
- The `project` folder couldn't be listed with the tool I had. I read `map.py` directly, and it already contains the fixed version (`points[index]`). If the folder holds other files, I haven't seen them.
