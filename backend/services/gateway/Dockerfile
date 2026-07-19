# Build context is backend/services (see docker-compose.yml) so the shared
# common/ package can be copied alongside the gateway's own source.
FROM python:3.12-slim

# Unbuffered stdout/stderr so `docker compose logs` shows output in real time.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common/ ./common/
COPY gateway/src/ ./src/

RUN adduser --disabled-password --gecos "" appuser
USER appuser

CMD ["python", "-m", "src.main"]
