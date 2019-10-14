#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py check_zcashd --wait 20
gunicorn --bind=0.0.0.0:8000 --workers=2 zfaucet.wsgi

