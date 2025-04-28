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

# Настройка БД
RUN echo "host all all 127.0.0.1/32 trust" >> /etc/postgresql/14/main/pg_hba.conf

RUN service postgresql start && sleep 5
# RUN service postgresql status && sleep 5
RUN ls -l "/var/log/postgresql" %% sleep 10

RUN psql createuser -s bot_user
RUN psql createdb bot_local_base -O bot_user

# Копирование файлов
COPY requirements.txt requirements.txt
COPY bot ./bot
COPY nginx ./nginx
COPY GH ./GH

# Настройка nginx
RUN ln -s ./nginx/nginx-bot-webhook-proxy /etc/nginx/sites-enabled
# Копирование Let's Encrypt сертификатов
RUN mkdir /etc/nginx/ssl && \ 
    cp ./nginx/certs/fullchain.pem /etc/nginx/ssl \
    cp ./nginx/certs/privkey.pem /etc/nginx/ssl

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск
ENTRYPOINT service postgresql start && service nginx start && python3 ./bot/main.py
