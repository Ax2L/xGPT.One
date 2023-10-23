#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <container_id> <image_name>"
    exit 1
fi

# Get the container ID and image name from command-line arguments
container_id="$1"
image_name="$2"

# Commit the container to a new image
new_image_name="${image_name}:latest"
docker commit "$container_id" "$new_image_name"

# Push the image to the registry
docker push "$new_image_name"

# Check if the push was successful
if [ $? -eq 0 ]; then
    echo "Image '$new_image_name' has been successfully pushed to the registry."
else
    echo "Failed to push image '$new_image_name' to the registry."
    exit 1
fi

# Optionally, you can clean up the local image after pushing it
docker rmi "$new_image_name"

exit 0
