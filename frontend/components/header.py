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
from components.xhelper import (
    display_session_data,
)
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
logourl="https://github.com/Ax2L/xGPT.One/blob/main/frontend/static/images/logo/xgpt.png?raw=true",

# Load CSS from JSON
with open('components/style/base.json', 'r') as file:
    data = json.load(file)

# Define a function to get common CSS for clickables
def get_clickable_css():
    return {
        "bgcolor": data["buttons"]["background_color"],
        "color": data["buttons"]["color"],
        "p": data["buttons"]["padding"],
        "textAlign": data["buttons"]["text_align"],
        "boxShadow": data["miscellaneous"]["box_shadow"]
    }

css_tabs = get_clickable_css()
css_iconbutton = get_clickable_css()
css_submenu_button = get_clickable_css()


# ^ Store "Base" values for CSS
base_colors = data["base_colors"]
typography = data["typography"]
layout = data["layout"]
header_frame = data["header_frame"]
headers = data["headers"]
sidebar = data["sidebar"]
inputs = data["inputs"]
logo = data["logo"]
submenu = data["submenu"]
buttons = data["buttons"]
containers = data["containers"]
miscellaneous = data["miscellaneous"]
# & CSS RULE DEFINITIONS -------------------------------------------------------

header_frame: {
    #"position": "fixed",
    #"display": "flex",
    #"justify-content": "space-between",
    #"align-items": "center",
    #"vertical-align": "middle",
    #"margin-top": "auto",
    #"margin-bottom": "auto",
    #"padding-top": "0 !important",
    #"margin-left": "-7px !important",
    #"margin-top": "-7px !important",
    #"top": "0 !important",
    #"left": "0 !important",
    #"right": "0 !important",
    #"min-width": "101%",
    "background-color": "#262730"
    #"z-index": "100",
}

# Instead of defining individual CSS rules, directly use values from the loaded JSON
css_header = {
    "display": data["headers"]["display"],
    "flex-direction": data["headers"]["flex_direction"],
    "align-items": data["headers"]["align_items"],
    "justify-content": data["headers"]["justify_content"]
}

css_subheader = {
    "filter": data["submenu"]["filter"],
    "p": data["submenu"]["padding"],
    "text-align": data["submenu"]["text_align"],
    "display": "flex",
    "bgcolor": data["submenu"]["background_color_active"],
    "flex-direction": "row",
    "align-items": "center",
    "justify-content": "space-between"
}

css_tabs = {
    "bgcolor": header_frame["button_bg"],
    "color": header_frame["button_color"],
    "filter": headers["filter"],
    "p": headers["padding"],
    "textAlign": headers["text_align"],
    "boxShadow": miscellaneous["box_shadow"]
}

css_tabsgroup = {
    #"bgcolor": headers["button_bg"],
    "filter": headers["filter"],
    "padding": headers["padding"],
    "text-align": headers["text_align"]
}

css_iconbutton = {
    #"bgcolor": headers["button_bg"],
    #"color": headers["button_color"],
    #"filter": headers["filter"],
    #"p": headers["padding"],
    #"text-align": headers["text_align"],
    "boxShadow": miscellaneous["box_shadow"]
}


css_iconbuttongroup = {
    #"bgcolor": headers["button_bg"],
    #"color": headers["button_color"],
    #"filter": headers["filter"],
    #"padding": headers["padding"],
    "textAlign": headers["text_align"]
}

css_submenu_button = {
    #"bgcolor": headers["button_bg"],
    #"color": headers["button_color"],
    #"filter": headers["filter"],
    #"padding": headers["padding"],
    #"text-align": headers["text_align"],
    "boxShadow": miscellaneous["box_shadow"]
}

css_submenu_buttongroup = {
    #"bgcolor": headers["button_bg"],
    #"color": headers["button_color"],
    #"filter": headers["filter"],
    #"padding": headers["padding"],
    #"textAlign": headers["text_align"],
    "boxShadow": miscellaneous["box_shadow"]
}


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
        st.session_state[f"color_active_{item['name']}_button"] = header_frame[
            "button_bg_active"
        ]

# & Subheader Buttons
def create_subheader_buttons(menu_item):
    """Creates the subheader buttons for the subsections."""
    subheader_elements = []
    for sub_item in menu_item.get("subheader", []):
        sub_element = mui.Button(
            label=sub_item["name"],
            onClick=partial(switch_page, sub_item["id"]),
            sx=css_submenu_button,
        )
        subheader_elements.append(sub_element)
    # Subheader navigation
    mui.ButtonGroup(
        *subheader_elements,
        #indicatorColor="primary",
        #textColor="primary",
        ariaLabel="standard width tabs",
        allowScrollButtonsMobile=True,
        centered=True,
        classes="header",
        visibleScrollbar=False,
        sx=css_submenu_buttongroup,
    )
    return subheader_elements

