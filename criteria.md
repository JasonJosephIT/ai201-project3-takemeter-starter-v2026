# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.70 on the test split, on all three seeds.

**Why this target:** Six balanced labels mean always guessing the biggest label
(`explainer`, 40 of 215) scores 18.6%, so 0.70 is almost four times that. It is
the point where I'd trust the model to sort a feed: wrong on fewer than one post in
three. It is ambitious for 215 rows pre-labelled by Jev and cut at 128 tokens, but
most of my labels carry surface cues (prices and "free" for `advertisement`, "just
saw" and "right now" for `reaction`, question marks and "recommendations" for
`explainer`), so a fine-tuned model should get there if the labels are consistent.

---

## 2. Every label has F1 of at least 0.40 on all three seeds.

**Why this target:** Each label has only about 5 posts in the test split (15% of 35),
so a single mistake moves that label's recall by 0.20. The floor has to survive that
noise, but 0.40 is still more than double the 0.17 of guessing at random. The label
most at risk is `analysis`, which shares my hardest boundary with `explainer`:
Orlando news posts are full of facts whether or not they argue anything.

---

## 3. The largest label has at most 1.25 times the posts of the smallest.

**Why this target:** I cut `explainer` from 136 posts to 40 to rebalance, so the file
sits at 40 / 35 = 1.14 now. Corrections during review can drift it back; past 1.25 the
smallest labels start losing test posts they can't spare.

---

## 4. I agree with the staff labels on at least 22 of 30 posts.

**Why this target:** The staff taxonomy's three labels match my first three almost word
for word, including the same `analysis` vs `hot_take` rule, so I should mostly agree.
22 / 30 (73%) leaves room for the `reaction` vs `hot_take` boundary on running posts,
which I never had to apply to Orlando ones.

---

## 5. Accuracy on the model's most-confident third of test posts is at least 0.15 higher than on its least-confident third, on all three seeds.

**Why this target:** The point of confidence is to flag posts for a person to check. If
the sure third isn't clearly more accurate than the unsure third, the flag is useless.
With about 11 posts per third, 0.15 is roughly two posts, the smallest gap I'd trust.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
