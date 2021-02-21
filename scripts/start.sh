#!/usr/bin/env bash
set -xe

GUNICORN_ACCESS_LOG_FORMAT='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s %({X-Forwarded-For}i)s'
WEB_CONCURRENCY=${WEB_CONCURRENCY:-4}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

${BASH_SOURCE%/*}/wait_for_database.sh
python ./manage.py migrate --noinput

if [[ -n "$DEV" ]]; then
  python ./manage.py loaddata
fi

gunicorn wdt.wsgi --access-logfile - --access-logformat "$GUNICORN_ACCESS_LOG_FORMAT" --bind="$HOST:$PORT"
