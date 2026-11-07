# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: anonymised.

## 1. On the board (1 min)
A receipt app should give the total of the item prices plus one fixed service fee.

```python
def total(prices, fee):
    return sum(prices) - fee
```

Run: `total([4, 6], 2)`. The prices are 4 and 6, and the service fee is 2.

## 2. Predict first (1 min)
Before anyone runs it: what number will `total([4, 6], 2)` give back? Write your guess down.

## 3. What happened (1 min)
The check printed: `FAIL expected 12, got 8` [result:test-1]. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes this. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the function has only one line that does any work. Look at that line.
2. Trace or compare: do the line by hand with 4, 6 and 2. What number does each part give? How does the result compare with the 12 the check expected?

Only after everyone has written their sentence in step 5:
3. The fix: the line subtracts the fee, but a service fee should be added. Change `- fee` to `+ fee`.

## 7. Reveal: what the classmate actually did (2 min)
1. The classmate asked the AI to write a small check for `total([4, 6], 2)` [prompt:1]. The AI wrote the check file [tool:test-write] and ran it [tool:test-1]. The recorded result was `FAIL expected 12, got 8` [result:test-1]. Who wrote the original `- fee` line is not recorded [snapshot:1:receipt.py].
2. The classmate asked the AI to "try a change" [prompt:2]. The AI changed the line to `return sum(prices) + 0` [tool:edit-2][result:edit-2][snapshot:2:receipt.py]. This did not use the fee at all.
3. The AI ran the check again and the recorded result was a failure: "FAIL version 2 still does not meet the expected result." [result:test-2]. That failed fix attempt is worth discussing: the AI changed the line, but the change still did not add the fee.
4. The classmate asked for the next change [prompt:3]. The AI changed the line to `return sum(prices) + fee` [tool:edit-3][result:edit-3][snapshot:3:receipt.py]. The AI's recorded run reported a pass for the one example: "PASS one fictional example, exit code 0" [result:test-3]. This is a recorded report, not a rerun by staff, and it covers only one example.

## 8. Next week
Variant: a tip function with the same kind of mistake in a new place.

```python
def with_tip(prices, tip):
    return sum(prices) - tip
```

Run `with_tip([5, 5], 3)`. The board says a tip should be added to the total, so students should expect 13. They predict first, then compare with the actual output.

Answer for the adult: the function gives 7 instead of 13. The tip is subtracted instead of added. The fix is `return sum(prices) + tip`. Ask students to name the one thing it has in common with this week's bug: a value that should be added is being subtracted.
