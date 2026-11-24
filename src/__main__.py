import sys

import fire

from src.commands_search import index, search_dataset, search
from src.errors import RagError
from src.commands_search import evaluate


def main() -> int:
    """Lanza la CLI y convierte los errores esperados en mensajes."""
    try:
        fire.Fire({"index": index, "search": search,
                   "search_dataset": search_dataset,
                   "evaluate": evaluate}, name="python -m src")
    except RagError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
