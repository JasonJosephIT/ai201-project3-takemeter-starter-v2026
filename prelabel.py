"""Pre-label the Reddit posts with TypeSafe Jev. Run once; then read and correct every row.

    pip install typesafe-sdk
    export TYPESAFE_API_KEY=...        # from https://console.typesafe.ai/
    python prelabel.py ~/Downloads/labels_dataset.csv

Writes labels.csv (text,label,note) beside the notebook. Rows are sorted least-confident
first, so the posts most likely to be wrong are at the top when you review.
"""
import csv
import sys

from typesafe_sdk import Choice, TypeSafeClient

# Same five labels as LABELS in takemeter.ipynb, worded as in the README's Label Taxonomy.
LABELS = {
    "analysis": "Takes a position, and a specific checkable fact (number, date, quote, record, "
                "named comparison) is a reason for it; remove the fact and the argument falls apart.",
    "hot_take": "Takes a confident position about the world with no load-bearing support; any "
                "number is decoration on a conclusion already reached.",
    "reaction": "Takes no position; the writer responds to something they are seeing or just "
                "experienced (hours, not weeks), in the moment. Feeling or first-hand report, not a story.",
    "explainer": "Takes no position and is not about the writer's own experience; asks for or passes "
                 "on information: a question, a recommendation request, a how-to, or news.",
    "anecdote": "Takes no position; the writer tells a story about something they experienced that "
                "is already over, told for the story itself.",
    "advertisement": "Promotes a business, product, service, event or giveaway the writer is connected "
                     "to (owns, works for, sells, organises) and invites readers to buy, visit, sign up "
                     "or attend. A customer recommending a place they like is not an ad.",
}

QUESTION = Choice(
    instructions="Which label best describes what this Reddit post from a Central Florida "
                 "subreddit is doing? Judge the post's purpose, not its topic or tone.",
    criteria=LABELS,
)


def main(src):
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    out = []
    with TypeSafeClient() as client:
        for i, r in enumerate(rows, 1):
            text = f"{r['title'].strip()}\n\n{r['summary'].strip()}".strip()
            answer = client.system_one(state={"post": text}, questions={"label": QUESTION}).answers["label"]
            out.append((answer.confidence, text, answer.choice, r["url"]))
            print(f"{i}/{len(rows)}  {answer.choice:<10} {answer.confidence:.2f}  {r['title'][:60]}")

    out.sort()
    with open("labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label", "note"])
        for conf, text, label, url in out:
            w.writerow([text, label, f"pre-labelled by Jev (confidence {conf:.2f}), unchecked; {url}"])
    print(f"Wrote labels.csv: {len(out)} rows")


if __name__ == "__main__":
    main(sys.argv[1])
