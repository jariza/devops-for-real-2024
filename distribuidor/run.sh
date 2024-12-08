#!/bin/bash
kill `pgrep -f 'distribuidor' -o`
source venv/bin/activate
gunicorn --access-logfile - -b 0.0.0.0:80 main:app --daemon
