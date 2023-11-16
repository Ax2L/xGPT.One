import streamlit as st
from streamlit_elements import mui
from components.utils.dashboard.DashUtils import (
    create_grid_settings,
    update_edit_item,
    update_dashboard_item_in_db,
    handleItemChange,
    handleLayoutChange,
    update_edit_layout,
    update_dashboard_layout_in_db,
)


def build_edit_item_form():
    item_nr = st.session_state["item_nr"]
    try:
        # Extract the item data from the session state
        item_data = st.session_state.all_items[item_nr]

        # Hardcoded input fields with onChange logic using lambda
        mui.TextField(
            label="ID",
            defaultValue=item_data[0],  # ID
            disabled=True,
        )
        mui.TextField(
            label="Name",
            defaultValue=item_data[1],  # Name
            onChange=lambda event: handleItemChange(event, "name"),
        )
        mui.TextField(
            label="Entrypoint",
            defaultValue=item_data[2],  # Entrypoint
            onChange=lambda event: handleItemChange(event, "entrypoint"),
        )
        mui.Checkbox(
            label="SSL",
            defaultChecked=item_data[3],  # SSL
            onChange=lambda event: handleItemChange(event, "ssl"),
        )
        mui.TextField(
            label="Repository",
            defaultValue=item_data[4],  # Repository
            onChange=lambda event: handleItemChange(event, "repository"),
        )
        mui.TextField(
            label="Documentation",
            defaultValue=item_data[5],  # Documentation
            onChange=lambda event: handleItemChange(event, "documentation"),
        )
        mui.TextField(
            label="Default Settings",
            defaultValue=item_data[6],  # Default Settings
            onChange=lambda event: handleItemChange(event, "settings_default"),
        )
        mui.TextField(
            label="User Settings",
            defaultValue=item_data[7],  # User Settings
            onChange=lambda event: handleItemChange(event, "settings_user"),
        )
        mui.TextField(
            label="Using in Dashboard",
            defaultValue=item_data[8],  # Using in Dashboard
            onChange=lambda event: handleItemChange(event, "using_in_dashboard"),
        )
        mui.TextField(
            label="URLs",
            defaultValue=item_data[9],  # URLs
            onChange=lambda event: handleItemChange(event, "urls"),
        )
        mui.TextField(
            label="Files",
            defaultValue=item_data[10],  # Files
            onChange=lambda event: handleItemChange(event, "files"),
        )
        mui.TextField(
            label="Tags",
            defaultValue=item_data[11],  # Tags
            onChange=lambda event: handleItemChange(event, "tags"),
        )
        mui.Button(
            "Save",
            onClick=lambda: update_dashboard_item_in_db(),
        ),
    except Exception as e:
        st.error(f"Error: {e}")


def build_edit_layout_form():
    layout_nr = st.session_state["layout_nr"]
    try:
        layout_data = st.session_state.all_layouts[layout_nr]

        mui.TextField(
            label="ID",
            defaultValue=layout_data[0],
            disabled=True,
        )
        mui.TextField(
            label="Name",
            defaultValue=layout_data[1],
            onChange=lambda event: handleLayoutChange(event, "name"),
        )
        mui.TextField(
            label="Description",
            defaultValue=layout_data[2],
            onChange=lambda event: handleLayoutChange(event, "description"),
        )
        mui.TextField(
            label="Tags",
            defaultValue=layout_data[3],
            onChange=lambda event: handleLayoutChange(event, "tags"),
        )
        mui.TextField(
            label="Items",
            defaultValue=layout_data[4],
            onChange=lambda event: handleLayoutChange(event, "items"),
        )
        mui.Button(
            "Save",
            onClick=lambda: update_dashboard_layout_in_db(),
        )
    except Exception as e:
        st.error(f"Error: {e}")
