#!/bin/bash

echo "Starting Git LFS installation..."

# Determine OS
OS="$(uname)"

case $OS in
"Darwin")
    echo "Detected macOS."
    # For MacOS
    echo "Navigating to git-lfs.github.com to download..."
    curl -L -O "https://github.com/git-lfs/git-lfs/releases/download/v2.13.3/git-lfs-darwin-amd64-v2.13.3.tar.gz"
    echo "Unzipping the downloaded file..."
    tar -zxvf git-lfs-darwin-amd64-v2.13.3.tar.gz
    echo "Changing directory to the unzipped folder..."
    cd git-lfs-2.13.3
    echo "Installing..."
    sudo ./install.sh
    ;;
"Linux")
    echo "Detected Linux."
    # For Linux
    echo "Navigating to git-lfs.github.com to download..."
    curl -L -O "https://github.com/git-lfs/git-lfs/releases/download/v2.13.3/git-lfs-linux-amd64-v2.13.3.tar.gz"
    echo "Unzipping the downloaded file..."
    tar -zxvf git-lfs-linux-amd64-v2.13.3.tar.gz
    echo "Changing directory to the unzipped folder..."
    cd git-lfs-2.13.3
    echo "Installing..."
    sudo ./install.sh
    ;;
"WindowsNT")
    echo "Windows is not supported by this shell script."
    ;;
*)
    echo "Unknown OS detected."
    ;;
esac

# Verify the installation
if [ "$OS" = "Darwin" ] || [ "$OS" = "Linux" ]; then
    echo "Verifying the installation..."
    git lfs install
    echo "Git LFS installation completed."
else
    echo "Installation not performed due to unknown OS or unsupported platform."
fi
