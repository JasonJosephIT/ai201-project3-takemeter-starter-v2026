# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter reads posts from Central Florida Reddit (r/orlando and r/centralflorida)
and sorts each one by what it is doing: arguing with evidence (`analysis`), asserting
without support (`hot_take`), responding in the moment (`reaction`), asking for or
passing on information (`explainer`), telling a story (`anecdote`), or selling
something (`advertisement`). Local subs mix all six in one feed, so the label tells a
reader whether a post is worth arguing with, answering, or skipping.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Every post gets exactly one label by answering four questions in order. The first
"yes" decides it, so two labels can never both be true.

0. **Is the post selling something?** It promotes a business, product, service, event
   or giveaway the writer is connected to and invites readers to buy, visit, sign up or
   attend → `advertisement`.
1. **Does the post take a position?** A judgment about how things are or should be
   that a reader could disagree with — not just the writer's own feelings.
   Yes → `analysis` if a checkable fact is a reason for the position, otherwise `hot_take`.
2. **No position. Is it about something the writer personally lived through?**
   Yes → `reaction` if it is happening now or just happened (hours, not weeks) and the
   post is the writer's response to it; `anecdote` if it is already over and told as a story.
3. **Neither.** It asks for or passes on information → `explainer`.

### `analysis`

**Definition:** Takes a position, and a specific, checkable fact (a number, date, quote,
record or named comparison) is a reason for it — remove the fact and the argument falls apart.

**Example 1:**
> Orange County schools finalizes $7.9B budget, district plans additional $8.5M in cuts. I had to do some math tonight. This budget is $7.9 billion. My hometown in Illinois is much smaller…

**Example 2:**
> An Investigation into AdventHealth: "Healing Ministry" or Billion-Dollar Monopoly? AdventHealth, one of the largest hospital systems in the U.S., operates under the mission "to extend the healing ministry of Christ." But a deep dive…

### `hot_take`

**Definition:** Takes a confident position about the world with no load-bearing support; any
number in it is decoration on a conclusion already reached.

**Example 1:**
> Resort fees are the biggest scam the hotel industry has ever come up with. I hope he takes them to the cleaners! 😤

**Example 2:**
> Am I the only one who notices this, but do people completely forget how to walk in public here? Seems like 80% of people walking around the shops love to take up the entire walkway…

### `reaction`

**Definition:** Takes no position; the writer is responding to something they are seeing or
just experienced, in the moment — feeling or first-hand report, not a story.

**Example 1:**
> Holy shit that was the brightest rocket launch I've seen from my backyard in Orlando

**Example 2:**
> MCO right now. Used MCO Reserve. No line, dedicated TSA. Took 3 minutes… Airside: total shit show. Gates 70-79. People are camped out in the food court.

### `explainer`

**Definition:** Takes no position and is not about the writer's own experience; it asks for
or passes on information — a question, a request for recommendations, a how-to, or news.

**Example 1:**
> Garage epoxy recommendation. I'm looking to have epoxy work done and wanted to sanity-check pricing. Is a budget under $1,000 reasonable for this type of job?

**Example 2:**
> You can watch movies and TV for free with an Orange County Library Card. If you didn't already know…

### `anecdote`

**Definition:** Takes no position; the writer tells a story about something they experienced
that is already over, told for the story itself.

**Example 1:**
> We food shop every Friday morning, and every Friday morning a crow is perched on the highest point of the Publix sign in front of the store… just yapping like it's holding court.

**Example 2:**
> I work over in the area and stop by sometimes, usually around 4:00 pm on weekdays. There's a security guard I always see. He's always on high alert and will appear out of nowhere.

### `advertisement`

**Definition:** Promotes a business, product, service, event or giveaway the writer is
connected to (owns, works for, sells, organises) and invites readers to buy, visit, sign up
or attend. A customer recommending a place they like is not an ad.

**Example 1:**
> Free Live Band Karaoke Hey everyone, wanted to post here for those who were interested in my last post about live band Karaoke. The band will be doing live band karaoke at Chronic Guru on Pine St with no cover or fees! T…

**Example 2:**
> Free medical marijuana cards for veterans All the details are in this flyer

### The hardest boundary

**Which two labels:** `analysis` vs `explainer`. Orlando posts often share news packed with
facts (budgets, votes, fees), so "has facts" can't be the test.

**The decision rule I used every time:** Ask "so what does the writer want me to think?" If
the facts lead to a judgment (this is wrong, a waste, a scam, should change), it's `analysis`.
If the facts are the whole point (what happened, what it costs, how to do it), it's `explainer`.



---

## The Dataset

**Where the posts came from:** 215 posts from r/orlando and r/centralflorida, all posted
between 2 January and 14 October 2026. The first 200 came from each subreddit's top
posts of the year. Reddit's API blocks my machine, so the rest came from the Arctic
Shift Reddit archive (`collect_more.py`, `find_ads.py`), newest first; ads were allowed
to include mod-removed posts, because that is where most ads end up. The `text` column is
the real post: title plus body, or the title alone for link and image posts.

