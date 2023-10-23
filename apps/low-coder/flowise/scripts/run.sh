#!/bin/bash

# Define a list of Docker container names to stop, remove, and delete images
containers=("flowise")

for container in "${containers[@]}"; do
    # Stop the container
    sudo docker stop "$container" || True

    # Remove the container
    sudo docker rm "$container" || True

    # Delete the associated image
    sudo docker image rm "$(sudo docker inspect -f '{{.Image}}' "$container")" || True
done

# Pull repo 
git pull

echo "Cleanup complete!"

# Copy .env to platform/ and next/
cp .env docker/.env || True

# Build the container
sudo docker build --no-cache -t flowise .

# Update the container using docker-compose
cd ./docker

sudo docker-compose up -d

echo "Build underway!"

cd ..