**Not checked:** I read the project folder's `shelf.py` only. I couldn't list the directory, so other files may exist. No run was saved for version 3. I haven't run the code, so I haven't confirmed that the final version passes.

## 1. Questions for Faye

1. Your idea says a shelf is full as soon as used slots equal capacity. If a shelf has 5 slots and 5 are used, what should `full(5, 5)` return? What did the first version return, and why?
2. The first version used `used > capacity`. In your own words, what is the difference between `>` and `>=`? Why does that difference matter for a shelf that has exactly 5 of 5 slots used?
3. The second version changed the line to `used >= capacity + 1`. Walk through `full(5, 5)` on that line. Does the "expected True, got False" failure still happen? Why?
4. The final version is `return used >= capacity`. What would you test to be sure it's right? Name at least one case exactly at the limit, one below it and one above it.
5. Who changed each version, and what did you do to figure out the fix? If you used an AI tool or a classmate, say where.

## 2. Note for the instructor: how much the AI did

**The evidence doesn't say how much the AI did, so I can't give a fair estimate.**

- **What the history shows.** `shelf.py` is two lines long and changed in three snapshots. The first used `>`. The second used `>= capacity + 1`. The third used `>= capacity`.
- **The order is from you.** The snapshots are in the folder-name order you supplied. Timestamps don't prove the sequence.
- **Authorship is unrecorded.** The notes say the writer and runner were not recorded. For version 3, the student wrote "I do not know who changed it."
- **No AI record exists.** No AI replies or tool calls were saved. That is not evidence the AI wasn't used, only that nothing was recorded.
- **Failure and fix.** Version 1 failed with "expected True, got False". The saved note says version 2 still failed. The final code matches the project idea. Nothing in the record shows version 3 was run.
- **Consent.** Classroom drill consent is missing, and the history marks public drafts as not permitted.

I'd rely on the questions above, asked live, to find out how much Faye understands the code and wrote it themself. The history can't answer that.

## 3. Weekly update for parents

**Not ready to send.** Consent for public drafts is missing, and no live link was supplied. This is a private draft for staff.

Hi,

This week Faye worked on Shelf Slots. It is a small program that decides when a shelf is full: a shelf is full as soon as the used slots equal its capacity.

Faye worked through three versions of one rule. The first treated a shelf as full only when it was over capacity, so a shelf with every slot used wasn't counted as full. The second attempt didn't fix that. The third version matches the intended rule.

Next step: the instructor will pick the next example for Faye to work on.
