# Imports
# ! Python libraries
import os
import re
from os import path
import json
from functools import partial
import numpy as np
import pandas as pd
import toml

# ! External libraries
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui

# ? Local modules
from components.xhelper import display_session_data, load_styles_from_toml, get_styles_toml_path
from components.xdatastore import ColorSettings
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


# * Header Styles
# Load STYLES from TOML file
if "base_style" not in st.session_state:
    st.session_state.base_style = ""    
STYLES = load_styles_from_toml()
print(f"{STYLES}")

# Session State
username = st.session_state.get("username", "admin")

# Cache the data
@st.cache_data
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}

# * Session State
username = st.session_state.get("username", "admin")


@st.cache_data
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


# ! Functions
# ? Helper functions
@st.cache_data
def check_for_logo_image(logo_path: str):
    if path.exists(logo_path):
        return Image.open(logo_path)
    st.warning("Logo image not found!")
    return None


def load_all_configs():
    return {key: load_config(value) for key, value in CONFIG_PATHS.items()}


def setup_page_config(page_name, this_wide, header_state):
    page_icon = check_for_logo_image(LOGO_PATH)
    st.set_page_config(
        page_title=f"xGPT.{page_name}",
        layout=this_wide,
        initial_sidebar_state=header_state,  # I'm assuming this was a typo
        page_icon=page_icon,
    )


def handle_click(item_id, idx):
    st.session_state["menu_active_button"] = item_id


def reset_active_button_color():
    for item in menu_config:
        st.session_state[f"color_active_{item['name']}_button"] = HEADER_STYLES[
            "button_active"
        ]


def create_subheader_buttons(menu_item):
    """Creates the subheader buttons for the subsections."""
    subheader_elements = []
    for sub_item in menu_item.get("subheader", []):
        sub_element = mui.Button(
            label=sub_item["name"],
            onClick=partial(switch_page, sub_item["id"]),
            sx=HEADER_STYLES["button_sx_basic"],
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
        sx=HEADER_STYLES["button_group_basic"],
    )
    return subheader_elements


def handle_icon_click(icon_id, idx):
    """Handles the icon click."""
    st.session_state["icon_active"] = icon_id


def load_svg(svg_path: str) -> str:
    with open(svg_path, "r") as file:
        return file.read()


# ? Header functions
def header_button(menu_config, page_name):
    # ^ Header frame
    with mui.Box(
        bgcolor=HEADER_STYLES.get(
            ".container_bg_normal--background-color", "#334155"
        ),  # Fallback to default color if key is not found
        fullWidth=True,
        sx=HEADER_STYLES["header"],
    ):
        # ^ Logo
        with mui.Grid(height="60", width="100"):
            mui.CardMedia(
                image="https://github.com/Ax2L/xGPT.One/blob/main/frontend/static/images/logo/xgpt.png?raw=true",
                component="img",
                height="60",
                width="100",
                background="transparent",
            )
        # ^ Tabs (central buttons)
        button_elements = []
        for idx, item in enumerate(menu_config):
            if item["place_center"] is not False:
                button_element = mui.Tab(
                    label=item["name"],
                    onClick=partial(handle_click, item["place"], idx),
                    sx={
                        "&:hover": {"backgroundColor": "#A5B4FC0A"},
                        **HEADER_STYLES["button_sx_basic"],
                    },
                )
                button_elements.append(button_element)
        # combine to TabsBar
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
        # ^ Right side icons
        icon_elements = []
        for idx, item in enumerate(menu_config):
            if item.get("place_side"):
                icon_n = item["icon"]
                icon_element = mui.IconButton(
                    icon=getattr(mui.icon, icon_n),
                    classes="header",
                    color="primary",
                    onClick=partial(handle_icon_click, item["place"], idx),
                    sx={
                        "&:hover": {
                            "backgroundColor": HEADER_STYLES.get(
                                ":root--base-danger", "#FF0000"
                            )
                        },
                        **HEADER_STYLES["button_sx_basic"],
                    },
                )
                icon_elements.append(icon_element)
        # combine to group
        with mui.Box(sx={"display": "flex"}):
            for icon in icon_elements:
                mui.IconButton(
                    icon=icon,
                    sx={
                        "&:hover": {
                            "backgroundColor": HEADER_STYLES.get(
                                ":root--base-danger", "#FF0000"
                            )
                        },
                        **HEADER_STYLES["button_sx_basic"],
                    },
                )
    # ^ Subheader navigation for each main header item
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
    # header_button(menu_config, source_page)
    with elements("HeaderNaviBar"):
        header_button(menu_config, source_page)
        selected_menu_button = st.session_state.get("menu_active_button", None)
        if selected_menu_button:
            switch_page(selected_menu_button)
    try:
        if display_session_data:
            with st.expander("Session States"):
                display_session_data()
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")


# ! Main Execution
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
