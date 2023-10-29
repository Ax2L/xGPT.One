# styles_process.py
import toml
import streamlit as st
import os

# Default settings
DEFAULT_SETTINGS = {
    'base_colors': {
        'primary': 'default_primary',
        'secondary': 'default_secondary',
        'success': 'default_success',
        'danger': 'default_danger',
        'warning': 'default_warning',
        'info': 'default_info'
    },
    'typography': {
        'font_family': 'default_font',
        'font_size': 'default_size',
        'color': 'default_color',
        'line_height': 'default_line_height'
    },
    'layout': {
        'container_max_width': 'default_max_width',
        'container_padding': 'default_padding',
        'row_display': 'default_display',
        'row_flex_wrap': 'default_flex_wrap',
        'column_flex': 'default_flex'
    },
    'headers': {
        'stHeader_background_color': 'default_background',
        'stHeader_filter': 'default_filter',
        'stHeader_padding': 'default_padding',
        'Header_background_color': 'default_background',
        'Header_filter': 'default_filter',
        'Header_padding': 'default_padding',
        'Header_text_align': 'default_text_align'
    },
    'buttons': {
        'button_display': 'default_display',
        'button_padding': 'default_padding',
        'button_border': 'default_border',
        'button_cursor': 'default_cursor',
        'button_transition': 'default_transition',
        'stButton_background_color': 'default_background',
        'stButton_filter': 'default_filter',
        'stButton_color': 'default_color',
        'MuiButton_background_color': 'default_background',
        'MuiButton_filter': 'default_filter',
        'MuiButton_color': 'default_color'
    },
    'containers': {
        'special_container_background_color': 'default_background',
        'special_container_filter': 'default_filter',
        'special_container_border': 'default_border'
    }
}

# ... [Your functions here: find_file, get_styles_toml_path, load_styles_from_toml] ...

if "toml_data" not in st.session_state:
    st.session_state.setdefault("toml_data", {})
toml_data = load_styles_from_toml()
st.session_state["toml_data"] = toml_data

# Update toml_data with missing keys and default values
for section, defaults in DEFAULT_SETTINGS.items():
    if section not in toml_data:
        toml_data[section] = defaults
    else:
        for key, default_value in defaults.items():
            toml_data[section][key] = toml_data[section].get(key, default_value)

BASE_COLORS = {
    '--base-primary': toml_data['base_colors']['primary'],
    '--base-secondary': toml_data['base_colors']['secondary'],
    '--base-success': toml_data['base_colors']['success'],
    '--base-danger': toml_data['base_colors']['danger'],
    '--base-warning': toml_data['base_colors']['warning'],
    '--base-info': toml_data['base_colors']['info']
}

TYPOGRAPHY = {
    'font-family': toml_data['typography']['font_family'],
    'font-size': toml_data['typography']['font_size'],
    'color': toml_data['typography']['color'],
    'line-height': toml_data['typography']['line_height']
}

LAYOUT = {
    'container': {
        'max-width': toml_data['layout']['container_max_width'],
        'margin': "0 auto",
        'padding': toml_data['layout']['container_padding']
    },
    'row': {
        'display': toml_data['layout']['row_display'],
        'flex-wrap': toml_data['layout']['row_flex_wrap']
    },
    'column': {
        'flex': toml_data['layout']['column_flex']
    }
}

# Enhanced Headers
HEADERS = {
    'stHeader': {
        'background-color': toml_data['headers']['stHeader_background_color'],
        'filter': toml_data['headers']['stHeader_filter'],
        'padding': toml_data['headers']['stHeader_padding']
    },
    'Header': {
        'background-color': toml_data['headers']['Header_background_color'],
        'filter': toml_data['headers']['Header_filter'],
        'padding': toml_data['headers']['Header_padding'],
        'text-align': toml_data['headers']['Header_text_align']
    }
}

# Enhanced Button Styles
BUTTONS = {
    'button': {
        'display': toml_data['buttons']['button_display'],
        'padding': toml_data['buttons']['button_padding'],
        'border': toml_data['buttons']['button_border'],
        'cursor': toml_data['buttons']['button_cursor'],
        'transition': toml_data['buttons']['button_transition']
    },
    'stButton': {
        'background-color': toml_data['buttons']['stButton_background_color'],
        'filter': toml_data['buttons']['stButton_filter'],
        'color': toml_data['buttons']['stButton_color']
    },
    'MuiButton': {
        'background-color': toml_data['buttons']['MuiButton_background_color'],
        'filter': toml_data['buttons']['MuiButton_filter'],
        'color': toml_data['buttons']['MuiButton_color']
    }
}

# Containers
CONTAINERS = {
    'special-container': {
        'background-color': toml_data['containers']['special_container_background_color'],
        'filter': toml_data['containers']['special_container_filter'],
        'border': toml_data['containers']['special_container_border']
    }
}

# Storing style blocks in session state
st.session_state["style_blocks"] = {
    "BASE_COLORS": BASE_COLORS,
    "TYPOGRAPHY": TYPOGRAPHY,
    "LAYOUT": LAYOUT,
    "HEADERS": HEADERS,
    "BUTTONS": BUTTONS,
    "CONTAINERS": CONTAINERS
}