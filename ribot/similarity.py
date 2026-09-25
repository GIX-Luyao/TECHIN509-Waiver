"""Vector comparison. See SPEC.md sections 2 and 3."""

import math
from collections.abc import Sequence


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Return the cosine of the angle between ``a`` and ``b``."""
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def top_k_indices(scores: Sequence[float], k: int) -> list[int]:
    """Return the indices of the ``k`` highest scores, highest first."""
    if k < 0:
        raise ValueError("k must be >= 0")

    ranked = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    return ranked[:k]
