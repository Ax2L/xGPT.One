import streamlit as st
from os import path
from PIL import Image

LOGO_PATH = "../resources/images/logo/favicon.ico"


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


def set_page_config(page_name, layout="wide", sidebar_state="auto"):
    page_name = page_name.replace("_", " ")
    st.set_page_config(
        page_title=f"xGPT.{page_name[0].upper()}{page_name.replace(page_name[0],'')}",
        page_icon=check_for_logo_image(),
        layout=layout,
        initial_sidebar_state=sidebar_state,
    )
