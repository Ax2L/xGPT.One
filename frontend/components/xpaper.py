import streamlit as st
from streamlit_elements import elements, mui, dashboard, html
from components.xdatastore import DashboardLayouts, DashboardItems
import json
from datetime import datetime

# !################################################################


def format_column_name(name):
    return " ".join(word.capitalize() for word in name.split("_"))


def display_dashboard_items():
    try:
        dashboard_items = DashboardItems()
        dashboard_items.load()
        column_names = dashboard_items.get_column_names()

        if dashboard_items.data:
            with mui.Paper():
                with mui.TableContainer():
                    with mui.Table():
                        with mui.TableHead():
                            with mui.TableRow():
                                [
                                    mui.TableCell(format_column_name(column_name))
                                    for column_name in column_names
                                ]
                        with mui.TableBody():
                            for row in dashboard_items.data:
                                with mui.TableRow():
                                    [mui.TableCell(str(cell)) for cell in row]
        else:
            st.write("No dashboard items found.")
    except Exception as e:
        st.error(f"Error displaying dashboard items: {e}")


def display_dashboard_layouts():
    try:
        dashboard_layouts = DashboardLayouts()
        dashboard_layouts.load()
        column_names = dashboard_layouts.get_column_names()

        if dashboard_layouts.data:
            with mui.Paper():
                with mui.TableContainer():
                    with mui.Table():
                        with mui.TableHead():
                            with mui.TableRow():
                                [
                                    mui.TableCell(format_column_name(column_name))
                                    for column_name in column_names
                                ]
                        with mui.TableBody():
                            for row in dashboard_layouts.data:
                                with mui.TableRow():
                                    [mui.TableCell(str(cell)) for cell in row]
        else:
            st.write("No dashboard layouts found.")
    except Exception as e:
        st.error(f"Error displaying dashboard layouts: {e}")


# !#################################################################


def create_iframe(url):
    with elements(url):  # Replace 'your_element_key' with a unique key for your element
        html.Iframe(src=url, style={"height": "400px", "width": "100%"})


def default_layout():
    """Return a default layout."""
    return [
        dashboard.Item("item_0", 0, 0, 2, 2),
        dashboard.Item("item_1", 2, 0, 2, 2),
        dashboard.Item("item_2", 0, 2, 1, 1),
    ]


def test_data_loading(test_page_id):
    try:
        # Initialize the DashboardLayouts instance
        test_layouts = DashboardLayouts(page_id=test_page_id)

        # Attempt to load data
        test_layouts.load()

        # Check if data is loaded
        if test_layouts.data:
            st.write("Data loaded successfully:", test_layouts.data)
        else:
            st.write("No data found for page_id:", test_page_id)

    except Exception as e:
        st.error("Error occurred while loading data:")
        st.exception(e)


def save_layout(layout):
    try:
        page_name = st.session_state["current_page"]
        layouts = DashboardLayouts(page_id=page_name)
        layouts.load()

        layout_json = json.dumps(layout)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if data exists for the page, update if it does, else insert new record
        if layouts.data:
            layouts.update("layout", layout_json)
            layouts.update("updated_at", current_time)
        else:
            layouts.insert(
                page_id=page_name,
                layout=layout_json,
                username="admin",
                page_name=page_name,
                description="Your description here",
                updated_at=current_time,
            )

        st.toast("Layout saved successfully.")
    except Exception as e:
        st.error(f"Error saving layout: {e}")
        st.exception(e)


def load_layout():
    try:
        page_id = st.session_state["current_page"]

        # Check if the layout is already in the session state
        if (
            "dashboard_layout" in st.session_state
            and st.session_state["dashboard_layout_page_id"] == page_id
        ):
            return st.session_state["dashboard_layout"]

        layouts = DashboardLayouts(page_id=page_id)
        layouts.load()

        if layouts.data:
            layout_json = layouts.data.get("layout")
            if layout_json:
                layout = json.loads(layout_json)
                st.session_state["dashboard_layout"] = layout
                st.session_state["dashboard_layout_page_id"] = page_id
                st.toast("Layout loaded successfully.")
                return layout

        st.toast("No saved layout found. Using default layout.")
        return default_layout()
    except Exception as e:
        st.error(f"Error loading layout: {e}")


def gen_dashboard(page, item_data):
    """
    Generate a dashboard with dynamic items.

    Args:
    - page (str): The current page name.
    - item_data (dict): A dictionary mapping item keys to their content.
    """
    display_dashboard_items()
    display_dashboard_layouts()
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = page
    st.session_state["current_page"] = page
    saved_layout = load_layout()

    if saved_layout:
        try:
            layout = [
                dashboard.Item(item["i"], item["x"], item["y"], item["w"], item["h"])
                for item in saved_layout
            ]
        except TypeError as e:
            st.error(f"Error in processing layout: {e}")
            layout = default_layout()
    else:
        layout = default_layout()

    # with elements("dashboard"):
    with dashboard.Grid(
        layout,
        isResizable=True,
        isDraggable=True,
        onResizeStop=save_layout,
        onDragStop=save_layout,
    ):
        for item_key in item_data:
            with mui.Paper(key=item_key):
                if item_data[item_key].startswith("http"):
                    html.Iframe(
                        src=item_data[item_key],
                        style={"height": "100%", "width": "100%"},
                    )
                else:
                    mui.Typography(item_data[item_key])


## Example usage
# item_data = {
#    "item_0": "http://localhost:3000",  # URL for iframe
#    "item_1": "Text content for second item",
#    "item_2": "Text content for third item",
# }

# gen_dashboard("your_page_name", item_data)
