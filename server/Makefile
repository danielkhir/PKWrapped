run:
	uv run fastapi dev app/main.py

lint:
	uv run ruff check

format:
	uv run ruff check --select I --fix && \
	uv run ruff format

fetch: data/moves.json data/species.json
	uv run scripts/etl_metadata.py
