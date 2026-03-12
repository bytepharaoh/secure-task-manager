#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
RUN_SERVER=true

usage() {
    cat <<'EOF'
Usage: ./scripts/bootstrap.sh [options]

Options:
  --no-runserver    Prepare the project but do not start Django's dev server
  --host HOST       Host for runserver (default: 127.0.0.1)
  --port PORT       Port for runserver (default: 8000)
  -h, --help        Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-runserver)
            RUN_SERVER=false
            shift
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

cd "$ROOT_DIR"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Error: $PYTHON_BIN is not available in PATH." >&2
    exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment in $VENV_DIR"
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [[ ! -f .env ]]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
fi

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check

if [[ "$RUN_SERVER" == true ]]; then
    exec python manage.py runserver "${HOST}:${PORT}"
fi

echo "Bootstrap completed successfully."
