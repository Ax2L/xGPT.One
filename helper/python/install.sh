#!/bin/bash

# Define the desired Python version
desired_python_version="3.11"  # Change this to your desired version

# Check if the desired Python version is already installed
if ! command -v python$desired_python_version &>/dev/null; then
    echo "Python $desired_python_version is not installed. Installing..."
    
    # Use your package manager to install Python (e.g., brew)
    if command -v brew &>/dev/null; then
        brew install python@$desired_python_version
    else
        echo "Homebrew package manager is required. Please install Python $desired_python_version manually."
        exit 1
    fi
    
    if [ $? -eq 0 ]; then
        echo "Python $desired_python_version installed successfully."
    else
        echo "Error installing Python $desired_python_version."
        exit 1
    fi
else
    echo "Python $desired_python_version is already installed."
fi

# Set the desired Python version as the default (macOS)
sudo ln -sf /usr/local/bin/python$desired_python_version /usr/local/bin/python

# Display the active Python version
active_python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Active Python version: $active_python_version"

# Optional: Install pip for the desired Python version
if ! command -v pip$desired_python_version &>/dev/null; then
    echo "Installing pip for Python $desired_python_version..."
    python$desired_python_version -m ensurepip
fi

# Optional: Upgrade pip to the latest version
pip$desired_python_version install --upgrade pip

echo "Python version switched to $desired_python_version."
