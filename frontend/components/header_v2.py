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


def handle_submenu_click(event, new_index):
    # Change page based on submenu button clicked
    menu_item = menu_config[new_index]
    switch_page(menu_item["id"])
    #            submenu_navbar(item)


# ^ MAIN PROCESS -------------------------------------------------------


# ^ LOGO (LEFT SIDE)
def create_logo():
    """Create and display the logo."""
    with mui.Grid(
        height=60,
        width=60,
        ml="20px",
        # mr="-15px",
        pt="18px",
        # bg=sb.container["HeaderBGColor"],
        sx={"justfyContent": "flext-start", "alignItems": "lext-start"},
    ):
        mui.CardMedia(
            image=logourl,
            component="img",
            # bg="transparent",
            height=60,
            width=70,
            # ml="70px",
            # mr="-70px",
            sx={
                "filter": sb.hover_filter["filter"],
                "&:hover": {
                    "filter": sb.hover_filter["hover_filter"],
                },
            },
        )


def check_active_color(view_id, color, default_color):
    # Extract the active button id from session_state and compare with view_id
    active_button_id = st.session_state.get("menu_active_button", 0)
    if active_button_id == view_id:
        # print(
        #    f"checked color and returned: {color}, tested id: {view_id}, with session_state: {active_button_id}"
        # )
        return color
    else:
        # print(
        #    f"checked color and returned default: {default_color}, tested id: {view_id}, with session_state: {active_button_id}"
        # )
        return default_color


# ^ HEADER TABS (CENTER)
def create_tabs(menu_config):
    """Create and display the tabs."""
    button_elements = []
    for idx, item in enumerate(menu_config):
        # Central buttons
        if item["place_center"] is not False:
            view_id = item["view_id"]
            active_boxshadow = check_active_color(
                view_id, sb.button["BoxShadowUp"], sb.button["BoxShadow"]
            )
            button_element = mui.Tab(
                textColor="inherit",
                indicatorColor="inherit",
                label=item["name"],
                # color="#666",  # active_color,
                # bgcolor="#666",  # active_color,
                onClick=partial(update_menu, item["view_id"], idx),
                sx={
                    "padding": "0 !important",
                    "textColor": sb.menu_list[view_id]["TextColor"],
                    "bgcolor": check_active_color(
                        view_id,
                        sb.menu_list[view_id]["BackgroundColor"],
                        sb.container["HeaderBG"],
                    ),
                    "boxShadow": active_boxshadow,
                    "color": check_active_color(
                        view_id, sb.menu_list[view_id]["TextColor"], sb.text["Default"]
                    ),
                    "filter": sb.hover_filter["filter"],
                    "&:hover": {
                        "color": check_active_color(
                            view_id, "black", sb.text["Default"]
                        ),
                        "color": check_active_color(
                            view_id, "#000", sb.text["BGColor"]
                        ),
                        "filter": sb.hover_filter["hover_filter"],
                    },
                    "&:active": {
                        "color": check_active_color(
                            view_id,
                            sb.menu_list[view_id]["ActiveTextColor"],
                            sb.text["Color"],
                        ),
                        "boxShadow": sb.menu_list[view_id]["ActiveBoxShadow"],
                    },
                    "&:selected": {
                        "color": check_active_color(
                            view_id,
                            sb.menu_list[view_id]["ActiveTextColor"],
                            sb.text["Color"],
                        ),
                        # "text": sb.menu_list[view_id]["ActiveTextColor"],
                        "boxShadow": sb.menu_list[view_id]["ActiveBoxShadow"],
                    },
                },
            )
            button_elements.append(button_element)
    with mui.Grid():
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
            # textColor="inherit",
            # indicatorColor="inherit",
            allowScrollButtonsMobile=False,
            centered=True,
            classes="headertabs",
            visibleScrollbar=False,
            value=st.session_state.get("menu_active_button") or 0,
            sx={
                "borderColor": "divider",
            }
            # sx={
            #    "&:MuiTabs-indicatorSpan": {
            #        "maxWidth": "40",
            #        "width": "100%",
            #        # "backgroundColor": "#635ee7",
            #    },
            # },
        )


