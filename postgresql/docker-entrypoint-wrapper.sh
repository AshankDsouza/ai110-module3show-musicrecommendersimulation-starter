#!/bin/sh
set -eu

export POSTGRES_DB="${POSTGRES_DB:-music_recommender}"
export POSTGRES_USER="${POSTGRES_USER:-postgres}"
export POSTGRES_HOST_AUTH_METHOD="${POSTGRES_HOST_AUTH_METHOD:-trust}"

exec /usr/local/bin/docker-entrypoint.sh postgres
