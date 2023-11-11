# components/header.py
# Check header.md in the /docs directory for more information
# ! Python libraries
from os import path
import json
from functools import partial

# ! External libraries
from PIL import Image
import streamlit as st
from streamlit_elements import elements, mui
from streamlit_extras.switch_page_button import switch_page
from contextlib import contextmanager

# ? Local modules
from components.style import stylebase as sb
from components.xhelper import check_logged_in

# * Initialization & Configurations
# * Constants
LOGO_PATH = "../resources/images/logo/favicon.ico"
CONFIG_PATHS = {
    "menu": "../config/streamlit/menu_config.json",
    "mlearning": "../config/streamlit/mlearning_config.json",
    "tools": "../config/streamlit/tools_config.json",
    "apps": "../config/streamlit/apps_config.json",
}
logourl = ("http://127.0.0.1:8334/data/images/logo/android-chrome-512x512.png",)

# * Loading configurations
configs = {}  # ^ Will hold all configurations loaded from json files
for key, value in CONFIG_PATHS.items():
    if not path.exists(value):
        st.error(f"Configuration file for {key} not found at {value}")
    else:
        configs[key] = json.load(open(value, "r"))

# * Deconstructing configs into individual variables
(
    menu_config,
    mlearning_config,
    tools_config,
    apps_config,
) = configs.values()


# & FUNCTIONS -------------------------------------------------------


# ? Helper functions
# ^ Function to load individual configuration files
def load_config(config_path: str) -> dict:
    """! Loads configuration from a json file.
    * Args:
    *   config_path (str): The path to the configuration json file.
    * Returns:
    *   dict: The configuration dictionary.
    """
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"! Error loading configuration: {e}")
        return {}


# ^ Function to check for logo image existence
def check_for_logo_image():
    """! Checks for the existence of the logo image file.
    * Args:
    *   logo_path (str): The path to the logo image file.
    * Returns:
    *   Image or None: The Image if file exists, otherwise None.
    """
    if path.exists(LOGO_PATH):
        return Image.open(LOGO_PATH)
    st.warning("^ Logo image not found at the specified path.")
    return None


# ^ Function to change page, extending default functionality
def change_page_extended(next_page):
    """! Changes the current page to the given next_page value.
    * Args:
    *   next_page (str): The next page to navigate to.
    """
    try:
        st.session_state["current_page"] = next_page.lower().replace("_page", "")
    except Exception as e:
        st.error(f"! Error changing page: {str(e)}")


# ^ Function to update the active state of menu items
def update_menu(item_id, idx):
    """! Updates the session state to reflect the active menu item.
    * Args:
    *   item_id (int): The ID of the menu item that is active.
    """
    st.session_state["menu_active_button"] = item_id


# ^ Function to update the active state of submenu items
def update_submenu(item_id, idx):
    """! Updates the session state to reflect the active submenu item.
    * Args:
    *   item_id (int): The ID of the submenu item that is active.
    """
    st.session_state["submenu_active_button"] = item_id
    change_page_extended(item_id)


# ^ Function to check and return the active color for an item
def check_active_color(session_state_name, view_id, color, default_color):
    """! Checks the session state and returns the active color if conditions match.
    * Args:
    *   session_state_name (str): The session state key to check.
    *   view_id (int): The ID of the view.
    *   color (str): The color to return if the view_id matches the session state.
    *   default_color (str): The default color to return if there is no match.
    * Returns:
    *   str: The active color based on the session state.
    """
    active_button_id = st.session_state.get(session_state_name)
    return color if active_button_id == view_id else default_color


# ^ MAIN PROCESS -------------------------------------------------------


# & Function to create and display the logo
def create_logo():
    """! Creates and displays the logo using Material UI's CardMedia component."""
    with mui.Grid(
        height=60,
        width=60,
        ml="10px",
        pt="8px",
        mr="5px",
        sx={"justfyContent": "flext-start", "alignItems": "lext-start"},
    ):
        mui.CardMedia(
            image=logourl,
            component="img",
            height=60,
            width=70,
            sx={
                "filter": sb.hover_filter["filter"],
                "&:hover": {
                    "filter": sb.hover_filter["hover_filter"],
                },
            },
        )


