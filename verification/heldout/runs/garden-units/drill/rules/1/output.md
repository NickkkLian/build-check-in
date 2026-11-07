# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: anonymised.

## 1. On the board (1 min)
A classmate's small app should turn litres into millilitres.

```python
def millilitres(litres):
    return litres * 100
```

Run: `millilitres(2)`

## 2. Predict first (1 min)
Before anyone runs it: what number will `millilitres(2)` give back? Write your guess down.

## 3. What happened (1 min)
The classmate's recorded test run printed: `FAIL expected 2000, got 200`. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that causes it. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the code is only one line long, so look at the line inside the function that does the maths.
2. Trace or compare: Work out by hand how many millilitres 1 litre should be. Then follow the code with 1 litre. What does it return, and how do the two numbers compare?

Only after everyone has written their sentence in step 5:
3. The fix: change the number the litres are multiplied by from 100 to 1000, so the line reads `return litres * 1000`.

## 7. Reveal: what the classmate actually did (2 min)
1. The classmate asked the AI for a small check of `millilitres(2)` [prompt:1].
2. The AI wrote the check file [tool:test-write] and ran it [tool:test-1]. The recorded result was `FAIL expected 2000, got 200` [result:test-1].
3. The classmate asked the AI to try a change [prompt:2]. The AI edited the line to multiply by 10 instead of 100 [tool:edit-2][result:edit-2][snapshot:2:water.py].
4. The AI ran the check again. The recorded result was a fail: "version 2 still does not meet the expected result" [result:test-2]. Making the number smaller moved the answer further from 2000, not closer.
5. The classmate reported changing the line by hand to multiply by 1000 [prompt:3]. The next version's file matches that report [snapshot:3:water.py]. Because it is the classmate's report, it is not proof of who typed it.
6. A run is recorded as passing one example with exit code 0 [result:test-3]. It is a recorded report, not a rerun by us, and the history does not show who ran it.

## 8. Next week
A different app with the same cause in a new place. A classmate's distance converter should turn kilometres into metres:

```python
def metres(km):
    return km * 100
```

Run `metres(3)` and the check expects 3000. Answer for the adult: the multiplier is wrong. 1 km is 1000 m, so the line needs `km * 1000`; the current line returns 300. Students who try `* 10` should see it move the answer the wrong way, as in the reveal.
