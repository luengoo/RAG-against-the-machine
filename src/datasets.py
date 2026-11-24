from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from src.errors import RagError
from src.models import RagDataset


M = TypeVar("M", bound=BaseModel)


def load_model(path: str, model: Type[M]) -> M:
    """Lee un fichero JSON y lo valida con el modelo pydantic dado."""
    if not path:
        raise RagError("Falta la ruta del fichero")
    try:
        with open(path, encoding="utf-8") as f:
            return model.model_validate_json(f.read())
    except FileNotFoundError as exc:
        raise RagError(f"{path}: el fichero no existe") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise RagError(f"{path}: no se puede leer ({exc})") from exc
    except ValidationError as exc:
        raise RagError(
            f"{path}: no tiene el formato de {model.__name__}") from exc


def load_dataset(path: str) -> RagDataset:
    """Lee un fichero de preguntas y lo valida como RagDataset."""
    return load_model(path, RagDataset)


def save_json(model: BaseModel, path: Path) -> None:
    """Guarda un modelo pydantic como JSON, creando la carpeta."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=2))
    except OSError as exc:
        raise RagError(f"{path}: no se puede escribir ({exc})") from exc
