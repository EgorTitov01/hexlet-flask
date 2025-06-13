#!/usr/bin/env bash

set -e

service postgresql start

until su postgres -c "pg_isready"; do
  echo "Waiting for postgres..."
  sleep 2
done

su postgres -c "psql -a -d hexlet -f init.sql"

make prod
