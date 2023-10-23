#!/bin/bash

# Ask for the port number
echo "Please enter the port number:"
read port_number

# Find the process ID using the port number
process_id=$(lsof -t -i:$port_number)

# Check if process_id is empty (no process using the port)
if [[ -z $process_id ]]; then
    echo "No process found using port $port_number"
    exit 1
else
    # Display the process ID and ask for confirmation to kill it
    echo "Process ID $process_id is using port $port_number"
    echo "Do you want to kill the process? (yes/no)"
    read answer

    # Check the user's answer
    if [ "$answer" == "yes" ]; then
        # Kill the process
        pid=$(lsof -t -i:$port_number)
        if [ ! -z "$pid" ]; then
            echo "Killing process running on port $port_number with PID $pid"
            kill -9 $pid
        fi

        echo "Process $process_id killed."
    else
        echo "Process $process_id not killed."
    fi
fi

    pid=$(lsof -t -i:8502)
    if [ ! -z "$pid" ]; then
        echo "Killing process running on port 8502 with PID $pid"
        kill -9 $pid
    fi