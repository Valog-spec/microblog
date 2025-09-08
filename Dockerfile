# Этап 1: Сборочный этап
FROM python:3.12-slim AS builder

# Create a working directory /src for the source code and /venv for the virtual environment
WORKDIR /src/

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for installing dependencies
COPY pyproject.toml pdm.lock README.md ./

# Install PDM and manually create a virtual environment in /venv
RUN pip install pdm \
    && python -m venv /venv \
    && . /venv/bin/activate \
    && pdm install --production

# Stage 2: Final Stage
FROM python:3.12-slim

# Working directory for the application /src
WORKDIR /src/

# Copy the installed virtual environment from the first stage into /venv
COPY --from=builder /venv /venv

# Copy the rest of the application files into /src
COPY . .

# Set environment variables to activate the virtual environment and add PYTHONPATH
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH="/src"

WORKDIR /src/app
EXPOSE 8080


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]