# ^ HEADER ICON BUTTON (RIGHT SIDE)
def create_icon_buttons(menu_config):
    """Create and display the icon buttons."""
    icon_elements = []
    with mui.Grid():
        icon_n = "Alarm"
        for idx, item in enumerate(menu_config):
            # Side icons/buttons
            view_id = item["view_id"]
            if item.get("place_side"):
                active_color = check_active_color(
                    view_id, sb.button["HeaderIconActive"], sb.button["HeaderIcon"]
                )
                active_boxshadow = check_active_color(
                    view_id, sb.button["ActiveBoxShadow"], sb.button["BoxShadow"]
                )
                icon_n = item["icon"]
                icon_element = mui.IconButton(
                    getattr(mui.icon, icon_n),
                    classes="iconbutton",
                    # iconColor="default",
                    color=active_color,
                    variant="soft",
                    onClick=partial(update_menu, item["view_id"], idx),
                    sx={
                        # "bg": "linear-gradient(270.deg, #005375 0%, #1E2A38 100%)",
                        "boxShadow": active_boxshadow,
                        "filter": sb.hover_filter["filter"],
                        "&:hover": {
                            "filter": sb.hover_filter["hover_filter"],
                        },
                        "&:active": {
                            "boxShadow": "inset -4px -4px 8px rgba(255, 255, 255, 0.15), inset 4px 4px 8px rgba(25, 28, 30, 0.7)",
                        },
                    },
                )
                icon_elements.append(icon_element)


