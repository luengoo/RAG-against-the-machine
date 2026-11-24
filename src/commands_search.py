import json
from typing import Any, List

from tqdm import tqdm
from pathlib import Path

from src.bm25 import search as bm25_search
from src.errors import IndexLoadError, EmptyQuestionError, InvalidKError
from src.errors import RagError
from src.indexer import build_index, load_index, save_index
from src.models import AnsweredQuestion
from src.models import MinimalSearchResults, StudentSearchResults
from src.datasets import load_dataset, save_json, load_model
from src.evaluation import question_recall


def _valid_int(value: Any, name: str, low: int, high: int) -> int:
    """Comprueba que un argumento de Fire es un entero en [low, high]."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidKError(f"--{name} debe ser un número entero")
    if not low <= value <= high:
        raise InvalidKError(f"--{name} debe estar entre {low} y {high}")
    return value


def index(max_chunk_size: int = 2000, raw_dir: str = "data/raw",
          processed_dir: str = "data/processed") -> None:
    """Trocea data/raw y guarda el índice en data/processed."""
    size = _valid_int(max_chunk_size, "max_chunk_size", 1, 2000)
    built = build_index(str(raw_dir), size)
    if not built.chunks:
        raise IndexLoadError(f"No hay ficheros que indexar en {raw_dir}")
    save_index(built, str(processed_dir))
    print(f"Ingestion complete! {len(built.chunks)} chunks. "
          f"Indices saved under {processed_dir}/")


def search(query: Any, k: int = 10,
           processed_dir: str = "data/processed") -> None:
    """Muestra las k fuentes más relevantes para una pregunta."""
    text = str(query).strip()
    if not text:
        raise EmptyQuestionError("La pregunta está vacía")
    top = _valid_int(k, "k", 1, 1000)
    idx = load_index(str(processed_dir))
    results = bm25_search(text, idx.postings, idx.lengths, top)
    output = MinimalSearchResults(
        question_id="query", question=text,
        retrieved_sources=[idx.chunks[d].to_source() for d, _ in results],
    )
    print(json.dumps(output.model_dump(), indent=2))


def search_dataset(dataset_path: str = "", k: int = 10,
                   save_directory: str = "data/output/search_results",
                   processed_dir: str = "data/processed") -> None:
    """Busca todas las preguntas de un dataset y guarda los resultados."""
    top = _valid_int(k, "k", 1, 1000)
    dataset = load_dataset(str(dataset_path))
    idx = load_index(str(processed_dir))
    results: List[MinimalSearchResults] = []
    for q in tqdm(dataset.rag_questions, desc="Buscando", unit="pregunta"):
        found = bm25_search(q.question, idx.postings, idx.lengths, top)
        results.append(MinimalSearchResults(
            question_id=q.question_id, question=q.question,
            retrieved_sources=[idx.chunks[d].to_source() for d, _ in found],
        ))
    out = Path(str(save_directory)) / Path(str(dataset_path)).name
    save_json(StudentSearchResults(search_results=results, k=top), out)
    print(f"Saved student_search_results to {out}")


def evaluate(student_search_results_path: str = "",
             dataset_path: str = "") -> None:
    """Calcula tu recall@k comparando tus resultados con las respuestas."""
    results = load_model(str(student_search_results_path),
                         StudentSearchResults)
    dataset = load_dataset(str(dataset_path))
    retrieved = {r.question_id: r.retrieved_sources
                 for r in results.search_results}
    questions = [q for q in dataset.rag_questions
                 if isinstance(q, AnsweredQuestion) and q.sources]
    if not questions:
        raise RagError(f"{dataset_path}: no tiene preguntas con fuentes")
    for k in (1, 3, 5, 10):
        if k > results.k:
            break
        total = sum(question_recall(retrieved.get(q.question_id, []),
                                    q.sources, k) for q in questions)
        print(f"Recall@{k}: {total / len(questions):.3f}")
