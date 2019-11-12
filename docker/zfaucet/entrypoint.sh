#!/bin/bash

set -e

python docker/zfaucet/wait_for.py --host db --port 5432 --timeout 60
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py check_zcashd --wait 240
python manage.py healthcheck
gunicorn --bind=0.0.0.0:8000 --workers=2 zfaucet.wsgi