def menu_icon_side_nav():
    # State to track which menu is open
    if "menu_index" not in st.session_state:
        st.session_state.menu_index = None

    def set_menu_index(index):
        st.session_state.menu_index = index

    def close_menu():
        st.session_state.menu_index = None

        # with elements("Test123"):
        # with mui.Sheet(sx={"borderRadius": "sm", "py": 1, "mr": 20}):
        with mui.List():
            # Apps Menu
            with mui.ListItem():
                if st.session_state.menu_index == 0:
                    with mui.Menu(open=True, onClose=close_menu):
                        mui.MenuItem(
                            "Application 1", onClick=lambda: set_menu_index(None)
                        )
                        mui.MenuItem(
                            "Application 2", onClick=lambda: set_menu_index(None)
                        )
                        mui.MenuItem(
                            "Application 3", onClick=lambda: set_menu_index(None)
                        )
                mui.IconButton(mui.icon.Apps, onClick=lambda: set_menu_index(0))

            # Settings Menu
            with mui.ListItem():
                if st.session_state.menu_index == 1:
                    with mui.Menu(open=True, onClose=close_menu):
                        mui.MenuItem("Setting 1", onClick=lambda: set_menu_index(None))
                        mui.MenuItem("Setting 2", onClick=lambda: set_menu_index(None))
                        mui.MenuItem("Setting 3", onClick=lambda: set_menu_index(None))
                mui.IconButton(mui.icon.Settings, onClick=lambda: set_menu_index(1))

            # Personal Menu
            with mui.ListItem():
                if st.session_state.menu_index == 2:
                    with mui.Menu(open=True, onClose=close_menu):
                        mui.MenuItem("Personal 1", onClick=lambda: set_menu_index(None))
                        mui.MenuItem("Personal 2", onClick=lambda: set_menu_index(None))
                        mui.MenuItem("Personal 3", onClick=lambda: set_menu_index(None))
                mui.IconButton(mui.icon.Person, onClick=lambda: set_menu_index(2))


def set_submenu_index(menu_id, submenu_index):
    if "submenu_index" not in st.session_state or not isinstance(
        st.session_state.submenu_index, dict
    ):
        st.session_state.submenu_index = {}
    st.session_state.submenu_index[menu_id] = submenu_index


def close_submenu(menu_id):
    if "submenu_index" in st.session_state and isinstance(
        st.session_state.submenu_index, dict
    ):
        st.session_state.submenu_index[menu_id] = None


@contextmanager
def submenu_context(menu_id):
    try:
        yield
    finally:
        close_submenu(menu_id)


# Modified function to create and display icon buttons with submenus
def create_icon_buttons(menu_config):
    with mui.ButtonGroup(variant="outlined", size="small"):
        for idx, item in enumerate(menu_config):
            if item.get("place_side"):
                view_id = item["view_id"]
                icon_name = item["icon"]
                active_color = check_active_color(
                    "menu_active_button",
                    view_id,
                    sb.button["HeaderIconActive"],
                    sb.button["HeaderIcon"],
                )
                active_boxshadow = check_active_color(
                    "menu_active_button",
                    view_id,
                    sb.button["ActiveBoxShadow"],
                    sb.button["BoxShadow"],
                )

                with mui.IconButton(
                    getattr(mui.icon, icon_name),
                    classes="iconbutton",
                    color=active_color,
                    variant="soft",
                    onClick=lambda idx=idx: set_submenu_index(idx, 0),
                ):
                    if st.session_state.submenu_index is not None:
                        with submenu_context(idx):
                            with mui.Menu(open=True):
                                for sub_idx, sub_item in enumerate(item["subheader"]):
                                    mui.MenuItem(
                                        sub_item["name"],
                                        onClick=lambda sub_idx=sub_idx: set_submenu_index(
                                            idx, sub_idx
                                        ),
                                    )


# Modified function to create and display tabs with submenus
def create_tabs(menu_config):
    for idx, item in enumerate(menu_config):
        if item["place_center"]:
            view_id = item["view_id"]
            with mui.Tab(
                textColor="inherit",
                indicatorColor="inherit",
                label=item["name"],
                onClick=lambda idx=idx: set_submenu_index(idx, 0),
            ):
                if st.session_state.submenu_index is not None:
                    with submenu_context(idx):
                        with mui.Menu(open=True):
                            for sub_idx, sub_item in enumerate(item["subheader"]):
                                mui.MenuItem(
                                    sub_item["name"],
                                    onClick=lambda sub_idx=sub_idx: set_submenu_index(
                                        idx, sub_idx
                                    ),
                                )


