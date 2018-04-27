LABEL maintainer="mestdagh.tom@gmail.com"
FROM python:3.6.5-slim-jessie

COPY . /usr/src
WORKDIR /usr/src
RUN pip install -r requirements.txt && pip install pandas cryptocmd
