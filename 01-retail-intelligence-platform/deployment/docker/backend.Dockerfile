FROM python:3.12.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080

WORKDIR /app

COPY backend/api/requirements-lock.txt /tmp/requirements-lock.txt
RUN python -m pip install --no-cache-dir --requirement /tmp/requirements-lock.txt

COPY backend ./backend
COPY data/processed/demand-insight ./data/processed/demand-insight
COPY reports ./reports
COPY deployment/docker/start-backend.py ./deployment/docker/start-backend.py

RUN addgroup --system --gid 10001 app \
    && adduser --system --uid 10001 --ingroup app --no-create-home app

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8080') + '/health', timeout=3)"

CMD ["python", "deployment/docker/start-backend.py"]
