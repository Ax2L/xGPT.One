# default.py

#// region [ rgba(50, 15, 100, 0.05)] Imports
import streamlit as st
from streamlit_extras.stateful_button import button
from streamlit_extras.stylable_container import stylable_container
from components.utils.navbar import NavBar
from streamlit_extras.switch_page_button import switch_page
from components.utils.auth_utils import load_config
import streamlit_authenticator as stauth
from components.utils.styles import *
from components.postgres import *
import hydralit_components as hc
from PIL import Image
import time

# Load Config
config = load_config()
image = Image.open('images/logo/logo_long.png')

# Background Image
import base64
show_loader
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Initialize Application
if "initial_set" not in st.session_state:
    # Initialize session_state if it doesn't exist
    st.session_state.setdefault("authentication_status", None)
    st.session_state.setdefault("openai_key", "")
    st.session_state.setdefault("name", "")
    st.session_state["current_page"] = ""
    st.session_state["openai_key"] = ""
    st.session_state["initial_set"] = True


if "shared" not in st.session_state:
    st.session_state["shared"] = True



#// region [ rgba(250, 215, 100, 0.05)] Styles Setup
style_sidebar_menu_container_styles_template = sidebar_menu_container_styles_template
style_sidebar_button_styles_template = sidebar_button_styles_template
style_sidebar_logout_button_styles_template = sidebar_logout_button_styles_template
style_sidebar_logout_placeholder_template = sidebar_logout_placeholder_template
style_sidebar_settings_content_container_styles_template = sidebar_settings_content_container_styles_template
style_sidebar_button_tools_template = sidebar_button_tools_template
#// endregion


#// region [ rgba(150, 15, 210, 0.05)] Sidebar Header Menu Functions
def sidebar_header_menu(authenticator):
    with st.sidebar:
        with st.container():
            
            col1, col2, col3 = st.columns([1, 1, 1.5])
            with col1:
                def wait_for_page():
                    with st.spinner(''):
                        time.sleep(10)  # Simulating a task that takes time.
            with col2:
                do = "nothing"
            with col3:
            # Show the loader
                st.image(image, width=100)
            st.divider()
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 0.4, 1])
            with col1:
                with stylable_container(
                    key="notification_button_sidebar",
                    css_styles=style_sidebar_button_styles_template
                ):
                    if button(":bell:", key="notification_button_sidebar"):
                        st.sidebar.write("notification_button_sidebar TODO")
            with col2:
                with stylable_container(
                    key="assistant_button_sidebar",
                    css_styles=style_sidebar_button_styles_template
                ):
                    if button("👤", key="assistant_button_sidebar"):
                        st.sidebar.write("TODO assistant_button_sidebar")
            with col3:
                with stylable_container(
                    key="tools_button_sidebar",
                    css_styles=style_sidebar_button_tools_template
                ):
                    if button(":toolbox:", key="tools_button_sidebar"):
                        do = "nothing"
                        # sidebar_settings_menu_content(authenticator, status=True)
            with col4:
                with stylable_container(
                    key="documentation_button_sidebar",
                    css_styles=style_sidebar_button_styles_template
                ):
                    if button("📖", key="documentation_button_sidebar"):
                        st.sidebar.write("TODO documentation_button_sidebar")
            
            # Placeholder
            with col5:
                with stylable_container(
                    key="sidebar_logout_placeholder",
                    css_styles=style_sidebar_logout_placeholder_template
                ):
                    if button("", key="sidebar_logout_placeholder_button"):
                        st.sidebar.write("sidebar_logout_placeholder_button TODO")
            # Settings
            with col6:
                with stylable_container(
                    key="settings_button_sidebar",
                    css_styles=style_sidebar_button_styles_template
                ):
                    if button(":gear:", key="settings_button_sidebar"):
                        # Toggle showing the settings menu
                        st.session_state.show_settings = not st.session_state.get("show_settings", False)
                        if st.session_state.get("show_settings", False):
                            with st.sidebar:
                                with stylable_container(
                                    key="sidebar_settings_container",
                                    css_styles=style_sidebar_settings_content_container_styles_template
                                ):
                                    tab1, tab2, tab3 = st.tabs(["User", "API", "Notes"])
                                    with tab1:
                                        st.write(f"Your current profile.")
                                        with st.expander("Check current User"):
                                            st.write(f"Username: {st.session_state['username']}")
                                            st.write(f"Name: {st.session_state['name']}")
                                            st.write(f"Email: youremail@example.com")
                                            authenticator.logout('Logout', 'sidebar', key='0EDCADAA156ABA8CB55F6')
                                        with st.expander("Change Name/Mail"):
                                            with st.spinner('Processing...'):
                                                try:
                                                    if authenticator.update_user_details(st.session_state["username"], 'Update User Details'):
                                                        st.success('Entries updated successfully ✅')
                                                except Exception as e:
                                                    st.error(f"Error: {str(e)} ❌")
                                        with st.expander("Change Password"):
                                            with st.spinner('Processing...'):
                                                try:
                                                    if authenticator.reset_password(st.session_state["username"], 'Reset Password'):
                                                        st.success('Password modified successfully ✅')
                                                except Exception as e:
                                                    st.error(f"Error: {str(e)} ❌")
                                    with tab2:
                                        with st.spinner('Processing...'):
                                            try:
                                                st.header("User Data Management")
                                                # Load existing data from Postgres using username as ID
                                                user = st.session_state["username"]

                                                with st.form("user_form"):
                                                    # User inputs with pre-filled data from the database
                                                    new_key_openai = st.text_input("API Key", value=db_get_value(user, 'key_openai'), key="openai_key", type="password")
                                                    new_dev_mode = st.toggle("Dev mode", value=db_get_value(user, 'dev_mode'), key="dev_mode")
                                                    submit_button = st.form_submit_button("Update")

                                                # Update user data if submit_button clicked
                                                if submit_button and new_key_openai is not None:
                                                    db_set_value(user, 'key_openai', new_key_openai)
                                                    db_set_value(user, 'dev_mode', new_dev_mode)
                                            except Exception as e:
                                                st.error(f"Error: {str(e)} ❌")
                                    with tab3:
                                        with st.spinner('Processing...'):
                                            try:
                                                st.header("Notes")
                                                # Load existing data from Postgres using username as ID
                                                user = st.session_state["username"]

                                                with st.form("user_form"):
                                                    # User inputs with pre-filled data from the database
                                                    new_notes = st.text_area("Notes", value=db_get_value(user, 'notes'), key="notes")
                                                    submit_button = st.form_submit_notes_button("Update")

                                                # Update user data if submit_button clicked
                                                if new_notes is not None:
                                                    db_set_value(user, 'notes', new_notes)
                                            except Exception as e:
                                                st.error(f"Error: {str(e)} ❌")#// endregion
            st.divider()


# Initial Setup
def setup():
    set_png_as_page_bg('images/blue_dark_bg.png')
    apply_styles()
    # with st.spinner('Loading...'):
    #     time.sleep(1)  # Simulating a task that takes time.

# Setup Navigation Bar
def setup_navbar(navbar_position_id, page_name):
    navbar = NavBar()
    navi = navbar.build_navbar(navbar_position_id)  # Page Navi Number is 0 for Home
    
    if navi != page_name:
        #switch_page(navi)
        do = "nothing"
