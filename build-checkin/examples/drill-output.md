# Debug Drill · 10 minutes
Status: Draft for the instructor. Anonymised. Classroom agreement: anonymised.

## 1. On the board (1 min)
A classmate's jumping game has a Continue button that should bring back the saved score and keep counting.
```js
function resumeGame(storage) {
  return {
    score: storage.getItem("score") || 0,
    best: 0,
  };
}

function addPoint(state) {
  state.score = state.score + 1;
  if (state.score > state.best) {
    state.best = state.score;
  }
  return state;
}
```
The test saves a score with `({ score: "5" })`, presses Continue, then scores one point.

## 2. Predict first (1 min)
Before anyone runs it: the saved score is 5. What will the score be after one more point? Write your guess down.

## 3. What happened (1 min)
AssertionError: Continue then hop: expected 6 got 51. Compare it with your guess.

## 4. Try it alone (3-4 min)
Find the line that makes 5 plus one point come out as 51. No AI and no talking yet.

## 5. Write one sentence: why did it break? (1 min)
Everyone writes one sentence before any fix is shown.

## 6. Hint ladder (adult only)
For students stuck in step 4, one at a time, about a minute apart:
1. Where to look: the line in resumeGame that reads the saved score.
2. What is wrong: the storage gives the score back as text ("5"), and adding 1 to text sticks the characters together.
Only after everyone has written their sentence in step 5:
3. The fix: turn it into a number when it is read: `score: Number(storage.getItem("score")) || 0,`

## 7. Reveal: what the classmate actually did (2 min)
1. The AI wrote the game and its test. The first test run failed with "expected 6 got 51" [tool:write-game][tool:write-test][result:test-1].
2. The classmate told the AI the score went from 5 to 51 and asked it to fix it [prompt:2].
3. The AI changed `state.score = state.score + 1` to `state.score += 1`. The test still said 51 [tool:edit-2][git:ce3d07aec6e2:game.js][result:test-2].
4. The classmate then asked the AI only where to look, not for new code [prompt:3].
5. The classmate reported changing the saved-score line by hand to use Number(...). The diff matches, and the recorded test passed [prompt:4][git:37d62952a1d5:game.js][result:test-3].

## 8. Next week
A form reads an age from a text box and shows "age next year" with `const next = input.value + 1;`. With 13 typed in, what shows, and why? Answer for the adult: "131", because the box's value is text; `Number(input.value) + 1` gives 14.
