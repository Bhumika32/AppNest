#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD"

ACTION=${1:-upgrade}
if [ "$ACTION" = "upgrade" ]; then
  python -m alembic upgrade head
elif [ "$ACTION" = "stamp" ]; then
  python -m alembic stamp head
else
  echo "Unknown action: $ACTION"
  exit 1
fi
