I couldn't open the `project` folder because it's a directory, so I used the history, the diffs and the session log instead. The diffs cover only `gallery.py`.

## Questions for Dara
These are for conversation. Dara has withdrawn consent for classroom drills, so don't score them or ask them in front of the group. Dara's earlier answers were "I do not know", "idk" and no answer, so the questions start small.

1. In version 1, `is_photo` only says yes to the tag `Photo` (capital P, rest lowercase). If the gallery is given `photo`, what do you expect it to answer, and why?
2. The version 1 check printed "expected True, got False". What do you think that message means in your own words?
3. Version 2 changed `Photo` to `PHOTO`, and the check still failed. Using `photo` as the example, what is still wrong?
4. Version 3 uses `tag.lower()`. What does `.lower()` do to a tag before the comparison?
5. The version 3 check passed on one example. Which other spellings of the tag (for example `PHOTO` or `pHoTo`) would you want to try before trusting it?

## Note for the instructor
- **How much the AI did:** The records show the AI made the version 2 and version 3 edits to `gallery.py`. In both cases the recorded edit matches the file change. Who wrote version 1 is unknown. The only student turns are three short requests ("write a small check", "try a change", "make the next change"). There is no record of Dara editing code.
- **Limits of the evidence:**
  - The history has no git repository, so the version order comes from folder names.
  - The "PASS" is a result recorded in the session. Nobody reran it independently, and it covers one example.
  - The check file the AI wrote contains only a comment line, yet the log shows FAIL and PASS outputs. I can't explain that gap from these files.
  - I can't give an AI percentage.
- **Understanding:** Dara's three check-in answers show no understanding yet. Q1 and Q2 got "I do not know" and "idk", and Q3 got no answer. That shows the answers weren't given. It doesn't show Dara can't understand. A short, low-pressure talk about version 3 would tell you more.
- **Consent:** Consent for public drafts is missing and drill consent is withdrawn. Keep everything here private to staff and family.
- **Next step:** Ask the instructor to select the next example.

## Weekly update for parents (private draft, please review before sending)
Hello,

This week Dara worked on Gallery Shelf, a small project with one goal: a gallery should accept the tag "photo" whatever its capital letters. Dara went through three versions with an AI assistant. The first two versions didn't give the right answer. The third now passes the one example check we ran.

The AI made most of the changes, and Dara's questions this week didn't yet show how the final fix works. So the next step is for the instructor to pick another example and go through it with Dara. There's nothing you need to do at home.
