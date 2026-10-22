from chunking_utils import split_range
from typing import List, Tuple


def chunker(file_text: str, max_chunk_size: int) -> List[Tuple[int, int]]:
    if len(file_text) <= max_chunk_size:
        return ((0, len(file_text)))
    else:
        cuts = header_cuts(file_text, 0, len(file_text))


def merge_spans(spans: List[Tuple[int, int]],
                max_size: int) -> List[Tuple[int, int]]:
    """Junta rangos contiguos mientras el resultado no pase de max_size."""
    merged: List[Tuple[int, int]] = []
    for a, b in spans:
        if merged and (b - merged[-1][0]) <= max_size:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def chunk_markdown(text: str, max_size: int) -> List[Tuple[int, int]]:
    """Trocea un texto Markdown en rangos de como mucho max_size caracteres."""
    if not text.strip():
        return []
    spans = split_range(text, 0, len(text), max_size)
    return merge_spans(spans, max_size)
