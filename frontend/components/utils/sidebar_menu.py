
# Imports and Global Variables
import streamlit as st
# components/utils/sidebar_menu.py
import os
from PIL import Image
from streamlit_elements import elements, mui, html
from components import postgres
import json

# Check if the image exists before trying to open it.
if os.path.exists("images/logo/logo_long.png"):
    image = Image.open("images/logo/logo_long.png")
else:
    image = None
    st.warning("Logo image not found!")

button_active = "rgba(119, 146, 227, 0.5)"


# Initialization of session state variables
if "menu_active_button" not in st.session_state:
    st.session_state.menu_active_button = ""
    st.session_state.active_section = ""
    st.session_state.ai_apps_accordion_active = ""


def settings_box():
    # User Settings
    with st.sidebar:
        st.header("Settings")
        # Next Settings
        with st.expander("API"):
            with st.spinner("Processing..."):
                try:
                    # Load existing data from Postgres using username as ID
                    user = st.session_state["username"]
                    with st.form("user_form"):
                        # User inputs with pre-filled data from the database
                        new_key_openai = st.text_input(
                            "API Key",
                            value=postgres.db_get_value(user, "openai_key"),
                            key="openai_key",
                            type="password",
                        )
                        new_dev_mode = st.toggle(
                            "Dev mode",
                            value=postgres.db_get_value(user, "dev_mode"),
                            key="dev_mode",
                        )
                        submit_button = st.form_submit_button("Update")
                    # Update user data if submit_button clicked
                    if submit_button and new_key_openai is not None:
                        postgres.db_set_value(user, "openai_key", new_key_openai)
                        postgres.db_set_value(user, "dev_mode", new_dev_mode)
                except Exception as e:
                    st.error(f"Error: {str(e)} ❌")


def change_page_extended(next_page):
    """Changes the current page."""
    try:
        next_page_short = str(next_page).lower().replace('_page','')
        st.write(next_page_short)
        st.session_state["current_page"] = next_page_short
        #switch_page(next_page_short)
    except Exception as e:
        st.error(f"Error: {str(e)} ❌")

    
def datastore_box():
    """Renders the datastore box in the sidebar."""
    with st.sidebar:
        # Title and Explanation
        st.markdown("## Datastore Tools")
        st.markdown(
            "Here, manage your **local files** and get an overview of "
            "the **Vector Database** using Attu and Milvus. "
            "_Further explanations and guides will be added soon._"
        )

        # Local Files Section
        with st.expander("Local Files"):
            st.markdown("Browse, upload, or manage your local files seamlessly.")
            if st.button("Open Filebrowser"):
                change_page_extended("data_file_manager")

        # Vector Database Section
        with st.expander("Vector Database (Milvus)"):
            st.markdown(
                "Utilize **Attu** to get an overview of Milvus. The default "
                "user credentials are configured in the `docker-compose` file and are as follows:\n"
                "- **Username:** minioadmin\n"
                "- **Password:** minioadmin\n\n"
                "_The configuration file path:_\n"
                "`helper/docker/docker-compose-db.yaml`"
            )
            # Note: Streamlit does not support `on_click` URL redirect via button yet.
            # Using `st.markdown` to create a hyperlink.
            st.markdown(
                "[Open Milvus Dashboard](https://localhost:8181)",
                unsafe_allow_html=True,
            )




# / region [ rgba(20, 150, 200, 0.03)] Sidebar AI Apps Content


# Function to generate the button vertical list
def button_vertical_list(icon_name, app_name, description, button_color, page_name):
    """Generates a vertical button list."""    
    with mui.Grid(
        container=True, direction="row", alignText="center",height="45px", justify="space-between", backgroundColor=button_color,style={"box-shadow": "rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset;",}):

        with mui.Grid(item=True, xs=9):
            mui.Typography(app_name)
            mui.Typography(description, variant="body2", style={"fontSize": "0.7rem"})
        
        with mui.Grid(item=True, xs=1):
            with mui.IconButton(
                variant="contained",
                backgroundColor=button_color,
                style={"margin-right": "100%", "margin-left": "0%", "self-align": "right",},
                onClick=lambda: change_page_extended(str(page_name).lower()),
            ):
                getattr(mui.icon, icon_name)()

    mui.Divider()



