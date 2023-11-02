# main.py
import json
import streamlit as st
from components import xhelper
from components.xdatastore import UserSettings
from components.utils import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page

# Constants and Configurations
page_name = "main"
default_np = "apps"
next_page = default_np


# Helper Functions
def load_custom_css():
    if f"{page_name}_css" not in st.session_state:
        """Load custom CSS style."""
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        print(f"css already active on {page_name}")
        

def initiate_session_states_from_json():
    """Initiate session state variables from JSON."""
    with open("../config/streamlit/session_state_initializer.json", "r") as file:
        initial_states = json.load(file)
    for key, value in initial_states.items():
        st.session_state.setdefault(key, value)


def authenticated_display():
    """Display the authenticated user's view."""
    with st.container():
        if "username" in st.session_state:
            user = UserSettings(username="admin")
            user.load()
            user.update("username", st.session_state["username"])
            st.subheader(f'Welcome back, {st.session_state["username"]}!')
            st.session_state["current_page"] = next_page
            switch_page(next_page)
            st.button("testStyle")
        else:
            st.error("Username is not set in the session. Please login again.")
            st.stop()


def display_login_sidebar_info():
    """Display login information in the sidebar."""
    with st.sidebar:
        st.markdown(new_user_info)

# Set Page settings and Icon
st.markdown(
    """
    <head>
        <link rel="icon" href="images/logo/favicon.ico"  type="image/x-icon">
    </head>
    """,
    unsafe_allow_html=True,
)

new_user_info = """
## Important Information for New Users

**Hello, New User!**

Please note that our multi-user solution is under development. Meanwhile, you can use the default admin credentials:

- **Username**: admin
- **Password**: changeme
- **Email**: admin@admin.com 

You can also manually install our Email Service. Find more details in the provided TODO section.
"""


# Initialization
if "initial_main" not in st.session_state:
    st.toast("Initializing application...")
    st.session_state.initial_main = True
    initiate_session_states_from_json()
    #print(f"Main Page initiated and st.session_state.initial_main is:{st.session_state.initial_main}")

if st.session_state['current_page']:
    next_page = st.session_state['current_page']

# Load Configurations
config = xhelper.load_config()

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Display Sidebar Info
display_login_sidebar_info()

# Authentication Logic
if st.session_state["authentication_status"] is False:
    st.toast("Authentication failed. Please verify your credentials.")
elif st.session_state["authentication_status"] is None:
    st.toast("Please enter your login credentials.")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.session_state.update({
        "authentication_status": True,
        "name": name,
        "username": username,
    })
    authenticated_display()

load_custom_css()