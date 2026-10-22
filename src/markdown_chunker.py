from typing import List, Tuple

from src.splitting import Finder, split_range, merge_spans


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


def chunk_markdown(text: str, max_size: int) -> List[Tuple[int, int]]:
    """Trocea un texto Markdown en rangos de como mucho max_size caracteres."""
    if not text.strip():
        return []
    spans = split_range(text, 0, len(text), max_size, MARKDOWN_FINDERS)
    return merge_spans(spans, max_size)


MARKDOWN_FINDERS: List[Finder] = [header_cuts, paragraph_cuts, line_cuts]
