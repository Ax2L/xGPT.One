# Helper functions related to authentication and email notification

import streamlit as st
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.message import EmailMessage
import os


def find_config_file(filename='../config/streamlit/config.yaml'):
    """Search for the config file and return its path."""
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
    return None  # Return None if file not found

config_path = find_config_file()

if not config_path:
    raise FileNotFoundError("config.yaml was not found in any subdirectories!")

def load_config():
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

def save_config(config):
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def send_email(subject, body, to_email, config):
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
    subject = "Your New Password"
    body = f"Hey {name},\n\nHere is your new password:\n\n {new_password}\n\nPlease change it once you log in."
    
    send_email(subject, body, to_email, config)

def send_forgot_username_email(name, username, to_email, config):
    subject = "Your Username Reminder"
    body = f"Hey {name},\n\nYour username is: \n\n{username}\n\n"
    
    send_email(subject, body, to_email, config)

if "authenticator" not in st.session_state:
    st.session_state["authenticator"] = ""
    # Initialize Authenticator
authenticator =  st.session_state["authenticator"]

