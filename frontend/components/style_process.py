# styles_process.py
# ? ------------------ Imports ------------------
import toml
import streamlit as st
import os

# ! ------------------ Default Settings ------------------
DEFAULT_SETTINGS = {
    "base_colors": {
        "primary": "default_primary",
        "secondary": "default_secondary",
        "success": "default_success",
        "danger": "default_danger",
        "warning": "default_warning",
        "info": "default_info",
    },
    "typography": {
        "font_family": "default_font",
        "font_size": "default_size",
        "color": "default_color",
        "line_height": "default_line_height",
    },
    "layout": {
        "container_max_width": "default_max_width",
        "container_padding": "default_padding",
        "row_display": "default_display",
        "row_flex_wrap": "default_flex_wrap",
        "column_flex": "default_flex",
    },
    "headers": {
        "stHeader_background_color": "default_background",
        "stHeader_filter": "default_filter",
        "stHeader_padding": "default_padding",
        "Header_background_color": "default_background",
        "Header_filter": "default_filter",
        "Header_padding": "default_padding",
        "Header_text_align": "default_text_align",
    },
    "buttons": {
        "button_display": "default_display",
        "button_padding": "default_padding",
        "button_border": "default_border",
        "button_cursor": "default_cursor",
        "button_transition": "default_transition",
        "stButton_background_color": "default_background",
        "stButton_filter": "default_filter",
        "stButton_color": "default_color",
        "MuiButton_background_color": "default_background",
        "MuiButton_filter": "default_filter",
        "MuiButton_color": "default_color",
    },
    "containers": {
        "special_container_background_color": "default_background",
        "special_container_filter": "default_filter",
        "special_container_border": "default_border",
    },
}


# ? ------------------ Helper Functions ------------------
def find_file(target_name, start_dir):
    """
    Search for a file with a given name, diving one level deeper each time.

    Parameters:
        target_name (str): The name of the file to search for.
        start_dir (str): The directory from which the search begins.

    Returns:
        str: The full path of the found file, or None if not found.
    """

    # Check current directory first
    for root, dirs, files in os.walk(start_dir):
        if target_name in files:
            return os.path.join(root, target_name)
        break  # Only check current directory

    # Check subdirectories, one level deeper
    for dir_name in os.listdir(start_dir):
        dir_path = os.path.join(start_dir, dir_name)
        if os.path.isdir(dir_path):
            for root, dirs, files in os.walk(dir_path):
                if target_name in files:
                    return os.path.join(root, target_name)
                break  # Only check current directory within the subdir

    return None


def get_styles_toml_path():
    file_name_to_search = "style_base.toml"
    start_directory = "."
    result = find_file(file_name_to_search, start_directory)
    if result:
        print(f"Found {file_name_to_search} at: {result}")
        return result
    else:
        print(f"{file_name_to_search} not found.")
        return None


def load_styles_from_toml():
    # Ensure session_state keys are initialized
    if "base_style" not in st.session_state:
        st.session_state.base_style = {}

    if "style_blocks" not in st.session_state:
        st.session_state.style_blocks = {"BASE_COLORS": {}}

    # Check if the TOML content is already in the session state.
    if not st.session_state.base_style:
        styles_path = get_styles_toml_path()

        # Ensure that styles_path is not None before proceeding
        if styles_path is None:
            print("Error: style_base.toml not found.")
            return {}

        with open(styles_path, "r") as toml_file:
            st.session_state.base_style = toml.load(toml_file)

    # Convert the TOML content to styles.
    styles = {}
    for key, value in st.session_state["style_blocks"]["BASE_COLORS"].items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                styles[f"{key}--{sub_key}"] = sub_value
        else:
            styles[key] = value

    return styles


# * ------------------ Main Code Execution ------------------
if "toml_data" not in st.session_state:
    st.session_state.setdefault("toml_data", {})
toml_data = load_styles_from_toml()
st.session_state["toml_data"] = toml_data

# ^ Update toml_data with missing keys and default values
for section, defaults in DEFAULT_SETTINGS.items():
    if section not in toml_data:
        toml_data[section] = defaults
    else:
        for key, default_value in defaults.items():
            toml_data[section][key] = toml_data[section].get(key, default_value)

BASE_COLORS = {
    "--base-primary": toml_data["base_colors"]["primary"],
    "--base-secondary": toml_data["base_colors"]["secondary"],
    "--base-success": toml_data["base_colors"]["success"],
    "--base-danger": toml_data["base_colors"]["danger"],
    "--base-warning": toml_data["base_colors"]["warning"],
    "--base-info": toml_data["base_colors"]["info"],
}

TYPOGRAPHY = {
    "font-family": toml_data["typography"]["font_family"],
    "font-size": toml_data["typography"]["font_size"],
    "color": toml_data["typography"]["color"],
    "line-height": toml_data["typography"]["line_height"],
}

