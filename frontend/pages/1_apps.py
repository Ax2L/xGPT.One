
#**** Default Page block: **********************************************
import streamlit as st
from components import xhelper
from streamlit_extras.switch_page_button import switch_page

# Constants 
PAGE_NAME = "apps"  # Set the page name; crucial for various functions

# ⁡⁣⁣⁢ Functions
def setup_page(page_name):
    """Setup and initialize the page."""
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)
    # Must stay here to prevent loading without session_state.username
    from components import header
    
    header.create_menu(page_name)

def load_custom_css():
    """Load custom CSS style."""
    with open("components/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ⁣⁣⁢>>>| SETUP PAGE |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Check if 'current_page' not in session state, initialize it and redirect to 'main'
setup_page(PAGE_NAME)

# Check for page change again, and execute the respective section if a change occurred.
xhelper.check_current_page(PAGE_NAME)
#load_custom_css()
#**** Default Page block end **********************************************
