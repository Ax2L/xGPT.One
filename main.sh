#!/bin/bash

#*
#* ╔══════════════════════════════════════════════════════════════════════════╗
#* ║                             🚀 xGPT.One                                  ║
#* ║     Unleash the Power of AI with Unprecedented Accessibility             ║
#* ╟──────────────────────────────────────────────────────────────────────────╢
#* ║ Script Name    : main.sh                                                 ║
#* ║ Description    : Main script to manage and control the AI project        ║
#* ║ Author         : [V.S]                                                   ║
#* ║ Version        : [0.0.6]                                                 ║
#* ╟──────────────────────────────────────────────────────────────────────────╢
#* ║ Additional Details                                                       ║
#* ║ - Ensure environment is set correctly before running the script          ║
#* ╚══════════════════════════════════════════════════════════════════════════╝
#*

#* ==============================================
#*                VARIABLES
#* ==============================================
PROJECT_DIR=$(pwd)
export PROJECT_DIR
LOCK_FILE="$PROJECT_DIR/init.lock"
GITHUB_LINK="https://github.com/Ax2L/xGPT.One"

# poetry shell || true

#* ==============================================
#*                FUNCTIONS
#* ==============================================
source $PROJECT_DIR/helper/setup/display_header.sh
source $PROJECT_DIR/helper/setup/clean_docker.sh
source $PROJECT_DIR/helper/setup/init_environment.sh
source $PROJECT_DIR/helper/setup/load_env.sh
source $PROJECT_DIR/helper/setup/build_docker_compose.sh
source $PROJECT_DIR/helper/setup/build_docker.sh
source $PROJECT_DIR/helper/setup/run_docker.sh
source $PROJECT_DIR/helper/setup/run_local_dev.sh
source $PROJECT_DIR/helper/setup/run_local_db.sh
source $PROJECT_DIR/helper/setup/run_local_assist.sh


reset_postgres() {
    echo "🔄 Resetting Postgres..."
    # Navigate to the directory containing the docker-compose file
    cd $PROJECT_DIR/helper/docker/xgpt-one/

    # Stop and remove the postgres container
    docker-compose -f docker-compose-postgres.yaml down -v --remove-orphans && \
    docker-compose -f docker-compose-postgres.yaml rm -fsv postgres && \
    docker volume prune -f

    # Redeploy the postgres container as a daemon
    docker-compose -f docker-compose-postgres.yaml up -d postgres

    # Return to the original directory
    cd -
    echo "✅ Postgres reset complete!"
}

initiate_postgres() {
    echo "🔄 Initiating Postgres tables..."
    cd $PROJECT_DIR/frontend/components/
    # Call the create_tables() function from the Python script
    python "xinit_db.py"
    echo "✅ Tables initiated in Postgres!"
}


# Additional Functions
build_assistant() {
    echo "🔄 Building Assistant Docker container..."
    docker build -t xgpt-assistant -f $PROJECT_DIR/apps/assistant/build/Dockerfile .
    echo "✅ Assistant Docker container built successfully!"
}

restart_assistant() {
    echo "🔄 Restarting Assistant..."
    cd $PROJECT_DIR/apps/assistant/build/
    
    # Deleting the old container
    docker-compose -f docker-compose.yaml down

    # Rerun docker-compose up
    docker-compose -f docker-compose.yaml up -d

    # Return to the original directory
    cd -
    echo "✅ Assistant restarted successfully!"
}

#* ==============================================
#*                SETUP
#* ==============================================

# ####################################### #
#    DO NOT MODIFY THIS FILE DIRECTLY     #
#     Use .env for all configurations     #
# ####################################### #

poetry env use `which python3.11` || true
. .venv/bin/activate || true
# Init .env
if [ ! -f ".env" ]; then
    cp env-template .env || true
fi
cp .env docker/.env || true
cp -r config/streamlit frontend/.streamlit || true
source .env || handle_error "Activating AI Environment Failed"

#* ==============================================
#*                MAIN EXECUTION
#* ==============================================
# Main execution
while true; do
    display_header "Main Menu"

    # Menu Options
    echo "║ [1] Run/Update Production"
    echo "║ [2] Build Image"
    echo "║ [3] Developer-Menu"
    echo "║ [4] Clean Docker"
    [ ! -f "$LOCK_FILE" ] && echo "║ [5] Initiate Environment"
    echo "║ [E]xit"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"

    read -r -p "Your choice: " choice

    case "$choice" in
    1) run_docker ;;
    2) build_docker ;;
    3)
        while true; do
            display_header "Developer Menu"
            echo "║ [1] Run Local Dev"
            echo "║ [2] Run Local DB"
            echo "║ [3] Run Local Assistant"
            echo "║ [4] Show FastAPI"
            echo "║ [5] Restart FastAPI"
            echo "║ [6] Stop FastAPI"
            echo "║ [7] Reset Postgres"
            echo "║ [8] initiate postgres"
            echo "║ [9] Build Assistant"
            echo "║ [10] Restart Assistant"
            echo "║ [E]xit"
            echo "╚════════════════════════════════════════════════════════════════════════╝"
            read -r -p "Developer choice: " dev_choice
            case "$dev_choice" in
            1) run_local_dev ;;
            2) run_local_db ;;
            3) run_local_assist ;;
            4) show_fastapi ;;
            5) restart_fastapi ;;
            6) stop_fastapi ;;
            7) reset_postgres ;;
            8) initiate_postgres ;;
            9) build_assistant ;;
            10) restart_assistant ;;
            E|e) break ;;
            *) echo "🔴 Invalid choice. Please try again. 🔴" ;;
            esac
        done
        ;;
    4) clean_docker ;;
    5) [ ! -f "$LOCK_FILE" ] && init_environment || echo "Init is already running." ;;
    E|e) 
        echo "👋 Exiting... See you next time in the AI universe! 👋"
        exit 0
        ;;
    *) echo "🔴 Invalid choice. Please try again. 🔴" ;;
    esac
done
