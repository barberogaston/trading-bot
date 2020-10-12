FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app
COPY . .
RUN pip install -r trading_bot/app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "trading_bot.app.main:app", "--reload", "--host", "0.0.0.0"]