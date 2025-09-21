FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/start.sh
COPY start.sh .

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 && python -m faststream run worker/consumer.py:app --host 0.0.0.0