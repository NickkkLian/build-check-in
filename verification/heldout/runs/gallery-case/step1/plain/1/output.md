Everything below comes from the build log. The log doesn't verify any of it, and I haven't re-run anything.

**Consent flags**
- Consent for public drafts is missing, so none of this should be posted publicly.
- Dara withdrew consent for classroom drills. Use the questions below one-on-one or in writing, not as a cold-call in front of the class.
- There is no live link, so I haven't claimed the project is deployed.

## 1. Questions for Dara

1. In your own words, what should `is_photo` return for `'photo'`, `'Photo'` and `'PHOTO'`? Why?
2. Version 1 compared against `'Photo'`, and the check failed. Why did a check for `'photo'` fail against that code?
3. Version 2 swapped `'Photo'` for `'PHOTO'` and still failed. Before you ran it, would you have predicted that? What does that fix still get wrong?
4. What does `tag.lower()` do, and why does comparing against lowercase `'photo'` make letter case stop mattering?
5. Your passing run tested one example. Name two other tags you would test next, such as `'pHoTo'`, `'photos'` or an empty string. What should each return?

## 2. Note for the instructor: how much the AI did

- **The AI made both recorded code changes.** The version 2 edit (`'Photo'` to `'PHOTO'`) and the version 3 edit (`tag.lower() == 'photo'`) each appear as AI edits in the session record, and each matches the file snapshots.
- **Version 1's origin is unknown.** The first `gallery.py` snapshot has no matching AI edit. It could be Dara's, the AI's or staff's, and the log can't say.
- **Dara's visible input was three short prompts.**
  - Prompt 1 stated the goal and asked for a check.
  - Prompts 2 and 3 were "Please try a change for version 2" and "Please make the next change for version 3". They don't show Dara choosing or reasoning about the fix.
  - Any manual edits or reasoning outside the log would be self-reported.
- **The AI diagnosed the problem.** Its one explanation was "The comparison is case-sensitive and the stored literal uses different case." The log shows no explanation from Dara.
- **Verification is thin.**
  - Two runs failed, then one run reported a pass on a single example.
  - These are recorded tool outputs, not independent reruns.
  - The recorded write of `test_case.py` contains only a comment line, and `test_case.py` isn't in the project folder I was given. I can't confirm what the check actually tested.
  - The final `gallery.py` does match the version 3 snapshot.
- **Don't read this as an AI percentage.** Two of the four changed-line records match AI edits and two are unknown. That is a count of changed lines, not who owns the final code.
- **Suggested follow-up:** have Dara explain the question 3 and 4 answers aloud or in writing. That shows whether the understanding is hers, whatever the log says.

## 3. Weekly update for parents

Hi, here is this week's update on Dara's project, Gallery Shelf.

Dara is building a small piece of a photo gallery. It should recognise a "photo" tag whether it's typed as `photo`, `Photo` or `PHOTO`.

This week the first two attempts didn't work. The third attempt worked on the one example it was tested on. The fix converts the tag to lowercase before comparing it. Dara used an AI assistant for this, and the code changes in the record were made by the assistant. Dara's next step is to talk through why the fix works and to test more kinds of tags. We'll ask the instructor to pick the next example.

This project isn't online yet.
