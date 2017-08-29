FROM python:2.7-alpine

RUN apk add --update \
    gcc \
    libc-dev \
    linux-headers

WORKDIR /app
ENV HOME /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY runserver.py runserver.py
EXPOSE 5050
