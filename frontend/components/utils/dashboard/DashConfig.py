import streamlit as st
from streamlit_elements import elements, mui
from components.utils.dashboard.DashDB import (
    dashboard_items_state_from_db,
    dashboard_layouts_state_from_db,
)
from components.utils.dashboard.DashLists import dash_item_list, dash_layout_list
from components.utils.dashboard.DashForms import (
    build_edit_item_form,
    build_edit_layout_form,
)

# Attributes
allowed_pages = ["apps", "dashboard_layouts_editor", "dashboard_items_editor"]
dashboard_names = ["Dashboard 1", "Dashboard 2", "Dashboard 3"]


# ^ Start
def configure_dash_items(page):
    if page in allowed_pages:
        # ^ Load from DB only if not editing an item
        if "all_items" not in st.session_state or st.session_state["all_items"] is None:
            dashboard_items_state_from_db()
        else:
            print("Skipping database load due to active item editing.")

        # ^ Build MUI Frame
        with elements("dashboard_items_editor"):
            dash_item_list()
            # ? Test if there is an edit item id
            if "item_nr" in st.session_state:
                build_edit_item_form()


# ^ Start
def configure_dash_layouts(page):
    if page in allowed_pages:
        # ^ Load from DB only if not editing an layout
        if (
            "all_layouts" not in st.session_state
            or st.session_state["all_layouts"] is None
        ):
            dashboard_layouts_state_from_db()
        else:
            print("Skipping database load due to active layout editing.")

        # ^ Build MUI Frame
        with elements("dashboard_layouts_editor"):
            dash_layout_list()
            # ? Test if there is an edit layout id
            if "layout_nr" in st.session_state:
                build_edit_layout_form()


def update_selected_dashboard(value):
    st.session_state["selected_dashboard"] = value


def update_edit_item(item_id):
    """Updates the session state with the selected item number for editing."""
    try:
        item_nr = st.session_state[f"item_count_id_{item_id}"]
        item_nr_int = int(item_nr)  # Convert to integer
        st.session_state["item_nr"] = item_nr_int
        # st.info(f"Selected item number for editing: {item_nr_int}")
    except ValueError:
        st.error("Invalid item number. It must be an integer.")


def dashboard_test(page):
    print("Lets try to find the issue!")
    if page in allowed_pages:
        print("page is allowedfa")
        # with elements("dashboard_test"):
        # selected_dashboard = mui.Autocomplete(
        #    options=dashboard_names,
        #    label="Select a Dashboard",
        #    onChange=(
        #        update_selected_dashboard("")
        #    ),  # Reference to the callback function
        # )
