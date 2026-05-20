# Dockerfile multi-stage — Guardian Agent
# Stage 1: build / install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime (minimal image)
FROM python:3.11-slim AS runtime

RUN groupadd -r guardian && useradd -r -g guardian -d /app -s /sbin/nologin guardian

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY engine.py .
COPY casos_prueba.md .
COPY guardia_api.py .
COPY guardian_client.py .
COPY test_engine.py .
COPY validar_conexion.py .

RUN chown -R guardian:guardian /app && chmod -R 550 /app && chmod 770 /app

USER guardian

ENV PYTHONUNBUFFERED=1
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY}

CMD ["sh", "-c", "python guardian_client.py && python -m pytest test_engine.py -v --tb=short 2>&1 | tee resultados.txt"]
