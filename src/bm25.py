from collections import Counter
from typing import Dict, List, Tuple
import math

from lexical import tokenize

Postings = Dict[str, List[Tuple[int, int]]]


def build_postings(documents: List[List[str]]) -> Tuple[Postings, List[int]]:
    """Índice invertido y longitud de cada documento.

    documents[i] es la lista de palabras del chunk i.
    """
    postings: Postings = {}
    lengths: List[int] = []
    for doc_id, words in enumerate(documents):
        lengths.append(len(words))
        for word, count in Counter(words).items():
            postings.setdefault(word, []).append((doc_id, count))
    return postings, lengths


def idf(df: int, n_docs: int) -> float:
    """Peso de una palabra que aparece en df de los n_docs documentos"""
    return math.log(1 + ((n_docs) - df + 0.5) / (df + 0.5))


def search(query: str, postings: Postings, lengths: List[int], k: int,
           k1: float = 1.5, b: float = 0.75) -> List[Tuple[int, float]]:
    """Los k chunks con mayor puntuación BM25 para la pregunta."""
    question_set = set(tokenize(query))
    if not lengths or k <= 0:
        return []
    n_docs = len(lengths)
    avgdl = sum(lengths) / n_docs
    scores: Dict[int, float] = {}
    for word in question_set:
        if word not in postings:
            continue
        weight = idf(len(postings[word]), n_docs)
        for doc_id, tf in postings[word]:
            norm = k1 * (1 - b + b * lengths[doc_id] / avgdl)
            score = weight * tf * (k1 + 1) / (tf + norm)
            scores[doc_id] = scores.get(doc_id, 0.0) + score
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ranked[:k]
