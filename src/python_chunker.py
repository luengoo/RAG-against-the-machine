from typing import List, Tuple
import ast

from src.splitting import Finder, split_range, merge_spans
from src.markdown_chunker import paragraph_cuts, line_cuts


def positions_finder(positions: List[int]) -> Finder:
    """Crea un buscador que devuelve las posiciones dadas dentro de
    (start, end)."""
    def finder(text: str, start: int, end: int) -> List[int]:
        return [p for p in positions if start < p < end]
    return finder


def line_starts(text: str) -> List[int]:
    """Posición de inicio de cada línea de text (índice 0 = línea 1)."""
    pos_list: List[int] = []
    pos: int = 0
    for line in text.splitlines(keepends=True):
        pos_list.append(pos)
        pos += len(line)
    return pos_list


def statement_starts(body: List[ast.stmt], starts: List[int]) -> List[int]:
    """Posición de inicio de cada sentencia de body (incluye decoradores)."""
    positions: List[int] = []
    for statement in body:
        decorators = getattr(statement, "decorator_list", [])
        first_line = min([statement.lineno] + [d.lineno for d in decorators])
        positions.append(starts[first_line - 1])
    return positions


def nested_starts(body: List[ast.stmt], starts: List[int]) -> List[int]:
    """Inicio de las sentencias dentro de las clases y funciones de body."""
    positions: List[int] = []
    for node in body:
        if isinstance(
                node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            positions.extend(statement_starts(node.body, starts))
    return positions


def chunk_python(text: str, max_size: int) -> List[Tuple[int, int]]:
    """Trocea código Python en rangos de como mucho max_size caracteres.

    Corta por clases y funciones; si el código no se puede analizar,
    lo trocea como texto (párrafos y líneas).
    """
    if not text.strip():
        return []
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        finders = [paragraph_cuts, line_cuts]
    else:
        starts = line_starts(text)
        finders = [positions_finder(statement_starts(tree.body, starts)),
                   positions_finder(nested_starts(tree.body, starts)),
                   paragraph_cuts, line_cuts]
    spans = split_range(text, 0, len(text), max_size, finders)
    return merge_spans(spans, max_size)
