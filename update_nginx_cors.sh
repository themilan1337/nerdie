#!/bin/bash

# Обновление nginx конфигурации для добавления CORS заголовков
# Запустите на сервере: bash update_nginx_cors.sh

cat > /etc/nginx/sites-available/nerdie.conf << 'NGINX_CONF'
server {
    listen 80;
    server_name auth.nerdie.lol;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name auth.nerdie.lol;

    ssl_certificate /etc/letsencrypt/live/auth.nerdie.lol/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/auth.nerdie.lol/privkey.pem;

    location / {
        # CORS headers
        add_header 'Access-Control-Allow-Origin' $http_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' $http_origin always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

server {
    listen 80;
    server_name rag.nerdie.lol;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name rag.nerdie.lol;

    ssl_certificate /etc/letsencrypt/live/auth.nerdie.lol/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/auth.nerdie.lol/privkey.pem;

    location / {
        # CORS headers
        add_header 'Access-Control-Allow-Origin' $http_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' $http_origin always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

server {
    listen 80;
    server_name ingest.nerdie.lol;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name ingest.nerdie.lol;

    ssl_certificate /etc/letsencrypt/live/auth.nerdie.lol/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/auth.nerdie.lol/privkey.pem;

    location / {
        # CORS headers
        add_header 'Access-Control-Allow-Origin' $http_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' $http_origin always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
NGINX_CONF

echo "✅ Nginx configuration updated!"
echo ""
echo "Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Configuration is valid. Reloading nginx..."
    systemctl reload nginx
    echo "✅ Nginx reloaded successfully!"
    echo ""
    echo "CORS should now work for:"
    echo "  - https://auth.nerdie.lol"
    echo "  - https://rag.nerdie.lol"
    echo "  - https://ingest.nerdie.lol"
else
    echo ""
    echo "❌ Configuration has errors. Please check the output above."
    echo "The old configuration has NOT been changed."
fi
