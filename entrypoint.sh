#!/bin/sh

echo "Esperando a PostgreSQL..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL disponible."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"