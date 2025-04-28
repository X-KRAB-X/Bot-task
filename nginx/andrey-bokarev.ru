server {
        server_name andrey-bokarev.ru www.andrey-bokarev.ru;

        location /webhook {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-NginX-Proxy true;
        }

        error_log /var/log/nginx/andrey-bokarev.ru_error.log;
        access_log /var/log/nginx/andrey-bokarev.ru_access.log;

    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/fullchain.pem; 
    ssl_certificate_key /etc/nginx/ssl/privkey.pem; 
}

server {
    if ($host = www.andrey-bokarev.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = andrey-bokarev.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

        listen 80;
        server_name andrey-bokarev.ru www.andrey-bokarev.ru;
    return 404; # managed by Certbot
}
