#!/bin/bash
source venv/bin/activate
gunicorn --access-logfile - -b 0.0.0.0:80 main:app --daemon