def bots_box():
    """Generates the bots box."""
    
    # Check if the config file exists before trying to open it.
    if not os.path.exists("apps_config.json"):
        st.warning("Configuration file (apps_config.json) not found!")
        return

    with open("apps_config.json", "r") as file:
        config = json.load(file)

        with elements("multiple_children_test"):
            
            def handle_click_tool_category(category_name):
                st.session_state.ai_apps_accordion_active = category_name
                st.write(f"Clicked on: {category_name}")  # Debug statement

            for category in config["categories"]:
                current_category_name = category["category_name"]
                callback_function = (
                    lambda _, name=current_category_name: handle_click_tool_category(
                        str(category["category_name"])
                    )
                )
                with mui.Accordion(
                    sx={
                        "fontSize": "0.9rem",
                        "margin-left": "-7px !important",
                        "margin-right": "-7px !important",
                        "-webkit-text-size-adjust": "100%",
                        "tab-size": "4",
                        "line-height": "inherit",
                        "--tw-bg-opacity": "1",
                        "--tw-text-opacity": "1",
                        "overflow-wrap": "break-word",
                        "border": "0 solid #000101",
                        "box-sizing": "border-box",
                        "--tw-shadow": "0 0#ffffff00",
                        "--tw-shadow-colored": "0 0#0000",
                        "justify-content": "center",
                        "text-align": "center",
                        "flex-grow": "1",
                        "borderRadius": {"type": "static", "content": "19.09375px"},
                        "borderWidth": {
                            "type": "static",
                            "content": "1.004934310913086px",
                        },
                        "borderColor": {
                            "type": "static",
                            "content": "rgba(20, 150, 200, 0.03)",
                        },
                        "borderStyle": {
                            "type": "static",
                            "content": "solid",
                        },
                        "background-color": "#334155",
                        "background-image": "linear-gradient(225deg, transparent 55px, #334155 0)",
                        "margin-bottom": "-15px",
                        "margin-top": "15px",
                        "padding-top": "5px",
                        "padding-bottom": "-15px",
                        "borderRadius": {"type": "static", "content": "40px"},
                        "borderWidth": {"type": "static", "content": "1px"},
                        "borderStyle": {"type": "static", "content": "solid"},
                        "background-image": "linear-gradient(225deg, transparent 55px, #334155 0)",
                    },
                    TransitionProps={"unmountOnExit": "true"},
                    onChange=callback_function,
                ):
                    with mui.AccordionSummary(
                        style={
                            "background": category["category_color"],
                            "shadowColor": category["category_color"],
                            "text-align": "center",
                            "item-align": "center",
                            "self-align": "center",
                            "max-height": "10px !important",
                        }
                    ):
                        getattr(mui.icon, category["icon"])()
                        mui.Typography(
                            category["category_name"],
                            sx={
                                "margin-right": "auto",
                                "margin-left": "auto",
                            },
                        )
                    with mui.AccordionDetails(
                        sx={
                            "fontSize": "0.9rem",
                            "margin-left": "-8px !important",
                            "margin-right": "-8px !important",
                        },
                    ):
                        for app in category["apps"]:
                            button_vertical_list(
                                app["icon"],
                                app["title"],
                                app["description"],
                                app["color"],
                                app["page_name"],
                            )


###


# Function to generate the button vertical list
def tools_vertical_list(icon_name, app_name, description, button_color, page_name):
    """Generates a vertical button list."""    
    with mui.Grid(
        container=True, direction="row", alignText="center",height="45px", justify="space-between", backgroundColor=button_color,style={"box-shadow": "rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset;",}):

        with mui.Grid(item=True, xs=9):
            mui.Typography(app_name)
            mui.Typography(description, variant="body2", style={"fontSize": "0.7rem"})
        
        with mui.Grid(item=True, xs=1):
            with mui.IconButton(
                variant="contained",
                backgroundColor=button_color,
                style={"margin-right": "100%", "margin-left": "0%", "self-align": "right",},
                onClick=lambda: change_page_extended(str(page_name).lower()),
            ):
                getattr(mui.icon, icon_name)()

    mui.Divider()



