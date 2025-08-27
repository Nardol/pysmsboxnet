# Repository Guidelines

## Project Structure & Module Organization

- `src/pysmsboxnet/`: Library code — `api.py` (async `Client`), `exceptions.py`, `_version.py` (generated), `py.typed`.
- `tests/`: Pytest suite (async via `pytest-asyncio`), e.g., `tests/test_api.py`.
- `docs/`: Sphinx sources; build to `docs/_build/html`.
- `scripts/`: Helper scripts, e.g., `run-in-env.sh` for type-checking in the active venv.
- `example.py`: Minimal usage; reads `SMSBOX_API_KEY` from the environment.

## Build, Test, and Development Commands

- Setup: `uv sync --group lint --group test --group doc` (Python ≥ 3.11).
- Lint/format: `uv run pre-commit run --all-files` (ruff, ruff-format, codespell, etc.).
- Type-check: `uv run mypy src/pysmsboxnet`.
- Test: `uv run pytest` or a single test `uv run pytest tests/test_api.py::test_ok`.
- Coverage: `uv run pytest --cov=./src --cov-report=term-missing`.
- Build package: `uv build`.
- Build docs: `uv run make -C docs html`.

## Coding Style & Naming Conventions

- Indentation: 4 spaces; use type hints everywhere (`py.typed` is shipped).
- Linting/formatting: Ruff (checks + import order), ruff-format via pre-commit. Long lines are allowed; most docstring rules apply.
- Naming: snake_case for functions/variables, PascalCase for classes, exceptions suffixed with `Exception` (see `exceptions.py`).
- Public APIs should include concise docstrings and logging where helpful.

## Testing Guidelines

- Frameworks: `pytest`, `pytest-asyncio` (strict mode), `aresponses` for HTTP mocking.
- Location/names: put tests in `tests/`, files `test_*.py`, functions `test_*`.
- Async tests: mark with `@pytest.mark.asyncio` and prefer `aiohttp.ClientSession` per examples.
- Coverage: aim to keep/improve coverage; `_version.py` and `__init__.py` are excluded in Codecov.

## Commit & Pull Request Guidelines

- Commits: follow Conventional Commits (e.g., `feat:`, `fix:`, `refactor:`, `chore(deps):`).
- PRs: provide a clear description, link related issues, include tests/docs updates, and note behavior changes.
- Before opening: run `uv run pre-commit run -a` and `uv run pytest`; ensure CI parity locally.

## Security & Configuration Tips

- Secrets: never commit keys. Use `SMSBOX_API_KEY` via environment (see `example.py`).
- Network calls: reuse an injected `aiohttp.ClientSession`; do not create global sessions.
- Logging: never log API keys or tokens; add log redaction for sensitive fields when configuring logging.
- Prevention: enable secret scanning in pre-commit (e.g., `detect-secrets` or `gitleaks`) and rotate any exposed keys immediately.
