"""Ablation of rerank: the same listwise reranker, but each passage is cut to 600 words and not 200.

Everything else is the same as rerank.py (hybrid's top 20, the same prompt, schema and fallback), so any
difference in the scores comes from how much of each page Claude sees.
"""

from __future__ import annotations

from p2 import claude, retrievers

NEEDS_CLAUDE = True

TOP = 20
BASE = "rerank"
PASSAGE_WORDS = 600  # rerank.py uses 200; this is the one thing the ablation changes

SCHEMA = {
    "type": "object",
    "properties": {
        "order": {
            "type": "array",
            "items": {"type": "integer", "minimum": 1, "maximum": TOP},
            "minItems": TOP,
            "maxItems": TOP,
        }
    },
    "required": ["order"],
}

SYSTEM = "You rank passages by how well each one answers a search query. Reply only with the structured order."


def _cut(text: str) -> str:
    words = text.split()
    return " ".join(words[:PASSAGE_WORDS]) + (" ..." if len(words) > PASSAGE_WORDS else "")


def _prompt(query: str, passages: list[str]) -> str:
    shown = "\n\n".join(f"[{i}] {_cut(p)}" for i, p in enumerate(passages, 1))
    return (
        f"Query: {query}\n\n"
        f"Below are {len(passages)} numbered passages. Order them from most to least relevant to the query: "
        f"a passage is relevant if it states the requirement the query asks about. "
        f"Return all {len(passages)} numbers, each exactly once, best first.\n\n{shown}"
    )


class Rerank:
    def __init__(self, corpus, cfg):
        self.corpus = corpus
        self.cfg = cfg
        self.first = retrievers.build("hybrid", corpus, cfg)
        self.model = cfg.model
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

    def _reorder(self, query: str, candidates: list[tuple[str, float]], texts: list[str]) -> list[tuple[str, float]]:
        """The candidates reordered by Claude, with scores that fall from top to bottom of the result."""
        head, tail = candidates[:TOP], candidates[TOP:]
        order = None
        if len(head) == TOP:  # fewer than 20 candidates: nothing worth a call
            reply = claude.call(_prompt(query, texts[:TOP]), SCHEMA, system=SYSTEM, model=self.model, cache_dir=claude.cache_folder(self.cfg))
            got = (reply.output or {}).get("order")
            if isinstance(got, list) and sorted(got) == list(range(1, TOP + 1)):
                order = got
        if order is None:
            order = list(range(1, len(head) + 1))  # keep the first-stage order
        ranked = [head[i - 1][0] for i in order] + [c[0] for c in tail]
        n = len(ranked)
        return [(item, float(n - r)) for r, item in enumerate(ranked)]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        candidates = self.first.search(text, max(k, TOP))
        passages = [self.corpus.docs[docid].text for docid, _ in candidates]
        return self._reorder(text, candidates, passages)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        candidates = self.first.search_chunks(text, max(k, TOP))
        passages = [self.chunk_text[cid] for cid, _ in candidates]
        return self._reorder(text, candidates, passages)[:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
