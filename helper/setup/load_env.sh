#!/bin/bash

load_env() {
  echo "Load Environment File .env"
  cp ".env" "$PROJECT_DIR/.env" || true  

  if [ -f "$PROJECT_DIR/.env" ]; then
    echo "🔄 Loading environment variables..."
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
  else
    echo "🔴 No .env file found. 🔴"
  fi
}