from os import path
import json
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui
from components.xhelper import display_session_data
from components.xdatastore import ColorSettings
from streamlit_extras.switch_page_button import switch_page
from functools import partial
import numpy as np
import pandas as pd
import streamlit as st


# Global Constants
LOGO_PATH = "images/logo/xgpt.png"
CONFIG_PATHS = {
    "menu": "../config/streamlit/menu_config.json",
    "mlearning": "../config/streamlit/mlearning_config.json",
    "tools": "../config/streamlit/tools_config.json",
    "apps": "../config/streamlit/apps_config.json",
    "footer": "../config/streamlit/footer_config.json",
    "color": "../config/streamlit/color_config.json",
}

# Header Styles
HEADER_STYLES = {
    "header_row_basic": {
        "border": "0",
        "position": "static",
        "align-items": "center",
        "padding": "8px 20px",
        "border-bottom": "var(--te-container-border)",
        "background": "var(--te-container-bg)",
        "z-index": "21",
        "transition-duration": "0s",
        "top": "0",
        "float": "left",
        "display": "block",
        "color": "white",
        "text-align": "center",
        "text-decoration": "none",
    },
    "container_bg_normal": "#334155",
    "container_bg_hover": "#A5B4FC0A",
    "button_box_shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
    "button_normal": "#1E1E1E",
    "button_hover": "#A5B4FC0A",
    "button_click": "#4F378B",
    "button_active": "#1E1E1E",
    "button_bg_normal": "#334155",
    "button_bg_hover": "#A5B4FC0A",
    "button_bg_active": "#4F378B",
    "button_sx_basic": {
        "background-color": "#1E1E1E",
        "color": "#FFFFFF",  # changed to white for visibility
        "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
        "p": 1.0,
        "align-items": "center",
    },
    "button_icon_basic": {
        "background-color": "#1E1E1E",
        "color": "#FFFFFF",  # changed to white for visibility
        "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
        "p": 1.0,
        "align-items": "center",
    },
    "logo_sx": {
        "height": "48px",
        "margin-right": "16px",
    },
}

# Initialize Session State
username = st.session_state.get("username", "admin")


@st.cache_data
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


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
    )
    return subheader_elements


def handle_icon_click(icon_id, idx):
    """Handles the icon click."""
    st.session_state["icon_active"] = icon_id


def load_svg(svg_path: str) -> str:
    with open(svg_path, "r") as file:
        return file.read()

def header_button(menu_config, page_name):
    with mui.Box(
        bgcolor=HEADER_STYLES["container_bg_normal"],
        fullWidth=True,
        sx={
            "display": "flex", 
            "justifyContent": "space-between", 
            "alignItems": "center"
        }
    ):
        # Logo
        mui.CardMedia(
            image="../static/images/logo/xgpt.png",
            component="img",
            height="150",
            width="50",
            background="transparent",
        )
        
        # Tabs (central buttons)
        button_elements = []
        for idx, item in enumerate(menu_config):
            if item["place_center"] is not False:
                button_element = mui.Tab(
                    label=item["name"],
                    onClick=partial(handle_click, item["place"], idx),
                    sx=HEADER_STYLES["button_sx_basic"],
                )
                button_elements.append(button_element)
        
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
                        "&:hover": {"backgroundColor": "#A5B4FC0A"},
                        **HEADER_STYLES["button_sx_basic"],
                    },
                )
                icon_elements.append(icon_element)
                
        with mui.Box(sx={"display": "flex"}): 
            for icon in icon_elements:
                mui.IconButton(
                    icon=icon,
                    sx={
                        "&:hover": {"backgroundColor": "#A5B4FC0A"},
                        **HEADER_STYLES["button_icon_basic"],
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


# Load configurations
configs = load_all_configs()
(
    menu_config,
    mlearning_config,
    tools_config,
    apps_config,
    footer_config,
    color_config,
) = configs.values()

# Load color settings
db_colors = ColorSettings(username=st.session_state["username"])
db_colors.load()
