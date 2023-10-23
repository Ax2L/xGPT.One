#!/bin/bash
# fast-ssh.sh

# Function to install fast-ssh
install_fast_ssh() {
    echo "Installing fast-ssh..."

    # Detect the operating system
    os_type="$(uname -s)"
    
    case "${os_type}" in
        Linux*)
            asset_name="fast-ssh-v.*-x86_64-unknown-linux-gnu.tar.gz"
            ;;
        Darwin*)
            asset_name="fast-ssh-v.*-x86_64-apple-darwin.tar.gz"
            ;;
        *)
            echo "Unsupported OS type: ${os_type}"
            return 1
            ;;
    esac

    # Download the appropriate fast-ssh version based on detected OS
    curl -s https://api.github.com/repos/Julien-R44/fast-ssh/releases/latest |
        grep "browser_download_url.*${asset_name}" |
        cut -d : -f 2,3 |
        tr -d \" |
        wget -qi -
        
    tar xzf fast-ssh*.tar.gz
    sudo cp fast-ssh /usr/local/bin/  # Using /usr/local/bin as it's more standard for macOS
    rm fast-ssh*.tar.gz
}

# Function to initialize SSH Config file if not exists
init_ssh_config() {
    echo "Checking SSH Config File..."
    ssh_config_file="$HOME/.ssh/config"
    if [ ! -f "$ssh_config_file" ]; then
        mkdir -p ~/.ssh
        touch ~/.ssh/config
        chmod 600 ~/.ssh/config
        echo "Creating example SSH Config File..."
        cat <<EOL > ~/.ssh/config
Host *
    UpdateHostKeys yes

Host Desktop
    HostName 192.168.1.10
    User YourCoolUsername
EOL
        echo "SSH Config File created at: $ssh_config_file"
    else
        echo "SSH Config File already exists at: $ssh_config_file"
    fi
}

# Check if fast-ssh is already installed
if ! command -v fast-ssh &>/dev/null; then
    install_fast_ssh
else
    echo "fast-ssh already installed."
fi

# Initialize SSH Config File if needed
init_ssh_config

# Run fast-ssh
echo "Launching fast-ssh..."
fast-ssh
