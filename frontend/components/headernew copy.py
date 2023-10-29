from os import path
import json
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui
from components.xhelper import display_session_data
from components.xdatastore import ColorSettings
from streamlit_extras.switch_page_button import switch_page

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
    "header_row_basic": f"""
        "border": "0",
        "position": "static",
        "align-items": "center",
        "padding": "8px 20px",
        "border-bottom": "var(--te-container-border)",
        "background": "var(--te-container-bg)",
        "z-index": "21",
        "transition-duration": "0s"
    """,
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
    "button_sx_basic": f"""
        "background-color": "#1E1E1E",
        "color": "#1E1E1E",
        "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.30)",
        "&:hover": {{"backgroundColor": "#A5B4FC0A"}},
        "p": 1.0,
        "align-items": "center",
    """
}

# Initialize Session State
username = st.session_state.get("username", "admin")


def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


def load_all_configs():
    return {key: load_config(value) for key, value in CONFIG_PATHS.items()}


def check_for_logo_image(logo_path: str):
    if path.exists(logo_path):
        return Image.open(logo_path)
    st.warning("Logo image not found!")
    return None


def setup_page_config(page_name, this_wide, header_state):
    page_icon = check_for_logo_image(LOGO_PATH)
    st.set_page_config(
        page_title=f"xGPT.{page_name}",
        layout=this_wide,
        initial_header_state=header_state,
        page_icon=page_icon,
    )


def handle_click(event, item_id):
    st.session_state["menu_active_button"] = item_id


def reset_active_button_color():
    for item in menu_config:
        st.session_state[
            f"color_active_{item['name']}_button"
        ] = HEADER_STYLES["button_active"]


def header_button(menu_config, page_name):
    with elements("mainHeaderBar"):
        with mui.Box(
            bgcolor=HEADER_STYLES["container_bg_normal"],
            fullWidth=True,
        ):
            with mui.AppBar(position="static"):
                button_elements = []
                for item in menu_config:
                    if item["id"] not in ["settings", "help"]:
                        button_element = mui.Tab(
                            label=item["name"],
                            icon=getattr(mui.icon, item["icon"]),
                            onClick=handle_click,
                            sx=HEADER_STYLES["button_sx_basic"],
                        )
                        button_elements.append(button_element)
                mui.Tabs(*button_elements,
                    indicatorColor="secondary",
                    textColor="inherit",
                    variant="fullWidth",
                    ariaLabel="full width tabs example",
                )
            
            with mui.SwipeableViews(
                index={value}
                onChangeIndex={handleChangeIndex}
            ):


def create_menu(source_page):
    header_button(menu_config, source_page)
    with elements("HeaderNaviBar"):
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
menu_config, mlearning_config, tools_config, apps_config, footer_config, color_config = configs.values()

# Load color settings
db_colors = ColorSettings(username=st.session_state["username"])
db_colors.load()
