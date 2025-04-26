FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /etc/nginx/sites-enabled/

COPY andrey-bokarev.ru /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/andrey-bokarev.ru /etc/nginx/sites-enabled/andrey-bokarev.ru
RUN nginx

RUN mkdir -p /var/www/certbot

RUN apt-get update && apt-get install -y certbot python3-certbot-nginx

ENV DOMAIN='andrey-bokarev.ru'
ENV EMAIL='gagamen2004@gmail.com'

RUN certbot --nginx \
    -d ${DOMAIN} \
    -m ${EMAIL} \
    --non-interactive \
    --agree-tos

RUN mkdir -p /etc/nginx/ssl

RUN ln -s /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /etc/nginx/ssl/fullchain.pem && \
    ln -s /etc/letsencrypt/live/${DOMAIN}/privkey.pem /etc/nginx/ssl/privkey.pem

EXPOSE 80 443
