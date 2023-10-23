# components/xlayout.py

import os
import json
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui, sync, html
from components.xhelper import display_session_data
from components.xdatastore import UserSettings, PageSettings, ColorSettings

# & === SET COMPONENT PARAMETER =====================
username = "admin"
try:
    username = st.session_state["username"]
except Exception as e:
    st.error(f"Error: {str(e)} ❌")


# & === CONFIG SECTION =====================
LOGO_PATH = "images/logo/logo_long.png"
CONFIG_PATHS = {
    "menu": "../config/streamlit/menu_config.json",
    "mlearning": "../config/streamlit/mlearning_config.json",
    "tools": "../config/streamlit/tools_config.json",
    "apps": "../config/streamlit/apps_config.json",
    "footer": "../config/streamlit/footer_config.json",
    "color": "../config/streamlit/color_config.json",
}
# ⁡⁢⁣⁣===| DATABASE SECTION |=========================================⁡
# Store DB Data
db_colors = ColorSettings(username=st.session_state["username"])
db_colors.load()


def load_config(path: str) -> dict:
    """
    Loads configuration data from a given path.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return None


def load_all_configs():
    """Loads all the necessary configuration files."""
    return {key: load_config(value) for key, value in CONFIG_PATHS.items()}


configs = load_all_configs()
(
    menu_config,
    mlearning_config,
    tools_config,
    apps_config,
    footer_config,
    color_config,
) = configs.values()


def check_for_logo_image(logo_path: str):
    """Checks for the existence of the logo image and returns it."""
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    st.warning("Logo image not found!")
    return None


image = check_for_logo_image(LOGO_PATH)


def change_page_extended(next_page):
    """Changes the current page."""
    try:
        st.session_state.setdefault("current_page", next_page)
        next_page_short = next_page.lower().replace("_page", "")
        st.session_state["current_page"] = next_page_short
        # TODO: CHANGE PAGE
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")


def gen_toggle(db_data, column, label):
    # Check if update is needed
    if st.session_state[column] != db_data.data.get(column) and not None:
        
        # Update the correct boolean Status
        if st.session_state[column]:
            db_data.update(column, False)
            st.toast(body="Database update successful")
        else:
            db_data.update(column, True)
            st.toast(body="Database update successful")



def sync_db_session(table, column):
    init_indicator = f"{column}_init"
    # load initialy DB Values
    if init_indicator not in st.session_state:
        # Run initial load from DB
        st.session_state[column] = table.data.get(column)
        st.session_state[init_indicator] = True
    else:
        table.monitor(column)


# * === Menu Content Box ---------------> Settings

def settings_box():
    """Renders the settings box in the sidebar."""
    st.header("Settings")

    with elements("Settings"):
        user = UserSettings(username=st.session_state["username"])
        user.load()
        page_config = PageSettings(username=st.session_state["username"])
        page_config.load()

        # Callback functions:
        # Save change in Session State
        def handle_change(event):
            st.session_state.openai_key = event.target.value

        # Save change in Session State when clicked
        def handle_boolean(table, column):
            def wrapper(event):
                # Swap the boolean status
                st.session_state[column] = not st.session_state[column]
                # Check
                if table == "user":
                    user.update(column, st.session_state[column])
                if table == "page_config":
                    page_config.update(column, st.session_state[column])

            return wrapper

        # List settings
        mui.List(
            # `Input` for (OpenAI Key)
            mui.ListItem(
                mui.TextField(
                    label="OpenAI Key",
                    value=st.session_state["openai_key"],
                    onChange=handle_change,
                    sx={
                        "min-width": "100%",
                    },
                ),
                width="100%"
            ),
            # Toggle for Developer View (enabled everything)
            mui.ListItem(
                mui.ListItemText(
                    "switch-list-label-dev_mode_switch", primary="Developer Mode"
                ),
                mui.Switch(
                    "dev_mode_switch",
                    onChange=handle_boolean("user", "dev_mode"),
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
                    onChange=handle_boolean("page_config", "show_session_data"),
                    inputProps=(
                        "aria-labelledby",
                        "switch-list-label-show_session_data",
                    ),
                ),
            ),
        )



def settings_box_Old():
    """Renders the settings box in the sidebar."""
    st.header("Settings")

    try:
        # Using a button for #? Dev Mode
        # dev_mode = st.empty()
        # dev_mode_disabled = dev_mode.button(f"Dev-view disabled",type="secondary",help="This is help")
        # if dev_mode_disabled:
        #    dev_mode = st.empty()
        #    dev_mode_disabled = dev_mode.button('Dev-view enabled', type="secondary", help="help here")
        #    st.session_state["dev_mode"] = not st.session_state["dev_mode"]
        # st.write(f"Dev Mode is {'ON' if st.session_state['dev_mode'] else 'OFF'}")

        #
        #
        ## Using a button for #? Session State
        # session_states_button = st.button("Show session-states")
        # if session_states_button:
        #    st.session_state["show_session_state"] = not st.session_state["show_session_state"]
        # st.write(f"Show Session States is {'ON' if st.session_state['show_session_state'] else 'OFF'}")
        # Load Postgres data.
        user = UserSettings(username=st.session_state["username"])
        user.load()
        page_config = PageSettings(username=st.session_state["username"])
        page_config.load()
        #! Test:
        gen_toggle(user, "dev_mode", "Developer Mode")
        gen_toggle(page_config, "show_session_data", "Show Session Data")

        # Getting #? OpenAI key input
        new_openai_key = st.text_input(
            "OpenAI Key", value=st.session_state["openai_key"]
        )
        # Button to update the database
        update_button = st.button("Update Settings")
        if update_button:
            # Update the session state and the database
            st.session_state["openai_key"] = new_openai_key
            user.update("dev_mode", st.session_state["dev_mode"])
            user.update("openai_key", st.session_state["openai_key"])
        st.write("Session state values:")
        st.write(st.session_state)
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")

    # try:
    #    # Using a button for #? Dev Mode
    #    dev_mode_button = st.button("Toggle Dev Mode")
    #    if dev_mode_button:
    #        st.session_state["dev_mode"] = not st.session_state["dev_mode"]
    #    st.write(f"Dev Mode is {'ON' if st.session_state['dev_mode'] else 'OFF'}")

    #    # Getting #? OpenAI key input
    #    openai_key = st.text_input("OpenAI Key", value=st.session_state["openai_key"])
    #    # Button to update the database
    #    update_button = st.button("Update Settings")
    #    if update_button:
    #        # Update the session state and the database
    #        st.session_state["openai_key"] = openai_key
    #        user = UserSettings(username="admin")
    #        user.update("dev_mode", st.session_state["dev_mode"])
    #        user.update("openai_key", st.session_state["openai_key"])
    #    st.write("Session state values:")
    #    st.write(st.session_state)

    # except Exception as e:
    #    st.error(f"Error: {str(e)} ❌")
    # try:
    #    # Send data and excecute
    #    if st.form_submit_button("Update", on_click=update_user_settings):
    #        st.success("Settings updated successfully!")

    # except Exception as e:
    #    st.error(f"Error: {str(e)} ❌")


# * === Menu Content Box ---------------> Datastore


def datastore_box():
    """Renders the datastore box in the sidebar."""
    # Title and Explanation
    st.markdown("## Datastore Tools")
    st.markdown(
        "Here, manage your **local files** and get an overview of "
        "the **Vector Database** using Attu and Milvus. "
        "_Further explanations and guides will be added soon._"
    )
    # Local Files Section
    with st.expander("Local Files"):
        st.markdown("Browse, upload, or manage your local files seamlessly.")
        if st.button("Open Filebrowser"):
            change_page_extended("data_file_manager")
    # Vector Database Section
    with st.expander("Vector Database (Milvus)"):
        st.markdown(
            "Utilize **Attu** to get an overview of Milvus. The default "
            "user credentials are configured in the `docker-compose` file and are as follows:\n"
            "- **Username:** minioadmin\n"
            "- **Password:** minioadmin\n\n"
            "_The configuration file path:_\n"
            "`helper/docker/docker-compose-db.yaml`"
        )
        # Note: Streamlit does not support `on_click` URL redirect via button yet.
        # Using `st.markdown` to create a hyperlink.
        st.markdown(
            "[Open Milvus Dashboard](https://localhost:8181)",
            unsafe_allow_html=True,
        )
    # Postgres
    with st.expander("Postgresql"):
        st.markdown("Modify, upload, or delete your chat-data seamlessly.")


# * === Menu Content Box ---------------> Apps, MLearning, Tools

def create_missing_states(name, value):
    if name not in st.session_state:
        st.session_state.setdefault(name, value)

def reset_active_card_color():
    # configs_list = [apps_config,mlearning_config,tools_config]
    default_card_background = "#1E1E1E"
    # for config in configs_list:
    try:
        for item in apps_config:
            st.session_state[
                f"color_active_{item['name']}_card"
            ] = default_card_background
    except Exception as e:
        print(f"Error: {e}")
    try:
        for item in mlearning_config:
            st.session_state[
                f"color_active_{item['name']}_card"
            ] = default_card_background
    except Exception as e:
        print(f"Error: {e}")
    try:
        for item in tools_config:
            st.session_state[
                f"color_active_{item['name']}_card"
            ] = default_card_background
    except Exception as e:
        print(f"Error: {e}")


def handle_click_card(name):  # Modified to take 'name' argument
    def wrapper(event):
        clicked = name
        reset_active_card_color()
        st.session_state[f"color_active_{clicked}_card"] = next(
            (item["active_color"] for item in menu_config if item["name"] == clicked),
            "#4F378B",
        )
        st.session_state["current_page"] = clicked
        st.session_state["active_section"] = clicked

    return wrapper


def cards_box(config, config_name):
    # Generate cards for each category in the configuration
    for category in config["categories"]:
        # Generate buttons for each app in the category
        for app in category[config_name]:
            create_app_card(app)


def create_app_card(app):
    create_missing_states(f"color_active_{app['page_name']}_card", "#1E1E1E")
    with mui.Paper(
        elevation={3},
        sx={
            "p": 1.5,
            "mb": 0.8,
            "bgcolor": app["color"],
            "background": f"linear-gradient(90deg, {app['color']}, 17%, rgba(0,0,0,0) 17%), linear-gradient(180deg, #243B55 50%, #141E30 50%)",
            "background": st.session_state[f"color_active_{app['page_name']}_card"],
            "cursor": "pointer",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
            "&:hover": {
                "backgroundColor": "#A5B4FC0A",  # Button hover effect
            },
        },
        onClick=handle_click_card(app["page_name"]),
        # onClick=lambda: st.session_state.update({"selected_page": app["page_name"]}),
    ):
        with mui.Grid(
            container=True,
            direction="row",
            justifyContent="start",
            wrap="nowrap",
            sx={},
        ):
            # Icon section
            with mui.Grid(item=True, xs={2}):
                getattr(mui.icon, app["icon"])(
                    sx={
                        "min-height": "100%",
                        "color": {app["color"]},
                    }
                )

            # Title and Description section
            with mui.Grid(item=True, xs={12}):
                # Title
                mui.Typography(
                    app["title"],
                    sx={
                        "margin-top": "-5px",
                        "padding-left": "10px",
                        "fontSize": "1rem",
                        "font-weight": "bold",
                        "color": {app["color"]},
                        "text-shadow": "2px 2px 4px #000000",
                    },
                )
                # Description
                mui.Typography(
                    app["description"],
                    sx={
                        "padding-left": "10px",
                        "fontSize": "0.8rem",
                        "filter": "brightness(150%)",
                        "color": "#F9F9F9",
                        "mt": 0,
                        "text-shadow": "2px 2px 4px #000000",
                    },
                )


# * === Main === Menu Button Group (2.Row) ===


def reset_active_button_color():
    for item in menu_config:
        st.session_state[f"color_active_{item['name']}_button"] = "#1E1E1E"
    for item in footer_config:
        st.session_state[f"color_active_{item['name']}_button"] = "#1E1E1E"


def handle_click_universal(name):  # Modified to take 'name' argument
    def wrapper(event):
        clicked = name
        reset_active_button_color()
        st.session_state[f"color_active_{clicked}_button"] = next(
            (item["active_color"] for item in menu_config if item["name"] == clicked),
            "#4F378B",
        )
        st.session_state["menu_active_button"] = clicked
        st.session_state["active_section"] = clicked

    return wrapper


def handle_click_close():  # Modified to take 'name' argument
    def wrapper(event):
        reset_active_button_color()
        st.session_state["menu_active_button"] = None
        st.session_state["active_section"] = None

    return wrapper


def sidebar_header_button(menu_config):
    with st.sidebar:
        with elements("sideMenuHeader"):
            """Generate Header Section icons."""
            mui.CardMedia(
                image="https://github.com/Ax2L/xGPT.One/blob/main/frontend/images/logo/logo_sidebar.png?raw=true",
                component="img",
                height="80",
                width="100",
                background="transparent",
                sx={
                    "max-height": "50",
                    "max-width": "50",
                    "margin-bottom": "10px",
                    "margin-top": "-10px",
                },
            )
            mui.Divider()
            with mui.Grid(
                container=True,
                direction="row",
                justifyContent="space-between",
                alignItems="center",
                spacing={1},
            ):
                # ? Main buttonsGroup row for Menu
                button_elements = []
                for item in menu_config:
                    if item["name"] not in ["settings", "help"]:
                        icon_n = item["icon"]
                        button_element = mui.Button(
                            getattr(mui.icon, icon_n),
                            onClick=handle_click_universal(item["name"]),
                            sx={
                                "background-color": st.session_state[
                                    f"color_active_{item['name']}_button"
                                ],
                                "color": item["color"],
                                "width": "100%",
                                "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
                                "&:hover": {
                                    "backgroundColor": "#A5B4FC0A",  # Button hover effect
                                },
                            },
                        )
                        button_elements.append(button_element)
                mui.ButtonGroup(
                    *button_elements,
                    variant="outlines",
                    label="outlined primary button group",
                    size="medium",
                    sx={
                        "width": "100%",
                        "margin-left": "auto",
                        "margin-right": "auto",
                        "align-items": "center",
                    },
                )
                if st.session_state["menu_active_button"] is not None:
                    mui.IconButton(
                        mui.icon.Close,
                        onClick=handle_click_close(),
                        sx={
                            "color": item["color"],
                            "margin-left": "80%",
                            "width": "20%",
                            "&:hover": {
                                "color": "#000000",
                            },
                        },
                    )


# * === Sidebar Bottom ---------------> Settings, Upload, Help


def sidebar_footer_button(footer_config):
    with st.sidebar:
        with elements("sidebarFooter"):
            button_elements = []
            for item in footer_config:
                # Assuming that item['icon'] is a string, e.g., 'RestoreIcon'
                # We need to retrieve the actual icon component from the mui.icons module
                icon_n = item["icon"]
                icon_component = getattr(mui.icon, icon_n)()

                button_element = mui.BottomNavigationAction(
                    icon=icon_component,  # This is the corrected part
                    label=item["name"],
                    value=item["name"],
                    onClick=handle_click_universal(item["name"]),
                    sx={
                        "background-color": st.session_state[
                            f"color_active_{item['name']}_button"
                        ],
                        "color": item["color"],
                        "&:hover": {
                            "backgroundColor": "rgba(255, 255, 255, 0.12)",  # Button hover effect
                        },
                    },
                )
                button_elements.append(button_element)

            mui.BottomNavigation(
                *button_elements,
                variant="contained",
                label="outlined primary footer button group",
                size="small",
                sx={
                    "width": "100%",
                    "margin-left": "auto",
                    "margin-right": "auto",
                    "bottom": "0 !important",
                    "align-items": "center",
                    "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
                },
            )


# * === Main ---------------> Runner
def create_menu(source_page):
    # Need to create the sidebar menu buttons and save the clicked one.
    # Call the function
    sidebar_header_button(menu_config)
    sidebar_footer_button(footer_config)
    with st.sidebar:
        with elements("sideMenuContent"):
            menu = st.session_state.menu_active_button
            # need to check if a button was pressed and process the selected action.
            selected_menu_button = st.session_state["menu_active_button"]

            if menu == "settings":
                settings_box()

            elif menu == "help":
                settings_box()

            elif menu == "datastore":
                datastore_box()

            elif menu == "apps":
                cards_box(apps_config, "apps")

            elif menu == "mlearning":
                cards_box(mlearning_config, "mlearning")

            elif menu == "tools":
                cards_box(tools_config, "tools")

            # need to check if a button was pressed and process the selected action.
            selected_menu_button = st.session_state["menu_active_button"]

            if selected_menu_button != source_page and selected_menu_button:
                do = "nothing"
                # st.write(f"OLALA You pressed the buttonue: {selected_menu_button}")
            else:
                do = "nothing"
                # st.write("No butonnue is seletectabled.")
    try:
        if display_session_data:
            with st.expander("Session States"):
                display_session_data()
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")
