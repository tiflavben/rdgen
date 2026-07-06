#!/bin/bash
cd /opt/rdgen
source .venv/bin/activate
# Load secrets
if [ -f .env_secrets ]; then
    export $(grep -v '^#' .env_secrets | xargs)
fi
# Start gunicorn with env vars
exec gunicorn -c gunicorn.conf.py rdgen.wsgi:application
