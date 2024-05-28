#!/bin/bash

# Start PostgreSQL
service postgresql start

# Start Nginx
service nginx start

# Start Gunicorn
cd /EPIC-Recommender
. venv/bin/activate
gunicorn --workers 3 --bind 0.0.0.0:8000 epicrproje.wsgi:application