**How I labelled them:** Pre-labelled with AI, then reviewed. TypeSafe's Jev model
labelled every post with one six-way question built from the definitions above
(`prelabel.py`). I reviewed the labels, least-confident first, and kept all 215 of
Jev's labels unchanged. The first pass gave 136 of 200 posts to `explainer`, so I cut
`explainer` to a random 40 and kept pulling posts until every other label had 35.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `explainer` | 40 | 18.6% |
| `analysis` | 35 | 16.3% |
| `hot_take` | 35 | 16.3% |
| `reaction` | 35 | 16.3% |
| `anecdote` | 35 | 16.3% |
| `advertisement` | 35 | 16.3% |
| **Total** | 215 | 100% |

**Three hard cases**

**1.**
> *The post:* "Why does every dealership in the Orlando area suck. I've had my best luck with Mullinax Ford in Apopka and have went to them for my last 2 vehicles…"
>
> *Could have been:* `hot_take`, `explainer` (it is phrased as a question) or `anecdote` (it tells the writer's history with one dealer).
>
> *I chose `hot_take`, because:* question 1 comes first, and "every dealership in the Orlando area sucks" is a position with no checkable support. The question mark is rhetorical.

**2.**
> *The post:* "Plans to charge for parking at Lake Baldwin park and dog park. They're going to charge for parking for non-Winter Park residents… I thought parks were free to the public? All this is going to do is cause people to park on the…"
>
> *Could have been:* `explainer` (it passes on local news) or `hot_take`.
>
> *I chose `hot_take`, because:* my hardest-boundary rule asks what the writer wants me to think. The news is there to set up "all this is going to do is…", a prediction offered with no evidence.

**3.**
> *The post:* "Study places. We need more late night study places. WHY IS ORLANDO SO BEHIND ON EVERYTHING… can a rich person invest in a 3rd space we can use to study…"
>
> *Could have been:* `explainer` (a request) or `hot_take`.
>
> *I chose `hot_take`, because:* "Orlando is behind on everything" is a general claim about the city, and the request is a wish rather than a question anyone could answer.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 10 epochs, learning rate 5e-5, batch size 16, max length 128 tokens,
seed 42. Trained on an Apple Silicon GPU (MPS), torch 2.14.1.

**Anything I changed from the defaults, and why:** The first run used the defaults
(3 epochs, learning rate 2e-5) and learned nothing: training loss went from 1.80 to
1.73, against 1.79 for guessing evenly across six labels, and the model predicted
`explainer` for every post (accuracy 0.182, macro F1 0.051; committed as evidence).
With 149 training posts and batches of 16, three epochs is only about 30 update steps.
I raised it to 10 epochs at 5e-5. Training loss then fell to 0.28, but validation
accuracy peaked at 0.636 after epoch 3 and ended at 0.485, so by the last epoch the model
is memorising the training posts. The trainer keeps the final epoch, not the best one.

**Split sizes:** 149 train / 33 validation / 33 test, stratified. Test split per label:
`analysis` 5, `hot_take` 6, `reaction` 5, `explainer` 6, `anecdote` 5, `advertisement` 6.
Every label is under 8 in the test split, so one post moves a label's recall by about
0.17 to 0.20, and per-label F1 will jump between seeds next unit.

**Result (seed 42, test split):** accuracy 0.364, macro F1 0.377.

| Label | F1 |
|---|---|
| `advertisement` | 0.727 |
| `hot_take` | 0.500 |
| `analysis` | 0.364 |
| `reaction` | 0.333 |
| `anecdote` | 0.182 |
| `explainer` | 0.154 |

The most-confident third of test posts was *less* accurate (0.364) than the
least-confident third (0.455). The biggest confusion is `reaction` vs `anecdote`
(3 reactions predicted as anecdotes, 2 the other way): both are about the writer's own
experience, and the only difference, how long ago it happened, is easy to cut off at 128
tokens.

---

## How I Used AI

**Moment 1**

- *What I asked for:* Pre-label the first 200 posts with my labels so I could review instead of starting cold.
- *What came back:* 136 of 200 posts (68%) labelled `explainer`, just under the notebook's 70% cap, with `anecdote` at 9 posts.
- *What I changed:* I kept a random 40 explainers and had more posts collected and labelled until each other label reached 35. I also had every post's text switched from an AI summary to the real post, so the model couldn't learn "written like a summary" as a label cue.

**Moment 2**

- *What I asked for:* Replace `explainer` with `advertisement`.
- *What came back:* Claude pointed out that `explainer` is the catch-all at the end of my decision order (questions, recommendation requests, news), so removing it would leave most posts with no label that fits.
- *What I changed:* I kept `explainer` and added `advertisement` as a sixth label, checked first ("is it selling something the writer is connected to?"), then collected 35 ads.

**Pre-labelling disclosure:** All 215 labels were pre-labelled by TypeSafe Jev
(`prelabel.py`, `collect_more.py`, `find_ads.py`), with Claude (Claude Code) writing the
scripts and drafting the label definitions with me. I reviewed the labels and kept every
one of Jev's choices. Each row's `note` column records Jev's confidence for that post.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

Both models on the same 33 held-out posts (`test_split.csv`, seed 42). Baseline is
`facebook/bart-large-mnli` zero-shot, reading `label_definitions.txt`.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.182 | 0.364 | +0.182 |
| Macro F1 | 0.102 | 0.377 | +0.275 |
| F1 — `analysis` | 0.278 | 0.364 | +0.086 |
| F1 — `hot_take` | 0.000 | 0.500 | +0.500 |
| F1 — `reaction` | 0.333 | 0.333 | 0.000 |
| F1 — `explainer` | 0.000 | 0.154 | +0.154 |
| F1 — `anecdote` | 0.000 | 0.182 | +0.182 |
| F1 — `advertisement` | 0.000 | 0.727 | +0.727 |

**Bare label names instead of definitions** (`baseline_results_bare_names.json`):
accuracy 0.212, macro F1 0.124. That is one post *better* than with my definitions, so
on this baseline my definitions were worth -0.03 accuracy. The baseline slots each
definition into "This post is {}.", and my definitions are clauses ("takes a position,
and a specific checkable fact…"), so the hypothesis it tests isn't a sentence. The
reported baseline above is the definitions run.

**What I predicted before I looked:**
The trained model will beat the baseline on `advertisement` and `hot_take`, where the label shows in the wording (prices, "free", events; all-caps complaints), and lose or tie on `explainer` and `anecdote`, where my definitions describe the post's purpose rather than its words.

**What the gap actually means:**
Half right. The biggest gains were `advertisement` (+0.73) and `hot_take` (+0.50), as
predicted, but the trained model also beat the baseline on `explainer` and `anecdote`,
only because the baseline scored 0 on both; it never predicted them. The baseline's
0.182 is the same as always guessing one label, so zero-shot NLI can't do this task at
all, and the fine-tuning added a real but small amount on this split.

---

## Run Log — Before

Five criteria across three seeds (`results_three_seeds_before.json`). Device: Apple
Silicon GPU (MPS), torch 2.14.1. Settings: 10 epochs, learning rate 5e-5, batch 16.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 | 0.364 | 0.545 | 0.606 | MISSED |
| 2. Every label F1 (lowest label) | ≥ 0.40 | 0.154 (`explainer`) | 0.400 (`explainer`, `anecdote`) | 0.286 (`reaction`) | MISSED |
| 3. Largest / smallest label | ≤ 1.25 | 1.14 | 1.14 | 1.14 | MET |
| 4. Agreement with staff labels | ≥ 22 / 30 | — | — | — | pending (Milestone 3) |
| 5. Most-confident third minus least-confident third | ≥ +0.15 | -0.091 | +0.455 | +0.182 | MISSED |

Spread across seeds:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.364 | 0.545 | 0.606 | 0.242 |
| Macro F1 | 0.377 | 0.538 | 0.599 | 0.223 |
| F1 — `analysis` | 0.364 | 0.462 | 0.571 | 0.208 |
| F1 — `hot_take` | 0.500 | 0.444 | 0.750 | 0.306 |
| F1 — `reaction` | 0.333 | 0.615 | 0.286 | 0.330 |
| F1 — `explainer` | 0.154 | 0.400 | 0.545 | 0.392 |
| F1 — `anecdote` | 0.182 | 0.400 | 0.533 | 0.352 |
| F1 — `advertisement` | 0.727 | 0.909 | 0.909 | 0.182 |

Accuracy moved 24 points across seeds, well over 10. With 5 or 6 test posts per
label, the dataset is too small for a stable measure: which posts land in the test split
decides most of the score.

### Confusion matrix

Seed 42. Rows are true labels, columns are the model's guesses.

| true \ predicted | analysis | hot_take | reaction | explainer | anecdote | advertisement |
|---|---|---|---|---|---|---|
| **analysis** | 2 | 0 | 0 | 2 | 1 | 0 |
| **hot_take** | 1 | 2 | 0 | 2 | 1 | 0 |
| **reaction** | 0 | 0 | 2 | 0 | 3 | 0 |
| **explainer** | 2 | 0 | 3 | 1 | 0 | 0 |
| **anecdote** | 0 | 0 | 2 | 1 | 1 | 1 |
| **advertisement** | 1 | 0 | 0 | 1 | 0 | 4 |

**My biggest off-diagonal number, and what it means:**
3 real `reaction` posts were called `anecdote` (and 2 went the other way), so the model
hasn't learned my question 2 split: both labels are the writer's own experience, and the
only difference, whether it just happened or is already over, is a time cue that often
sits past the 128-token cut. A close second: 3 real `explainer` posts were called
`reaction`.

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