# ? Header functions
def header_navbar(menu_config):
    # ^ Header frame
    with mui.Box(  # * Header frame
        classes="flexcontainer",
        flexGrow=1,
        fullWidth=True,
        alignItems="center",
        verticalAlign="center",
        justifyContent="space-between",
        # pt="15px",
        # bg=sb.container["HeaderBGColor"],
        top=0,
        # left=0,
        # mb="",
        # sx={
        #    "margin": "0",
        # },
    ):
        with mui.AppBar(
            position="static",
            classes="headerapp",
            visibleScrollbar=False,
            # bg=sb.container["HeaderBGColor"],
            fullWidth=True,
            ml=0,
            sx=sb.header_special,
        ):
            with mui.Grid(
                container=True,
                spacing=3,
                visibleScrollbar=False,
                # bg=sb.container["HeaderBGColor"],
            ):  # & Logo
                create_logo()
                with mui.Grid(ariaLabel="HeaderMenu"):
                    with mui.Box(  # * Header frame
                        classes="flexcontainer",
                        flexGrow=1,
                        fullWidth=True,
                        # alignItems="center",
                        # verticalAlign="center",
                        justifyContent="space-between",
                        # pt="15px",
                        # bg=sb.container["HeaderBGColor"],
                        # pl="260px",
                    ):  # & Header
                        with mui.AppBar(
                            # position="relativ",
                            classes="headerapp",
                            visibleScrollbar=False,
                            # bg=sb.container["HeaderBGColor"],
                            # fullWidth=True,
                            sx={
                                "background": "transparent",
                                "box-shadow": "none",
                                # "margin": "0",
                            },
                        ):
                            with mui.Grid(
                                container=True,
                                spacing=2,
                                visibleScrollbar=False,
                                # bgcolor="transparent",
                                pt="35px",
                                mt="-30px",
                                pr=1,
                                sx={
                                    "justify-content": "space-between",
                                },
                            ):
                                with mui.Grid(mr="auto", ml="auto"):
                                    create_tabs(menu_config)
                                # create_icon_buttons(menu_config)

                        # & Subheader
                        create_icon_buttons(menu_config)
                        with mui.SwipeableViews(
                            axis="x",
                            index=st.session_state.get("menu_active_button") or 0,
                            # flexGrow=1,
                            # fullWidth=True,
                            onChangeIndex=update_menu,
                            # visibleScrollbar=False,
                        ):
                            with mui.Grid(
                                container=True,
                                # bg=sb.container["SubHeaderBGColor"],
                                pl="10px",
                                # ml="150px",
                                # mr="150px",
                                verticalAlinments=True,
                                pt="20px",
                                mb="100px",
                                spacing=1,
                                # bgcolor="!transparent",
                                height="50px",
                                visibleScrollbar=False,
                                sx={
                                    "boxShadow": sb.button["BoxShadowDown"],
                                    "color": sb.menu_list[item["view_id"]]["TextColor"],
                                    "bgcolor": sb.menu_list[item["view_id"]][
                                        "BackgroundColor"
                                    ],
                                    # "background": "linear-gradient(270.deg, #1E2A38 0%, #005375 100%)",
                                    # "boxShadow": "-6.22302px -6.22302px 18.6691px #3B4451, 6.22302px 6.22302px 18.6691px #000000",
                                    # "boxShadow": "inset -4px -4px 8px rgba(255, 255, 255, 0.15), inset 4px 4px 8px rgba(25, 28, 30, 0.7)",
                                },
                            ):
                                for item in menu_config:
                                    subheader_config = item["subheader"]
                                    newvalue = (
                                        st.session_state.get("submenu_active_button")
                                        or 0
                                    )
                                    with mui.ButtonGroup(
                                        variant="outlined",
                                        value=newvalue,
                                        onChange=update_submenu,
                                        size="small",
                                        mr="auto",
                                        ml="auto",
                                        sx={
                                            "boxShadow": "-6.22302px -6.22302px 18.6691px #3B4451, 6.22302px 6.22302px 18.6691px #000000",
                                        }
                                        # ariaLabel="outlined primary button group",
                                    ):
                                        for subitem in subheader_config:
                                            icon_n = subitem["icon"]
                                            view_id = item["view_id"]
                                            active_boxshadow = check_active_color(
                                                view_id,
                                                sb.button["BoxShadowUp"],
                                                sb.button["BoxShadow"],
                                            )
                                            icon_element = mui.Button(
                                                subitem["name"],
                                                getattr(mui.icon, icon_n),
                                                label=subitem["name"],
                                                # value=subitem["id"],
                                                variant="outlined",
                                                mt="auto",
                                                mb="auto",
                                                bgcolor="#000000",
                                                size="small",
                                                onClick=partial(
                                                    update_submenu, subitem["id"]
                                                ),
                                                p=1,
                                                m=10,
                                                pb=50,
                                                sx={
                                                    # "bg": check_active_color(
                                                    #    view_id,
                                                    #    sb.menu_list[view_id][
                                                    #        "BackgroundColor"
                                                    #    ],
                                                    #    sb.text["Default"],
                                                    # ),
                                                    # "boxShadow": active_boxshadow,
                                                    # "color": check_active_color(
                                                    #    view_id,
                                                    #    sb.menu_list[view_id]["TextColor"],
                                                    #    sb.text["Default"],
                                                    # ),
                                                    # "filter": sb.hover_filter["filter"],
                                                    "&:hover": {
                                                        "color": check_active_color(
                                                            view_id,
                                                            sb.menu_list[view_id][
                                                                "HoverBackgroundColor"
                                                            ],
                                                            sb.text["Default"],
                                                        ),
                                                        "filter": sb.hover_filter[
                                                            "hover_filter"
                                                        ],
                                                    },
                                                    "&:active": {
                                                        "color": check_active_color(
                                                            view_id,
                                                            sb.menu_list[view_id][
                                                                "ActiveTextColor"
                                                            ],
                                                            sb.text["Default"],
                                                        ),
                                                        "boxShadow": "inset -4px -4px 8px rgba(255, 255, 255, 0.15), inset 4px 4px 8px rgba(25, 28, 30, 0.7)    ",
                                                    },
                                                },
                                            )
                                            icon_element

                            # with mui.Grid():
                            #    mui.Typography(" ")


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


def init(page):
    check_logged_in(page)
    create_menu()
    st.markdown(
        """
        <style>
        body {
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
