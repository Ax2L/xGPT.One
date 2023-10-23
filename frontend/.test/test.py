import streamlit as st
import streamlit_authenticator as stauth
from components.default import sidebar_header_menu
from components.utils.auth_utils import load_config
from components.utils.navbar import NavBar
from streamlit_extras.#switch_page_button import #switch_page

# Setting page configurations
# st.set_page_config(
#     page_title="xGPT.One",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="auto",
#     menu_items={
#         'Get Help': 'https://github.com/Ax2L/xGPT.One/help',
#         'Report a bug': "https://github.com/Ax2L/xGPT.One/bug",
#         'About': "# Unveil the Universe of AI: Your Own AI-Driven Sidekick at Your Fingertips!"
#     }
# )

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

if "initial_set" not in st.session_state:
    st.session_state.authentication_status = None
    st.session_state.openai_key = ""
    st.session_state.name = ""
    st.session_state.current_page = "Home"
    st.session_state.initial_set = True

if "shared" not in st.session_state:
    st.session_state.shared = True

# Initialize NavBar
navbar = NavBar()
selected_menu_id = navbar.build_navbar()

# Update current page based on navbar selection
if selected_menu_id != st.session_state.current_page:
    st.session_state.current_page = selected_menu_id
    #switch_page(selected_menu_id.lower())

sidebar_header_menu(authenticator)  # Sidebar only visible for logged-in users

def load_selected_page():
    page_name = st.session_state.current_page.lower()
    page_module = None
    
    # Dynamically import the selected page
    if page_name in ["assistant", "demogpt", "home"]:
        page_module = __import__(page_name)
        
    # Call the show_page() function from the selected page
    if page_module and hasattr(page_module, "show_page"):
        page_module.show_page()

# Login
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.session_state.authentication_status = True
    st.session_state.name = name
    st.session_state.username = username
    load_selected_page()

# Create Account
try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

