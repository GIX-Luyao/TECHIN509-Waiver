"""A deterministic offline embedding. No network, no API key, no randomness."""

import hashlib

DIMS = 16


def embed(text: str) -> list[float]:
    """Hash the words of ``text`` into a fixed-length bag-of-words vector."""
    vector = [0.0] * DIMS
    for token in text.lower().split():
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        vector[int(digest, 16) % DIMS] += 1.0
    return vector
