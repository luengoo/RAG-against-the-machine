from typing import List, Tuple, Callable

Finder = Callable[[str, int, int], List[int]]


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


def split_range(text: str, start: int, end: int,
                max_size: int, finders: List[Finder],
                level: int = 0) -> List[Tuple[int, int]]:
    """Parte text[start:end] en rangos de como mucho max_size caracteres.

    Usa primero los cortes del nivel `level` y, si algún
    trozo sigue siendo demasiado grande, los del nivel siguiente.
    """
    if end - start <= max_size:
        return [(start, end)]
    if level >= len(finders):
        return [(i, min(i + max_size, end))
                for i in range(start, end, max_size)]
    cuts = finders[level](text, start, end)
    bounds = [start, *cuts, end]

    result: List[Tuple[int, int]] = []
    for a, b in zip(bounds, bounds[1:]):
        if b - a <= max_size:
            result.append((a, b))
        else:
            result.extend(
                split_range(text, a, b, max_size, finders, level + 1)
            )
    return result
