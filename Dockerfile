FROM python:3.12

WORKDIR /app

COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000