button_elements = []
icon_elements = []


def handle_icon_click(icon_id, idx):
    """Handles the icon click."""
    st.session_state["icon_active"] = icon_id


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


def load_svg(svg_path: str) -> str:
    with open(svg_path, "r") as file:
        return file.read()

def create_logo():
    """Create and display the logo."""
    with mui.Grid(
        height=logo["height"],
        width=logo["width"],
        ml=logo["ml"],
        mr=logo["mr"],
    ):
        mui.CardMedia(
            image=logourl,
            component="img",
            height=logo["height"],
            width=logo["width"],
            background=logo["bg"],
            sx={"filter": "drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4))",
                "&:hover": {"filter": "drop-shadow(3px 5px 2px rgb(255 255 255 / 0.2))",},
            },
        )


def create_tabs(menu_config):
    """Create and display the tabs."""
    button_elements = []
    for idx, item in enumerate(menu_config):
        # Central buttons
        if item["place_center"] is not False:
            button_element = mui.Tab(
                textColor="#DDDDDD",
                label=item["name"],
                onClick=partial(handle_click, item["id"], idx),
                sx={
                    **css_tabs,
                    "&:hover": {"background-color": data["header_frame"]["button_bg_hover"]}
                }
            )
            button_elements.append(button_element)
    with mui.Grid():
        mui.Tabs(
            *button_elements,
            textColor="secondary",
            indicatorColor="secondary",
            ariaLabel="secondary tabs",
            allowScrollButtonsMobile=True,
            centered=True,
            classes="header",
            visibleScrollbar=False,
        )


def create_icon_buttons(menu_config):
    """Create and display the icon buttons."""
    icon_elements = []
    for idx, item in enumerate(menu_config):
        # Side icons/buttons
        if item.get("place_side"):
            icon_n = item["icon"]
            icon_element = mui.IconButton(
                icon=getattr(mui.icon, icon_n),
                classes="iconbutton",
                edge="end",
                size="medium",
                iconColor=headers["border_color"],
                onClick=partial(handle_icon_click, item["place"], idx),
                sx={
                    "&:hover": {"background-color": base_colors["secondary_hover"]},
                    **css_iconbutton,
                },
            )
            icon_elements.append(icon_element)
    with mui.Grid():

        with mui.Toolbar():
            for icon in icon_elements:
                mui.IconButton(icon=icon)


# ? Header functions
def header_button(menu_config):
    # ^ Header frame
    with mui.Box(
        classes="flexcontainer",
        #display=header_frame["display"],
        #justifyContent=header_frame["justify_content"],
        #height=header_frame["height"],
        flexGrow=1,
        #sx={
        #    "bgcolor": header_frame["background_color"],
        #}
    ):
        with mui.AppBar(
            #position="flex",
            position="static",
            classes="headerapp",
            #fullWidth="100%",
            #sx={"width": "100%"},
            fullWidth="100%",
            p=1,
            sx={
                "bgcolor": header_frame["background_color"],
            }
        ):
            with mui.Grid(
                container=True, 
                spacing=3, 
                    sx={
                    "bgcolor": header_frame["background_color"],
                    "pt": 2.5,
                    "display": "flex",
                    "flex-direction": "row",
                    "align-items": "center",
                    "justify-content": "space-between",
                }
            ):
                create_logo()
                create_tabs(menu_config)
                create_icon_buttons(menu_config)

            # Subheader navigation for each main header item
    with mui.SwipeableViews(
        index=st.session_state.get("menu_active_button") or 0,
        onChangeIndex=handle_click,
    ):
        mui.Typography("Hello world"),
        for item in menu_config:
            with mui.AppBar(
                classes="subheader",
                fullWidth="100%",
                p=1,
                sx={
                    "display": "flex",
                    "bgcolor": submenu["background_color"],
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
            st.text(f"Selected button: {selected_menu_button}"),
            #switch_page(selected_menu_button)

        # This section was adjusted to handle a potential AttributeError
        # by checking if 'display_session_data' is callable.
        try:
            if callable(display_session_data):
                with st.expander("Session States"):
                    display_session_data()
        except Exception as e:
            st.error(f"Error: {str(e)} ❌")
