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

# ? Local modules
from components.style import stylebase as sb
from components.xhelper import check_logged_in
from components import xdash

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


def drawer():
    # State to manage the drawer's open status
    if "drawer_open" not in st.session_state:
        st.session_state.drawer_open = False

    # Toggle function for the drawer
    def toggle_drawer():
        st.session_state.drawer_open = not st.session_state.drawer_open

        # Streamlit Elements
        # with elements("drawer_example"):
        # Button to open/close the drawer
        mui.Button("Toggle Drawer", onClick=toggle_drawer)

        # The Drawer component
        with mui.Drawer(
            open=st.session_state.drawer_open,
            onClose=toggle_drawer,
            anchor="top",  # Drawer position: 'left', 'right', 'top', 'bottom'
            sx={
                "width": "250",  # Width of the drawer
                "backdropFilter": "blur(10px)",  # Blur effect on the backdrop
                ".MuiDrawer-paper": {
                    "width": "250",  # Width of the drawer paper
                    "boxSizing": "border-box",
                },
            },
        ):
            # Content of the drawer
            with mui.List():
                for text in ["Item 1", "Item 2", "Item 3"]:
                    with mui.ListItem(button=True):
                        mui.ListItemText(text)


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


# & Function to create and display tabs in the header
def create_tabs(menu_config):
    """! Creates and displays tabs for the header section.
    * Args:
    *   menu_config (dict): The configuration for menu items.
    """
    button_elements = []
    for idx, item in enumerate(menu_config):
        # Central buttons
        if item["place_center"] is not False:
            view_id = item["view_id"]
            button_element = mui.Tab(
                textColor="inherit",
                indicatorColor="inherit",
                label=item["name"],
                onClick=partial(update_menu, item["view_id"], idx),
                sx={
                    "padding": "0 !important",
                    "textColor": sb.menu_list[view_id]["TextColor"],
                    "boxShadow": check_active_color(
                        "menu_active_button",
                        view_id,
                        sb.button["BoxShadowUp"],
                        sb.menu_list[view_id]["BoxShadow"],
                    ),
                    "color": check_active_color(
                        "menu_active_button",
                        view_id,
                        sb.menu_list[view_id]["ActiveTextColor"],
                        sb.menu_list[view_id]["TextColor"],
                    ),
                    "bgcolor": check_active_color(
                        "menu_active_button",
                        view_id,
                        sb.menu_list[view_id]["ActiveBackgroundColor"],
                        "transparent",
                    ),
                    "BorderColor": sb.menu_list[view_id]["BorderColor"],
                    "border-bottom": "1px solid "
                    + sb.menu_list[view_id]["BorderColor"],
                    "filter": sb.hover_filter["filter"],
                    "&:hover": {
                        "color": sb.menu_list[view_id]["HoverTextColor"],
                        "bgcolor": sb.menu_list[view_id]["HoverBackgroundColor"],
                        "filter": sb.hover_filter["hover_filter"],
                    },
                    "&:active": {
                        "color": sb.menu_list[view_id]["HoverTextColor"],
                        "bgcolor": sb.menu_list[view_id]["HoverBackgroundColor"],
                        "filter": sb.hover_filter["hover_filter"],
                    },
                },
            )
            button_elements.append(button_element)
    mui.Tabs(
        *button_elements,
        role="fullWidth",
        display="flex",
        justifyContent="center",
        indicatorPlacement="top",
        variant="inhert",
        textColor=sb.button["Header"],
        indicatorColor=sb.button["HeaderActive"],
        ariaLabel="tabs",
        allowScrollButtonsMobile=False,
        centered=True,
        classes="headertabs",
        visibleScrollbar=False,
        value=st.session_state.get("menu_active_button") or 0,
        sx={
            "borderBottom": "1 !important",
            "borderColor": "divider !important",
        },
    )


