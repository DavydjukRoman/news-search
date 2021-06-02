FROM python:3.9
RUN python -m pip install -U pip

RUN mkdir app
COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app
