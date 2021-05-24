FROM python:3.8-slim-buster

WORKDIR /stock-prediction

COPY .version setup.py start.py gunicorn.conf.py ./
COPY app ./app

RUN pip install .

CMD [ "gunicorn", "-c" , "gunicorn.conf.py", "app:create_app()"]
