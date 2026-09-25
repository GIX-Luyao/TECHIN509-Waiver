"""Chunk retrieval over an in-memory corpus. See SPEC.md section 4."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from ribot.similarity import cosine_similarity


@dataclass(frozen=True)
class Hit:
    """One retrieved chunk."""

    text: str
    score: float
    index: int


class Retriever:
    """Scores every chunk against a query and returns the best matches."""

    def __init__(
        self,
        chunks: Sequence[str],
        embed_fn: Callable[[str], list[float]],
        min_score: float = 0.0,
    ) -> None:
        self.chunks = list(chunks)
        self.embed_fn = embed_fn
        self.min_score = min_score

    def search(self, query: str, k: int = 3) -> list[Hit]:
        """Return at most ``k`` hits, highest score first."""
        if k < 1:
            raise ValueError("k must be >= 1")

        query_vector = self.embed_fn(query)
        scored = [
            Hit(text=chunk, score=cosine_similarity(query_vector, self.embed_fn(chunk)), index=i)
            for i, chunk in enumerate(self.chunks)
        ]
        kept = [hit for hit in scored if hit.score >= self.min_score]
        kept.sort(key=lambda hit: (-hit.score, hit.index))
        return kept[:k]
