import streamlit as st
from components.utils.postgres.xdatastore import UserSettings, PageSettings
from streamlit_extras.switch_page_button import switch_page


page_name = "test"
if "current_page" not in st.session_state:
    st.session_state.current_page = page_name
    switch_page("main")

# Initialization (only done once)
if "initialized" not in st.session_state:
    user = UserSettings(username="admin")
    user.load()

    # Initialize session state from data object
    st.session_state["dev_mode"] = user.data.get("dev_mode", False)
    st.session_state["openai_key"] = user.data.get("openai_key", None)

    st.session_state["initialized"] = True


# Using a button for #? Dev Mode
dev_mode_button = st.button("Toggle Dev Mode")
if dev_mode_button:
    st.session_state["dev_mode"] = not st.session_state["dev_mode"]
st.write(f"Dev Mode is {'ON' if st.session_state['dev_mode'] else 'OFF'}")


# Getting #? OpenAI key input
# Load data from DB frist, if not available or Empty, or default, then use the st.session_state to load from their.
# print()
# and update the database columns with this information.

new_openai_key = st.text_input("OpenAI Key", value=st.session_state["openai_key"])
# Button to update the database
update_button = st.button("Update Settings")
if update_button:
    # Update the session state and the database
    st.session_state["openai_key"] = new_openai_key
    user = UserSettings(username="admin")
    user.update("dev_mode", st.session_state["dev_mode"])
    user.update("openai_key", st.session_state["openai_key"])
st.write("Session state values:")
st.write(st.session_state)
