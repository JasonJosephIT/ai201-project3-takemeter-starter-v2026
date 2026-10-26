---
status: active
progress: Unit 6 M1-M2 done; M3 (staff labels) waiting on me
next_date:
updated: 2026-10-26
---

## Now
Unit 6: baseline 0.182 vs trained 0.364 (seed 42). Three seeds 0.364 / 0.545 / 0.606 (spread 0.24). Criteria 1, 2, 5 MISSED, 3 MET, 4 pending. Biggest confusion reaction -> anecdote.

## Next
- M3: label the 30 posts in my_staff_labels.csv under data/staff_taxonomy.md, then get data/staff_labels.csv from the TF and run agreement.py.
- M4: verdict + diagnosis per criterion, using the agreement report.
- M5: one fix (candidates: relabel reaction/anecdote boundary, or keep best validation epoch), RUN_LABEL = "after".

## Decisions
- 2026-10-26: Criteria set: accuracy >= 0.70, every label F1 >= 0.40, largest/smallest <= 1.25, staff agreement >= 22/30, confident third >= least-confident third + 0.15.
- 2026-10-26: Training changed from 3 epochs / 2e-5 (underfit, predicted explainer for everything) to 10 epochs / 5e-5.
- 2026-10-26: Added `advertisement` as a 6th label (step 0: is it selling something the writer is connected to?), kept `explainer` as the catch-all. find_ads.py collects 35 ads; existing 180 rows untouched.
- 2026-10-26: Taxonomy written (Milestone 2) in Project 3 README + label_definitions.txt: three ordered questions (position? → lived it? → else explainer) make labels mutually exclusive. Hardest boundary: analysis vs explainer. Label ids stay analysis/hot_take/reaction/explainer/anecdote.
- 2026-10-26: Jev (TypeSafe) is used only for the first-pass labels; training is the notebook's DistilBERT.
- 2026-10-26: Balance to ~35 per label (about 175 rows), keeping 40 of the 136 explainers.
- 2026-10-26: Text is the real post (title + body, or title only for link posts), not the summaries, so the model can't learn summary style as a label cue.
- 2026-10-26: More posts come from the Arctic Shift archive, because Reddit's API blocks this machine.

## Open items / waiting on
- Milestone 3: criteria.md still blank.
- README pre-labelling disclosure.

## Idea Shelf
