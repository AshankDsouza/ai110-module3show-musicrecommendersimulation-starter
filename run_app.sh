#!/usr/bin/env bash
set -euo pipefail

# Load local secrets/config if present (kept out of git).
if [[ -f .env.local ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env.local
  set +a
fi

# Start PostgreSQL in the background.
docker compose up --build -d db ollama

# Pull the model inside the Ollama container for reproducibility across machines.
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
echo "Ensuring Ollama model is available in container: ${OLLAMA_MODEL}"
docker compose exec -T ollama ollama pull "${OLLAMA_MODEL}"

# Run one-shot loader and wait for it to finish.
docker compose up --build load-data

# Install local Python dependencies and run the app.
python3 -m pip install -r requirements.txt

# Default to local Ollama endpoint unless overridden.
export OPENAI_BASE_URL="${OPENAI_BASE_URL:-http://localhost:11434/v1}"
export OPENAI_MODEL="${OPENAI_MODEL:-${OLLAMA_MODEL}}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-ollama}"

python3 -m src.main

# cleanup
docker compose down -v

