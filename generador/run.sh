#!/bin/bash
kill `pgrep -f 'generador' -o`
source venv/bin/activate
gunicorn --access-logfile - -b 0.0.0.0:5001 main:app --daemon
