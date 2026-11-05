# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Leo is building Pixel Hop, a one-button jumping game where Continue brings back a saved score.
2. Fixed or explained: Leo reported changing one line by hand and wrote: "The saved score comes back as text so I put Number() around it."
3. The AI: The AI wrote the first version of the game and its test, and its first fix did not solve the problem.
4. Next: [instructor: add next week's step]
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- A1: what Leo saw on screen is his account; the recorded test shows the same symptom [prompt:2][result:test-1].
- A4: the hand change is student-reported; the diff matches [prompt:4][git:37d62952a1d5:game.js] and the recorded test passed [result:test-3].
- A5: this is a proposed check, not an event in the history. The recorded AI test used one saved value [tool:write-test].

## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [git:d8e855fe79bb:game.js]
AI did: wrote the game and test; the test reported "expected 6 got 51" [tool:write-game][tool:write-test][result:test-1].

Answer A1, copied unchanged:
> It showed 51 after Continue and one hop. I had 5 saved so I expected 6.

### Version 2 [git:ce3d07aec6e2:game.js]
AI did: changed the score line; the recorded test still failed [tool:edit-2][result:test-2].

Answer A2, copied unchanged:
> Because += 1 is the same as + 1. It was still adding to text.

Answer A3, copied unchanged:
> It had already tried a fix and it still said 51. I wanted to find the line myself.

### Version 3 [git:37d62952a1d5:game.js]
Recorded fact: a passing test result was recorded; who ran the final test is unknown [result:test-3].

Answer A4, copied unchanged:
> The saved score comes back as text so I put Number() around it. Then 5 + 1 is 6 and the test passed.

Answer A5, copied unchanged:
> I would save a different number, press Continue and hop once to see if it adds one.
