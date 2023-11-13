import streamlit as st
from streamlit_elements import elements, mui


# * === Menu Content Box ---------------> Settings


def settings_box():
    """Renders the settings box in the header."""
    st.header("Settings")

    with elements("Settings"):
        if "input_openai_key" not in st.session_state:
            st.session_state.input_openai_key = ""
        user = UserSettings(username=st.session_state["username"])
        user.load()
        page_config = PageSettings(username=st.session_state["username"])
        page_config.load()
        if "openaik" not in st.session_state:
            st.session_state.openaik = user.data.get("openai_key")

        def update_changes():
            def wrapper(event):
                try:
                    # Ensure the existence of session state variables
                    st.session_state.setdefault("dev_mode", False)
                    st.session_state.setdefault("show_session_data", False)

                    # ? `openai_key`______________________________________
                    user.update(
                        "openai_key", st.session_state["openaik"]
                    )  # Update the database

                    # ? `dev_mode`________________________________________
                    user.update("dev_mode", bool(st.session_state["dev_mode"]))

                    # ? `show_session_data`_______________________________
                    page_config.update(
                        "show_session_data", bool(st.session_state["show_session_data"])
                    )
                    st.toast(':green["Changes saved!"]')
                except Exception as e:
                    st.error(f"Error: {str(e)} ❌")
                    st.toast(f":red[Error: {str(e)} ❌")

            return wrapper  # Invoke the inner function

        # Save change in Session State when clicked
        def handle_boolean(column):
            def wrapper(event):
                # Swap the boolean status
                st.session_state[column] = not st.session_state[column]

            return wrapper

        # * Settings Material Section

        def handle_change():
            def wrapper(event):
                st.session_state.openaik = event.target.value

            return wrapper  # Invoke the inner function

        mui.List(
            # `Input` for (OpenAI Key)
            mui.ListItem(
                mui.TextField(
                    label="OpenAI Key",
                    value=st.session_state.openaik,
                    onChange=handle_change(),
                    placeholder="Enter OpenAI-Key",
                    type="password",
                    sx={
                        "min-width": "100%",
                    },
                ),
                width="100%",
            ),
            # Toggle for Developer View (enabled everything)
            mui.ListItem(
                mui.ListItemText(
                    "switch-list-label-dev_mode_switch", primary="Developer Mode"
                ),
                mui.Switch(
                    "dev_mode_switch",
                    onChange=handle_boolean("dev_mode"),
                    inputProps=("aria-labelledby", "switch-list-label-dev_mode_switch"),
                ),
            ),
            # `Switch` for Session Data View (Display the current Session)
            mui.ListItem(
                mui.ListItemText(
                    "switch-list-label-show_session_data", primary="Show Session Data"
                ),
                mui.Switch(
                    "show_session_data_switch",
                    onChange=handle_boolean("show_session_data"),
                    inputProps=(
                        "aria-labelledby",
                        "switch-list-label-show_session_data",
                    ),
                ),
            ),
            # `Save changes` Button
            mui.ListItem(
                mui.ListItemButton(
                    "Save changes",
                    alignItems="center",
                    sx={
                        "p": 1.5,
                        "mb": 0.8,
                        # "bgcolor": app["color"],
                        # "background": f"linear-gradient(90deg, {app['color']}, 17%, rgba(0,0,0,0) 17%), linear-gradient     (180deg, #243B55 50%, #141E30 50%)",
                        "cursor": "pointer",
                        "display": "flex",
                        "flex-direction": "column",
                        "align-items": "center",
                        "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
                        "&:hover": {
                            "backgroundColor": "#A5B4FC0A",  # Button hover effect
                        },
                    },
                    onClick=update_changes(),
                ),
            ),
        )
