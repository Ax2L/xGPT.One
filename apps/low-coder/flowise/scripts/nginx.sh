#!/bin/bash

# Specify the domain
domain="flowise.xgpt.one"

# Create Nginx configuration file
config_file="/etc/nginx/conf.d/${domain}.conf"

echo "Creating Nginx configuration file: ${config_file}"

# Nginx configuration template
config_template=$(cat << EOF
server {
        listen 80;
        server_name $domain;
        return 301 https://$host$request_uri;
}


server {
        listen 443 ssl http2;
        server_name $domain;
        ssl_certificate /etc/letsencrypt/live/$domain/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/$domain/privkey.pem;

        access_log /var/log/nginx/$domain.access.log;
        error_log /var/log/nginx/$domain.error.log;
        add_header Strict-Transport-Security "max-age=63072000; preload";
        add_header X-Frame-Options DENY;
        client_max_body_size 250M;

        # use it if you would like to prohibit access to everyone running a public vm
        # satisfy any;
        #allow your ip adress /32;
        #allow allow 172.25.0.0/24;
        # deny all;
        # use it for having a http auth secured login
        #auth_basic "Please Login";
        #auth_basic_user_file ssl/.htpasswd;

location / {
        proxy_pass http://localhost:3600/;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}

EOF
)

# Write the configuration to the file
echo "$config_template" | sudo tee "$config_file" > /dev/null

# Test the Nginx configuration
sudo nginx -t

# Reload Nginx to apply changes
sudo systemctl reload nginx
