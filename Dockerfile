# Этап 1: Сборочный этап
FROM python:3.12-slim AS builder

WORKDIR /src/

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pdm.lock README.md ./

RUN pip install pdm \
    && python -m venv /venv \
    && . /venv/bin/activate \
    && pdm install --production

# Stage 2: Final Stage
FROM python:3.12-slim

WORKDIR /src/

COPY --from=builder /venv /venv

COPY . .

ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH="/src"

WORKDIR /src/app
EXPOSE 8080


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]