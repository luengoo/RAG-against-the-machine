SGOINFRE ?= /sgoinfre/students/$(USER)
STORE    := $(SGOINFRE)/rag_against_the_machine
ENV_VARS := UV_PROJECT_ENVIRONMENT UV_CACHE_DIR UV_PYTHON_INSTALL_DIR \
            HF_HOME UV_LINK_MODE

ifneq ($(wildcard $(SGOINFRE)),)
export UV_PROJECT_ENVIRONMENT := $(STORE)/.venv
export UV_CACHE_DIR           := $(STORE)/uv-cache
export UV_PYTHON_INSTALL_DIR  := $(STORE)/uv-python
export HF_HOME                := $(STORE)/huggingface
export UV_LINK_MODE           := copy
endif

ifneq ($(wildcard $(SGOINFRE)),)
UV_BIN_DIR ?= $(STORE)/bin
else
UV_BIN_DIR ?= $(HOME)/.local/bin
endif
UV := $(or $(shell command -v uv 2>/dev/null),$(UV_BIN_DIR)/uv)
UV_INSTALLER := https://astral.sh/uv/install.sh

.PHONY: all install run debug clean fclean lint lint-strict env

all: run

$(UV_BIN_DIR)/uv:
	@echo "uv no está instalado: instalándolo en $(UV_BIN_DIR)"
	@mkdir -p $(UV_BIN_DIR)
	@if command -v curl >/dev/null 2>&1; then \
		curl -LsSf $(UV_INSTALLER); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -qO- $(UV_INSTALLER); \
	else \
		echo "echo 'Error: hace falta curl o wget para instalar uv' >&2; exit 1"; \
	fi | env UV_INSTALL_DIR="$(UV_BIN_DIR)" UV_NO_MODIFY_PATH=1 sh
	@test -x $@ || { echo "Error: no se pudo instalar uv en $@" >&2; exit 1; }

install: $(UV)
	@[ ! -d "$(SGOINFRE)" ] || mkdir -p $(STORE)
	$(UV) sync

run: $(UV)
	$(UV) run python -m src

debug: $(UV)
	$(UV) run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

fclean: clean
	rm -rf .venv $(STORE)

lint: $(UV)
	$(UV) run flake8 . && \
	$(UV) run mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

lint-strict: $(UV)
	$(UV) run flake8 . && $(UV) run mypy . --strict

# Uso: eval "$$(make -s env)"   (también añade uv al PATH de tu terminal)
env:
	@$(foreach v,$(ENV_VARS),echo 'export $(v)=$($(v))';)
	@echo 'export PATH=$(dir $(UV)):$$PATH'
