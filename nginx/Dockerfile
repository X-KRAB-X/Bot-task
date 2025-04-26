FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /etc/nginx/sites-enabled/
RUN mkdir /etc/nginx/ssl

COPY andrey-bokarev.ru /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/andrey-bokarev.ru /etc/nginx/sites-enabled/andrey-bokarev.ru

RUN mkdir -p /var/www/certbot


FROM base

RUN apt-get update && apt-get install -y certbot python3-certbot-nginx

ENV DOMAIN='andrey-bokarev.ru'
ENV EMAIL='gagamen2004@gmail.com'

RUN certbot --nginx \
    -d ${DOMAIN} \
    -m ${EMAIL} \
    --non-interactive \
    --agree-tos

EXPOSE 80 443
