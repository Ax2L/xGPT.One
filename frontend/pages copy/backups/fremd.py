# fremd.py
#! 1. Create a 



#// region [ rgba(250, 15, 100, 0.05)] Imports
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_elements import elements, mui, html
from components.default import sidebar_header_menu
from components.utils.auth_utils import load_config
import hydralit_components as hc
from streamlit_extras.#switch_page_button import #switch_page
from components.utils.navbar import navbar, p_navbar
#// endregion

#// region [ rgba(250, 215, 200, 0.05)] Switch Pages
#* ||--------------------------------------------------------------------------------||
#* ||                                    # Config                                    ||
#* ||--------------------------------------------------------------------------------||
# Load Config
config = load_config()

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
#// endregion

# // region [ rgba(50, 100, 110, 0.2)] Navigation Data and Theme
#? ||--------------------------------------------------------------------------------||
#? ||                                    # NavBar                                    ||
#? ||--------------------------------------------------------------------------------||
 [ rgba(50, 200, 150, 0.05)] Navigation Data and Theme
#// region [ rgba(50, 100, 140, 0.2)] Navigation Data and Theme
page = "fremd"
# build the navbar and store its data. 
navigation = navbar()
# Display menu id
p_navbar(used_navbar=navigation,page_id=page)
# TODO st.text(navigation)
# Check the action in: the menu.
def check_nav_action(m_id, p_id):
    try: # Compare the pressed button with the current page
        # Same button as current page:
        if (str(m_id)).lower() == p_id:
            """You clicked on the Page you currently in."""
            do = "nothing"
        else: # If the pressed button is another page
            #switch_page(str(m_id))
            do = "nothing"
    except Exception as e:
        st.error(f"An error occurred: {e}")
    
# // region [ rgba(150, 100, 135, 0.2)] Navigation Data and Theme

# check_nav_action(p_navbar, "home")

    
#// region [ rgba(250, 15, 100, 0.05)] Sidebar Initialization
#? ||--------------------------------------------------------------------------------||
#? ||                                    # Sidebar                                   ||
#? ||--------------------------------------------------------------------------------||
sidebar_header_menu(authenticator)
#// endregion

#// region [ rgba(100, 200, 150, 0.05)] Authenticated Display
def authenticated_display():
    #- ||--------------------------------------------------------------------------------||
    #- ||                                  # User Zone                                   ||
    #- ||--------------------------------------------------------------------------------||
    st.header('Home')
    
    with st.container():
        # Home-related Code
        user_name = st.session_state['username']
        st.subheader(f'Welcome {user_name}', divider='gray')    
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.expander("User Details 🛈", expanded=True):
                st.write(f"**👤 Username: {st.session_state['username']}**")
                st.write(f"**📛 Name: {st.session_state['name']}**")
                st.write(f"**📧 Email: youremail@example.com**")

        with col2:
            tab1, tab2, tab3 = st.tabs(["Password", "User", "API Keys"])

            with tab1:
                with st.spinner('Processing...'):
                    try:
                        if authenticator.reset_password(st.session_state["username"], 'Reset Password 🔄'):
                            st.success('Password modified successfully ✅')
                    except Exception as e:
                        st.error(f"Error: {str(e)} ❌")

            with tab2:
                with st.spinner('Processing...'):
                    try:
                        if authenticator.update_user_details(st.session_state["username"], 'Update User Details 🔄'):
                            st.success('Entries updated successfully ✅')
                    except Exception as e:
                        st.error(f"Error: {str(e)} ❌")

            with tab3:
                with st.spinner('Processing...'):
                    try:
                        st.subheader("Update your OpenAI Key 🔐")
                        new_key = st.text_input("Your OpenAI API Key", value=st.session_state.openai_key, type="password")
                        if st.button("Update Key"):
                            with st.spinner('Updating OpenAI Key...'):
                                st.session_state.openai_key = new_key
                                st.success("API Key Updated Successfully ✅")
                    except Exception as e:
                        st.error(f"Error: {str(e)} ❌")
#// endregion

#// region [ rgba(100, 200, 150, 0.05)] Dashboard Elements

    with elements("dashboard"):
    #- ||--------------------------------------------------------------------------------||
    #- ||                                # Grid Dashboard                                ||
    #- ||--------------------------------------------------------------------------------||
        # You can create a draggable and resizable dashboard using
        # any element available in Streamlit Elements.

        from streamlit_elements import dashboard

        # First, build a default layout for every element you want to include in your dashboard
        
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 2, 2),
            dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=False, moved=False),
            dashboard.Item("third_item", 0, 2, 1, 1, isResizable=False),
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
#// endregion

#// region [ rgba(250, 15, 100, 0.05)] Authentication Logic
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.session_state["authentication_status"] = True
    st.session_state["name"] = name
    st.session_state["username"] = username
    authenticated_display()
#// endregion

