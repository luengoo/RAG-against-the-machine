"""Prueba rápida: construir el índice y medir el recall@5."""

import time

from src.bm25 import build_postings, search
from src.corpus import chunk_corpus, scoring_text
from src.evaluation import iou
from src.lexical import tokenize
from src.models import AnsweredQuestion, RagDataset
from src.indexer import load_texts


def main() -> None:
    """Construye el índice y prueba las preguntas de docs y de código."""
    start = time.time()
    chunks = chunk_corpus("data/raw", 2000)
    texts = load_texts([c.file_path for c in chunks])
    documents = [tokenize(scoring_text(c, texts[c.file_path]))
                 for c in chunks]
    postings, lengths = build_postings(documents)
    print(f"Índice: {len(chunks)} chunks, {len(postings)} palabras, "
          f"{time.time() - start:.1f}s")

    for name in ("docs", "code"):
        path = f"data/datasets/AnsweredQuestions/dataset_{name}_public.json"
        with open(path, encoding="utf-8") as f:
            dataset = RagDataset.model_validate_json(f.read())
        found = 0
        total = 0
        for q in dataset.rag_questions:
            if not isinstance(q, AnsweredQuestion):
                continue
            total += 1
            ref = q.sources[0]
            for doc_id, _score in search(q.question, postings, lengths, 5):
                if iou(chunks[doc_id].to_source(), ref) >= 0.05:
                    found += 1
                    break
        print(f"{name}: {found}/{total} preguntas con la fuente en el top 5")


if __name__ == "__main__":
    main()
