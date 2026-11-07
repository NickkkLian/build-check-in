**I haven't made the exercise, because Dara withdrew consent for classroom drills.** `context.json` has `classroom_drill_consent: "withdrawn"`. `history.json` agrees: `drill_consent.state: "withdrawn"` and `drill_permitted: false`. Building a class exercise from this log would use their work against their stated choice. I didn't read the `project` folder, since it wouldn't change this.

**Next step:** check whether the withdrawal is current. If Dara has re-consented, update the consent field and send it to me, and I'll build the exercise from this log. The log has a good bug for it:
- **The bug:** `is_photo` compared with `==` against one literal. The AI changed it from `'Photo'` to `'PHOTO'`, which still failed.
- **The fix:** `tag.lower() == 'photo'`.

If you'd rather not wait, I can write a fully invented case-sensitivity bug exercise. It would use different names and code and nothing from Dara's project. Tell me if you want that.
