# Build check-in: Cleo, Trail Pins

Everything below comes from three snapshots of `map.py`, three chat lines and the pasted answers. The snapshot order is the folder-name order that staff supplied. Timestamps don't prove which came first.

## 1. Questions for Cleo

Questions 1 to 3 are the ones Cleo already answered. I've kept them because the answers don't show understanding yet. Questions 4 and 5 are new, for a follow-up.

1. At version 1, `pick(['lake', 'hill', 'gate'], 0)` gave you `hill`, and you expected `lake`. Which position does the list start counting from, and why does `hill` come out?
2. At version 2 the line changed from `points[index + 1]` to `points[1 + index]`, and you reported it still gave the same point. Why did swapping the order of the two numbers change nothing?
3. At version 3 the line became `points[index]`. What does `pick(['lake', 'hill', 'gate'], 2)` return now? Say how you worked it out.
4. What would the old version 1 code do with `pick(['lake', 'hill', 'gate'], 2)`? Describe what you'd see.
5. Your note says you didn't record who made the version 3 change or whether you ran a test. Tell us in your own words: who wrote that line, and how do you know it works?

## 2. Note for the instructor: how much the AI did

**Bottom line: the record can't say how much the AI did.** Please don't read an AI percentage from this.

- **What the files show.** The bug was `points[index + 1]`, which is off by one. Version 2 only reordered the same sum (`1 + index`), so behaviour didn't change. Version 3 fixed it with `points[index]`. The current `map.py` matches version 3.
- **Who wrote each change.** All 4 changed-line records are marked "unknown or conflicting". There is no AI log, no git history and no student note that matches any of the diffs.
- **What the chat shows.** Cleo asked the AI to explain the bug before changing anything at version 2. We have no AI reply in the record, so we can't tell whether the AI's explanation led to version 3.
- **Cleo's own words.** Cleo wrote that they "did not record who changed" version 3 or any test run. This is self-reported and unverified.
- **Understanding.** The answers don't show it yet. Q1 ("I changed some things") doesn't answer what the question asked. Q2 says Cleo isn't sure what the change did. Q3 has no answer. Cleo did notice the bug and report it clearly, but that is the only understanding the record supports.
- **Tests.** There's no recorded test run. Nobody has independently confirmed that version 3 works. From reading the code, `points[index]` looks right for a zero-based index.
- **Suggested next step.** Ask Cleo to walk through Q1 and Q3 aloud with the list in front of them. Then have Cleo run `pick` on two or three indexes and note what comes back.

## 3. Weekly update for Cleo's parents

**Not ready to send.** The record has no parent-sharing consent: its state and scope are both "missing". Please get that first. The draft is ready for when it's in place.

> Hi, here's this week's update on Cleo's project, Trail Pins. It's a route picker that should return the point at the position you choose.
>
> Cleo found a bug: the picker was returning the wrong stop. It gave "hill" when "lake" was expected. After a couple of attempts, the code now looks correct on reading. It picks the point at exactly the position asked for.
>
> We're still working on Cleo explaining in their own words why the bug happened and why the fix works. Cleo also hasn't run a test yet to confirm it. Next week we'll go through the code together and run a few checks.
