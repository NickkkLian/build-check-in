# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Faye is building Shelf Slots, a small program that says whether a shelf is full once the used slots reach its capacity.
2. Fixed or explained: Faye wrote, "At three out of three there is no room left."
3. The AI: The saved record shows no AI replies or AI edits. Who wrote each of the three versions is not recorded.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- Q1 [prompt:1][snapshot:1:shelf.py]: A1 is an own answer in Faye's words. It fits the version 1 failure note ("expected True, got False"), where the line is `used > capacity` [snapshot:1:shelf.py]. The note comes from you. It is a recorded report, not a rerun, and it does not say who ran it.
- Q2 [prompt:2][snapshot:2:shelf.py]: A2 is an own answer. It fits the saved note that version 2 "still has the same failure" [prompt:2]. Version 2 changed the line to `used >= capacity + 1` [snapshot:2:shelf.py]. Nobody recorded a run for it, and the writer is unknown. A2 is a short, general statement, so you could ask Faye to say where in the line the boundary is missed.
- Q3 [prompt:3][snapshot:3:shelf.py]: A3 is an own answer and matches the history. Version 3 changed the line to `used >= capacity` [snapshot:3:shelf.py]. No run for version 3 is saved, and the writer is unknown [prompt:3]. Faye's "I do not know who made the edits" is accurate. Do not credit Faye or the AI with any of the three edits.
- Attribution: all 4 changed lines are `unknown_or_conflicting`, and no AI reply or tool call was saved [prompt:2]. The note's line 3 says only that nothing is recorded.
- Consent: classroom and public consent are `missing`, so the note and showcase page stay private and no drill is allowed. The version order is the folder order you supplied, and timestamps do not prove chronology [snapshot:1:shelf.py].
- No answers look pasted or AI-written, none are missing, and none contain personal details, other students' names or instructions.

## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:shelf.py]
AI did: not recorded
Answer A1, copied unchanged:
> At three out of three there is no room left.

### Version 2 [snapshot:2:shelf.py]
AI did: not recorded
Answer A2, copied unchanged:
> The second version still misses the exact boundary.

### Version 3 [snapshot:3:shelf.py]
AI did: not recorded
Answer A3, copied unchanged:
> I looked at the three versions. I do not know who made the edits.
