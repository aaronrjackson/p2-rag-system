"""Fetch the Counter-Strike articles of English Wikipedia as plain-text Markdown files for `p2 ingest`.

Walks the category tree under the roots below (two levels of subcategories), fetches each article's
plain text through the MediaWiki API (one request per article, politely spaced, backing off on 429),
drops sections that hold no prose (References, External links, ...), and writes one file per article:

    <out>/<slug>.md          "# Title", a blank line, the cleaned body
    <out>/sources.json       slug -> title, page URL, revision id (used to fill the manifest's source column)

Wikipedia text is CC BY-SA 4.0; the manifest records each page's address and revision for attribution.

    uv run python scripts/fetch_wikipedia.py --limit 10 --out ../p2-raw-trial     # a trial
    uv run python scripts/fetch_wikipedia.py                                      # everything, into ../p2-raw
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://en.wikipedia.org/w/api.php"
UA = "CSCI598E-P2-student-project (https://github.com/aaronrjackson/p2-rag-system)"
ROOTS = [
    "Category:Counter-Strike",
    "Category:Counter-Strike players",
    "Category:Counter-Strike teams",
    "Category:Counter-Strike competitions",
]
MAX_DEPTH = 2
PAUSE_S = 1.5
SKIP_SECTIONS = {
    "references", "external links", "notes", "see also", "further reading", "bibliography",
    "citations", "sources", "footnotes", "gallery", "explanatory notes",
}
MIN_WORDS = 150


def get(**params) -> dict:
    params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    for _ in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                body = r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(int(e.headers.get("retry-after", "30")) + 2)
                continue
            raise
        time.sleep(PAUSE_S)
        return json.loads(body)
    raise SystemExit("Wikipedia kept rate limiting; try again later.")


def members(category: str) -> list[dict]:
    out, cont = [], {}
    while True:
        d = get(action="query", list="categorymembers", cmtitle=category, cmlimit=500, cmtype="page|subcat", **cont)
        out += d["query"]["categorymembers"]
        if "continue" not in d:
            return out
        cont = d["continue"]


def article_titles() -> list[str]:
    seen, queue, titles = set(ROOTS), [(r, 0) for r in ROOTS], {}
    while queue:
        category, depth = queue.pop(0)
        for m in members(category):
            if m["ns"] == 14 and m["title"] not in seen and depth < MAX_DEPTH:
                seen.add(m["title"])
                queue.append((m["title"], depth + 1))
            elif m["ns"] == 0:
                titles.setdefault(m["title"], category)
    return sorted(titles)


def slug(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s or "page"


HEADING = re.compile(r"^(=+)\s*(.+?)\s*=+\s*$")


def clean(text: str) -> str:
    """Section headings become '## ...'; sections without prose, and empty ones, are dropped."""
    sections: list[tuple[int, str, list[str]]] = [(0, "", [])]
    for line in text.splitlines():
        m = HEADING.match(line.strip())
        if m:
            sections.append((len(m.group(1)), m.group(2), []))
        else:
            sections[-1][2].append(line)
    out, skipping_level = [], None
    for level, name, lines in sections:
        if skipping_level is not None and level > skipping_level:
            continue
        skipping_level = None
        if level and name.lower() in SKIP_SECTIONS:
            skipping_level = level
            continue
        body = "\n".join(l.rstrip() for l in lines).strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        if level and not body:
            continue
        out.append((f"{'#' * max(level, 2)} {name}\n\n" if level else "") + body)
    return "\n\n".join(p for p in out if p.strip()) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="../p2-raw", help="folder for the files (keep it outside the repo)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N articles (a trial)")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    titles = article_titles()
    print(f"{len(titles)} articles in the category tree")
    if args.limit:
        step = max(1, len(titles) // args.limit)
        titles = titles[::step][: args.limit]  # spread over the alphabet, not only the first N
    sources, kept = {}, 0
    for i, title in enumerate(titles, 1):
        d = get(action="query", prop="extracts|revisions", explaintext=1, exlimit=1, rvprop="ids", titles=title, redirects=1)
        page = next(iter(d["query"]["pages"].values()))
        body = clean(page.get("extract", ""))
        words = len(body.split())
        if words < MIN_WORDS:
            print(f"[{i}/{len(titles)}] skip {page['title']} ({words} words)")
            continue
        name = slug(page["title"])
        (out / f"{name}.md").write_text(f"# {page['title']}\n\n{body}", encoding="utf-8", newline="\n")
        url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(page["title"].replace(" ", "_"), safe="()_,'")
        sources[name] = {"title": page["title"], "url": url, "revid": page["revisions"][0]["revid"], "words": words}
        kept += 1
        if i % 10 == 0 or args.limit:
            print(f"[{i}/{len(titles)}] {page['title']} ({words} words)")
    (out / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    total = sum(s["words"] for s in sources.values())
    print(f"kept {kept} articles, {total:,} words, about {int(total * 1.4):,} tokens, in {out}")


if __name__ == "__main__":
    main()
