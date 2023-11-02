
#**** Default Page block: **********************************************
import streamlit as st
from components import xhelper
from streamlit_extras.switch_page_button import switch_page
from components import header

# Constants 
PAGE_NAME = "apps" 
# ⁡⁣⁣⁢ Functions
def setup_page(page_name):
    """Setup and initialize the page."""
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)

def load_custom_css():
    if f"{PAGE_NAME}_css" not in st.session_state:
        """Load custom CSS style."""
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        print(f"css already active on {PAGE_NAME}")

header.create_menu(PAGE_NAME)

# ⁣⁣⁢>>>| SETUP PAGE |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Check if 'current_page' not in session state, initialize it and redirect to 'main'
setup_page(PAGE_NAME)

# Check for page change again, and execute the respective section if a change occurred.
# xhelper.check_current_page(PAGE_NAME)
#**** Default Page block end **********************************************
load_custom_css()