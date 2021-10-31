FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py
ENV OFFSET="500"

CMD ["sh", "-c", "python3 /code/main.py $MONGO_HOST $OFFSET"]