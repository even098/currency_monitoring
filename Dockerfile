# Dockerfile
FROM python:3.11-slim

WORKDIR .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "bot/main.py"]
CMD ["celery", "-A", "currency_monitoring", "worker", "--loglevel=info"]
CMD ["celery", "-A", "currency_monitoring", "beat", "--loglevel=info"]