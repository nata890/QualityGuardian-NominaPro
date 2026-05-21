# Dockerfile multi-stage — Guardian Agent
# Stage 1: build / install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
COPY infra/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime (minimal image)
FROM python:3.11-slim AS runtime

RUN groupadd -r guardian && useradd -r -g guardian -d /app -s /sbin/nologin guardian

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src/engine.py src/engine.py
COPY src/guardia_api.py src/guardia_api.py
COPY src/guardian_client.py src/guardian_client.py
COPY src/__init__.py src/__init__.py
COPY tests/test_engine.py tests/test_engine.py
COPY scripts/validar_conexion.py scripts/validar_conexion.py
COPY .env .env

RUN chown -R guardian:guardian /app && chmod -R 550 /app && chmod 770 /app

USER guardian

ENV PYTHONUNBUFFERED=1
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY}

CMD ["sh", "-c", "python src/guardian_client.py && python -m pytest tests/test_engine.py -v --tb=short 2>&1 | tee resultados.txt"]
