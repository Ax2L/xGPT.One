# pages/1_apps.py --
# ! Do not modify this section below! >>>
import streamlit as st
from components import xinit_page

# ^ Constants
PAGE_NAME = "apps"
# * Initializing the page with required configurations
xinit_page.set_page_config(PAGE_NAME, "wide", "collapsed")

#! <<< Do not modify this section above!

# ? Local modules
from components import xheader, xhelper, xforms


# & Functions
def setup_page(page_name):
    """* Setup and initialize the page.
    * Args:
    *   page_name (str): Name of the current page.
    """
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)


def load_custom_css():
    """* Load custom CSS for the page if not already active."""
    if f"{PAGE_NAME}_css" not in st.session_state:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            st.session_state.setdefault("{PAGE_NAME}_css", True)
    else:
        print(f"css already active on {PAGE_NAME}")


# & Page Initialization Process
xheader.init(PAGE_NAME)

# * Setting up the page environment
setup_page(PAGE_NAME)

# ! Content Section


# ~ Sidebar Content
with st.sidebar:
    st.text("Some Sidebar content")

# ~ Main Page Content

st.text("Some Main content")

if "edit_item" in st.session_state and not None:
    xforms.display_edit_item_form()


# * Loading custom CSS at the end
load_custom_css()
