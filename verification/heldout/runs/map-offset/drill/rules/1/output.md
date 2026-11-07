# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: yes.

## 1. On the board (1 min)
A route picker should return the point at the selected zero-based index. Zero-based means the first item is index 0.

```python
def pick(points, index):
    return points[index + 1]
```

Run (the example list is made up for class; it is not recorded in the classmate's history):
`points = ["lake", "hill", "bridge"]`, then `pick(points, 0)`.

## 2. Predict first (1 min)
Before anyone runs it: what will `pick(points, 0)` give back? Write your guess down.

## 3. What happened (1 min)
The history records no failing test or error output. The classmate reported: "got hill instead of lake." Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes it. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the `return` line. It is the only line that picks an item.
2. Trace or compare: when `index` is 0, which place in the list does the expression inside the square brackets point to? Is that the place the app is supposed to use?

Only after everyone has written their sentence in step 5:

3. The fix: the extra `+ 1` shifts every pick one place along. Return `points[index]`.

## 7. Reveal: what the classmate actually did (2 min)
1. Version 1 returned `points[index + 1]`. [snapshot:1:map.py]
2. The classmate reported getting "hill instead of lake." [prompt:1]
3. Version 2 changed the line to `points[1 + index]`. This only swaps the order of the two numbers, so the position picked stays the same. [snapshot:2:map.py] Who made this change is not recorded.
4. The classmate then reported it "still gives the same point" and asked for the bug to be explained before changing anything. [prompt:2] No reply to that request is recorded.
5. Version 3 changed the line to `points[index]`. [snapshot:3:map.py] The classmate said they did not record who made this change or any test run. [prompt:3] So who made the fix and whether it was tested are both unknown.

## 8. Next week
Variant: a stop-list screen shows the stop at a zero-based position.
```python
def show_stop(stops, position):
    return stops[position + 1]
```
Run `show_stop(["gate", "cafe", "pier"], 0)` and ask what comes back and why.
Answer for the adult: it returns "cafe" instead of "gate". The same cause is in a new place: the `+ 1` moves the pick one place along in a zero-based list. The fix is `stops[position]`.
