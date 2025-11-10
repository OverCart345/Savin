FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
