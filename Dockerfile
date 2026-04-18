FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r services/api_gateway/requirements.txt

ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn services.api_gateway.main:app --host 0.0.0.0 --port ${PORT:-8000}"]