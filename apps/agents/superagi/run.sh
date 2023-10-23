#!/bin/bash

# Load configurations from x.conf
RepoName=$(awk -F "=" '/RepoName/ {print $2}' config/x.conf)
RepoURL=$(awk -F "=" '/RepoURL/ {print $2}' config/x.conf)
Branch=$(awk -F "=" '/Branch/ {print $2}' config/x.conf)
AppPath=$(awk -F "=" '/AppPath/ {print $2}' config/x.conf)
TempRepoPath=$(awk -F "=" '/TempRepoPath/ {print $2}' config/x.conf)
SSLPath=$(awk -F "=" '/SSLPath/ {print $2}' config/x.conf)
NginxConfig=$(awk -F "=" '/NginxConfig/ {print $2}' config/x.conf)

# Step 1: Clone or update the GitHub repository
cd /tmp
if [ -d "$RepoName" ]; then
    cd "$RepoName"
    git pull origin "$Branch"
else
    git clone "$RepoURL"
    cd "$RepoName"
fi

# Step 2: Copy configurations and check certificate validity
cd "$AppPath"
cp docker/config.yaml "$TempRepoPath/config.yaml"
cp -r docker/* "$TempRepoPath/"

# Verify SSL certificate
if ! openssl x509 -checkend 0 -noout -in "$SSLPath"; then
    ./scripts/certificate.sh || true
fi

# Step 3: Update nginx.conf if necessary
if ! cmp -s config/nginx.conf "$NginxConfig"; then
    systemctl stop nginx
    cp "$AppPath/config/nginx.conf" "$NginxConfig"
    systemctl restart nginx
fi

# Step 4: Execute Docker commands
cd "$TempRepoPath"
docker-compose up -d
docker-compose logs









## Old:
#// # Step 1: Clone or update the GitHub repository
#// cd /tmp
#// if [ -d "SuperAGI" ]; then
#// cd SuperAGI
#// git pull origin master
#// else
#// git clone https://github.com/TransformerOptimus/SuperAGI
#// cd SuperAGI
#// fi
#// 
#// # Step 2: Copy config.yaml and check certificate validity
#// cd /opt/xGPT-One/apps/superagi
#// cp docker/config.yaml /tmp/SuperAGI/config.yaml 
#// cp -r docker/* /tmp/SuperAGI/ 
#// 
#// # Check if certificate is valid
#// if ! openssl x509 -checkend 0 -noout -in /etc/letsencrypt/live/superagi.xgpt.one/fullchain.pem; then
#// # Execute certificate.sh if certificate is not valid
#// ./scripts/certificate.sh || true
#// fi
#// 
#// # Step 3: Update nginx.conf if necessary
#// if ! cmp -s config/nginx.conf /etc/nginx/conf.d/superagi.xgpt.one.conf; then
#// # Stop nginx
#// systemctl stop nginx
#// 
#// # Update $fqdn.conf
#// cp /opt/xGPT-One/apps/superagi/config/nginx.conf /etc/nginx/conf.d/superagi.xgpt.one.conf
#// 
#// # Restart nginx
#// systemctl restart nginx
#// fi
#// 
#// # Step 4: Execute "docker-compose up -d" and show logs
#// cd /tmp/SuperAGI
#// docker-compose up -d
#// docker-compose logs
##