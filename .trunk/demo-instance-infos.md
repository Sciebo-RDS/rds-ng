# Addresses

- URL: https://sciebo-rds-ncpoc.uni-muenster.de
- Externe IP: 128.176.196.30
- Interne IP: 128.176.136.4

# Config Frontend

```
[network.client]
server_address = "https://sciebo-rds-ncpoc.uni-muenster.de:9001"

[frontend]
authentication_scheme = "host"
host_api_url = "https://sciebo-rds-ncpoc.uni-muenster.de/apps/rdsng/api/"
```

## Config NGINX

```
server {
        listen 443 default_server ssl;
        listen [::]:443 default_server ssl;

        include snippets/server-cert.conf;
        include snippets/ssl-params.conf;

        server_name sciebo-rds-ncpoc.uni-muenster.de;

        location / {
                proxy_pass http://localhost:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_hide_header X-Frame-Options;
                proxy_read_timeout 10m;
                proxy_send_timeout 10m;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}

server {
        listen 80;
        listen [::]:80;

        return 301 https://sciebo-rds-ncpoc.uni-muenster.de$request_uri;
}

server {
        listen 9000 ssl;
        listen [::]:9000 ssl;

        include snippets/server-cert.conf;
        include snippets/ssl-params.conf;

        server_name rds;

        location / {
                proxy_pass http://localhost:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_hide_header X-Frame-Options;
                proxy_read_timeout 10m;
                proxy_send_timeout 10m;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}

server {
        listen 9001 ssl;
        listen [::]:9001 ssl;

        include snippets/server-cert.conf;
        include snippets/ssl-params.conf;

        server_name rdsbe;

        location / {
                proxy_pass http://localhost:4200;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
        }
}
```
