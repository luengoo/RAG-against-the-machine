from typing import List


def chunker(file_text: str, max_chunk_size: int) -> List[tuple[int, int]]:
    if len(file_text) <= max_chunk_size:
        return ((0, len(file_text)))
    else:
        cuts = header_cuts(file_text, 0, len(file_text))

def header_cuts(text: str, start: int, end: int) -> List[int]:
    """Posiciones donde empieza cada encabezado Markdown dentro de (start, end).

    Ignora los '#' que están dentro de bloques de código ```.
    """
    cuts: List[int] = []
    pos = 0
    in_code = False
    for line in text.splitlines(keepends=True):
        stripped_line = line.lstrip()
        if stripped_line.startswith("```"):
            in_code = not in_code
        if not in_code and is_header(line) and start < pos < end:
            cuts.append(pos)
        pos += len(line)
    return cuts



def split_range(text: str, start: int, end: int,
                max_size: int, level: int) -> List[tuple[int, int]]:
    

def is_header(line: str) -> bool:
    """True si la línea es un encabezado Markdown (de # a ######)."""
    n = len(line) - len(line.lstrip("#"))
    return 1 <= n <= 6 and line[n:].startswith(" ")