# & Function to create and display icon buttons in the header
def create_icon_buttons(menu_config):
    """! Creates and displays icon buttons in the header section.
    * Args:
    *   menu_config (dict): The configuration for menu items.
    """
    icon_n = "Alarm"
    with mui.ButtonGroup(
        variant="text",
        size="small",
    ):
        for idx, item in enumerate(menu_config):
            # Side icons/buttons
            view_id = item["view_id"]
            if item.get("place_side"):
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
                icon_n = item["icon"]
                mui.Button(
                    getattr(mui.icon, icon_n),
                    classes="utils-button",
                    color=active_color,
                    variant="inhert",
                    onClick=partial(update_menu, item["view_id"], idx),
                    sx={
                        "boxShadow": active_boxshadow,
                        "filter": sb.hover_filter["filter"],
                        "color": check_active_color(
                            "menu_active_button",
                            view_id,
                            sb.menu_list[view_id]["ActiveTextColor"],
                            sb.menu_list[view_id]["TextColor"],
                        ),
                        "bgcolor": check_active_color(
                            "menu_active_button",
                            view_id,
                            sb.menu_list[view_id]["ActiveBackgroundColor"],
                            "transparent",
                        ),
                        "filter": sb.hover_filter["filter"],
                        "&:hover": {
                            "color": sb.menu_list[view_id]["HoverTextColor"],
                            "bgcolor": sb.menu_list[view_id]["HoverBackgroundColor"],
                            "filter": sb.hover_filter["hover_filter"],
                        },
                        "&:active": {
                            "color": sb.menu_list[view_id]["HoverTextColor"],
                            "bgcolor": sb.menu_list[view_id]["HoverBackgroundColor"],
                            "filter": sb.hover_filter["hover_filter"],
                        },
                    },
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
        id = subitem["id"]
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
                    id,
                    sb.button["BoxShadowDown"],
                    sb.button["BoxShadow"],
                ),
                "color": check_active_color(
                    "submenu_active_button",
                    id,
                    sb.menu_list[view_id]["ActiveTextColor"],
                    sb.menu_list[view_id]["TextColor"],
                ),
                "bgcolor": check_active_color(
                    "submenu_active_button",
                    id,
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
    ):
        with mui.AppBar(
            classes="xgpt",
            position="static",
            visibleScrollbar=False,
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
                # create_logo()
                drawer()
                with mui.Grid(mr="auto", ml="auto"):
                    create_tabs(menu_config)
            subheader_navbar(menu_config)


# & Function to initialize the menu creation process
def init(page):
    """! Initializes the menu creation process based on the given page.
    * Args:
    *   page (str): The current page being rendered.
    """

    check_logged_in(page)
    with st.sidebar:
        with elements("SideNaviBar"):
            with mui.AppBar(
                alignItems="center",
                visibleScrollbar=False,
                fullWidth=True,
                ml=0,
                sx=sb.header_special,
            ):
                with mui.Grid(
                    container=True,
                    mt="5px",
                    ml="5px",
                    mb="50px",
                ):
                    create_icon_buttons(menu_config)
    # State to manage the drawer's open status
    if "drawer_open" not in st.session_state:
        st.session_state.drawer_open = False

    # Toggle function for the drawer
    def toggle_drawer():
        st.session_state.drawer_open = not st.session_state.drawer_open

    # with st.sidebar:
    with elements("HeaderNaviBar"):
        # Button to open/close the drawer
        with mui.Box(  # * Header frame
            classes="xgpt",
            flexGrow=1,
            # fullWidth=True,
            alignItems="center",
            verticalAlign="center",
            justifyContent="space-between",
            top=0,
            # pt="-5px",
            # ml="-10px",
            # mr="-50px",
            # pl="-50px",
            minWidth="100%",
        ):
            with mui.AppBar(
                classes="xgpt",
                visibleScrollbar=False,
                fullWidth=True,
                ml=0,
                sx=sb.header_special,
            ):
                with mui.Grid(
                    container=True,
                    direction="row",
                    height="50px",
                    justifyContent="space-between",
                    alignItems="center",
                ):
                    mui.Grid()

                    mui.Button(
                        mui.icon.Menu,
                        onClick=toggle_drawer,
                        variant="inhert",
                        padding=0,
                        height="180px",
                        alignItems="center",
                        verticalAlign="center",
                    )

        # The Drawer component
        with mui.Drawer(
            open=st.session_state.drawer_open,
            onClose=toggle_drawer,
            anchor="top",  # Drawer position: 'left', 'right', 'top', 'bottom'
            visibleScrollbar=False,
            sx={
                ".MuiDrawer-paper": {
                    "boxSizing": "border-box",
                },
            },
        ):
            # ^ Content of the drawer
            with mui.AppBar(
                classes="xgpt",
                visibleScrollbar=False,
                fullWidth=True,
                ml=0,
                sx=sb.header_special,
            ):
                with mui.Grid(
                    container=True,
                    direction="row",
                    height="50px",
                    justifyContent="space-between",
                    alignItems="center",
                ):
                    mui.Grid()

                    mui.Button(
                        mui.icon.Menu,
                        onClick=toggle_drawer,
                        variant="inhert",
                        padding=0,
                        height="180px",
                        alignItems="center",
                        verticalAlign="center",
                    )

        # Main content area
        # Apply blur effect if the drawer is open
        main_content_style = {}
        with mui.Box(sx=main_content_style):
            # Add your main content here
            item_data = {
                "item_0": "http://localhost:8334",  # URL for iframe
                "item_1": "Text content for second item",
                "item_2": "Text content for third item",
            }
        mui.Box(
            height="50px",
            visibleScrollbar=False,
        )
        xdash.configure_dash_items(page)
        # xpaper.gen_dashboard(page, item_data)
