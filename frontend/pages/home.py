# home.py
import time
import streamlit as st
from streamlit_elements import elements, mui, html

#* ||--------------------------------------------------------------------------------||
#* ||                                 # Default Setup                                ||
#* ||--------------------------------------------------------------------------------||
from streamlit_extras.switch_page_button import switch_page

# Set Page Name
page_name = "Home" #! Important
# Authenticated User Display
if "authenticator" not in st.session_state or "username" not in st.session_state:
    st.error("Username or authenticator is not set in the session. Please login again.")
    switch_page('main')
else:
    pass

# Add custom CSS Style
with open('components/utils/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load Dependencies
from components import xlayout

# Generate Menu
menu = xlayout.sidebar_header_button()
if "selected_menu_button" not in st.session_state:
    st.session_state.setdefault("selected_menu_button", None)


selected_menu_button = st.session_state['selected_menu_button']


if menu == "settings":
    menu_button = xlayout.settings_box()
    if menu_button != page_name:
        st.write("IM ABOUT TO SWITCHING PAGE TO:"+menu_button+"waiting 10 Seconds from now...")
        time.sleep(10)
        switch_page()
elif menu == "help":
    xlayout.settings_box()

elif menu == "datastore":
    xlayout.datastore_box()

elif menu == "bots":
    xlayout.bots_box()

elif menu == "tools":
    xlayout.tools_box()

elif menu == "mlearning":
    xlayout.mlearning_box()



#* ||___________________________________________________________________________||



def lets_dashboard():
    
    with elements("dashboard"):
        # You can create a draggable and resizable dashboard using
        from streamlit_elements import dashboard

        # First, build a default layout for every element you want to include in your dashboard

        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 2, 2),
            dashboard.Item("second_item", 2, 0, 2, 2),
            dashboard.Item("third_item", 0, 2, 1, 2),
        ]

        # Next, create a dashboard layout using the 'with' syntax. It takes the layout
        # as first parameter, plus additional properties you can find in the GitHub links below.

        with dashboard.Grid(layout):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item (cannot drag)", key="second_item")
            mui.Paper("Third item (cannot resize)", key="third_item")

        # If you want to retrieve updated layout values as the user move or resize dashboard items,
        # you can pass a callback to the onLayoutChange event parameter.

        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item (cannot drag)", key="second_item")
            mui.Paper("Third item (cannot resize)", key="third_item")



def authenticate_user():
    """Check whether the user is authenticated or not and redirect if necessary."""
    if "authenticator" not in st.session_state or "username" not in st.session_state:
        st.error("Username or authenticator is not set in the session. Please login again.")
        switch_page('main')
        st.stop()

def lets_dashboard():
    """Code for the dashboard display."""



def render_home_page():
    """Rendering and logic for the home page after authentication."""
    
    st.header('Home')
    st.subheader(f'Welcome {st.session_state["username"]}')
    
    # Add your other logic and UI display code for the authenticated home page...
    lets_dashboard()


# Main structure
authenticate_user()
render_home_page()