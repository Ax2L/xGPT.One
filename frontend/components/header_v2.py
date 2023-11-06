# Imports
# ! Python libraries
from os import path
import json
from functools import partial

# ! External libraries
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui
from streamlit_extras.switch_page_button import switch_page

# ? Local modules
from components.style import stylebase as sb
from components.xdatastore import ColorSettings
from components.xhelper import display_session_data, check_logged_in

# ! Initialization & Configurations
# * Constants
LOGO_PATH = "../resources/images/logo/favicon.ico"
CONFIG_PATHS = {
    "menu": "../config/streamlit/menu_config.json",
    "mlearning": "../config/streamlit/mlearning_config.json",
    "tools": "../config/streamlit/tools_config.json",
    "apps": "../config/streamlit/apps_config.json",
    "footer": "../config/streamlit/footer_config.json",
    "color": "../config/streamlit/color_config.json",
}
logourl = ("http://127.0.0.1:8334/data/images/logo/android-chrome-512x512.png",)


# ! Functions
# ? Helper functions
@st.cache_data
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


def load_configs(config_paths):
    configs = {}
    for key, value in config_paths.items():
        if not path.exists(value):
            st.error(f"Configuration file for {key} not found at {value}")
        else:
            configs[key] = load_config(value)
    return configs


# Use the function to load all configs
configs = load_configs(CONFIG_PATHS)
# * Loading configurations
(
    menu_config,
    mlearning_config,
    tools_config,
    apps_config,
    footer_config,
    color_config,
) = configs.values()
# * Loading color settings
db_colors = ColorSettings(username=st.session_state["username"])
db_colors.load()

# & FUNCTIONS -------------------------------------------------------


# ? Helper functions
@st.cache_data
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


def load_configs(config_paths):
    configs = {}
    for key, value in config_paths.items():
        if not path.exists(value):
            st.error(f"Configuration file for {key} not found at {value}")
        else:
            configs[key] = load_config(value)
    return configs


for key, value in CONFIG_PATHS.items():
    if not path.exists(value):
        st.error(f"Configuration file for {key} not found at {value}")


def check_for_logo_image(logo_path: str):
    """Checks for the existence of the logo image and returns it."""
    if path.exists(logo_path):
        return Image.open(logo_path)
    st.warning("Logo image not found!")
    return None


def change_page_extended(next_page):
    """Changes the current page."""
    try:
        st.session_state.setdefault("current_page", next_page)
        next_page_short = next_page.lower().replace("_page", "")
        st.session_state["current_page"] = next_page_short
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")


def update_menu(item_id, idx):
    st.session_state["menu_active_button"] = item_id


def update_submenu(item_id, idx):
    st.session_state["submenu_active_button"] = item_id


def handle_icon_click(icon_id, idx):
    """Handles the icon click."""
    st.session_state["icon_active"] = icon_id


def reset_active_button_color():
    for item in menu_config:
        st.session_state[f"color_active_{item['name']}_button"] = sb.button["Hover"]


# ^ MAIN PROCESS -------------------------------------------------------


# ^ LOGO
def create_logo():
    """Create and display the logo."""
    with mui.Grid(height=50, width=60, ml="70px", mr="-70px"):
        mui.CardMedia(
            image=logourl,
            component="img",
            bg="transparent",
            height=50,
            width=60,
            ml="70px",
            mr="-70px",
            sx={
                "filter": "drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4))",
                "&:hover": {
                    "filter": "drop-shadow(3px 5px 2px rgb(255 255 255 / 0.2))"
                },
            },
        )


# ^ HEADER TABS
def create_tabs(menu_config):
    """Create and display the tabs."""
    button_elements = []
    for idx, item in enumerate(menu_config):
        # Central buttons
        if item["place_center"] is not False:
            button_element = mui.Tab(
                # textColor="#DDDDDD",
                label=item["name"],
                onClick=partial(update_menu, item["id"], idx),
            )
            button_elements.append(button_element)
    with mui.Grid():
        mui.Tabs(
            *button_elements,
            role="fullWidth",
            variant="normal",
            textColor="primary",
            indicatorColor="primary",
            ariaLabel="full width tabs",
            allowScrollButtonsMobile=False,
            centered=True,
            classes="header",
            visibleScrollbar=False,
        )


# ^ HEADER EXTRA BUTTON
def create_icon_buttons(menu_config):
    """Create and display the icon buttons."""
    icon_elements = []
    with mui.Grid():
        mui.Typography("Searchbar and buttons")


# ? Header functions
def header_navbar(menu_config):
    # ^ Header frame
    with mui.Box(
        classes="flexcontainer",
        flexGrow=1,
    ):
        with mui.AppBar(
            # position="flex",
            classes="headerapp",
            visibleScrollbar=False,
            p=1,
            sx=sb.header_special,
        ):
            with mui.Grid(
                container=True,
                spacing=3,
                visibleScrollbar=False,
                sx={"justify-content": "space-between"},
            ):
                create_logo()
                create_tabs(menu_config)
                create_icon_buttons(menu_config)


# ? Submenu functions
def submenu_navbar(submenu_config):
    with mui.SwipeableViews(
        axis="x",
        index=submenu_config["place"],
        onChangeIndex=update_menu,
    ):
        mui.Typography("Submenu")


# ? Menu creation function
def create_menu():
    # todo Just a Header NaviBar with Tabs
    with elements("HeaderNaviBar"):
        header_navbar(menu_config)
        ## todo: SwipeableViewsas Subnmenubar, direct under the Navibar and flex.
        # selected_menu_button = st.session_state.get("menu_active_button", 0)
        # if selected_menu_button:
        #    for item in menu_config:
        #        if item["id"] == selected_menu_button:
        #            st.text(f"Selected button: {selected_menu_button}")
        #            submenu_navbar(item)
        # todo: Buttons in Submenu to change the page.


def init(page):
    check_logged_in(page)
    create_menu()
