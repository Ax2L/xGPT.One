# components/css/rawbase_style.py
# ? ------------------ Imports ------------------
import streamlit as st

base_colors = """
primary = "#007BFF"
primary_hover = "#0056b3"
primary_active = "#004c99"
primary_click = "#003366"
secondary = "#6C757D"
secondary_hover = "#545b62"
secondary_active = "#444d52"
secondary_click = "#343c42"
success = "#28A745"
success_hover = "#1f7a33"
success_active = "#196e2b"
success_click = "#145223"
danger = "#DC3545"
danger_hover = "#b02c39"
danger_active = "#94232d"
danger_click = "#721922"
warning = "#FFC107"
warning_hover = "#cc9e06"
warning_active = "#997a05"
warning_click = "#665304"
info = "#17A2B8"
info_hover = "#128192"
info_active = "#0d607c"
info_click = "#093f66"
"""

typography = """
font_family = "Arial, sans-serif"
font_size = "16px"
color = "#333"
line_height = "1.5"

"""
layout = """
max_width = "1200px"
padding = "0 15px"
row_display = "flex"
row_flex_wrap = "wrap"
column_flex = "1"
"""

headers = """
background_color = "#262730"
background_color_hover = "#202024"
background_color_active = "#19191d"
border = "0"
border_bottom = "#A5334155"
border_color = "#DDDDDD"
border_color_hover = "#AAAAAA"
border_color_active = "#888888"
border_color_click = "#666666"
box_shadow = ""
button_color = "#1E1E1E"
button_color_hover = "#171717"
button_color_click = "#101010"
button_color_active = "#0b0b0b"
button_bg = "#334155"
button_bg_hover = "#2a3544"
button_bg_click = "#202933"
button_bg_active = "#151d22"
filter = "brightness(0.9)"
position = "static"
align_items = "center"
padding = "0"
z_index = "21"
transition_duration = "0s"
text_align = "center"
TabsGroup_indicatorColor = "primary"
TabsGroup_textColor = "primary"
TabsGroup_variant = "normal"
"""

logo = """
background = "transparent"
height = 60
width = 100
ml = "70px"
mr = "-70px"
background_hover = "#DDDDDD"
"""

submenu = """
align_items = "center"
background_color = "#334155"
background_color_hover = "#2a3544"
background_color_active = "#202933"
background_color_click = "#151d22"
border = "0"
border_bottom = "#A5334155"
border_color = "#DDDDDD"
border_color_hover = "#AAAAAA"
border_color_active = "#888888"
border_color_click = "#666666"
box_shadow = ""
button_color = "#1E1E1E"
button_color_hover = "#171717"
button_color_click = "#101010"
button_color_active = "#0b0b0b"
button_bg = "#334155"
button_bg_hover = "#2a3544"
button_bg_click = "#202933"
button_bg_active = "#151d22"
button_basic_background_color = "#1E1E1E"
button_basic_box_shadow = "0px 4px 4px rgba(0, 0, 0, 0.30)"
button_basic_color = "#FFFFFF"
button_basic_color_hover = "#DDDDDD"
button_basic_color_click = "#BBBBBB"
button_basic_color_active = "#888888"
button_box_shadow = "0px 4px 4px rgba(0, 0, 0, 0.30)"
filter = "brightness(0.9)"
height = ""
padding = "0"
position = "static"
text_align = "center"
text_color = "#FFFFFF"
text_color_hover = "#DDDDDD"
text_color_click = "#BBBBBB"
text_color_active = "#888888"
transition_duration = "0s"
width = ""
z_index = "21"
margin = "0"
margin_left = "0"
margin_right = "0"
margin_top = "0"
margin_bottom = "0"
"""

buttons = """
display = "inline-block"
padding = "10px 20px"
border = "none"
cursor = "pointer"
transition = "all 0.3s"
background_color = "#FFC107"
filter = "hue-rotate(10deg)"
color = "#fff"
promo_background_color = "#28A745"
promo_filter = "grayscale(50%)"
promo_font_size = "1.25em"
"""

containers = """
background_color = "#6C757D"
filter = "contrast(1.2)"
border = "2px solid #DC3545"
"""

unsorted = """
header_frame_background_color = "#334155"
container_bg_normal = "#334155"
container_bg_hover = "#2a3544"
button_box_shadow = "0px 4px 4px rgba(0, 0, 0, 0.30)"
button_normal = "#1E1E1E"
button_hover = "#171717"
button_click = "#101010"
button_active = "#0b0b0b"
button_bg_normal = "#334155"
button_bg_hover = "#2a3544"
button_bg_active = "#202933"
button_basic_background_color = "#1E1E1E"
button_basic_color = "#FFFFFF"
button_basic_box_shadow = "0px 4px 4px rgba(0, 0, 0, 0.30)"
logo_margin_right = "16px"
"""


# ? ------------------ Helper Functions ------------------
# Convert the block string to a dictionary
def block_to_dict(block_string):
    style_dict = {}
    lines = block_string.strip().split("\n")
    for line in lines:
        key, value = line.split("=")
        key = key.strip()
        value = value.strip()
        # remove quotation marks if value is a string
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif (
            "." in value
        ):  # if the value looks like a number with decimal points, convert it
            try:
                value = float(value)
            except ValueError:
                pass  # it wasn't a float after all
        else:  # if the value looks like an integer, convert it
            try:
                value = int(value)
            except ValueError:
                pass  # it wasn't an int after all

        style_dict[key] = value

    return style_dict


def store_style():
    # Parse each block and store in session_state
    if "style_settings" not in st.session_state:
        blocks = {
            "base_colors": base_colors,
            "typography": typography,
            "layout": layout,
            "headers": headers,
            "logo": logo,
            "submenu": submenu,
            "buttons": buttons,
            "containers": containers,
            "unsorted": unsorted,
        }

        for block_name, block_string in blocks.items():
            st.session_state[block_name] = block_to_dict(block_string)

    print("Styles loaded into st.session_state")


# Entry point
if __name__ == "__main__":
    store_style()
