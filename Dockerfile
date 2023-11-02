FROM python:3.10

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

WORKDIR /fastapi_app/src

CMD gunicorn main:api_app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000