#!/bin/bash

build_docker_compose() {
  load_env
  echo "Generating docker-compose.yml..."
  python3 $PROJECT_DIR/scripts/build_docker-compose.yml.py || {
    echo "Failed to build docker-compose.yml"
    exit 1
  }
}