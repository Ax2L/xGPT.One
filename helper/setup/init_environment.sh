#!/bin/bash

init_environment() {
  if [ -f "$LOCK_FILE" ]; then
    echo "Init script is already running. Please wait..."
    return
  fi
  touch "$LOCK_FILE"
  echo "Initiating environment..."
  "$PROJECT_DIR/init.sh" & 
  wait
  rm "$LOCK_FILE"
  echo "Environment initiated successfully."
}