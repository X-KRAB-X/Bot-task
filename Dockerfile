FROM ubuntu:jammy

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /Bot-task

# Установка всех утилит
RUN apt-get update 

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-pip 
    #nginx \
    #postgresql 


# Настройка зависимостей
COPY requirements.txt requirements.txt
COPY bot ./bot
COPY nginx ./nginx
COPY .env .env

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

