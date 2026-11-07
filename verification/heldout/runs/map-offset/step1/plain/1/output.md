## Questions for Cleo

1. In version 1, `pick` returned `points[index + 1]`. If you asked for index 2 and the points were hill, ridge, lake, what would it return, and why does that match your "got hill instead of lake" report? (This assumes hill is the point you got and lake the one you wanted.)
2. Version 2 changed `index + 1` to `1 + index`, and you said it still gave the same point. Why didn't that change anything?
3. Version 3 is `points[index]`. Why does this fix it? What does "zero-based index" mean here, and which point does index 0 return?
4. What would `pick(points, 0)` return in version 1 and in version 3? What does `pick` do if you ask for the last index in version 1, and why?
5. You didn't record any test run. What one quick check could you do now to show version 3 is right? Which index would you try, and what answer would you expect?

## Note for the instructor

**How much the AI did is unknown from this log, and I can't give a percentage.**
- **What the log shows:** three versions of one file, `map.py`. It has a single function, and a one-line change in each version.
- **Who made each change:** the log doesn't say. All four changed lines are marked unknown or conflicting. Cleo wrote that she did not record who changed version 3 or whether any test was run. The log has no AI replies. Only Cleo's three messages are there.
- **Order of versions:** it comes from the folder names you supplied. Timestamps don't prove the order.
- **What Cleo did show:**
  - She reported the symptom clearly in version 1 ("hill instead of lake").
  - She asked for the bug to be explained before she changed anything, which is a good habit.
- **What's unconfirmed:** whether she understood the fix. Version 2 was a rewording that didn't change the behavior. Version 3 is the actual fix.
- **Next step:** use the questions above in person. Her answers to 1 to 3 will tell you more than the log can.
- **Drill consent:** consent for a classroom drill is "yes". Public-copy consent is missing.

## Weekly update for parents

**Not drafted.** The log has no permission recorded for public or parent-facing text about Cleo. The instructor should confirm that permission before I write it.

I also don't want to guess at what Cleo did herself. Once permission is confirmed, the update would say only what the log supports:
- Cleo is working on Trail Pins, a route picker.
- She found that it returned the wrong point, and she worked through three versions to fix it.
