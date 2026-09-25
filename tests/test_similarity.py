from ribot.similarity import cosine_similarity, top_k_indices


def test_identical_unit_vectors_are_maximally_similar():
    assert cosine_similarity([1.0, 0.0, 0.0], [1.0, 0.0, 0.0]) == 1.0


def test_orthogonal_unit_vectors_are_unrelated():
    assert cosine_similarity([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]) == 0.0


def test_length_mismatch_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        cosine_similarity([1.0, 0.0], [1.0, 0.0, 0.0])


def test_top_k_returns_the_best_scores_first():
    assert top_k_indices([0.1, 0.8, 0.4], 2) == [1, 2]


def test_top_k_of_zero_is_empty():
    assert top_k_indices([0.1, 0.8, 0.4], 0) == []
