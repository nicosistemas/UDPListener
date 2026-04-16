FROM python:3.11-slim

WORKDIR /app

COPY listener-minilog .

RUN pip install --no-cache-dir requests

CMD ["python", "listener-minilog.py"]
