import streamlit as st
from components import header


# Constants
PAGE_NAME = "test_style"


def load_custom_css():
    if f"{PAGE_NAME}_css" not in st.session_state:
        # ^ Load custom CSS style.
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        print(f"css already active on {PAGE_NAME}")


header.create_menu(PAGE_NAME)

st.title("Style Test UI")

with st.sidebar:
    # Dropdown for selecting a style block
    selected_block = st.selectbox(
        "Select a style block:",
        [
            "base_colors",
            "typography",
            "layout",
            "headers",
            "logo",
            "submenu",
            "buttons",
            "containers",
            "unsorted",
        ],
    )

    # Allow users to modify a specific style in the selected block
    style_key = st.text_input("Enter style key to modify:", "")
    style_value = st.text_input("Enter new value for the style:", "")

    if st.button("Update Style"):
        if style_key and style_value:
            try:
                # Update the style
                st.session_state[selected_block][style_key] = style_value
                st.success(f"Updated {style_key} to {style_value} in {selected_block}")
            except KeyError:
                st.error(f"{style_key} not found in {selected_block}")
        else:
            st.warning("Please enter both style key and value")

    # Display options
    show_options = st.multiselect(
        "What would you like to display?",
        ["Current settings for selected block", "All styles in session_state"],
        default=["Current settings for selected block"],
    )

# Display the current settings for the selected style block
if "Current settings for selected block" in show_options:
    st.subheader(f"Settings for {selected_block}")
    if st.session_state.get(selected_block):
        for key, value in st.session_state[selected_block].items():
            st.write(f"{key}: {value}")

# Display all styles in session state
if "All styles in session_state" in show_options:
    st.subheader("All styles in session_state")
    for block_name, block_content in st.session_state.items():
        if block_name in [
            "base_colors",
            "typography",
            "layout",
            "headers",
            "logo",
            "submenu",
            "buttons",
            "containers",
            "unsorted",
        ]:
            st.write(f"## {block_name}")
            for key, value in block_content.items():
                st.write(f"- {key}: {value}")

load_custom_css()
