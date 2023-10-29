import time
import streamlit as st
from components import xlayout
from streamlit_extras.switch_page_button import switch_page

#? ==============================================
#?                 SETUP SECTION
#? ==============================================

# Set the page name; crucial for various functions
page_name = "test"  #! Important

# If 'current_page' not in session state, initialize it and redirect to 'main'
if "username" not in st.session_state:
    st.session_state.setdefault("current_page", page_name)
    switch_page('main')

# Import custom CSS Style
with open("components/utils/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ⁡⁢⁣⁡⁣⁢⁡⁣⁢⁣===| PAGE NAVIGATION SECTION |================================⁡⁡⁡
# If the current page doesn't match and isn't None, switch to it
current_site = st.session_state['current_page']
if current_site != page_name and current_site is not None:
    switch_page(current_site)

# If the current page doesn't match and isn't None, switch to it
current_site = st.session_state['current_page']
if current_site != page_name and current_site is not None:
    switch_page(current_site)

#? ==============================================
#?                CONTENT SECTION
#? ==============================================

# Load Sidebar Menu, saving pressed button in session_state
xlayout.create_menu(page_name)

# Check for page change again, and execute the respective section if a change occurred.
current_site = st.session_state['current_page']
if current_site != page_name and current_site is not None:
    switch_page(current_site)
    st.write("Current Page is not mine:" + current_site)
else:
    st.write("You clicked on the current page:" + current_site + " your page is:" + page_name)
