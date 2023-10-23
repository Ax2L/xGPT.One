#!/bin/bash

# Determine OS
OS="$(uname -s)"

# Function to check if wtfutil is installed
is_wtfutil_installed() {
    if command -v wtfutil &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to install wtfutil on macOS
install_mac() {
    if ! is_wtfutil_installed; then
        echo "Installing wtfutil on macOS..."
        if ! brew install wtfutil; then
            echo "Error: Failed to install wtfutil on macOS."
            exit 1
        fi
    else
        echo "wtfutil is already installed. Checking for updates..."
        if ! brew upgrade wtfutil; then
            echo "Error: Failed to update wtfutil on macOS."
            exit 1
        fi
    fi
}

# Function to install wtfutil on Linux
install_linux() {
    # Check if wtfutil is installed
    if ! is_wtfutil_installed; then
        echo "Installing wtfutil on Linux..."
        # You can add Linux specific installation steps here.
        # For instance, if you wanted to use a package manager like apt:
        # sudo apt-get update
        # sudo apt-get install -y wtfutil
        # Note: As of my last training, there's no direct apt package for wtfutil.
        # You might need to fetch binaries or build from source.

        # Placeholder error for demonstration
        echo "Error: Installation method for Linux not specified."
        exit 1
    else
        echo "wtfutil is already installed on Linux."
        # If there's an update mechanism for Linux, you can implement it here.
    fi
}

# Start wtfutil with config
start_wtfutil() {
    if ! is_wtfutil_installed; then
        echo "Error: wtfutil is not installed."
        exit 1
    fi
    wtfutil --config=config.yml
}

# Determine OS and Install or Update
case "${OS}" in
    Darwin*)    install_mac ;;
    Linux*)     install_linux ;;
    *)          echo "Error: Unsupported OS" ;;
esac

# Start wtfutil
start_wtfutil
