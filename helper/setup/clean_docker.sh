
#!/bin/bash

clean_docker() {
  echo "Cleaning up Docker..."
  sh $PROJECT_DIR/helper/clean/cleanDocker_and_run.sh || {
    echo "Failed to clean Docker"
  }
  echo "Docker cleaned successfully."
}