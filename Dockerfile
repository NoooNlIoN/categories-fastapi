FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.lock .
COPY pyproject.toml .

RUN pip install --no-cache-dir -r requirements.lock

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
alembic upgrade head\n\
echo "Starting application..."\n\
python src/main.py\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
