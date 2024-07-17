#!/bin/sh
source venv/bin/activate
exec gunicorn -b :5050 --access-logfile - --error-logfile - app --timeout 300
