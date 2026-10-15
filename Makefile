UV          = uv
PYTHON_MAIN = python -m src

.PHONY: all install run check test debug clean fclean lint lint-strict

all: run

# Crea .venv en la carpeta del proyecto e instala las dependencias.
install:
	$(UV) sync

# De momento solo comprueba que el paquete arranca; cambiará cuando
# existan los comandos (index, search...).
run:
	$(UV) run $(PYTHON_MAIN)

# Script de comprobación de los modelos (paso 1).
check:
	$(UV) run python -m tests.check_models

test:
	$(UV) run pytest -q

debug:
	$(UV) run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

fclean: clean
	rm -rf .venv

lint:
	$(UV) run flake8 . --exclude .venv && \
	$(UV) run mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV) run flake8 . --exclude .venv && $(UV) run mypy . --strict
