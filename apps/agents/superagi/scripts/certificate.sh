#!/bin/bash

# Install Certbot
sudo snap install --classic certbot
sudo systemctl stop nginx

# Generate SSL certificates
declare -a domains=("superagi.xGPT.one")

for domain in "${domains[@]}"; do
    sudo certbot certonly --standalone -d "$domain" --staple-ocsp --agree-tos -m vsewolodschmidt@gmail.com
done

sudo systemctl restart nginx


