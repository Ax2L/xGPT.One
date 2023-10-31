#!/bin/bash

run_local_assist() {
    echo "🔄 Running local Assistant..."

    # Navigate to the directory
    cd $PROJECT_DIR/apps/assistant/build/

    # Execute the commands
    /opt/homebrew/bin/yarn install
    /opt/homebrew/bin/yarn dev

    # Return to the original directory
    cd -
    echo "✅ Local Assistant is running!"
}
