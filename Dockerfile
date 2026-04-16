FROM python:3.11-slim
WORKDIR /app
COPY listener.py /app/listener.py
RUN pip install requests
CMD ["python", "listener.py"]
