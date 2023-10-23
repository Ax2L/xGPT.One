# home.py
import streamlit as st
from streamlit_extras.#switch_page_button import #switch_page
from components.utils.navbar import NavBar
from components.utils.styles import apply_styles
import streamlit_authenticator as stauth
from components import default
from PIL import Image
import time

# Load Config
logo = Image.open('images/logo/logo_long.png')

page_name = "Home" # Important
navi_id = 0 # Important
# Initial Setup

# Setup Navigation Bar
def setup_interface():
    navbar = NavBar()
    navi = navbar.build_navbar(navi_id)  # Page Navi Number is 0 for Home
    
    if navi != page_name:
        #switch_page(navi)

# Authenticated User Display
if "authenticator" or "username" not in st.session_state:
    st.error("Username is not set in the session. Please login again.")
else:
    if "initiate_home" not in st.session_state:
        apply_styles()
        st.write("I did it!, And maybe again :D")
        st.session_state.setdefault('initiate_home', True)
    authenticator = st.session_state['authenticator']
    default.sidebar_header_menu(authenticator)
    st.header('Home')
    st.subheader(f'Welcome {st.session_state["username"]}')
    # TODO: What esle should be in Home?
