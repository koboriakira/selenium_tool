FROM python:3.11-slim-buster

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN \
  pip install -r requirements.txt
