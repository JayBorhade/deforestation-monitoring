#!/bin/bash
set -e

# run alembic migrations
if command -v alembic >/dev/null 2>&1; then
  echo "Running alembic upgrade head..."
  alembic upgrade head
else
  echo "alembic not installed"
fi

# start the API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
