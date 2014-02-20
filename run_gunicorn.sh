#!/usr/bin/env sh
source venv/bin/activate
gunicorn wsgi:application -D -c ./misc/gunicorn.py
deactivate
