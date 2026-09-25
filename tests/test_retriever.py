import pytest
from ribot.retriever import Retriever

CORPUS = [
    "vacation policy: twenty days of paid leave",
    "expense reports go through the finance portal",
    "paid leave requests need manager approval",
    "the office kitchen is restocked on mondays",
]

# Hand-written unit vectors, so the expected similarity of each chunk to the query
# is exactly its first component: 0.6, 0.0, 0.8, 0.0.
VECTORS = {
    CORPUS[0]: [0.6, 0.8, 0.0],
    CORPUS[1]: [0.0, 1.0, 0.0],
    CORPUS[2]: [0.8, 0.6, 0.0],
    CORPUS[3]: [0.0, 0.0, 1.0],
    "paid leave": [1.0, 0.0, 0.0],
}


def embed(text: str) -> list[float]:
    return VECTORS[text]


def test_search_returns_at_most_k_hits():
    retriever = Retriever(CORPUS, embed)
    assert len(retriever.search("paid leave", k=2)) == 2


def test_search_ranks_the_best_chunk_first():
    retriever = Retriever(CORPUS, embed)
    assert [hit.index for hit in retriever.search("paid leave", k=4)] == [2, 0, 1, 3]


def test_search_drops_chunks_below_the_threshold():
    retriever = Retriever(CORPUS, embed, min_score=0.5)
    assert [hit.index for hit in retriever.search("paid leave", k=4)] == [2, 0]


def test_search_rejects_a_nonsense_k():
    retriever = Retriever(CORPUS, embed)
    with pytest.raises(ValueError):
        retriever.search("paid leave", k=0)
