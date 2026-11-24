from typing import List

from src.models import MinimalSource


IOU_THRESHOLD = 0.05


def question_recall(retrieved: List[MinimalSource],
                    expected: List[MinimalSource], k: int) -> float:
    """Fracción de las fuentes esperadas encontradas en los k primeros."""
    if not expected:
        return 0.0
    found = sum(
        any(iou(r, e) >= IOU_THRESHOLD for r in retrieved[:k])
        for e in expected
    )
    return found / len(expected)


def iou(a: MinimalSource, b: MinimalSource) -> float:
    """IoU de dos fuentes (0 si son de ficheros distintos)."""
    if a.file_path != b.file_path:
        return 0.0
    intersection = (min(a.last_character_index, b.last_character_index)
                    - max(a.first_character_index, b.first_character_index))
    if intersection <= 0:
        return 0.0
    union = (max(a.last_character_index, b.last_character_index)
             - min(a.first_character_index, b.first_character_index))
    return intersection / union
