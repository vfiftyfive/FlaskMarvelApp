FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py
ENV OFFSET="700"
ENV API_PRIVATE_KEY="2ff768c5567a1e2035dcef735e2be04e7af86daa"

CMD ["sh", "-c", "python3 /code/main.py $MONGO_HOST $OFFSET"]