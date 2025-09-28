FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

RUN apt-get update

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
