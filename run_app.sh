#!/usr/bin/env bash
set -euo pipefail

# Start PostgreSQL in the background.
docker compose up --build -d db

# Run one-shot loader and wait for it to finish.
docker compose up --build load-data

# Install local Python dependencies and run the app.
python3 -m pip install -r requirements.txt
python3 -m src.main