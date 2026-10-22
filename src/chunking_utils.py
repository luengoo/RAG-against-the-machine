from typing import List, Tuple
from chunking import merge_spans as merge


def split_range(text: str, start: int, end: int,
                max_size: int, level: int = 0) -> List[Tuple[int, int]]:
    """Parte text[start:end] en rangos de como mucho max_size caracteres.

    Usa primero los cortes del nivel `level` (encabezados) y, si algún
    trozo sigue siendo demasiado grande, los del nivel siguiente.
    """
    if end - start <= max_size:
        return [(start, end)]
    if level >= len(FINDERS):
        return [(i, min(i + max_size, end))
                for i in range(start, end, max_size)]
    cuts = FINDERS[level](text, start, end)
    bounds = [start, *cuts, end]

    result: List[Tuple[int, int]] = []
    for a, b in zip(bounds, bounds[1:]):
        if b - a <= max_size:
            result.append((a, b))
        else:
            result.extend(
                split_range(text, a, b, max_size, level + 1)
            )
    return result


def header_cuts(text: str, start: int, end: int) -> List[int]:
    """Posiciones donde empieza cada encabezado Markdown dentro de (start, end)

    Ignora los '#' que están dentro de bloques de código ```.
    """
    cuts: List[int] = []
    pos: int = 0
    in_code: bool = False
    for line in text.splitlines(keepends=True):
        stripped_line = line.lstrip()
        if stripped_line.startswith("```"):
            in_code = not in_code
        if not in_code and is_header(line) and start < pos < end:
            cuts.append(pos)
        pos += len(line)
    return cuts


def line_cuts(text: str, start: int, end: int) -> List[int]:
    """Posición de inicio de cada línea dentro de (start, end)."""
    cuts: List[int] = []
    pos: int = 0
    for line in text.splitlines(keepends=True):
        if start < pos < end:
            cuts.append(pos)
        pos += len(line)
    return cuts


def paragraph_cuts(text: str, start: int, end: int) -> List[int]:
    """Inicio de cada párrafo (línea tras una línea en blanco) en
    (start, end)."""
    cuts: List[int] = []
    pos: int = 0
    prev_blank: bool = False
    for line in text.splitlines(keepends=True):
        blank: bool = line.strip() == ""
        if prev_blank and not blank and start < pos < end:
            cuts.append(pos)
        prev_blank = blank
        pos += len(line)
    return cuts


def is_header(line: str) -> bool:
    """True si la línea es un encabezado Markdown (de # a ######)."""
    n = len(line) - len(line.lstrip("#"))
    return 1 <= n <= 6 and line[n:].startswith(" ")


FINDERS = [header_cuts, paragraph_cuts, line_cuts]
