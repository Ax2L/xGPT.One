#!/bin/bash

# Define the specific name or keyword to search for
NAME_KEYWORD="my_keyword" # Modify this as per your need

# Function to handle errors
handle_error() {
    echo "🔴 Error Alert: $1 🔴"
    echo "🚨 Aborting. 🚨"
    exit 1
}

# Delete containers with the specified name
echo "Deleting containers with name containing '$NAME_KEYWORD'..."
container_ids=$(docker ps -a --filter "name=$NAME_KEYWORD" -q)
if [ -n "$container_ids" ]; then
    docker rm -f $container_ids || handle_error "Deleting containers failed"
else
    echo "No containers found with name containing '$NAME_KEYWORD'."
fi

# Delete images with the specified name
echo "Deleting images with name containing '$NAME_KEYWORD'..."
image_ids=$(docker images --filter "reference=$NAME_KEYWORD" -q)
if [ -n "$image_ids" ]; then
    docker rmi -f $image_ids || handle_error "Deleting images failed"
else
    echo "No images found with name containing '$NAME_KEYWORD'."
fi

# Delete volumes with the specified name
echo "Deleting volumes with name containing '$NAME_KEYWORD'..."
volume_ids=$(docker volume ls --filter "name=$NAME_KEYWORD" -q)
if [ -n "$volume_ids" ]; then
    docker volume rm $volume_ids || handle_error "Deleting volumes failed"
else
    echo "No volumes found with name containing '$NAME_KEYWORD'."
fi

# Delete networks with the specified name
echo "Deleting networks with name containing '$NAME_KEYWORD'..."
network_ids=$(docker network ls --filter "name=$NAME_KEYWORD" -q)
if [ -n "$network_ids" ]; then
    docker network rm $network_ids || handle_error "Deleting networks failed"
else
    echo "No networks found with name containing '$NAME_KEYWORD'."
fi

# Deleting Docker build cache
echo "Deleting Docker build cache..."
docker builder prune -af || handle_error "Deleting build cache failed"

# Deleting all unused (dangling) images, containers, and volumes
echo "Deleting all unused data..."
docker system prune -af || handle_error "Deleting all unused data failed"

# Delete networks with the specified name
echo "Deleting networks with name containing '$NAME_KEYWORD'..."
network_ids=$(docker network ls --filter "name=$NAME_KEYWORD" -q)
if [ -n "$network_ids" ]; then
    docker network rm $network_ids || handle_error "Deleting networks failed"
else
    echo "No networks found with name containing '$NAME_KEYWORD'."
fi


# Execute main.sh
echo "Executing main.sh..."
chmod +x main.sh || handle_error "Making main.sh executable failed"
./main.sh || handle_error "Executing main.sh failed"

echo "Done! All operations successful."
