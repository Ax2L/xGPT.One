
#**** Default Page block: **********************************************
import streamlit as st
from components import xhelper
from streamlit_extras.switch_page_button import switch_page

# Constants 
PAGE_NAME = "apps"  # Set the page name; crucial for various functions

def load_custom_css(STYLES_PATH):
    """Load custom CSS style."""
    #print(f"PATH::{STYLES_PATH}")
    with open(STYLES_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ⁡⁣⁣⁢ Functions
def setup_page(page_name):
    """Setup and initialize the page."""
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)
    from components import headernew
    # Determine the directory of this script
    STYLES_PATH = xhelper.find_file("xstyles.toml",".")
    # Must stay here to prevent loading without session_state.username
    headernew.create_menu(page_name)
    #load_custom_css(STYLES_PATH)


# ⁣⁣⁢>>>| SETUP PAGE |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Check if 'current_page' not in session state, initialize it and redirect to 'main'
setup_page(PAGE_NAME)

# Check for page change again, and execute the respective section if a change occurred.
xhelper.check_current_page(PAGE_NAME)
#**** Default Page block end **********************************************
