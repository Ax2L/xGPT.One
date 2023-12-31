#!/bin/bash

run_local_dev() {
  # load_env
  echo "Running local dev..."
  cd frontend || true
  pwd || true
  
  # Run the Python script to generate CSS
  poetry run python components/style/cssgen.py || true

  poetry run streamlit run main.py --theme.base="dark" || true
  echo "Local dev running successfully."
}