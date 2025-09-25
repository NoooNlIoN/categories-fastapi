FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.lock .
COPY pyproject.toml .

RUN pip install --no-cache-dir -r requirements.lock

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY start.sh .

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
