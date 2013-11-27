#!/usr/bin/env sh
source venv/bin/activate
gunicorn wsgi:application -D -c ./misc/gunicorn.py
echo "Don't forget to update global_var.styl"
deactivate
