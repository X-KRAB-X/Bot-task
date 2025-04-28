FROM ubuntu:jammy

# Логи
ENV PYTHONUNBUFFERED=1

# Временная зона во избежание ошибок
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /Bot-task

# Установка всех утилит
RUN apt-get update 

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    nginx \
    postgresql postgresql-client 

# Копирование файлов
COPY requirements.txt requirements.txt
COPY bot ./bot
COPY nginx ./nginx
COPY GH ./GH

# Настройка nginx
RUN ln -s ./nginx/nginx-bot-webhook-proxy /etc/nginx/sites-enabled/nginx-bot-webhook-proxy
# Копирование Let's Encrypt сертификатов
RUN mkdir /etc/nginx/ssl
RUN cp ./nginx/certs/fullchain.pem /etc/nginx/ssl/fullchain.pem
RUN cp ./nginx/certs/privkey.pem /etc/nginx/ssl/privkey.pem

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN nginx -t

# Запуск
ENTRYPOINT service nginx restart && python3 ./bot/main.py
