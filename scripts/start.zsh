#!/bin/zsh

set -e
# Get .env
source .env

#docker run --rm --name bedello_postgres -d -v $(pwd)/db_vol:/var/lib/postgresql/data -e POSTGRES_PASSWORD=bedello1234 -e POSTGRES_USER=bedello_app -e POSTGRES_DB=bedello -d -p 5432:5432 postgres:12-alpine
#pg_isready --dbname=bedello --host=localhost --username=bedello_app --

# Load python environment
echo "Starting docker db container..."
cd app
poetry run uvicorn main:app --reload
