FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8000
WORKDIR /app/trading_bot/app/
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]