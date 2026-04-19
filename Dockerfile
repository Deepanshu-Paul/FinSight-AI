FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r services/api_gateway/requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "services.api_gateway.main:app", "--host", "0.0.0.0", "--port", "10000"]