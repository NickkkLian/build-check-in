# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: yes.

## 1. On the board (1 min)
A classmate's waiting-list app should serve the person who arrived first. The list is written in arrival order, so `'red'` arrived first and `'blue'` arrived second.

```python
def serve(items):
    return items.pop()
```

Run: `serve(['red', 'blue'])`. The result is not shown.

## 2. Predict first (1 min)
Before anyone runs it: what will `serve(['red', 'blue'])` give back? Write your guess down.

## 3. What happened (1 min)
The recorded check failed with: `FAIL expected 'red', got 'blue'`. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes this. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the second line of the code, the one that hands back an item.
2. Trace or compare: in `['red', 'blue']`, which item arrived first? Which item does that line hand back? Does the line pick the item you expected?

Only after everyone has written their sentence in step 5:

3. The fix: `pop()` with nothing in the brackets takes the last item in the list. To serve the earliest arrival, take the item at position 0: `items.pop(0)`.

## 7. Reveal: what the classmate actually did (2 min)
1. The classmate described the rule (the earliest arrival is served first). They asked the AI to write a small check for `serve(['red', 'blue'])` [prompt:1].
2. The AI wrote the check file [tool:test-write]. The AI then ran it, and the recorded result was `FAIL expected 'red', got 'blue'` [tool:test-1][result:test-1].
3. The first version of the code used `items.pop()`. The history does not show who wrote it [snapshot:1:queue.py]. The record shows no explanation of the cause from the AI.
4. The classmate asked the AI to "try a change" [prompt:2]. The AI edited the line to `items[-1]` [tool:edit-2][result:edit-2][snapshot:2:queue.py].
5. The AI ran the check again. The recorded result was `FAIL version 2 still does not meet the expected result.` [tool:test-2][result:test-2]
   - Adult note, from reading the code and not from the record: `items[-1]` also picks the last item. The AI changed how the line was written but not which item it picks.
6. The classmate asked for "the next change" [prompt:3]. The AI edited the line to `items.pop(0)` [tool:edit-3][result:edit-3][snapshot:3:queue.py].
7. The AI ran the check again and recorded `PASS one fictional example, exit code 0` [tool:test-3][result:test-3]. This is a recorded report, not a rerun.

Ask the class: why did the first AI change fail while the second one worked?

## 8. Next week
Variant: a ticket line app should call the person who has waited longest.

```python
def call_next(line):
    return line.pop()
```

Run: `call_next(['first', 'second', 'third'])`, where `'first'` joined the line earliest.

Answer for the adult: it returns `'third'`, the last item, instead of `'first'`. This is the same cause as the original bug. The fix is `line.pop(0)`. A tempting wrong fix is `line[-1]`, which still picks the last item.
