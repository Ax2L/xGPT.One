#!/bin/bash

#// region [ rgba(0, 100, 250, 0.05)] Initialization
# Check if docker-compose.yml is not available
if [ ! -f docker-compose.yml ]; then
    # Download the file using wget
    wget https://github.com/milvus-io/milvus/releases/download/v2.3.1/milvus-standalone-docker-compose.yml -O docker-compose.yml
fi
#// endregion

#// region [ rgba(0, 100, 250, 0.05)] Run Docker Compose
# Run the docker-compose file
docker-compose up -d
#// endregion

