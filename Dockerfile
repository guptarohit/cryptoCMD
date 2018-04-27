FROM python:3.6.5-slim-jessie

ADD requirements.txt /usr/src/requirements.txt
WORKDIR /usr/src
RUN pip install -r requirements.txt && pip install pandas cryptocmd

ADD . /usr/src
