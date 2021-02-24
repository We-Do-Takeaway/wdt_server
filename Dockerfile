FROM python:3.9

WORKDIR /app

RUN pip install poetry

COPY ./manage.py .
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./scripts ./scripts
COPY ./wdt ./wdt

RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev

CMD ["scripts/start.sh"]
