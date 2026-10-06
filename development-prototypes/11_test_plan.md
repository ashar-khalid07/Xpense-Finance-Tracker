# Manual test plan

| Area | Input/action | Expected result |
|---|---|---|
| Start-up | Run `python app.py` | Server starts and `/` renders without an exception. |
| Empty state | Fresh database | Table says there are no expenses; charts render without breaking. |
| Add | Groceries / 25.50 / Food / valid date | Row is persisted, total and charts update. |
| Amount validation | 0, -5, `abc`, blank | Entry is rejected with a useful message. |
| Required values | Blank description/category | Entry is rejected. |
| Date validation | Invalid or malformed date | Entry is rejected rather than crashing. |
| Category validation | Tamper POST value to `Other` | Server rejects it even if browser validation is bypassed. |
| Sort | Two records on different dates | Newest date appears first. |
| Date filter | Start/end around a subset | Only matching rows appear; total/charts/export match the subset. |
| Reversed dates | End date earlier than start | Error is shown and invalid range is discarded. |
| Category filter | Select Food | Only Food entries appear. |
| Combined filters | Date range + Food | Both conditions are applied together. |
| Edit | Change amount/category/date | Existing row changes; ID remains the same. |
| Delete | Confirm deletion | Row disappears and aggregates recalculate. |
| CSV | Description contains comma/quotes | CSV remains valid because `csv.writer` escapes the field. |
| Currency precision | Add 0.10 and 0.20 | Stored/displayed values behave as decimal money, not binary float artefacts. |
