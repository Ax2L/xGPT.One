import streamlit as st
import subprocess
import psutil

from components.xgpt_styles import apply_page_settings, apply_styles


# Apply page settings
apply_page_settings("Supervisor")

# Apply custom styles
# apply_styles() # unstable

# Global variable to store the process
proc = None

# Function to start the process
def start_process():
    try:
        global proc
        proc = subprocess.Popen(["poetry", "run", "luigid"])
        st.success("Successfully started the process.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Function to stop the process
def stop_process():
    try:
        proc.terminate()
        st.success("Successfully stopped the process.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Function to show logs (Dummy function, you need to link it to real logs)
def show_logs():
    st.text("Showing logs here...")

# Function to show resource utilization
def resource_utilization():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    st.write(f"CPU Usage: {cpu_percent}%")
    st.write(f"Memory Usage: {memory_info.percent}%")

# Streamlit app
st.title('Supervisor Dashboard')

# User role emulation
user_role = st.sidebar.selectbox("Select Your Role", ["Admin", "Supervisor", "Viewer"])

# Status Overview
if user_role in ["Admin", "Supervisor", "Viewer"]:
    st.header("Status Overview")
    st.write("Display real-time status here...")  # You'll need to implement real-time status checking

# Control Buttons
if user_role in ["Admin", "Supervisor"]:
    st.header("Process Control")
    if st.button("Start"):
        start_process()
    if st.button("Stop"):
        stop_process()

# Show Logs
if user_role in ["Admin", "Supervisor", "Viewer"]:
    st.header("Logs Viewer")
    if st.button("Show Logs"):
        show_logs()

# Resource Monitoring
if user_role in ["Admin", "Supervisor", "Viewer"]:
    st.header("Resource Monitoring")
    if st.button("Show Resources"):
        resource_utilization()

# Admin-only Components
if user_role == "Admin":
    st.header("Admin Section")
    st.write("Additional admin features can go here...")
