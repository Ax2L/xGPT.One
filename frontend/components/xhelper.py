# Helper functions related to authentication and email notification

import os
import yaml
import toml
import smtplib
from email.message import EmailMessage
from yaml.loader import SafeLoader
import streamlit as st
from components import style_process

from streamlit_extras.switch_page_button import switch_page
LOGO_PATH = "images/logo/xgpt.png"
# Determine the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if "style_blocks" not in st.session_state:
    style_process.store_style_block()

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



def find_file(target_name, start_dir):
    """
    Search for a file with a given name, diving one level deeper each time.
    
    Parameters:
        target_name (str): The name of the file to search for.
        start_dir (str): The directory from which the search begins.
    
    Returns:
        str: The full path of the found file, or None if not found.
    """
    
    # Check current directory first
    for root, dirs, files in os.walk(start_dir):
        if target_name in files:
            return os.path.join(root, target_name)
        break  # Only check current directory
    
    # Check subdirectories, one level deeper
    for dir_name in os.listdir(start_dir):
        dir_path = os.path.join(start_dir, dir_name)
        if os.path.isdir(dir_path):
            for root, dirs, files in os.walk(dir_path):
                if target_name in files:
                    return os.path.join(root, target_name)
                break  # Only check current directory within the subdir

    return None



def get_styles_toml_path():
    file_name_to_search = "style_base.toml"
    start_directory = "."
    result = find_file(file_name_to_search, start_directory)
    if result:
        print(f"Found {file_name_to_search} at: {result}")
        return result
    else:
        print(f"{file_name_to_search} not found.")
        return None


def load_styles_from_toml():
    # Check if the TOML content is already in the session state.
    if 'base_style' not in st.session_state:
        styles_path = get_styles_toml_path()

        # Ensure that styles_path is not None before proceeding
        if styles_path is None:
            print("Error: xstyles.toml not found.")
            return {}

        with open(styles_path, 'r') as toml_file:
            st.session_state.base_style = toml.load(toml_file)

    # Convert the TOML content to styles.
    styles = {}
    for key, value in st.session_state["style_blocks"]["BASE_COLORS"].items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                styles[f"{key}--{sub_key}"] = sub_value
        else:
            styles[key] = value

    return styles

