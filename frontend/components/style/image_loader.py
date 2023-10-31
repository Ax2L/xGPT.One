import streamlit as st
from PIL import Image
LOGO_PATH = "images/logo/logo_long.png"
from os import path


def check_for_logo_image(logo_path: str):
    """Checks for the existence of the logo image and returns it."""
    if path.exists(logo_path):
        return Image.open(logo_path)
    st.warning("Logo image not found!")
    return None
