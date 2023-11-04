# **** Default Page block: **********************************************
import streamlit as st
from components import xhelper, header, header_v2

# Constants
PAGE_NAME = "apps"
header_v2.init()
# Set Page settings and Icon
st.markdown(
    """
    <head>
        <link rel="icon" href="http://127.0.0.1:8334/data/images/logo/favicon-32x32.png"  type="image/x-icon">
    </head>
    """,
    unsafe_allow_html=True,
)


# &⁡⁣⁣⁢ Functions
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


# Build header, forwards back and forwards to main if not logged in.
# header.create_menu(PAGE_NAME)

# ⁣⁣⁢>>>| SETUP PAGE |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Check if 'current_page' not in session state, initialize it and redirect to 'main'
setup_page(PAGE_NAME)

# Check for page change again, and execute the respective section if a change occurred.
# xhelper.check_current_page(PAGE_NAME)

# **** Default Page block end **********************************************
load_custom_css()
