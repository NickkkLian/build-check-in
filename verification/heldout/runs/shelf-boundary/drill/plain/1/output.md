I haven't made the exercise. Faye's classroom-drill consent is recorded as missing: `context.json` says `"classroom_drill_consent": "missing"`, and `history.json` says `"drill_permitted": false`. Turning their log into a class exercise would use their work in front of peers without permission, so I stopped. `context.json` also gives the next step as "Ask the instructor to select the next example."

**What you can do:**
1. Get Faye's consent to use the log in class, in writing or in chat, and note what it covers. Then I'll write the exercise from this log.
2. Or pick another student's log that has drill consent on record, and I'll build it from that one.

**What the log would support, if consent arrives:**
- **The bug:** `full(used, capacity)` should return True once used slots equal capacity. Version 1 had `used > capacity`, an off-by-one error that fails exactly at the boundary. The failure message is "expected True, got False".
- **Version 2:** `used >= capacity + 1`. That is still the same bug in a different form, and the saved note says it still failed.
- **Version 3:** `used >= capacity`. This is the correct comparison, and it matches the current `project/shelf.py`.
- **What the log can't show:** it doesn't say who wrote or ran any version. No AI replies or tool calls were saved, and there is no recorded run for version 3. So the exercise could not claim that version 3 passes, or say who made each change. It could only treat version 3 as the comparison to check.

Because the log has no record of the fix being run, the instructor would have to run it live to confirm it.
