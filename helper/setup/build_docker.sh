#!/bin/bash

build_docker() {
  load_env
  echo "Building Docker Image..."
  pwd || {
    echo "Failed to change directory to apps/xgpt/"
    exit 1
  }
  docker build -f $PROJECT_DIR/apps/xgpt/docker/Dockerfile . -t "xgpt-streamlit" || {
    echo "Failed to build Docker image"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Docker image built successfully."
}