upstream bot {
    server bot:8000;
}

server {
        server_name andrey-bokarev.ru www.andrey-bokarev.ru;

        location /webhook {
                proxy_pass http://bot;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-NginX-Proxy true;
        }

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        error_log /var/log/nginx/andrey-bokarev.ru_error.log;
        access_log /var/log/nginx/andrey-bokarev.ru_access.log;


    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/andrey-bokarev.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/andrey-bokarev.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf; 
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; 


}

server {
    listen 80;
    server_name andrey-bokarev.ru www.andrey-bokarev.ru;
    return 301 https://$host$request_uri;
}
