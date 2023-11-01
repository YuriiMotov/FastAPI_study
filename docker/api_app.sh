#!/bin/bash

alembic upgrade head

cd src

python init_db.py

gunicorn main:api_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000