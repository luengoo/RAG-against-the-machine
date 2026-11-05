from src.models import MinimalSource


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
