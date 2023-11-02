# Helper functions related to authentication and email notification

import os
import yaml
import toml
import smtplib
from email.message import EmailMessage
from yaml.loader import SafeLoader
import streamlit as st

from streamlit_extras.switch_page_button import switch_page
LOGO_PATH = "images/logo/xgpt.png"
# Determine the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_config_file(filename=f"../../config/streamlit/config.yaml"):
    """Search for the config file and return its path."""
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            return os.path.join(root, filename)
    return None  # Return None if file not found

config_path = "../config/streamlit/config.yaml"
def load_config():
    # Locate and validate the config path
    if not config_path:
        raise FileNotFoundError("config.yaml was not found in any subdirectories!")
    """Load configuration from the config file."""
    with open(config_path, 'r') as file:
        return yaml.load(file, Loader=SafeLoader)


def save_config(config):
    # Locate and validate the config path
    config_path = find_config_file()
    if not config_path:
        raise FileNotFoundError("config.yaml was not found in any subdirectories!")
    """Save configuration to the config file."""
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def send_email(subject, body, to_email, config):
    """Send an email using the provided SMTP configuration."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = config['smtp']['username']
    msg['To'] = to_email

    with smtplib.SMTP(config['smtp']['server'], config['smtp']['port']) as server:
        if config['smtp']['use_tls']:
            server.starttls()
        server.login(config['smtp']['username'], config['smtp']['password'])
        server.send_message(msg)


def send_reset_password_email(name, new_password, to_email, config):
    """Send a reset password email."""
    subject = "Your New Password"
    body = f"Hey {name},\n\nHere is your new password:\n\n {new_password}\n\nPlease change it once you log in."
    send_email(subject, body, to_email, config)


def send_forgot_username_email(name, username, to_email, config):
    """Send a forgot username email."""
    subject = "Your Username Reminder"
    body = f"Hey {name},\n\nYour username is: \n\n{username}\n\n"
    send_email(subject, body, to_email, config)



def display_dev_info():
    # Check if dev_mode is enabled
    if st.session_state.get('dev_mode', False):
        # Show the Streamlit sidebar navigation
        st.markdown("""
            <style>
                div[data-testid="stSidebarNav"] {display: block;}
            </style>
        """, unsafe_allow_html=True)
        
        # Displaying active parameters in session_state
        st.write("### Active Parameters")
        active_params = {key: value for key, value in st.session_state.items() if key != "previous_params"}
        st.write(active_params)
        
        # Displaying parameters that were active but are now inactive (if available)
        st.write("### Previously Active Parameters")
        previous_params = st.session_state.get("previous_params", {})
        inactive_params = {key: value for key, value in previous_params.items() if key not in active_params}
        st.write(inactive_params)
        
        # Update the session_state to save the current parameters
        st.session_state["previous_params"] = active_params.copy()
    else:
        # Hide the Streamlit sidebar navigation
        st.markdown("""
            <style>
                div[data-testid="stSidebarNav"] {display: none;}
            </style>
        """, unsafe_allow_html=True)


def display_session_data():
    """Displays session state data if session_state.show_session_data is True."""
    if st.session_state.get("show_session_data", False):
        st.write(st.session_state)


def check_logged_in(page_name):
    # If 'current_page' not in session state, initialize it and redirect to 'main'
    if "username" not in st.session_state:
        st.session_state.setdefault("current_page", page_name)
        switch_page('main')


def check_current_page(page_name):
    # If the current page doesn't match and isn't None, switch to it
    current_site = st.session_state['current_page']
    if current_site != page_name and current_site is not None:
        switch_page(current_site)
