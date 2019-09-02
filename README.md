# flask-auth-for-raspi
Very simple password authentication server for nginx

Nginx の設定例

```
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

http {
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
    upstream auth {
        server 127.0.0.1:4900;
    }

    server {
        listen *:80;
        server_name example.com;
        auth_request /auth;

        location = /auth {
            internal;
            proxy_pass http://auth;
            proxy_pass_request_body off;
            proxy_set_header Content-Length "";
        }

        location = /login {
            auth_request off;
            proxy_pass http://auth;
        }

        error_page 401 = @error401;

        location @error401 {
            return 302 http://$http_host/login;
        }

    }
}
```

