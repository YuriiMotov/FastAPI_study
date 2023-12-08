#!/bin/bash

cd src

if [ -d /tmp_multiproc ]; then rm -Rf /tmp_multiproc; fi
mkdir /tmp_multiproc

gunicorn main:web_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000