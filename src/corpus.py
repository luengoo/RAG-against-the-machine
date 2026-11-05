from typing import List, Tuple
from pathlib import Path

from tqdm import tqdm
from src.models import Chunk
from src.markdown_chunker import TEXT_FINDERS, chunk_markdown
from src.python_chunker import chunk_python
from src.splitting import merge_spans, split_range


def chunk_text(text: str, max_size: int) -> List[Tuple[int, int]]:
    """Trocea el texto plano por párrafos y líneas."""
    if not text.strip():
        return []
    spans = split_range(text, 0, len(text), max_size, TEXT_FINDERS)
    return merge_spans(spans, max_size)


def chunk_file(text: str, file_path: str, max_size: int) -> List[Chunk]:
    """Trocea un fichero según su extensión y devuelve sus chunks."""
    if file_path.endswith(".py"):
        spans = chunk_python(text, max_size)
    elif file_path.endswith(".md"):
        spans = chunk_markdown(text, max_size)
    else:
        spans = chunk_text(text, max_size)
    return [Chunk(file_path=file_path, start=a, end=b) for a, b in spans]


def iter_corpus_files(raw_dir: str,
                      extensions: Tuple[str, ...] = (".py", ".md", ".txt")
                      ) -> List[str]:
    """Rutas de los ficheros de raw_dir con alguna de las extensiones."""
    paths = [
        path.as_posix()
        for path in Path(raw_dir).rglob("*")
        if path.is_file() and path.suffix in extensions
    ]
    return sorted(paths)


def chunk_corpus(raw_dir: str, max_size: int) -> List[Chunk]:
    """Trocea todos los ficheros del corups."""
    chunks: List[Chunk] = []
    for path in tqdm(iter_corpus_files(raw_dir), desc="Troceando",
                     unit="fichero"):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        chunks.extend(chunk_file(text, path, max_size))
    return chunks
