import re
from typing import List

WORD_RE = r"[A-Za-z0-9_]+"
CAMEL_RE = r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z0-9]+|[A-Z0-9]+"
MIN_PIECE = 3
STOPWORDS = {
    "a", "an", "the", "is", "are", "be", "how", "what", "which", "when",
    "where", "why", "do", "does", "can", "i", "in", "of", "to", "for",
    "and", "or", "with", "on", "by", "it", "its", "this", "that", "from",
    "as", "at", "vllm",
}


def split_identifier(word: str) -> List[str]:
    """Piezas de un identificador snake_case o camelCase (sin minúsculas)."""
    pieces: List[str] = []
    for part in word.split("_"):
        pieces.extend(re.findall(CAMEL_RE, part))
    return pieces


def tokenize(text: str) -> List[str]:
    """Convierte un texto en la lista de palabras que se comparan."""
    tokens: List[str] = []
    for word in re.findall(WORD_RE, text):
        lowered = word.lower()
        if lowered in STOPWORDS:
            continue
        tokens.append(lowered)
        pieces = split_identifier(word)
        if pieces != [word]:
            for piece in pieces:
                piece = piece.lower()
                if len(piece) >= MIN_PIECE and piece not in STOPWORDS:
                    tokens.append(piece)
    return tokens
