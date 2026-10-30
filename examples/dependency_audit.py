"""Check the packages of a requirements.txt against PyPI.

    python dependency_audit.py requirements.txt --out audit.csv

For every package it writes the version you pin (when the line has ==), the
latest version on PyPI and its release date, the Python versions it requires,
whether that version is yanked and how many known vulnerabilities PyPI lists
for it. Options (-r, -e), URLs and comments are skipped.
"""

import argparse
import re

from quanticdata_package_registry_api import PackageRegistry, write

FIELDS = ["name", "version", "released_at", "requires_python", "yanked", "known_vulnerabilities",
          "development_status", "license", "url"]


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def read_requirements(path):
    """Package name -> pinned version (or None), in file order."""
    pins = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if not line or line.startswith(("-", "git+", "http://", "https://")):
                continue
            match = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?\s*(?:==\s*([^\s,;]+))?", line)
            if match and not any(normalize(n) == normalize(match.group(1)) for n in pins):
                pins[match.group(1)] = match.group(2)
    return pins


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("requirements", help="path to a requirements.txt")
    parser.add_argument("--out", default="audit.csv")
    args = parser.parse_args()

    pins = read_requirements(args.requirements)
    names = list(pins)
    registry = PackageRegistry()
    rows = []
    for i in range(0, len(names), 50):  # one run reads up to 50 packages
        batch = names[i:i + 50]
        for p in registry.pypi(batch, max_results=len(batch)):
            pinned = next((v for n, v in pins.items() if normalize(n) == normalize(p["name"])), None)
            rows.append({"pinned": pinned, **{field: p.get(field) for field in FIELDS}})

    flagged = [r for r in rows if r["yanked"] or (r["known_vulnerabilities"] or 0) > 0]
    outdated = [r for r in rows if r["pinned"] and r["pinned"] != r["version"]]
    write(rows, args.out)
    print(f"{len(rows)} packages written to {args.out}: {len(outdated)} pinned to a version other than the latest, "
          f"{len(flagged)} yanked or with known vulnerabilities")


if __name__ == "__main__":
    main()
