FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY Pipfile* /code/
RUN pip install pipenv && set -ex && pipenv install --deploy --system
COPY . /code/
