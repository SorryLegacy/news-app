FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock alembic.ini /app/

RUN poetry install --no-root --no-dev

COPY app/ /app/app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["sh", "-c", "poetry run alembic upgrade head && cd app/ && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
