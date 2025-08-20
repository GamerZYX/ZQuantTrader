FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir nicegui==2.4.0 httpx==0.27.0

COPY app.py ./app.py

EXPOSE 3000

CMD ["python", "app.py"]


