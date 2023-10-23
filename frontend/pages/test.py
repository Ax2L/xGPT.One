import streamlit as st
from components.xdatastore import UserSettings, PageSettings, ColorSettings
from streamlit_extras.switch_page_button import switch_page

# ⁡⁣⁣⁢>>>| SET PAGE PARAMETER |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Set the page name; crucial for various functions
page_name = "test"  #! Important


# ⁡⁢⁣⁣===| SETUP SECTION |=========================================⁡
# If 'current_page' not in session state, initialize it and redirect to 'main'
if "username" not in st.session_state:
    st.session_state.setdefault("current_page", page_name)
    switch_page('main')

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
with open("components/utils/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ⁡⁢⁣⁡⁣⁢⁡⁣⁢⁣===| PAGE NAVIGATION SECTION |================================⁡⁡⁡
# Check if a different page is selected and switch if necessary
new_page = st.session_state['current_page']
if new_page == page_name:
    st.write("Found my own page button:" + new_page)
else:
    st.write("Found page button of:" + new_page)

# If the current page doesn't match and isn't None, switch to it
current_site = st.session_state['current_page']
if current_site != page_name and current_site is not None:
    switch_page(current_site)


# ⁡⁣⁢⁣===| CONTENT SECTION |=========================================⁡
# Load Sidebar Menu, saving pressed button in session_state
xlayout.create_menu(page_name)

# Check for page change again, and execute the respective section if a change occurred.
current_site = st.session_state['current_page']
if current_site != page_name and current_site is not None:
    switch_page(current_site)
    st.write("Current Page is not mine:" + current_site)
else:
    st.write("You clicked on the current page:" + current_site + " your page is:" + page_name)


#? ==============================================
#!                        Tests
#! ==============================================


