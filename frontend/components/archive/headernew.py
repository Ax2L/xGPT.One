# Imports
# ! Python libraries
from os import path
import json
from functools import partial

# ! External libraries
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui

# ? Local modules
from components.utilsnents.utilsnents.utilsnents.utils.xhelper import (
    display_session_data,
)
from components.utils.postgres.xdatastore import ColorSettings
from streamlit_extras.switch_page_button import switch_page

# ! Initialization & Configurations
# * Constants
LOGO_PATH = "images/logo/xgpt.png"
CONFIG_PATHS = {
    "menu": "../config/streamlit/menu_config.json",
    "mlearning": "../config/streamlit/mlearning_config.json",
    "tools": "../config/streamlit/tools_config.json",
    "apps": "../config/streamlit/apps_config.json",
    "footer": "../config/streamlit/footer_config.json",
    "color": "../config/streamlit/color_config.json",
}

from components import style_process

tomldata = style_process.load_styles_from_toml()
HEADERS = style_process.HEADERS

# * Header Styles
# Load STYLES from TOML file
if "style_blocks" not in st.session_state:
    style_process.store_style_block()

# * Session State
username = st.session_state.get("username", "admin")


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


for key, value in CONFIG_PATHS.items():
    if not path.exists(value):
        st.error(f"Configuration file for {key} not found at {value}")


def load_all_configs():
    return {key: load_config(value) for key, value in CONFIG_PATHS.items()}


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


# def setup_page_config(page_name, this_wide, header_state):
#    page_icon = check_for_logo_image(LOGO_PATH)
#    st.set_page_config(
#        page_title=f"xGPT.{page_name}",
#        layout=this_wide,
#        initial_sidebar_state=header_state,  # I'm assuming this was a typo
#        page_icon=page_icon,
#    )


def handle_click(item_id, idx):
    st.session_state["menu_active_button"] = item_id


def reset_active_button_color():
    for item in menu_config:
        st.session_state[f"color_active_{item['name']}_button"] = HEADERS[
            "button_active"
        ]


# & Subheader Buttons
def create_subheader_buttons(menu_item):
    """Creates the subheader buttons for the subsections."""
    subheader_elements = []
    for sub_item in menu_item.get("subheader", []):
        sub_element = mui.Button(
            label=sub_item["name"],
            onClick=partial(switch_page, sub_item["id"]),
            sx=HEADERS["submenu_button"],
        )
        subheader_elements.append(sub_element)
    # Subheader navigation
    mui.ButtonGroup(
        *subheader_elements,
        indicatorColor="primary",
        textColor="primary",
        variant="standard",
        ariaLabel="standard width tabs",
        allowScrollButtonsMobile=True,
        centered=True,
        classes="header",
        visibleScrollbar=False,
        sx=HEADERS["submenu_buttongroup"],
    )
    return subheader_elements


def handle_icon_click(icon_id, idx):
    """Handles the icon click."""
    st.session_state["icon_active"] = icon_id


# * Loading configurations
configs = load_all_configs()
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


def load_svg(svg_path: str) -> str:
    with open(svg_path, "r") as file:
        return file.read()


# ? Header functions
def header_button(menu_config):
    # ^ Header frame
    with mui.Box(
        classes="flex-container",
        bgcolor=tomldata["headers--background_color"],
        filter=tomldata["headers--filter"],
        padding=tomldata["headers--padding"],
        textAlign=tomldata["headers--text_align"],
        # sx=HEADERS["main"],
    ):
        with mui.AppBar(
            position="static",
            classes="Header",
        ):
            # ^ Logo
            with mui.Grid(
                height=tomldata["logo--height"],
                width=tomldata["logo--width"],
                ml=tomldata["logo--ml"],
                mr=tomldata["logo--mr"],
            ):
                mui.CardMedia(
                    image="https://github.com/Ax2L/xGPT.One/blob/main/frontend/static/images/logo/xgpt.png?raw=true",
                    component="img",
                    height="60",
                    width="100",
                    background="transparent",
                    # sx={
                    #    "&:hover": {"background_color": tomldata#  ["logo--background_hover"]},
                    #    **HEADERS["logo"],
                    # },
                )
                with mui.Grid():
                    button_elements = []
                    icon_elements = []
                    for idx, item in enumerate(menu_config):
                        # Central buttons
                        if item["place_center"] is not False:
                            button_element = mui.Tab(
                                label=item["name"],
                                onClick=partial(handle_click, item["place"], idx),
                                sx=HEADERS["tabs"],
                            )
                            button_elements.append(button_element)

                        # Side icons/buttons
                        if item.get("place_side"):
                            icon_n = item["icon"]
                            icon_element = mui.IconButton(
                                icon=getattr(mui.icon, icon_n),
                                classes="header",
                                color="primary",
                                onClick=partial(handle_icon_click, item["place"], idx),
                                sx={
                                    "&:hover": {"backgroundColor": "#A5B4FC0A"},
                                    **HEADERS["iconbutton"],
                                },
                            )
                            icon_elements.append(icon_element)

                        # Main header navigation
                        mui.Tabs(
                            *button_elements,
                            indicatorColor="primary",
                            textColor="primary",
                            variant="standard",
                            ariaLabel="standard width tabs",
                            allowScrollButtonsMobile=True,
                            centered=True,
                            classes="header",
                            visibleScrollbar=False,
                        )

            # Right side icons
            with mui.Box(sx={"margin-left": "auto"}):
                for icon in icon_elements:
                    mui.IconButton(
                        icon=icon,
                        sx={
                            "&:hover": {"backgroundColor": "#A5B4FC0A"},
                            **HEADERS["iconbuttongroup"],
                        },
                    )

        # Subheader navigation for each main header item
        with mui.SwipeableViews(
            axis="x",
            index=st.session_state.get("menu_active_button") or 0,
            onChangeIndex=handle_click,
        ):
            for item in menu_config:
                with mui.Box(
                    sx={
                        "p": 1,
                        "display": "flex",
                        "flex-direction": "row",
                        "align-items": "center",
                        "justify-content": "space-between",
                    }
                ):
                    # Subheader navigation
                    mui.Tabs(*create_subheader_buttons(item))


# ? Menu creation function
def create_menu(source_page):
    with elements("HeaderNaviBar"):
        header_button(menu_config)
        selected_menu_button = st.session_state.get("menu_active_button", None)
        if selected_menu_button:
            switch_page(selected_menu_button)

        # This section was adjusted to handle a potential AttributeError
        # by checking if 'display_session_data' is callable.
        try:
            if callable(display_session_data):
                with st.expander("Session States"):
                    display_session_data()
        except Exception as e:
            st.error(f"Error: {str(e)} ❌")
