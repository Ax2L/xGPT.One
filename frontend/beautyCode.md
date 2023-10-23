Can you please:
- restructure my main.py, 
    - in an order that is the most efficient, 
    - easy to understand, 
    - beautiful to read 
    - and with better reporting, I want for example that we use more often st. toast to display updates of actions,
    - use more often 
    - rewrite the text to make them better formatted and professional.
    - and as well as st.Exception(e), please use therefore the following Streamlit Script that you should provide me updated, 


- ! but without removing any logic! Otherwise, I will freak out!.:





```python
from components.utils import first
import json
from PIL import Image
import streamlit as st
from components.utils import streamlit_authenticator as stauth
from components import xhelper
from components.xdatastore import UserSettings
from streamlit_extras.switch_page_button import switch_page

default_np = "test"
next_page = default_np

def initiate_session_states_from_json():
    """Initiate session state variables from JSON."""
    with open("../config/streamlit/session_state_initializer.json", "r") as file:
        initial_states = json.load(file)
        #
    for key, value in initial_states.items():
        st.session_state.setdefault(key, value)
        #
# Initialize Application
if "initial_main" not in st.session_state:
    initiate_session_states_from_json()


if st.session_state['current_page'] != "" and not None:
    next_page = st.session_state['current_page']


def authenticated_display():
    """Display the authenticated user's view."""
    with st.container():
        if "username" in st.session_state:
            user = UserSettings(username="admin")
            user.load()
            user.update("username", st.session_state["username"])
            st.subheader(f'Welcome back {st.session_state["username"]}!')
            st.session_state["current_page"] = next_page
            switch_page(next_page)
        else:
            st.error("Username is not set in the session. Please login again.")
            st.stop()


def login_sidebar_info():
    """Display login information in the sidebar."""
    with st.sidebar:
        st.markdown(mew_user_info)


mew_user_info = """
# Important!
Hello new User!
I will soon continue on the multiuser solution, till then, you have to use the default admin user:
Username: admin
Init-Password: changeme
Init-Mail: admin@admin.com 
You could theoretically use already the E-Mail Service, but you need to install it manually, all details are in the #TODO"
"""


# Load Config
config = xhelper.load_config()

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if st.sidebar:
    login_sidebar_info()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# Main Function
name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status:
    st.session_state.update({
        "authentication_status": True,
        "name": name,
        "username": username,
    })
    authenticated_display()
```
