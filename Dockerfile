FROM python:3.6

COPY requirements-py3.txt requirements.txt

RUN set -ex &&\
    apt-get update && apt-get install -y virtualenv &&\
    pip install --upgrade -r requirements.txt
