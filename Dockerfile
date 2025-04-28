FROM ubuntu:jammy

WORKDIR /Bot-task

# Установка всех утилит
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nginx \
    postgresql 


# Настройка зависимостей
COPY requirements.txt requirements.txt
COPY bot ./bot
COPY nginx ./nginx
COPY .env .env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

