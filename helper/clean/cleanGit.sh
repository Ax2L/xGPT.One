#!/bin/bash

# Navigate to the directory from which the script is being run
cd "$PWD"

# Check if the directory is a git repository
if [ ! -d ".git" ]; then
    echo "This is not a Git repository. Exiting."
    exit 1
fi

# Confirm changes with the user
read -p "This will remove all files ignored by git in $PWD. Are you sure? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Remove untracked files and directories (-f is 'force', -d removes directories as well)
    git clean -fd
fi
