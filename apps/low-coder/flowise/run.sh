#!/bin/bash

# Navigate to docker directory to run the docker-compose commands
cd docker

# Build and run docker-compose
docker-compose down
docker-compose build
docker-compose up -d
