def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0:
        raise ValueError("overlap must not be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += step

    return chunks
