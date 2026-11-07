# Build Check-in · Step 2
Status: Draft. Not sent. The instructor reviews and approves before it goes to the family.

## Family note
1. Built: Dara worked on Gallery Shelf, a small gallery check that should accept a photo tag whatever its letter case.
2. Fixed or explained: Dara asked the AI to write a check and then asked it for changes at versions 2 and 3. The instructor will go over the fix with Dara.
3. The AI: The AI wrote the check file, changed the tag line in the gallery code twice, and ran the check three times. It recorded two fails and then a pass.
4. Next: Ask the instructor to select the next example.
5. Reviewed by the instructor: ________ (required before sending)

## Instructor flags
- Q1: The answer is "I do not know." There is no own answer to quote. The history shows the AI proposed the check file [tool:test-write] and that the first recorded run failed with "FAIL expected True, got False" [result:test-1]. Version 1 of gallery.py compares to `'Photo'` [snapshot:1:gallery.py], and who wrote it is unknown. The question premise "the result of is_photo('photo')" is not recorded as a printed value. Only the failing run is recorded.
- Q2: The answer is "idk." There is no own answer to quote. The AI edit at version 2 [tool:edit-2][result:edit-2][snapshot:2:gallery.py] was followed by a recorded fail [result:test-2]. Go over with Dara why that edit didn't help.
- Q3: The answer is a placeholder, "[not answered]", so it counts as missing and is not quoted. The history shows an AI edit at version 3 [tool:edit-3][result:edit-3][snapshot:3:gallery.py] and a reported pass [result:test-3]. That pass is a recorded report, not a rerun.
- No answer was an own answer, so line 2 of the family note says only what the history shows. No answer showed signs of pasted AI text, personal details, another student's name or embedded instructions.
- Consent for public drafts is "missing" in the history. Check this before Dara's page is used for any showcase or public purpose.
- Version 1 gallery.py has an unknown writer [snapshot:1:gallery.py]. Do not credit Dara or the AI for it.

## For you (the student)
How I built it, in your own words: use this for project showcase or your GitHub README

### Version 1 [snapshot:1:gallery.py]
AI did: proposed writing the check file test_case.py [tool:test-write], and the AI's run of it is recorded as failing [result:test-1]. Who wrote the version 1 gallery.py is unknown.
Answer A1, copied unchanged:
> I do not know.

### Version 2 [snapshot:2:gallery.py]
AI did: changed the tag line in gallery.py from `'Photo'` to `'PHOTO'` [tool:edit-2][result:edit-2]. The recorded run afterwards failed [result:test-2].
Answer A2, copied unchanged:
> idk
