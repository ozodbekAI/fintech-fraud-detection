#!/bin/sh
uvicorn app.main:app --host 0.0.0.0 --port 8080 &
python -m faststream run worker/consumer.py:app --host 0.0.0.0 &
wait