# & Function to create and display the subheader content
def create_subheader_content(item):
    """! Creates and displays the content for the subheader section.
    * Args:
    *   item (dict): The configuration for a particular header item.
    """
    subheader_config = item["subheader"]
    for subitem in subheader_config:
        icon_n = subitem["icon"]
        view_id = item["view_id"]
        page_id = subitem["id"]
        mui.Button(
            subitem["name"],
            getattr(mui.icon, icon_n),
            label=subitem["name"],
            variant="text",
            size="small",
            color="inherit",
            onClick=partial(update_submenu, subitem["id"]),
            sx={
                "mr": "5px",
                "ml": "5px",
                "boxShadow": check_active_color(
                    "submenu_active_button",
                    page_id,
                    sb.button["BoxShadowDown"],
                    sb.button["BoxShadow"],
                ),
                "color": check_active_color(
                    "submenu_active_button",
                    page_id,
                    sb.menu_list[view_id]["ActiveTextColor"],
                    sb.menu_list[view_id]["TextColor"],
                ),
                "bgcolor": check_active_color(
                    "submenu_active_button",
                    page_id,
                    sb.menu_list[view_id]["BackgroundColor"],
                    sb.menu_list[view_id]["BackgroundColor"],
                ),
                "filter": sb.hover_filter["filter"],
                "&:hover": {
                    "color": sb.menu_list[view_id]["HoverTextColor"],
                    "bgcolor": sb.menu_list[view_id]["HoverBackgroundColor"],
                    "filter": sb.hover_filter["hover_filter"],
                },
                "&:active": {
                    "color": sb.menu_list[view_id]["ActiveTextColor"],
                    "bgcolor": sb.menu_list[view_id]["ActiveBackgroundColor"],
                    "filter": sb.hover_filter["hover_filter"],
                },
            },
        )


def subheader_navbar(menu_config):
    with mui.SwipeableViews(
        index=st.session_state.get("menu_active_button") or 0,
        onChangeIndex=update_menu,
    ):
        for item in menu_config:
            view_id = item["view_id"]
            with mui.Grid(
                container=True,
                spacing=0,
                direction="row",
                justifyContent="center",
                alignItems="center",
                mt="1px",
                mb="10px",
                pl="244px",
                flexGrow=1,
                fullWidth=True,
                visibleScrollbar=False,
                sx={
                    "-webkit-background-clip": "text",
                    "color": sb.menu_list[item["view_id"]]["TextColor"],
                },
            ):
                create_subheader_content(item)


# & Function to create and manage the navigation bar in the header
def header_navbar(menu_config):
    """! Manages the creation and display of the navigation bar in the header section.
    * Args:
    *   menu_config (dict): The configuration for menu items.
    """
    with mui.Box(  # * Header frame
        classes="xgpt",
        flexGrow=1,
        fullWidth=True,
        alignItems="center",
        verticalAlign="center",
        justifyContent="space-between",
        top=0,
        pt="-5px",
        ml="-10px",
        mr="-50px",
        pl="-50px",
        minWidth="100%",
    ):
        with mui.AppBar(
            classes="xgpt",
            position="static",
            visibleScrollbar=False,
            fullWidth=True,
            ml=0,
            sx=sb.header_special,
        ):
            with mui.Grid(
                container=True,
                classes="xgpt",
                visibleScrollbar=False,
                mt="5px",
                direction="row",
                height="50px",
            ):
                create_logo()
                with mui.Grid():
                    create_icon_buttons(menu_config)
                with mui.Grid(mr="auto", ml="auto"):
                    create_tabs(menu_config)
            subheader_navbar(menu_config)


# & Function to initialize the menu creation process
def init2(page):
    """! Initializes the menu creation process based on the given page.
    * Args:
    *   page (str): The current page being rendered.
    """
    check_logged_in(page)
    # with st.sidebar:
    with elements("HeaderNaviBar"):
        header_navbar(menu_config)


# Simplified context manager for debugging
@contextmanager
def submenu_context(menu_id):
    try:
        yield
    finally:
        # Debug print to check if this part of the code is reached
        st.write("Closing submenu for menu_id:", menu_id)


# Simplified function to create and display icon buttons with submenus
def create_icon_buttons(menu_config):
    with mui.ButtonGroup(variant="outlined", size="small"):
        for idx, item in enumerate(menu_config):
            if item.get("place_side"):
                with mui.IconButton(
                    getattr(mui.icon, item["icon"]),
                    onClick=lambda idx=idx: set_submenu_index(idx, 0),
                ):
                    # Debug print to check if button is created
                    st.write(f"Button created for {item['name']}")


# Simplified function to create and display the navigation bar
def header_navbar(menu_config):
    with mui.Box():
        with mui.AppBar():
            create_logo()
            create_icon_buttons(menu_config)


# Simplified initialization function
def init(page):
    check_logged_in(page)
    with elements("HeaderNaviBar"):
        header_navbar(menu_config)
