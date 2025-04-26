FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY andrey-bokarev.ru /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/andrey-bokarev.ru /etc/nginx/sites-enabled/

RUN apt-get update && apt-get install -y certbot python3-certbot-nginx

ENV DOMAIN='andrey-bokarev.ru'
ENV EMAIL='gagamen2004@gmail.com'

RUN mkdir /etc/nginx/ssl

RUN certbot --nginx \
    -d ${DOMAIN} \
    -m ${EMAIL} \
    --non-interactive \
    --agree-tos

RUN ln -s /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /etc/nginx/ssl/fullchain.pem && \
    ln -s /etc/letsencrypt/live/${DOMAIN}/privkey.pem /etc/nginx/ssl/privkey.pem

EXPOSE 80 443
