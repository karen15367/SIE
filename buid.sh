#!/usr/bin/env bash
# exit on error

ser -o errexit

#poetry install

pip install -r requirements.txt
pip install --upgrade pip

python manage.py collectstatic --no--input
python manage.py migrate