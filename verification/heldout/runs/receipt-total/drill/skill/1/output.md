# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: anonymised.

## 1. On the board (1 min)
A classmate built a small receipt calculator. It should add up the item prices and add one fixed service fee, so the total is the prices plus the fee.

```python
def total(prices, fee):
    return sum(prices) - fee
```

Run: call `total([4, 6], 2)` and print what comes back.

## 2. Predict first (1 min)
Before anyone runs it: what number will `total([4, 6], 2)` give back? Write your guess down.

## 3. What happened (1 min)
The check the classmate's AI ran said: `FAIL expected 12, got 8`. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes it. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the one line inside `total` that builds the returned number. Look at what it does with `fee`.
2. Trace or compare: Say the items add up to 10 and the fee is 2. What number does that line work out, and how does it compare with the 12 the check expected?

Only after everyone has written their sentence in step 5:

3. The fix: the line subtracts the fee. It must add it: `return sum(prices) + fee`.

## 7. Reveal: what the classmate actually did (2 min)
1. The classmate asked the AI to write a small check for a fixed-fee receipt example. [prompt:1]
2. The AI wrote the check file. [tool:test-write][result:test-write]
3. The AI ran the check. The recorded result was `FAIL expected 12, got 8`. [tool:test-1][result:test-1] Who wrote the first version of the calculator line is not recorded. [snapshot:1:receipt.py]
4. The classmate asked the AI to try a change for version 2. [prompt:2]
5. The AI edited the line to `sum(prices) + 0`. [tool:edit-2][result:edit-2][snapshot:2:receipt.py] This was the failed fix: it dropped the subtraction but also left the fee out.
6. The AI ran the check again. The recorded result was `FAIL version 2 still does not meet the expected result.` [tool:test-2][result:test-2]
7. The classmate asked the AI for the next change for version 3. [prompt:3]
8. The AI edited the line to `sum(prices) + fee`. [tool:edit-3][result:edit-3][snapshot:3:receipt.py]
9. The AI ran the check, and the recorded result was a reported pass. [tool:test-3][result:test-3] This is a recorded report, not a rerun by us.

## 8. Next week
Variant: a shop function should take a price and a coupon amount off it. It is written as `def final_price(price, discount): return price + discount`. A check expects `final_price(10, 3)` to give 7. Answer for the adult: the same cause in a new place. The sign on the adjustment is the wrong way round, so the amount is added when it should be taken off. The fix is `return price - discount`. Ask students to trace the numbers (10 and 3) before they edit.
