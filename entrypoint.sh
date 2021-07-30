#!/bin/sh

while ! nc -z db 5432
do
  echo sleeping...
  sleep 0.1
done
flask db upgrade

exec "$@"