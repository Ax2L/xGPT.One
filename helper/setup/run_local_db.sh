#!/bin/bash
# helper/setup/run_local_db.sh

FASTAPI_SCREEN_SESSION="fastapi_session"

# Functions to manage FastAPI process
show_fastapi() {
  echo "Attaching to FastAPI screen session..."
  screen -r $FASTAPI_SCREEN_SESSION
}

restart_fastapi() {
  echo "Restarting FastAPI..."
  # Sending Ctrl+C to the screen session to stop FastAPI
  screen -X -S $FASTAPI_SCREEN_SESSION kill
  # Giving it some time to gracefully shutdown
  sleep 2
  # Starting FastAPI within the screen session
  screen -S $FASTAPI_SCREEN_SESSION -X stuff "poetry run start$(printf \\r)"
}


stop_fastapi() {
  echo "Stopping FastAPI..."
  # Sending Ctrl+C to the screen session to stop FastAPI
  screen -X -S $FASTAPI_SCREEN_SESSION kill
}

wait_for_url_and_port() {
  echo "Waiting for $MILVUS_HOST:$MILVUS_PORT..."
  while ! nc -z $MILVUS_HOST $MILVUS_PORT; do   
    sleep 0.1 # sleep for 100ms before check again
  done
  echo "$MILVUS_HOST:$MILVUS_PORT is available."
}

run_local_db() {
  load_env
  echo "Running local db..."
  docker-compose -f helper/docker/xgpt-one/docker-compose-db.yaml up -d || {
    echo "Failed to run local db"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Local db running successfully."
  wait_for_url_and_port
  
  # Check if a screen session named $FASTAPI_SCREEN_SESSION exists
  if screen -list | grep -q "$FASTAPI_SCREEN_SESSION"; then
    echo "FastAPI screen session already exists."
  else
    echo "Creating a new screen session for FastAPI..."
    # Creating a detached screen, executing FastAPI within
    screen -S $FASTAPI_SCREEN_SESSION -dm bash -c "poetry run start; exec sh"
    echo "FastAPI is now running in a screen session named $FASTAPI_SCREEN_SESSION."
  fi
}
