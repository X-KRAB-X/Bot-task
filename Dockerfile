FROM python:3.12.6

WORKDIR /Bot-task

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY bot ./bot
COPY .env .env
