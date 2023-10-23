# app.py

#// region [ rgba(250, 215, 200, 0.05)] Switch Pages
#* ||--------------------------------------------------------------------------------||
#* ||                                    # Config                                    ||
#* ||--------------------------------------------------------------------------------||
import streamlit as st
st.set_page_config( # Only one in the Project is allowed!
    page_title="xGPT.One",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/Ax2L/xGPT.One/help',
        'Report a bug': "https://github.com/Ax2L/xGPT.One/bug",
        'About': "# Unveil the Universe of AI: Your Own AI-Driven Sidekick at Your Fingertips!"
    }
)

import streamlit_authenticator as stauth
from components.utils.auth_utils import load_config
from streamlit_extras.#switch_page_button import #switch_page
#// endregion

#// region [ rgba(250, 15, 200, 0.05)] Switch Pages
if "initial_set" not in st.session_state:
    # Initialize session_state if it doesn't exist
    st.session_state.setdefault("authentication_status", None)
    st.session_state.setdefault("openai_key", "")
    st.session_state.setdefault("name", "")
    st.session_state.setdefault("active", "")
    st.session_state.setdefault("hidden", "")
    st.session_state.setdefault("current_page", None)
    st.session_state.setdefault("openai_key", None)
    st.session_state["initial_set"] = True
    
#// endregion

#// region [ rgba(25, 215, 200, 0.05)] 
# Enable shared pages
if "shared" not in st.session_state:
    st.session_state["shared"] = True

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = "app"
#// endregion

#// region [ rgba(100, 150, 250, 0.05)] Initialization
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

#// region [ rgba(100, 200, 150, 0.05)] Authenticated Display
def authenticated_display():
    #- ||--------------------------------------------------------------------------------||
    #- ||                                  # User Zone                                   ||
    #- ||--------------------------------------------------------------------------------||
    #- Go Home when logged in ^^
    if st.session_state["authentication_status"]:
        # st.session_state["current_page"] = "home"
        #switch_page("home")
#// endregion

#// region [ rgba(250, 15, 100, 0.05)] Authentication Logic

#// #||--------------------------------------------------------------------------------||
#// #||                                # Forgot Username                               ||
#// #||--------------------------------------------------------------------------------||
#// try:
#//     username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
#//     if username_of_forgotten_username:
#//         st.success('Username to be sent securely')
#//         # Username should be transferred to user securely
#//     else:
#//         st.error('Email not found')
#// except Exception as e:
#//     st.error(e)
#// 
#// 
#// #||--------------------------------------------------------------------------------||
#// #||                                # Forgot Password                               ||
#// #||--------------------------------------------------------------------------------||
#// try:
#//     username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
#//     if username_of_forgotten_password:
#//         st.success('New password to be sent securely')
#//         # Random password should be transferred to user securely
#//     else:
#//         st.error('Username not found')
#// except Exception as e:
#//     st.error(e)
#// endregion

#// region [ rgba(120, 105, 10, 0.2)] Switch Pages
#||--------------------------------------------------------------------------------||
#||                                    # Login                                     ||
#||--------------------------------------------------------------------------------||
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.session_state["authentication_status"] = True
    st.session_state["name"] = name
    st.session_state["username"] = username
    authenticated_display()
#// endregion
#// region [ rgba(20, 105, 10, 0.2)] Switch Pages
#||--------------------------------------------------------------------------------||
#||                                # Create Account                                ||
#||--------------------------------------------------------------------------------||
try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)
#// endregion


#  #// region [ rgba(20, 105, 10, 0.2)] Switch Pages
#  #||--------------------------------------------------------------------------------||
#  #||                        # Create Page Session.stats                             ||
#  #||--------------------------------------------------------------------------------||
#  try:
#      if "current_site" not in st.session_state:
#          st.session_state.setdefault("current_page", "app")
#  except Exception as e:
#      st.error(e)
#  
#  
#  #// endregion