def tools_box():
    """Generates the tools box."""
    
    # Check if the config file exists before trying to open it.
    if not os.path.exists("tools_config.json"):
        st.warning("Configuration file (tools_config.json) not found!")
        return

    with open("tools_config.json", "r") as file:
        config = json.load(file)

        with elements("multiple_children_test"):
            
            def handle_click_app_category(category_name):
                st.session_state.ai_tools_accordion_active = category_name
                st.write(f"Clicked on: {category_name}")  # Debug statement

            for category in config["categories"]:
                current_category_name = category["category_name"]
                callback_function = (
                    lambda _, name=current_category_name: handle_click_app_category(
                        str(category["category_name"])
                    )
                )
                with mui.Accordion(
                    sx={
                        "fontSize": "0.9rem",
                        "margin-left": "-7px !important",
                        "margin-right": "-7px !important",
                        "-webkit-text-size-adjust": "100%",
                        "tab-size": "4",
                        "line-height": "inherit",
                        "--tw-bg-opacity": "1",
                        "--tw-text-opacity": "1",
                        "overflow-wrap": "break-word",
                        "border": "0 solid #000101",
                        "box-sizing": "border-box",
                        "--tw-shadow": "0 0#ffffff00",
                        "--tw-shadow-colored": "0 0#0000",
                        "justify-content": "center",
                        "text-align": "center",
                        "flex-grow": "1",
                        "borderRadius": {"type": "static", "content": "19.09375px"},
                        "borderWidth": {
                            "type": "static",
                            "content": "1.004934310913086px",
                        },
                        "borderColor": {
                            "type": "static",
                            "content": "rgba(20, 150, 200, 0.03)",
                        },
                        "borderStyle": {
                            "type": "static",
                            "content": "solid",
                        },
                        "background-color": "#334155",
                        "background-image": "linear-gradient(225deg, transparent 55px, #334155 0)",
                        "margin-bottom": "-15px",
                        "margin-top": "15px",
                        "padding-top": "5px",
                        "padding-bottom": "-15px",
                        "borderRadius": {"type": "static", "content": "40px"},
                        "borderWidth": {"type": "static", "content": "1px"},
                        "borderStyle": {"type": "static", "content": "solid"},
                        "background-image": "linear-gradient(225deg, transparent 55px, #334155 0)",
                    },
                    TransitionProps={"unmountOnExit": "true"},
                    onChange=callback_function,
                ):
                    with mui.AccordionSummary(
                        style={
                            "background": category["category_color"],
                            "shadowColor": category["category_color"],
                            "text-align": "center",
                            "item-align": "center",
                            "self-align": "center",
                            "max-height": "10px !important",
                        }
                    ):
                        getattr(mui.icon, category["icon"])()
                        mui.Typography(
                            category["category_name"],
                            sx={
                                "margin-right": "auto",
                                "margin-left": "auto",
                            },
                        )
                    with mui.AccordionDetails(
                        sx={
                            "fontSize": "0.9rem",
                            "margin-left": "-8px !important",
                            "margin-right": "-8px !important",
                        },
                    ):
                        for app in category["tools"]:
                            button_vertical_list(
                                app["icon"],
                                app["title"],
                                app["description"],
                                app["color"],
                                app["page_name"],
                            )






######## ! BUILDING ! mlearningS_BOX ##############


# Function to generate the button vertical list
def mlearning_vertical_list(icon_name, app_name, description, button_color, page_name):
    """Generates a vertical button list."""    
    with mui.Grid(
        container=True, direction="row", alignText="center",height="45px", justify="space-between", backgroundColor=button_color,style={"box-shadow": "rgba(50, 50, 93, 0.25) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.3) 0px 18px 36px -18px inset;",}):

        with mui.Grid(item=True, xs=9):
            mui.Typography(app_name)
            mui.Typography(description, variant="body2", style={"fontSize": "0.7rem"})
        
        with mui.Grid(item=True, xs=1):
            with mui.IconButton(
                variant="contained",
                backgroundColor=button_color,
                style={"margin-right": "100%", "margin-left": "0%", "self-align": "right",},
                onClick=lambda: change_page_extended(str(page_name).lower()),
            ):
                getattr(mui.icon, icon_name)()

    mui.Divider()



