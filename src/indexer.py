from typing import Dict, List
from pathlib import Path

from pydantic import ValidationError

from src.models import BM25Index
from src.corpus import chunk_corpus, scoring_text
from src.lexical import tokenize
from src.bm25 import build_postings

INDEX_FILE = "index.json"


class IndexLoadError(Exception):
    """El índice no existe o no se puede leer."""


def load_texts(paths: List[str]) -> Dict[str, str]:
    """Lee cada fichero una sola vez: ruta -> texto completo."""
    texts: Dict[str, str] = {}
    for path in paths:
        if path not in texts:
            with open(path, encoding="utf-8") as f:
                texts[path] = f.read()
    return texts


def build_index(raw_dir: str, max_size: int) -> BM25Index:
    """Trocea el corpus y construye el índice."""
    chunks = chunk_corpus(raw_dir, max_size)
    texts = load_texts([c.file_path for c in chunks])
    documents = [tokenize(scoring_text(c, texts[c.file_path]))
                 for c in chunks]
    postings, lengths = build_postings(documents)
    return BM25Index(max_chunk_size=max_size, chunks=chunks,
                     postings=postings, lengths=lengths)


def save_index(index: BM25Index, directory: str) -> None:
    """Guarda el índice en directory/index.json."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    with open(Path(directory) / INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(index.model_dump_json())


def load_index(directory: str) -> BM25Index:
    """Carga el índice guardado con save_index."""
    path = Path(directory) / INDEX_FILE
    try:
        with open(path, encoding="utf-8") as f:
            return BM25Index.model_validate_json(f.read())
    except FileNotFoundError as exc:
        raise IndexLoadError(
            f"No hay índice en {directory}: ejecuta primero el comando index"
        ) from exc
    except (OSError, ValidationError) as exc:
        raise IndexLoadError(
            f"El índice de {path} está dañado o no se puede leer: {exc}"
        ) from exc
