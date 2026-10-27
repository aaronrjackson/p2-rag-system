"""Rewrite the manifest's source column with each Wikipedia page's real address and revision (permalink).

sources.json comes from fetch_wikipedia.py. Run from the repo root: uv run python scripts/fix_sources.py ../p2-raw
"""

import csv
import json
import sys
from pathlib import Path
from urllib.parse import quote

raw = Path(sys.argv[1] if len(sys.argv) > 1 else "../p2-raw")
sources = json.loads((raw / "sources.json").read_text(encoding="utf-8"))
manifest = Path("corpora/own/manifest.tsv")
with manifest.open(encoding="utf-8", newline="") as f:
    rows = list(csv.reader(f, delimiter="\t"))
header, body = rows[0], rows[1:]
col = header.index("source")
missing = 0
for row in body:
    info = sources.get(row[0])
    if not info:
        missing += 1
        continue
    row[col] = f"https://en.wikipedia.org/w/index.php?title={quote(info['title'].replace(' ', '_'), safe='()_,')}&oldid={info['revid']}"
with manifest.open("w", encoding="utf-8", newline="\n") as f:
    csv.writer(f, delimiter="\t", lineterminator="\n").writerows([header, *body])
print(f"{len(body) - missing} sources fixed, {missing} not in sources.json")
