# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: yes.

## 1. On the board (1 min)
A classmate's waiting-list app has a function that hands back the next person to serve. The rule is that the earliest arrival is served first. The list is in arrival order, so 'red' arrived before 'blue'.
```python
def serve(items):
    return items.pop()
```
Run: `serve(['red', 'blue'])`. Check that the answer matches the rule.

## 2. Predict first (1 min)
Before anyone runs it: which color will `serve(['red', 'blue'])` hand back? Write your guess down.

## 3. What happened (1 min)
The classmate's recorded check said: `FAIL expected 'red', got 'blue'` [result:test-1]. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes it. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the single line inside `serve` that picks which item to hand back.
2. Trace or compare: Which color does the rule say goes first? Which color does that line hand back? Where does each one sit in the list?

Only after everyone has written their sentence in step 5:
3. The fix: `items.pop()` with no number takes the last item in the list. Using `items.pop(0)` takes the first item, which is the earliest arrival.

## 7. Reveal: what the classmate actually did (2 min)
1. The classmate asked the AI to write a small check for `serve(['red', 'blue'])` on the first version [prompt:1].
2. The AI wrote the check file [tool:test-write]. The result only says "File written." [result:test-write]
3. A run of the check is recorded as failing: `FAIL expected 'red', got 'blue'` [tool:test-1][result:test-1]. Who wrote the first version of the function is not recorded [snapshot:1:queue.py].
4. The classmate asked the AI to try a change for version 2 [prompt:2].
5. The AI failed fix: it changed the line to `return items[-1]` [tool:edit-2][result:edit-2][snapshot:2:queue.py]. That still picks the last item.
6. The recorded run for version 2 failed again: "FAIL version 2 still does not meet the expected result." [result:test-2]
7. The classmate asked the AI for the next change [prompt:3].
8. The AI changed the line to `return items.pop(0)` [tool:edit-3][result:edit-3][snapshot:3:queue.py].
9. A recorded run reports a pass: "PASS one fictional example, exit code 0" [result:test-3]. This is a recorded report, not a rerun. Ask the class whether one example is enough to trust it.

## 8. Next week
Variant: a print-shop app has `def next_job(jobs): return jobs[-1]`. The rule is that the job sent first prints first. Students predict what `next_job(['poster', 'flyer'])` returns, then find the cause. Answer for the adult: it returns 'flyer'. The line takes from the last position, not the first. The fix is `jobs[0]`, or `jobs.pop(0)` if the job should also leave the list. This is the same cause as the original, taking from the wrong end, in a new place.
