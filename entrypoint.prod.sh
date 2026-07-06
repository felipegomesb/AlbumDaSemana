#!/bin/sh
set -e

# Collect static files and run migrations (non-interactive)
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Garante que a musica do dia ja esteja definida ao iniciar
python manage.py rotacionar_musica || true

# Start Gunicorn; use exec so it receives signals from Docker (PID 1)
exec gunicorn albumDaSemana.wsgi:application \
	--bind 0.0.0.0:8000 \
	--workers 3 \
	--access-logfile - \
	--error-logfile -