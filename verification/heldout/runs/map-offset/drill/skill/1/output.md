# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: yes.

## 1. On the board (1 min)
A classmate's route-picker should return the point at the chosen zero-based position in a list: position 0 is the first point, position 1 is the second, and so on.
```python
def pick(points, index):
    return points[1 + index]
```
Run: `pick(["lake", "hill", "park"], 0)`. The list is an example for class. The history names only "hill" and "lake", not the full list.

## 2. Predict first (1 min)
Before anyone runs it: what will `pick(["lake", "hill", "park"], 0)` give back? Write your guess down.

## 3. What happened (1 min)
The classmate reported: got hill instead of lake. The history records no error message or test output. Compare that with your guess.

## 4. Try it alone (3-4 min)
Find the part of the line that makes the wrong point come back. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the single `return` line. Look at what is inside the square brackets.
2. Trace or compare: if `index` is 0, what number is inside the brackets? Which place in the list does that number point to, and which place did the picker's description say it should return?

Only after everyone has written their sentence in step 5:
3. The fix: the `1 +` adds one to the index, so every pick lands one point late. Use `points[index]`, with no added number.

## 7. Reveal: what the classmate actually did (2 min)
1. Version 1 had `points[index + 1]`. Who wrote it is unknown. [snapshot:1:map.py]
2. The classmate reported getting "hill instead of lake". [prompt:1]
3. Version 2 changed the line to `points[1 + index]`. This only swaps the order of the two added terms. Who made the change is unknown, and the history records no AI edit for it. [snapshot:2:map.py]
4. The classmate then reported it "still gives the same point" and asked the AI to explain the bug before changing anything. [prompt:2] The AI's reply is not recorded, so we cannot say whether it explained anything.
5. Version 3 has `points[index]`, with no added number. Who made this change is unknown. The classmate said they did not record who changed it or any test run, so the history shows no passing test. [snapshot:3:map.py][prompt:3]
6. The history records no AI fix at all, failed or successful. A fix attempt that failed is visible only as the version 2 line, which is still wrong. Its author is unknown.

## 8. Next week
Variant: a name-picker returns `names[position + 1]`, and the classmate expects the first name when `position` is 0. Ask students to predict, find the cause and write one sentence before any fix. Answer for the adult: the same cause in a new place. The extra `+ 1` moves every pick one place along, so position 0 returns the second name. The fix is `names[position]`.
