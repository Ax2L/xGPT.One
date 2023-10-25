#!/bin/bash

run_local_assist() {
    echo "🔄 Running local Assistant..."

    # Navigate to the directory
    cd $PROJECT_DIR/apps/assistant/build/

    # Execute the commands
    yarn install
    yarn dev

    # Return to the original directory
    cd -
    echo "✅ Local Assistant is running!"
}
