FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app


USER appuser

EXPOSE 5000

CMD [
  "gunicorn",
  "--config",
  "gunicorn.conf.py",
  "--bind",
  "0.0.0.0:5000",
  "--workers",
  "2",
  "--access-logfile",
  "-",
  "--error-logfile",
  "-",
  "wsgi:app"
]