def mlearning_box():
    """Generates the mlearning box."""
    
    # Check if the config file exists before trying to open it.
    if not os.path.exists("mlearning_config.json"):
        st.warning("Configuration file (mlearning_config.json) not found!")
        return

    with open("mlearning_config.json", "r") as file:
        config = json.load(file)

        with elements("multiple_children_test"):
            
            def handle_click_app_category(category_name):
                st.session_state.ai_mlearning_accordion_active = category_name
                st.write(f"Clicked on: {category_name}")  # Debug statement

            for category in config["categories"]:
                current_category_name = category["category_name"]
                callback_function = (
                    lambda _, name=current_category_name: handle_click_app_category(
                        str(category["category_name"])
                    )
                )
                with mui.Accordion(
                    sx={
                        "fontSize": "0.9rem",
                        "margin-left": "-7px !important",
                        "margin-right": "-7px !important",
                        "-webkit-text-size-adjust": "100%",
                        "tab-size": "4",
                        "line-height": "inherit",
                        "--tw-bg-opacity": "1",
                        "--tw-text-opacity": "1",
                        "overflow-wrap": "break-word",
                        "border": "0 solid #000101",
                        "box-sizing": "border-box",
                        "--tw-shadow": "0 0#ffffff00",
                        "--tw-shadow-colored": "0 0#0000",
                        "justify-content": "center",
                        "text-align": "center",
                        "flex-grow": "1",
                        "borderRadius": {"type": "static", "content": "19.09375px"},
                        "borderWidth": {
                            "type": "static",
                            "content": "1.004934310913086px",
                        },
                        "borderColor": {
                            "type": "static",
                            "content": "rgba(20, 150, 200, 0.03)",
                        },
                        "borderStyle": {
                            "type": "static",
                            "content": "solid",
                        },
                        "background-color": "#334155",
                        "background-image": "linear-gradient(225deg, transparent 55px, #334155 0)",
                        "margin-bottom": "-15px",
                        "margin-top": "15px",
                        "padding-top": "5px",
                        "padding-bottom": "-15px",
                        "borderRadius": {"type": "static", "content": "40px"},
                        "borderWidth": {"type": "static", "content": "1px"},
                        "borderStyle": {"type": "static", "content": "solid"},
                        "background-image": "linear-gradient(225deg, transparent 55px, #334155 0)",
                    },
                    TransitionProps={"unmountOnExit": "true"},
                    onChange=callback_function,
                ):
                    with mui.AccordionSummary(
                        style={
                            "background": category["category_color"],
                            "shadowColor": category["category_color"],
                            "text-align": "center",
                            "item-align": "center",
                            "self-align": "center",
                            "max-height": "10px !important",
                        }
                    ):
                        getattr(mui.icon, category["icon"])()
                        mui.Typography(
                            category["category_name"],
                            sx={
                                "margin-right": "auto",
                                "margin-left": "auto",
                            },
                        )
                    with mui.AccordionDetails(
                        sx={
                            "fontSize": "0.9rem",
                            "margin-left": "-8px !important",
                            "margin-right": "-8px !important",
                        },
                    ):
                        for app in category["mlearning"]:
                            button_vertical_list(
                                app["icon"],
                                app["title"],
                                app["description"],
                                app["color"],
                                app["page_name"],
                            )






#########!!!!!!!!!

# Add this at the end of your script or wherever you wish to see the currently active accordion.
#f "ai_apps_accordion_active" in st.session_state:
#   st.write(f"Active accordion: {st.session_state.ai_apps_accordion_active}")
#lse:
#   st.write("No accordion is active.")
#


