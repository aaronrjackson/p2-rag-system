"""Hybrid retrieval: reciprocal rank fusion (RRF) of bm25 and dense.

Each item scores the sum of 1 / (RRF_K + rank) over the rankings it appears in, with RRF_K = 60 as in
the 13 lab. Both systems are asked for their full rankings, because a document that is 11th in both
lists can belong in the fused top 10.
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False

RRF_K = 60
PARTS = ("bm25", "dense")


def rrf(rankings: list[list[tuple[str, float]]]) -> list[tuple[str, float]]:
    """Fuse best-first rankings of (id, score) pairs; equal fused scores fall in id order."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item, _score) in enumerate(ranking, 1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (RRF_K + rank)
    return order(fused.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        self.parts = [retrievers.build(name, corpus, cfg) for name in PARTS]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(self.parts[0].chunks)

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([p.search(text, self.n_docs) for p in self.parts])[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([p.search_chunks(text, self.n_chunks) for p in self.parts])[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
