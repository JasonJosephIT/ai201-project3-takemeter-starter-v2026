"""Rebalance labels.csv: keep 40 explainers, then pull more posts until every label has TARGET.

    source .venv/bin/activate
    export TYPESAFE_API_KEY=...
    python collect_more.py

Posts come from the Arctic Shift Reddit archive (Reddit's own API blocks this machine).
Every row's text becomes the real post (title + body), including the 200 already labelled,
which were only title + summary. Mixing summaries with real posts would let the model learn
"written like a summary" instead of the label.

Writes labels.csv (the old one is kept as labels_jev_v1.csv). Least confident rows first.
"""
import csv
import json
import os
import random
import re
import time
import urllib.parse
import urllib.request

from typesafe_sdk import TypeSafeClient

from prelabel import QUESTION

TARGET = 35            # per label
KEEP_EXPLAINERS = 40
MAX_SCANNED = 2000     # stop here even if some label is still short
SUBS = ["orlando", "centralflorida"]
AFTER, BEFORE = "2026-01-01", "2026-10-15"
API = "https://arctic-shift.photon-reddit.com/api"


def get(path, **params):
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "takemeter-labeling/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["data"]


def usable(p):
    body = (p.get("selftext") or "").strip()
    return bool(body and body not in ("[removed]", "[deleted]") and not p.get("removed_by_category")
            and not p.get("stickied") and p.get("distinguished") != "moderator"
            and (p.get("num_comments") or 0) >= 3)


def post_text(p):
    return f"{p['title'].strip()}\n\n{p['selftext'].strip()}"


def posts(sub):
    """Newest first, one page of 100 at a time."""
    before = BEFORE
    while True:
        page = get("posts/search", subreddit=sub, after=AFTER, before=before,
                   limit=100, sort="desc")
        if not page:
            return
        yield from page
        before = page[-1]["created_utc"]
        time.sleep(1)


def label(client, text):
    a = client.system_one(state={"post": text[:4000]}, questions={"label": QUESTION}).answers["label"]
    return a.choice, a.confidence


def main():
    old = list(csv.DictReader(open("labels.csv", encoding="utf-8")))
    if not os.path.exists("labels_jev_v1.csv"):
        os.rename("labels.csv", "labels_jev_v1.csv")

    explainers = [r for r in old if r["label"] == "explainer"]
    random.Random(42).shuffle(explainers)
    kept = [r for r in old if r["label"] != "explainer"] + explainers[:KEEP_EXPLAINERS]

    # Swap each kept row's summary for the real post.
    ids = {re.search(r"/comments/(\w+)/", r["note"]).group(1): r for r in kept}
    found = {}
    for chunk in [list(ids)[i:i + 100] for i in range(0, len(ids), 100)]:
        for p in get("posts/ids", ids=",".join(chunk)):
            found[p["id"]] = p
    rows, seen = [], set()
    with TypeSafeClient() as client:
        for pid, r in ids.items():
            p = found.get(pid)
            url = r["note"].split("; ")[-1]
            if p:
                # Re-judge on what the model will see: the full post, or just the title for link posts.
                body = (p.get("selftext") or "").strip()
                text = post_text(p) if body not in ("", "[removed]", "[deleted]") else p["title"].strip()
                choice, conf = label(client, text)
            else:
                text, choice = r["text"], r["label"]  # not in the archive: keep the summary
                conf = float(re.search(r"confidence ([\d.]+)", r["note"]).group(1))
            rows.append((conf, text, choice, url))
            seen.add(pid)

        counts = {k: 0 for k in QUESTION.criteria}
        for row in rows:
            counts[row[2]] += 1
        print("Kept from first pass:", counts)

        scanned = 0
        for sub in SUBS:
            for p in posts(sub):
                if all(n >= TARGET for n in counts.values()) or scanned >= MAX_SCANNED:
                    break
                if p["id"] in seen or not usable(p):
                    continue
                seen.add(p["id"])
                scanned += 1
                text = post_text(p)
                choice, conf = label(client, text)
                if counts[choice] >= TARGET:
                    continue
                counts[choice] += 1
                rows.append((conf, text, choice, f"https://www.reddit.com/r/{p['subreddit']}/comments/{p['id']}/"))
                print(f"{scanned:>4} scanned  {choice:<10} {conf:.2f}  {counts}")

    rows.sort()
    with open("labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label", "note"])
        for conf, text, choice, url in rows:
            w.writerow([text, choice, f"pre-labelled by Jev (confidence {conf:.2f}), unchecked; {url}"])
    print(f"Wrote labels.csv: {len(rows)} rows, scanned {scanned} new posts. Final counts: {counts}")


if __name__ == "__main__":
    main()
