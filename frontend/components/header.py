# components/xlayout.py

from os import path
import json
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui
from components.xhelper import display_session_data
from components.xdatastore import ColorSettings
from streamlit_extras.switch_page_button import switch_page

# ===== GLOBAL CONSTANTS =============================================
LOGO_PATH = "images/logo/xgpt.png"
CONFIG_PATHS = {
    "menu": "../config/streamlit/menu_config.json",
    "mlearning": "../config/streamlit/mlearning_config.json",
    "tools": "../config/streamlit/tools_config.json",
    "apps": "../config/streamlit/apps_config.json",
    "footer": "../config/streamlit/footer_config.json",
    "color": "../config/streamlit/color_config.json",
}

# ===== HEADER STYLES ================================================
HEADER_CONTAINER_BACKGROUND_NORMAL_COLOR = "#334155"
HEADER_CONTAINER_BACKGROUND_HOVER_COLOR = "#A5B4FC0A"
HEADER_BUTTON_BOX_SHADOW = "0px 4px 4px rgba(0, 0, 0, 0.30)"
HEADER_BUTTON_NORMAL_COLOR = "#1E1E1E"
HEADER_BUTTON_HOVER_COLOR = "#A5B4FC0A"
HEADER_BUTTON_CLICK_COLOR = "#4F378B"
HEADER_BUTTON_ACTIVE_COLOR = "#1E1E1E"
HEADER_BUTTON_BACKGROUND_NORMAL_COLOR = "#334155"
HEADER_BUTTON_BACKGROUND_HOVER_COLOR = "#A5B4FC0A"
HEADER_BUTTON_BACKGROUND_ACTIVE_COLOR = "#4F378B"
HEADER_BUTTON_EACH_SX_BASIC = f"""
                            "background-color": {HEADER_BUTTON_BACKGROUND_NORMAL_COLOR},
                            "color": {HEADER_BUTTON_NORMAL_COLOR},
                            "box-shadow": {HEADER_BUTTON_BOX_SHADOW},
                            "&:hover": {{
                                "backgroundColor": {HEADER_BUTTON_HOVER_COLOR},
                            }},
                            "p": 1.0,
                            "align-items": "center",
                        """

# ===== INITIALIZE SESSION STATE =====================================
username = st.session_state.get("username", "admin")


# ===== FUNCTIONS ===================================================
def load_config(path: str) -> dict:
    """
    Loads configuration data from a given path.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


def load_all_configs():
    """Loads all the necessary configuration files."""
    return {key: load_config(value) for key, value in CONFIG_PATHS.items()}


def check_for_logo_image(logo_path: str):
    """Checks for the existence of the logo image and returns it."""
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


def change_page_extended(next_page):
    """Changes the current page."""
    try:
        st.session_state.setdefault("current_page", next_page)
        next_page_short = next_page.lower().replace("_page", "")
        st.session_state["current_page"] = next_page_short
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")


def reset_active_button_color():
    for item in menu_config:
        st.session_state[
            f"color_active_{item['name']}_button"
        ] = HEADER_BUTTON_ACTIVE_COLOR
    for item in footer_config:
        st.session_state[
            f"color_active_{item['name']}_button"
        ] = HEADER_BUTTON_ACTIVE_COLOR


def handle_click_universal(name):  # Modified to take 'name' argument
    def wrapper(event):
        clicked = (HEADER_BUTTON_BACKGROUND_ACTIVE_COLOR,)
        reset_active_button_color()
        st.session_state[f"color_active_{clicked}_button"] = next(
            (item["active_color"] for item in menu_config if item["id"] == clicked),
            HEADER_BUTTON_BACKGROUND_ACTIVE_COLOR,
        )
        st.session_state["menu_active_button"] = clicked
        st.session_state["active_section"] = clicked

    return wrapper


def handle_click_close():
    reset_active_button_color()
    st.session_state["menu_active_button"] = None
    st.session_state["active_section"] = None


def toggle_sidebar():
    # Load the custom CSS
    st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)
    
    # Check if sidebar is currently displayed
    is_sidebar_visible = st.session_state.get("is_sidebar_visible", True)
    
    # Button to toggle the sidebar visibility
    if st.button("Toggle Sidebar"):
        is_sidebar_visible = not is_sidebar_visible
        st.session_state["is_sidebar_visible"] = is_sidebar_visible
    
    # Applying the CSS class based on the button click
    if is_sidebar_visible:
        st.markdown('<script>document.querySelector("section[data-testid=\'stSidebar\']").classList.add("show-sidebar");</script>', unsafe_allow_html=True)
        st.markdown('<script>document.querySelector("section[data-testid=\'stSidebar\']").classList.remove("hide-sidebar");</script>', unsafe_allow_html=True)
    else:
        st.markdown('<script>document.querySelector("section[data-testid=\'stSidebar\']").classList.add("hide-sidebar");</script>', unsafe_allow_html=True)
        st.markdown('<script>document.querySelector("section[data-testid=\'stSidebar\']").classList.remove("show-sidebar");</script>', unsafe_allow_html=True)


def header_button(menu_config, page_name):
    if f"color_active_{page_name}_card" not in st.session_state:
        st.session_state[f"color_active_{page_name}_card"] = ""

    with elements("mainHeaderBar"):
        """Generate Header Section icons."""
        with mui.Grid(
            container=True,
            direction="row",
            justifyContent="space-between",
            alignItems="center",
            spacing={1},
        ):
            button_elements = []
            for item in menu_config:
                if item["id"] not in ["settings", "help"]:
                    icon_n = item["icon"]
                    button_element = mui.BottomNavigationAction(
                        label=item["name"],
                        icon=getattr(mui.icon, icon_n),
                        onClick=handle_click_universal(item["id"]),
                        sx=HEADER_BUTTON_EACH_SX_BASIC,
                    )
                    button_elements.append(button_element)
            with mui.Paper(
                elevation={3},
                fullWidth=True,
                sx={
                    "width": "100%",
                    "pt": 1.2,
                    "mb": 1,
                    "color": HEADER_CONTAINER_BACKGROUND_NORMAL_COLOR,
                    "display": "static",
                    "flex-direction": "column",
                    "align-items": "center",
                    "&:hover": {
                        "color": HEADER_CONTAINER_BACKGROUND_HOVER_COLOR,
                    },
                },
            ):
                mui.BottomNavigation(
                    *button_elements,
                    variant="elevation",
                    label="primary button group",
                    size="medium",
                    showLabels=True,
                ),


def create_menu(source_page):
    # Need to create the header menu buttons and save the clicked one.
    # Call the function
    header_button(menu_config, source_page)
    with elements("HeaderNaviBar"):
        menu = st.session_state.menu_active_button
        # need to check if a button was pressed and process the selected action.
        selected_menu_button = st.session_state["menu_active_button"]
        st.write("Now comes the shit:")

        if menu == "settings":
            switch_page("settings")

        elif menu == "documentation":
            switch_page("documentation")

        elif menu == "datastore":
            switch_page("datastore")

        elif menu == "apps":
            switch_page("apps")

        elif menu == "machine_learning":
            switch_page("machine_learning")

        elif menu == "documentation":
            switch_page("1_documentation")

        elif menu == "tools":
            switch_page("tools")

        # need to check if a button was pressed and process the   elected action.
        selected_menu_button = st.session_state["menu_active_button"]

        if selected_menu_button != source_page and selected_menu_button:
            do = "nothing"

        else:
            do = "nothing"
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
