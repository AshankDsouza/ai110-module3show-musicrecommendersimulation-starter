#!/usr/bin/env bash
set -euo pipefail

# Start PostgreSQL in the background.
docker compose up --build -d db ollama

# Pull the model inside the Ollama container for reproducibility across machines.
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
export OLLAMA_MODEL
echo "Ensuring Ollama model is available in container: ${OLLAMA_MODEL}"
docker compose exec -T ollama ollama pull "${OLLAMA_MODEL}"

# Run one-shot loader and wait for it to finish.
docker compose up --build load-data

# Run the app inside Docker so the full workflow is reproducible and the output
# streams directly into this terminal.
docker compose run --rm app python -m src.main

# cleanup
docker compose down -v

