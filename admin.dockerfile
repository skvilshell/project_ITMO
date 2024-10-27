FROM python:3.6

WORKDIR /app

COPY ./admin_main.py ./
COPY ./admin_modules.py ./

CMD [ "python", "admin_main.py" ]