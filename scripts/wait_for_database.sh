#!/usr/bin/env bash
set -e +x

RETRIES=10

# Waiting for the the server to listen on the port is not enough as
# database commands will fail while the database server is starting up
until RESULT=$(python -c "from psycopg2 import connect; connect('$DATABASE_URL').close()" 2>&1) || [ $RETRIES -eq 0 ]; do
  echo "Waiting for successful PostgreSQL connection, $((RETRIES--)) remaining attempts..."
  sleep 3
done

if [ "$RETRIES" -eq "0" ]; then
  echo "$RESULT"
  echo "PostgreSQL connection failed"
  exit 1
fi

exit 0
