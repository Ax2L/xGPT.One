
# Function to check and kill process on port 8502
kill_process_on_port_8501() {
    pid=$(lsof -t -i:8501)
    if [ ! -z "$pid" ]; then
        echo "Killing process running on port 8501 with PID $pid"
        kill -9 $pid
    fi
}


# Function to check and kill process on port 8502
kill_process_on_port_8502() {
    pid=$(lsof -t -i:8502)
    if [ ! -z "$pid" ]; then
        echo "Killing process running on port 8502 with PID $pid"
        kill -9 $pid
    fi
}

# Invoke the function at the beginning of the script
kill_process_on_port_8501

kill_process_on_port_8502