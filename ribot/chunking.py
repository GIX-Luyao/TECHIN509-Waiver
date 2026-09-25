"""Splitting documents into overlapping windows. See SPEC.md section 1."""


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """Split ``text`` into overlapping chunks of at most ``size`` characters."""
    if not isinstance(size, int) or size < 1:
        raise ValueError("size must be an integer >= 1")
    if not isinstance(overlap, int) or overlap < 0 or overlap >= size:
        raise ValueError("overlap must be an integer in the range [0, size)")

    normalized = text.strip()
    if not normalized:
        return []

    step = size - overlap
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = start + size
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start += step
    return chunks
