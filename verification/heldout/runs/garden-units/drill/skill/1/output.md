# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: anonymised.

## 1. On the board (1 min)
This small program should turn a number of litres into millilitres.

```python
def millilitres(litres):
    return litres * 100
```

Run: call `millilitres(2)`.

## 2. Predict first (1 min)
Before anyone runs it: what will `millilitres(2)` give back? Write your guess down.

## 3. What happened (1 min)
The recorded check said: "FAIL expected 2000, got 200" [result:test-1]. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes this. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the function has only one working line. Start with what happens to `litres` on that line.
2. Trace or compare: What number do you get if you put 1 litre through the line by hand? How does that compare with how many millilitres you know are in 1 litre?

Only after everyone has written their sentence in step 5:
3. The fix: the multiplier is 100, but one litre is 1000 millilitres. Change `litres * 100` to `litres * 1000`.

## 7. Reveal: what the classmate actually did (2 min)
1. Version 1 had the line `litres * 100` [snapshot:1:water.py]. Who wrote that line is unknown from the record.
2. The classmate asked for a small check, and the AI wrote the check file [prompt:1][tool:test-write][result:test-write].
3. The AI ran the check and the recorded result was a failure: "FAIL expected 2000, got 200" [tool:test-1][result:test-1].
4. The classmate asked the AI to try a change for version 2 [prompt:2].
5. The AI changed the multiplier from 100 to 10 [tool:edit-2][result:edit-2][snapshot:2:water.py]. This was the failed fix: the number moved the wrong way.
6. The AI ran the check again and the recorded result was still a failure: "FAIL version 2 still does not meet the expected result." [tool:test-2][result:test-2]
7. The classmate reported changing the line by hand to `litres * 1000` at version 3 [prompt:3][snapshot:3:water.py]. The classmate reported this; the record cannot show who typed it.
8. A check was run and recorded as "PASS one fictional example, exit code 0" [tool:test-3][result:test-3]. This is a recorded report, not a rerun by us.

## 8. Next week
Variant: a program turns kilometres into metres with `return km * 100`. Run it with `km = 3`. Answer for the adult: the same kind of bug, a wrong multiplier. One kilometre is 1000 metres, so the line should be `km * 1000`, and `3` should give `3000`, not `300`.
