FROM python:latest


RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        python3-psycopg2 \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pipenv

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system
RUN pip install psycopg2-binary gunicorn

COPY . /app