# Sidebar Header Row 2 with mui buttons
def sidebar_header_button():
    """Renders the sidebar header button."""
    with st.sidebar:
        st.image(image, width=100)
        # Your existing mui.ButtonGroup code
        with elements("multiple_children"):

            def reset_active_button_color():
                st.session_state.color_active_settings_button = "transparent"
                st.session_state.color_active_help_button = "transparent"
                st.session_state.color_active_datastore_button = "transparent"
                st.session_state.color_active_tools_button = "transparent"
                st.session_state.color_active_dashboard_button = "transparent"
                st.session_state.color_active_bots_button = "transparent"
                st.session_state.color_active_mlearning_button = "transparent"

            # Initialize a new item in session state called "my_text"
            if "color_active_settings_button" not in st.session_state:
                st.session_state.menu_active_button = ""
                st.session_state.active_section = ""
                reset_active_button_color()

            def handle_click_settings():
                st.session_state.menu_active_button = "settings"
                st.session_state.active_section = "settings"
                reset_active_button_color()
                st.session_state.color_active_settings_button = button_active

            def handle_click_help():
                st.session_state.menu_active_button = "help"
                st.session_state.active_section = "help"
                reset_active_button_color()
                st.session_state.color_active_help_button = button_active

            def handle_click_datastore():
                st.session_state.menu_active_button = "datastore"
                st.session_state.active_section = "datastore"
                reset_active_button_color()
                st.session_state.color_active_datastore_button = button_active

            def handle_click_bots():
                st.session_state.menu_active_button = "bots"
                st.session_state.active_section = "bots"
                reset_active_button_color()
                st.session_state.color_active_bots_button = button_active
                
            def handle_click_mlearning():
                st.session_state.menu_active_button = "mlearning"
                st.session_state.active_section = "mlearning"
                reset_active_button_color()
                st.session_state.color_active_mlearning_button = button_active
                
            def handle_click_tools():
                st.session_state.menu_active_button = "tools"
                st.session_state.active_section = "tools"
                reset_active_button_color()
                st.session_state.color_active_tools_button = button_active

            def handle_click_dashboard():
                st.session_state.menu_active_button = "dashboard"
                st.session_state.active_section = "dashboard"
                reset_active_button_color()
                st.session_state.color_active_dashboard_button = button_active

            mui.ButtonGroup(
                mui.Button(
                    mui.icon.Settings,
                    onClick=handle_click_settings,
                    sx={
                        "background-color": st.session_state.color_active_settings_button,
                        "color": "#F2F7FA",
                    },
                ),
                mui.Button(
                    mui.icon.HelpCenter,
                    onClick=handle_click_help,
                    sx={
                        "background-color": st.session_state.color_active_help_button,
                        "color": "#E1EBF2",
                    },
                ),
                mui.Button(
                    mui.icon.Folder,
                    onClick=handle_click_datastore,
                    sx={
                        "background-color": st.session_state.color_active_datastore_button,
                        "color": "#E1EBF2",
                    },
                ),
                mui.Button(
                    mui.icon.SmartToy,
                    onClick=handle_click_bots,
                    sx={
                        "background-color": st.session_state.color_active_bots_button,
                        "color": "#BACDE0",
                    },
                ),
                # mui.IconButton(mui.icon.Apps, onClick=handle_click_apps),
                mui.Button(
                    mui.icon.School,
                    onClick=handle_click_mlearning,
                    sx={
                        "background-color": st.session_state.color_active_mlearning_button,
                        "color": "#BACDE0",
                    },
                ),
                mui.Button(
                    mui.icon.Handyman,
                    onClick=handle_click_tools,
                    sx={
                        "background-color": st.session_state.color_active_tools_button,
                        "color": "#95AECF",
                    },
                ),
                # mui.IconButton(mui.icon.Dashboard, onClick=handle_click_dashboard),
                mui.Button(
                    mui.icon.Assistant,
                    onClick=handle_click_dashboard,
                    sx={
                        "background-color": st.session_state.color_active_dashboard_button,
                        "color": "#95AECF",
                    },
                ),
                variant="contained",
                label="outlined primary button group",
                size="small",
                sx={
                    "-webkit-text-size-adjust": "100%",
                    "tab-size": "4",
                    "line-height": "inherit",
                    "--tw-bg-opacity": "1",
                    "--tw-text-opacity": "1",
                    "overflow-wrap": "break-word",
                    "border": "0 solid #000101",
                    "box-sizing": "border-box",
                    "--tw-shadow": "0 0#ffffff00",
                    "--tw-shadow-colored": "0 0#0000",
                    "display": "flex",
                    "flex-grow": "1",
                    "justify-content": "center",
                    "background-color": "#334155",
                    "filter": "drop-shadow(0 0 10px black)",
                    "min-width": "100%",
                    "margin-right": "-8px",
                    "margin-left": "-8px",
                    "margin-top": "-8px",
                    "padding-bottom": "8px",
                },
            ),
            mui.LinearProgress(
                value=100,
                variant="determinate",
                sx={
                    "margin-bottom": "8px",
                    "max-height": "8px",
                    "margin-right": "-8px",
                    "margin-left": "-8px",
                    # "padding-bottom": "-8px",
                },
            )
    return st.session_state.menu_active_button



