#!/usr/bin/env sh
gunicorn wsgi:application -D -c ./misc/gunicorn.py
