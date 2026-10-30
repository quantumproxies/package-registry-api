"""Hacker News stories and Stack Overflow questions about a tool, in one CSV.

    python tech_mentions.py duckdb --top 30 --out duckdb_mentions.csv

Writes the stories and the questions that match a term side by side: source,
title, score (points or votes), replies (comments or answers), date and link,
newest first.
"""

import argparse

from quanticdata_package_registry_api import PackageRegistry, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("term")
    parser.add_argument("--top", type=int, default=30, help="results per source (max 100)")
    parser.add_argument("--site", default="stackoverflow", help="Stack Exchange site, e.g. serverfault")
    parser.add_argument("--out", default="mentions.csv")
    args = parser.parse_args()

    registry = PackageRegistry()
    rows = []
    for s in registry.hackernews(args.term, max_results=args.top):
        rows.append({"source": "hacker_news", "title": s["title"], "score": s["points"], "replies": s["comments"],
                     "created_at": s["created_at"], "link": s["hn_url"]})
    for q in registry.stackoverflow(args.term, site=args.site, sort="votes", max_results=args.top):
        rows.append({"source": args.site, "title": q["title"], "score": q["score"], "replies": q["answer_count"],
                     "created_at": q["created_at"], "link": q["link"]})

    rows.sort(key=lambda r: r["created_at"] or "", reverse=True)
    write(rows, args.out)
    print(f"{len(rows)} mentions of {args.term!r} written to {args.out}")


if __name__ == "__main__":
    main()
