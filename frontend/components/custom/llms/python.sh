#!/bin/bash

# Function to purge Python and related packages
function purge_python {
    echo "Purging Python..."
    if command -v brew &>/dev/null; then
        brew uninstall --ignore-dependencies python python@3.10 python@2
        brew cleanup
    else
        echo "Homebrew package manager is required for purging. Exiting..."
        exit 1
    fi
    echo "Python purged successfully."
}

# Function to install Python 3.11.5 and set it as the default
function install_python_3_11_5 {
    desired_python_version="3.11.5"
    
    # Check if Python 3.11.5 is already installed
    if python3 --version | grep -qF "$desired_python_version"; then
        echo "Python $desired_python_version is already installed."
    else
        echo "Installing Python $desired_python_version..."
        if command -v brew &>/dev/null; then
            brew install python@$desired_python_version
            if [ $? -eq 0 ]; then
                echo "Python $desired_python_version installed successfully."
            else
                echo "Error installing Python $desired_python_version."
                exit 1
            fi
        else
            echo "Homebrew package manager is required for installation. Exiting..."
            exit 1
        fi
    fi

    # Set Python 3.11.5 as the default
    sudo ln -sf /usr/local/bin/python$desired_python_version /usr/local/bin/python
    sudo ln -sf /usr/local/bin/python$desired_python_version /usr/local/bin/python3

    # Display the active Python version
    active_python_version=$(python --version 2>&1 | awk '{print $2}')
    echo "Active Python version: $active_python_version"

    # Install and upgrade pip for Python 3.11.5
    if ! command -v pip$desired_python_version &>/dev/null; then
        echo "Installing pip for Python $desired_python_version..."
        python$desired_python_version -m ensurepip
    fi

    # Upgrade pip to the latest version
    pip$desired_python_version install --upgrade pip
    echo "Python version switched to $desired_python_version."
}

# Display the menu
while true; do
    echo "Menu:"
    echo "1. [ Purge Python ]"
    echo "2. [ Install 3.11.5 ]"
    echo "3. [ E ]xit"

    read -rp "Select an option: " choice

    case "$choice" in
    1)
        purge_python
        ;;
    2)
        install_python_3_11_5
        ;;
    3 | [eE])
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option. Please select a valid option."
        ;;
    esac
done