LAYOUT = {
    "container": {
        "max-width": toml_data["layout"]["container_max_width"],
        "margin": "0 auto",
        "padding": toml_data["layout"]["container_padding"],
    },
    "row": {
        "display": toml_data["layout"]["row_display"],
        "flex-wrap": toml_data["layout"]["row_flex_wrap"],
    },
    "column": {"flex": toml_data["layout"]["column_flex"]},
}


# ! ------------------ Styles Initialization ------------------
if "base_colors" in toml_data:
    BASE_COLORS = {
        "--base-primary": toml_data["base_colors"].get("primary", "default_value"),
        "--base-secondary": toml_data["base_colors"].get("secondary", "default_value"),
        "--base-success": toml_data["base_colors"].get("success", "default_value"),
        "--base-danger": toml_data["base_colors"].get("danger", "default_value"),
        "--base-warning": toml_data["base_colors"].get("warning", "default_value"),
        "--base-info": toml_data["base_colors"].get("info", "default_value"),
    }
else:
    print("Warning: 'base_colors' not found in toml_data")
    BASE_COLORS = {}

# & Base Typography
TYPOGRAPHY = {
    "font-family": toml_data["typography"]["font_family"],
    "font-size": toml_data["typography"]["font_size"],
    "color": toml_data["typography"]["color"],
    "line-height": toml_data["typography"]["line_height"],
}

# ~ Base Layout Objects
LAYOUT = {
    "container": {
        "max-width": toml_data["layout"]["container_max_width"],
        "margin": "0 auto",
        "padding": toml_data["layout"]["container_padding"],
    },
    "row": {
        "display": toml_data["layout"]["row_display"],
        "flex-wrap": toml_data["layout"]["row_flex_wrap"],
    },
    "column": {"flex": toml_data["layout"]["column_flex"]},
}

# ^ Enhanced Headers
HEADERS = {
    "stHeader": {
        "background-color": toml_data["headers"]["stHeader_background_color"],
        "filter": toml_data["headers"]["stHeader_filter"],
        "padding": toml_data["headers"]["stHeader_padding"],
    },
    "header": {
        "background-color": toml_data["headers"]["Header_background_color"],
        "filter": toml_data["headers"]["Header_filter"],
        "padding": toml_data["headers"]["Header_padding"],
        "text-align": toml_data["headers"]["Header_text_align"],
    },
    "header_flex": {
        "background-color": toml_data["headers"]["Header_background_color"],
        "filter": toml_data["headers"]["Header_filter"],
        "padding": toml_data["headers"]["Header_padding"],
        "text-align": toml_data["headers"]["Header_text_align"],
    },
    "button_sx_basic": {
        "background-color": toml_data["headers"]["Header_background_color"],
        "filter": toml_data["headers"]["Header_filter"],
        "padding": toml_data["headers"]["Header_padding"],
        "text-align": toml_data["headers"]["Header_text_align"],
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
    },
    "button_group_basic": {
        "background-color": toml_data["headers"]["Header_background_color"],
        "filter": toml_data["headers"]["Header_filter"],
        "padding": toml_data["headers"]["Header_padding"],
        "text-align": toml_data["headers"]["Header_text_align"],
    },
}

# * Enhanced Button Styles
BUTTONS = {
    "button": {
        "display": toml_data["buttons"]["button_display"],
        "padding": toml_data["buttons"]["button_padding"],
        "border": toml_data["buttons"]["button_border"],
        "cursor": toml_data["buttons"]["button_cursor"],
        "transition": toml_data["buttons"]["button_transition"],
    },
    "stButton": {
        "background-color": toml_data["buttons"]["stButton_background_color"],
        "filter": toml_data["buttons"]["stButton_filter"],
        "color": toml_data["buttons"]["stButton_color"],
    },
    "MuiButton": {
        "background-color": toml_data["buttons"]["MuiButton_background_color"],
        "filter": toml_data["buttons"]["MuiButton_filter"],
        "color": toml_data["buttons"]["MuiButton_color"],
    },
}

# ? Containers
CONTAINERS = {
    "special-container": {
        "background-color": toml_data["containers"][
            "special_container_background_color"
        ],
        "filter": toml_data["containers"]["special_container_filter"],
        "border": toml_data["containers"]["special_container_border"],
    }
}


# todooo#   Storing style blocks in session state
st.session_state["style_blocks"] = {
    "BASE_COLORS": BASE_COLORS,
    "TYPOGRAPHY": TYPOGRAPHY,
    "LAYOUT": LAYOUT,
    "HEADERS": HEADERS,
    "BUTTONS": BUTTONS,
    "CONTAINERS": CONTAINERS,
}
