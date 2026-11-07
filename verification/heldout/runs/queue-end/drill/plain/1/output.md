# 10-minute debugging exercise: "Who gets served first?"

This is based on one bug in the Queue Board log. The first `serve` took the last arrival, not the first. The version-2 "fix" rewrote the line without changing what it did. The student's name and code are not on the handout, and the exercise uses a new example. `context.json` records classroom drill consent as "yes".

**What the log shows**
- Version 1 used `items.pop()`. The check `serve(['red', 'blue'])` failed with "expected 'red', got 'blue'".
- Version 2 changed that line to `items[-1]`. It still returned `'blue'`, so the check failed again.
- Version 3 used `items.pop(0)`, and the log reports one pass.
- The log has limits you should know about. The test file in the session holds only a comment, and `test_case.py` isn't in the project folder, so I couldn't see the real assertion. The pass is a recorded result, not one I reran. I could only read `queue.py`, so I didn't confirm that no other files exist in the project folder.

## Handout for students

```python
# line.py
def next_customer(line):
    """The line is ordered by arrival: the first person in the list arrived first.
    Remove and return the person who should be served next."""
    return line.pop()

line = ["Mia", "Omar", "Lena"]
print(next_customer(line))   # we expect Mia
print(line)                  # we expect ['Omar', 'Lena']
```

Students should run the code and read what it prints.

## Run of show

| Min | Activity |
|---|---|
| 0–2 | Hand out the code. Ask students to predict the output before they run it. |
| 2–4 | Students run it. The output is `Lena` and `['Mia', 'Omar']`, which differs from what was expected. In pairs, they say which line is wrong and why. |
| 4–7 | **The trap.** Students try the fix `return line[-1]`, run it, and see the first print is still wrong. Ask: "This changed the code, so why didn't the behavior change?" |
| 7–9 | Students find a change that gets both lines of output right. Ask them to check the second print too. |
| 9–10 | Debrief using the questions below. |

## Answer key
- **Bug:** `pop()` takes from the end, so the newest arrival is served first. That is a stack, not a queue.
- **The trap:** `line[-1]` also reads the last item. It only swaps one way of getting the last item for another. It also stops removing the person from the list, so the second print would be wrong.
- **Fix:** `return line.pop(0)`. Both outputs then match: `Mia` and `['Omar', 'Lena']`.
- **Extra challenge:** What happens when `line` is empty? Both `pop()` and `pop(0)` raise an `IndexError`. Ask what the program should do instead.

## Debrief questions
1. Before changing code, what did the failing output tell us? Which words in it pointed to "last, not first"?
2. The second attempt was a change that didn't change the behavior. How could we have known that before running it?
3. Our check only tested one input. What other check would catch a wrong fix? For example, try three people, or check the list after the call.
4. If an AI assistant says "this fixes it", what evidence would convince you?

## For the instructor
- Keep the focus on method: predict, read the failure, change behavior rather than wording, then check everything. Don't treat the original attempts as mistakes by the student.
- If a pair finishes early, have them write the one-line check that would have failed on both the original and the second version.
