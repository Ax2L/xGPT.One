import streamlit as st

from components.utils.postgres.xdatastore import (
    UserSettings,
    PageSettings,
    ColorSettings,
)
from streamlit_extras.switch_page_button import switch_page

# ⁡⁣⁣⁢>>>| SET PAGE PARAMETER |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Set the page name; crucial for various functions
page_name = "assistant"  #! Important


# ⁡⁢⁣⁣===| SETUP SECTION |=========================================⁡
# If 'current_page' not in session state, initialize it and redirect to 'main'
if "username" not in st.session_state:
    st.session_state.setdefault("current_page", page_name)
    switch_page("main")

# Must stay here to prevent loading without session_state.username
from components import xlayout

# ⁡⁢⁣⁣===| DATABASE SECTION |=========================================⁡
# Store DB Data
user = UserSettings(username=st.session_state["username"])
user.load()
page_config = PageSettings(username=st.session_state["username"])
page_config.load()
db_colors = ColorSettings(username=st.session_state["username"])
db_colors.load()


# ⁡⁢⁣⁣---| INIT SECTION |-------------------------------------------⁡
# (database) 1.Initialization (only done once)
if "initialized" not in st.session_state:
    # Initialize session state from data object
    st.session_state["dev_mode"] = user.data.get("dev_mode", False)
    st.session_state["openai_key"] = user.data.get("openai_key", None)
    st.session_state["initialized"] = True


# ⁡⁢⁣⁣+++| STYLE SECTION |++++++++++++++++++++++++++++++++++++++++++⁡
# Import custom CSS Style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ⁡⁢⁣⁡⁣⁢⁡⁣⁢⁣===| PAGE NAVIGATION SECTION |================================⁡⁡⁡
# Check if a different page is selected and switch if necessary
new_page = st.session_state["current_page"]

# If the current page doesn't match and isn't None, switch to it
current_site = st.session_state["current_page"]
if current_site != page_name and current_site is not None:
    switch_page(current_site)


# ⁡⁣⁢⁣===| CONTENT SECTION |=========================================⁡
# Load Sidebar Menu, saving pressed button in session_state

# Check for page change again, and execute the respective section if a change occurred.
current_site = st.session_state["current_page"]
if current_site != page_name and current_site is not None:
    switch_page(current_site)


# ? ==============================================
#!                        Tests
#! ==============================================


import streamlit.components.v1 as components


# st.set_page_config(layout='wide')

link1 = "http://127.0.0.1:3000"

# Set page to full width
# st.set_page_config(layout='wide')


# Use the full screen width and height
# components.iframe(link1, height=st.get_container_width(), width=st.get_container_width())


components.iframe(link1, height=1000, width=1000)
# components.html('<#iframe  src="http://localhost:3000/" width="800" height="600"></ iframe>', width=820, height=620)
