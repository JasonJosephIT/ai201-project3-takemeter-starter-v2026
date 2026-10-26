---
status: active
progress: Unit 5 done (taxonomy, 215 labels, criteria, training, write-up); Unit 6 next
next_date:
updated: 2026-10-26
---

## Now
Unit 5 pushed to github.com/JasonJosephIT/ai201-project3-takemeter-starter-v2026. Seed 42: accuracy 0.364, macro F1 0.377 (target 0.70). Validation peaked at 0.636 after epoch 3, then overfit.

## Next
- Unit 6 M1: run baseline.py.
- Unit 6 M2: three seeds (RUN_LABEL = "before").
- Candidate fix for M5: keep the best validation epoch (or ~4 epochs) instead of the last.
- Spot-check low-confidence labels: some look wrong by my own decision order (e.g. 'He Was Found Dead Friday' labelled analysis).

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
