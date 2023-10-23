#!/bin/bash

#// region [ rgba(0, 100, 250, 0.05)] HEADER

# Print the header
print_header() {
cat << "EOF"
+------------------------------------------------------------------+
|             #####  ######  #######     #######                   |
|     #    # #     # #     #    #        #     # #    # ######     |
|      #  #  #       #     #    #        #     # ##   # #          |
|       ##   #  #### ######     #        #     # # #  # #####      |
|       ##   #     # #          #    ### #     # #  # # #          |
|      #  #  #     # #          #    ### #     # #   ## #          |
|     #    #  #####  #          #    ### ####### #    # ######     |
|                                                                  |
|               🤖 AI Powered. Human Inspired. 🌍                  |
|                                                                  |
|           GitHub: https://github.com/Ax2L/xGPT.One               |
|                                                                  |
+------------------------------------------------------------------+
EOF
}
#// endregion


# Determine platform, OS, and location.
determine_platform() {
    UNAME=$(uname | tr "[:upper:]" "[:lower:]")
    case $UNAME in
    'linux')
        PLATFORM='linux'
        ;;
    'darwin')
        PLATFORM='macos'
        ;;
    *)
        echo "Unknown platform $UNAME"
        exit 1
        ;;
    esac
    export PLATFORM
}

# Check for Homebrew on macOS and install it if not present
check_homebrew() {
    if [[ $PLATFORM == 'macos' ]]; then
        if ! command -v brew >/dev/null 2>&1; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
    fi
}

# Check and install Python 3.11, Go, and Git
install_dependencies() {
    echo "Checking and installing dependencies..."
    
    if [[ $PLATFORM == 'linux' ]]; then
        # Linux
        sudo apt update
        command -v python3.11 >/dev/null 2>&1 || { sudo apt install -y python3.11; }
        command -v go >/dev/null 2>&1 || { sudo apt install -y golang-go; }
        command -v git >/dev/null 2>&1 || { sudo apt install -y git; }
    elif [[ $PLATFORM == 'macos' ]]; then
        # macOS
        brew install python@3.11
        brew install go
        brew install git
        if ! brew list docker >/dev/null 2>&1; then
            brew install docker
        fi
        if ! brew list docker-compose >/dev/null 2>&1; then
            brew install docker-compose
        fi
    fi
}
#// endregion

#// region [ rgba(200, 200, 0, 0.05)] PTERM_INSTALLATION
install_pterm() {
    echo "Installing PTerm library..."
    if [ ! -f "go.mod" ]; then
        go mod init tempmodule
    fi
    go get -u github.com/pterm/pterm
}
#// endregion

#// region [ rgba(100, 100, 100, 0.05)] SCRIPT_EXECUTION
print_header
determine_platform
check_homebrew
install_dependencies

# Check if Go is installed, if not, install it
command -v go >/dev/null 2>&1 || { install_go; }

# Check if PTerm is installed, if not, install it
if ! go list -m github.com/pterm/pterm >/dev/null 2>&1; then
    install_pterm;
fi

# Check for main.go before running it
if [ -f "helper/setup/main.go" ]; then
    go run helper/setup/main.go
else
    echo "main.go file not found!"
fi

#// endregion