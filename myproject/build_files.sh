#!/bin/bash
echo "==> Building Dependencies..."
python3 -m pip install -r requirements.txt

echo "==> Gathering Static Files..."
python3 manage.py collectstatic --noinput --clear