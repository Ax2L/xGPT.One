## styles_process.py
## ? ------------------ Imports ------------------
#import toml
#import streamlit as st
#import os
#
## First object: Cleanup CSS
#cleanup_css = """
#<html>
#<head>
#<style>
#:root {
#    font-family: Roboto;
#
#}
#.title {
#    font-size: 34px;
#    font-family: "Roboto";
#    font-weight: 400;
#    width: 360px;
#    height: 40px;
#}
#body {
#    margin: 0;
#    padding: 0;
#}
#h1, h2, h3, p {
#    margin-block-start: 0;
#    margin-block-end: 0;
#}
#header[data-testid="stHeader"] {
#    display: none !important;
#}
#/* Cleanup the Header Styles */
#section[tabindex="0"] div[data-testid="block-container"] {
#    padding-top: 0 !important;
#    padding-bottom: 0 !important;
#    padding-left: 0 !important;
#    padding-right: 0 !important;
#    display: flex !important;
#    align-items: center !important;
#    justify-content: center !important;
#    position: fixed !important;
#    top: 0 !important;
#    left: 0 !important;
#}
#section[data-testid="stSidebar"] {
#    background-color: #262730;
#}
#</style>
#</head>
#</html>
#"""
#
## Second object: End of Script Components
#end_of_script_components = """
#<html>
#<head>
#<!-- Hypothetical end of script components. Adjust according to your needs. -->
#<script>
#    // Add your JavaScript here.
#    console.log("End of script components loaded.");
#</script>
#<!-- You can also add other components or tags as needed -->
#</head>
#</html>
#"""
#
## Streamlit functions to apply the above CSS and JavaScript
#def apply_cleanup_css():
#    st.markdown(cleanup_css, unsafe_allow_html=True)
#
#def apply_end_of_script_components():
#    st.markdown(end_of_script_components, unsafe_allow_html=True)
#
#
## ? ------------------ Helper Functions ------------------
#def find_file(target_name, start_dir):
#    """
#    Search for a file with a given name, diving one level deeper each time.
#
#    Parameters:
#        target_name (str): The name of the file to search for.
#        start_dir (str): The directory from which the search begins.
#
#    Returns:
#        str: The full path of the found file, or None if not found.
#    """
#
#    # Check current directory first
#    for root, dirs, files in os.walk(start_dir):
#        if target_name in files:
#            return os.path.join(root, target_name)
#        break  # Only check current directory
#
#    # Check subdirectories, one level deeper
#    for dir_name in os.listdir(start_dir):
#        dir_path = os.path.join(start_dir, dir_name)
#        if os.path.isdir(dir_path):
#            for root, dirs, files in os.walk(dir_path):
#                if target_name in files:
#                    return os.path.join(root, target_name)
#                break  # Only check current directory within the subdir
#
#    return None
#
#
#def get_styles_toml_path():
#    file_name_to_search = "style_base.toml"
#    start_directory = "."
#    result = find_file(file_name_to_search, start_directory)
#    if result:
#        print(f"Found {file_name_to_search} at: {result}")
#        return result
#    else:
#        print(f"{file_name_to_search} not found.")
#        return None
#
## ! ------------------ Default Settings ------------------
#def toml_to_style_settings(filepath):
#    # Load the TOML content
#    with open(filepath, 'r') as file:
#        content = toml.load(file)
#    
#    # Prepare the style_settings dictionary
#    style_settings = {}
#    
#    for section, attributes in content.items():
#        style_section = {}
#        for attribute, value in attributes.items():
#            style_section[attribute] = f"default_{attribute}"
#        style_settings[section] = style_section
#
#    return style_settings
#
## Load the styles from 'base_styles.toml' into the style_settings dictionary
#filepath = "./components/style_base.toml"
#DEFAULT_SETTINGS = toml_to_style_settings(filepath)
#
#
#def load_styles_from_toml():
#    # Ensure session_state keys are initialized
#    if "base_style" not in st.session_state:
#        st.session_state.base_style = {}
#
#    if "style_blocks" not in st.session_state:
#        st.session_state.style_blocks = {"BASE_COLORS": {}}
#
#    # Check if the TOML content is already in the session state.
#    if not st.session_state.base_style:
#        styles_path = "./components/style_base.toml"
#
#        # Ensure that styles_path is not None before proceeding
#        if styles_path is None:
#            print("Error: style_base.toml not found.")
#            return {}
#
#        with open(styles_path, "r") as toml_file:
#            st.session_state.base_style = toml.load(toml_file)
#
#    # Convert the TOML content to styles.
#    styles = {}
#    for key, value in st.session_state.base_style.items():
#        if isinstance(value, dict):
#            for sub_key, sub_value in value.items():
#                styles[f"{key}--{sub_key}"] = sub_value
#        else:
#            styles[key] = value
#    st.session_state.base_style = styles
#    return styles
#
#
## * ------------------ Main Code Execution ------------------
#toml_data = load_styles_from_toml()
#if "toml_data" not in st.session_state:
#    st.session_state.setdefault("toml_data", toml_data)
#
#BASE_COLORS = {
#    "--base-primary": toml_data["base_colors--primary"],
#    "--base-secondary": toml_data["base_colors--secondary"],
#    "--base-success": toml_data["base_colors--success"],
#    "--base-danger": toml_data["base_colors--danger"],
#    "--base-warning": toml_data["base_colors--warning"],
#    "--base-info": toml_data["base_colors--info"],
#}
#
#TYPOGRAPHY = {
#    "font-family": toml_data["typography--font_family"],
#    "font-size": toml_data["typography--font_size"],
#    "color": toml_data["typography--color"],
#    "line-height": toml_data["typography--line_height"],
#}
#
#LAYOUT = {
#    "container": {
#        "max-width": toml_data["layout--max_width"],
#        "margin": "0 auto",
#        "padding": toml_data["layout--padding"],
#    },
#    "row": {
#        "display": toml_data["layout--row_display"],
#        "flex-wrap": toml_data["layout--row_flex_wrap"],
#    },
#    "column": {"flex": toml_data["layout--column_flex"]},
#}
#
#
## ! ------------------ Styles Initialization ------------------
#if "base_colors" in toml_data:
#    BASE_COLORS = {
#        "--base-primary": toml_data["base_colors"]["primary--default_value"],
#        "--base-secondary": toml_data["base_colors"]["secondary--default_value"],
#        "--base-success": toml_data["base_colors"]["success--default_value"],
#        "--base-danger": toml_data["base_colors"]["danger--default_value"],
#        "--base-warning": toml_data["base_colors"]["warning--default_value"],
#        "--base-info": toml_data["base_colors"]["info--default_value"],
#    }
#else:
#    print("Warning: 'base_colors' not found in toml_data")
#    BASE_COLORS = {}
#
## & Base Typography
#TYPOGRAPHY = {
#    "font-family": toml_data["typography--font_family"],
#    "font-size": toml_data["typography--font_size"],
#    "color": toml_data["typography--color"],
#    "line-height": toml_data["typography--line_height"],
#}
#
## ~ Base Layout Objects
#LAYOUT = {
#    "container": {
#        "max-width": toml_data["layout--max_width"],
#        "margin": "0 auto",
#        "padding": toml_data["layout--padding"],
#    },
#    "row": {
#        "display": toml_data["layout--row_display"],
#        "flex-wrap": toml_data["layout--row_flex_wrap"],
#    },
#    "column": {"flex": toml_data["layout--column_flex"]},
#}
#
## ^ Enhanced Headers
#HEADERS = {
#    "off": {},
#    "main": {
#        "display": "flex",
#        "flex-direction": "row",
#        "align-items": "center",
#        "justify-content": "space-between",
#    },
#    "header": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#    },
#    "logo": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#        "height": "60",
#        "width": "100",
#        "background": "transparent",
#    },
#    "tabs": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#        "display": "flex",
#        "align-items": "center",
#        "justify-content": "center",
#    },
#    "tabsgroup": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#    },
#    "iconbutton": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#    },
#    "iconbuttongroup": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#    },
#    "submenu_button": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#    },
#        "submenu_buttongroup": {
#        "background-color": toml_data["headers--background_color"],
#        "filter": toml_data["headers--filter"],
#        "padding": toml_data["headers--padding"],
#        "text-align": toml_data["headers--text_align"],
#    },
#}
#
## * Enhanced Button Styles
#BUTTONS = {
#    "button": {
#        "display": toml_data["buttons--display"],
#        "padding": toml_data["buttons--padding"],
#        "border": toml_data["buttons--border"],
#        "cursor": toml_data["buttons--cursor"],
#        "transition": toml_data["buttons--transition"],
#    }
#}
#
## ? Containers
#CONTAINERS = {
#    "special-container": {
#        "background-color": toml_data["containers--background_color"
#        ],
#        "filter": toml_data["containers--filter"],
#        "border": toml_data["containers--border"],
#    }
#}
#
#def store_style_block():
#    # ^Storing style blocks in session state'
#    st.session_state["style_blocks"] = {
#        "BASE_COLORS": BASE_COLORS,
#        "TYPOGRAPHY": TYPOGRAPHY,
#        "LAYOUT": LAYOUT,
#        "HEADERS": HEADERS,
#        "BUTTONS": BUTTONS,
#        "CONTAINERS": CONTAINERS,
#    }
#
#if "style_blocks" not in st.session_state:
#    store_style_block()