#!/bin/sh
exec gunicorn -b :5050 --workers 1 --access-logfile - --error-logfile - app --timeout 600
