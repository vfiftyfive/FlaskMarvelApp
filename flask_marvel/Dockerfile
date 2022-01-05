FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
ENV MONGO_HOST="172.17.0.2"

CMD ["gunicorn", "--conf", "app/gunicorn_conf.py", "--bind", "0.0.0.0:80", "app.main:app"]