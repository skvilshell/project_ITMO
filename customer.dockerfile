FROM python:3.6

WORKDIR /app

COPY ./customers_main.py ./
COPY ./customers_modules.py ./

CMD [ "python", "admin_main.py" ]