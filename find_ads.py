"""Find advertisement posts and add them to labels.csv. Leaves the existing rows alone.

    source .venv/bin/activate
    export TYPESAFE_API_KEY=...
    python find_ads.py

Ads are rare, so posts are screened 20 at a time with one yes/no question each, and only
the likely ads get the full six-way label. A post is kept only if that label is advertisement.
"""
import csv
import re

from typesafe_sdk import Noul, TypeSafeClient

from collect_more import SUBS, post_text, posts
from prelabel import LABELS, QUESTION

TARGET = 35
MAX_SCANNED = 4000
BATCH = 20


def candidate(p):
    body = (p.get("selftext") or "").strip()
    # Mod-removed posts are kept: removed spam is exactly where ads end up.
    return body not in ("", "[removed]", "[deleted]") and not p.get("stickied") \
        and p.get("distinguished") != "moderator"


def screen(client, batch):
    texts = [post_text(p)[:1500] for p in batch]
    questions = {f"p{i}": Noul(instructions=f"Is `posts[{i}]` an advertisement? {LABELS['advertisement']}")
                 for i in range(len(texts))}
    answers = client.system_one(state={"posts": texts}, questions=questions).answers
    return [p for i, p in enumerate(batch) if answers[f"p{i}"].noul >= 0.5]


def main():
    rows = list(csv.DictReader(open("labels.csv", encoding="utf-8")))
    seen = {m.group(1) for r in rows if (m := re.search(r"/comments/(\w+)/", r["note"]))}
    found, scanned = [], 0

    with TypeSafeClient() as client:
        for sub in SUBS:
            batch = []
            for p in posts(sub):
                if len(found) >= TARGET or scanned >= MAX_SCANNED:
                    break
                if p["id"] in seen or not candidate(p):
                    continue
                seen.add(p["id"])
                batch.append(p)
                if len(batch) < BATCH:
                    continue
                scanned += len(batch)
                for c in screen(client, batch):
                    text = post_text(c)
                    a = client.system_one(state={"post": text[:4000]}, questions={"label": QUESTION}).answers["label"]
                    if a.choice == "advertisement" and len(found) < TARGET:
                        url = f"https://www.reddit.com/r/{c['subreddit']}/comments/{c['id']}/"
                        found.append({"text": text, "label": "advertisement",
                                      "note": f"pre-labelled by Jev (confidence {a.confidence:.2f}), unchecked; {url}"})
                        print(f"{scanned:>5} scanned  ad {len(found)}/{TARGET}  {c['title'][:60]}")
                batch = []
            if len(found) >= TARGET or scanned >= MAX_SCANNED:
                break

    rows += found
    rows.sort(key=lambda r: float(re.search(r"confidence ([\d.]+)", r["note"]).group(1)))
    with open("labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["text", "label", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"Added {len(found)} ads after scanning {scanned} posts. labels.csv now has {len(rows)} rows.")


if __name__ == "__main__":
    main()
