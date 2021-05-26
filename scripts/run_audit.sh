#!/usr/bin/env bash

set -e

poetry run mypy app tests --show-error-codes 
poetry run black app tests --check --line-length 120
poetry run isort --check-only app tests

/Users/nicolas/.homebrew/bin/flake8 app tests
#poetry run flake8 app tests
echo "Flake Done"

