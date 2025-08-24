FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
RUN prisma generate

COPY .env.production .env

EXPOSE 3100

CMD ["gunicorn", "--bind", "0.0.0.0:3100", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker"]