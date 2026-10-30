"""npm packages for a few search phrases, merged into one CSV.

    python npm_landscape.py "react state management" "react global store" --top 50

A package found by more than one phrase appears once, with every phrase that
found it in found_by; the CSV is sorted by weekly downloads, so the packages
people install most come first.
"""

import argparse

from quanticdata_package_registry_api import PackageRegistry, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("phrases", nargs="+")
    parser.add_argument("--top", type=int, default=30, help="packages per phrase (max 100)")
    parser.add_argument("--out", default="npm_landscape.csv")
    args = parser.parse_args()

    registry = PackageRegistry()
    found = {}
    for phrase in args.phrases:
        run = registry.npm(phrase, max_results=args.top)
        print(f"{phrase!r}: {len(run)} packages")
        for p in run:
            row = found.setdefault(p["name"], {**{k: v for k, v in p.items() if k != "rank"}, "found_by": []})
            row["found_by"].append(phrase)

    rows = sorted(found.values(), key=lambda r: r.get("downloads_weekly") or 0, reverse=True)
    write(rows, args.out)
    print(f"{len(rows)} distinct packages written to {args.out}")


if __name__ == "__main__":
    main()
