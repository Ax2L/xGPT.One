#!/bin/bash

run_docker() {
  load_env
  wait
  echo "Creating Docker network..."
  docker network create xgpt || {
    echo "Docker network exists or failed to create"
  }
  echo "Running/Updating Production..."
  cd $PROJECT_DIR/apps/xgpt/docker || {
  cp $PROJECT_DIR/apps/xgpt/.env $PROJECT_DIR/apps/xgpt/docker/.env || true
    echo "Failed to change directory to apps/xgpt/"
    exit 1
  }
  docker-compose up -d || {
    echo "Failed to run Docker"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Production running/updating successfully."
}