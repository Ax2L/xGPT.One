import streamlit as st
from streamlit_elements import elements, mui, dashboard, html
from components.xdatastore import DashboardLayouts, DashboardItems
import json
from datetime import datetime

# ?##########################################################################

import streamlit as st
import psycopg2
from streamlit_elements import mui


def get_dashboard_items():
    conn = psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, tags, id FROM dashboard_items")
    items = cursor.fetchall()
    conn.close()
    return items


def xpaper():
    items = get_dashboard_items()

    with mui.Paper():
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("Name", style={"fontWeight": "bold"})
                        mui.TableCell("Description", style={"fontWeight": "bold"})
                        mui.TableCell("Tags", style={"fontWeight": "bold"})
                        mui.TableCell("Actions", style={"fontWeight": "bold"})

                with mui.TableBody():
                    for item in items:
                        with mui.TableRow():
                            mui.TableCell(item[0], noWrap=True)
                            mui.TableCell(item[1], noWrap=True)
                            mui.TableCell(item[2], noWrap=True)
                            with mui.TableCell():
                                mui.Button("Edit")
                                mui.Button("Delete")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button("Add Item", variant="contained", color="primary")


# Example usage
# st.set_page_config(page_title="xGPT.One Dashboard", layout="wide")


# ?##########################################################################


# !################################################################
# Helper function to format column names
def format_column_name(name):
    return " ".join(word.capitalize() for word in name.split("_"))


# Display dashboard items with updated table structure
def display_dashboard_items():
    try:
        dashboard_items = DashboardItems()
        dashboard_items.load()

        if dashboard_items.data:
            with mui.Paper():
                with mui.TableContainer():
                    with mui.Table(stickyHeader=True):
                        with mui.TableHead():
                            with mui.TableRow():
                                mui.TableCell(
                                    "Name",
                                    style={"width": "20%", "whiteSpace": "nowrap"},
                                )
                                mui.TableCell(
                                    "Description", style={"whiteSpace": "nowrap"}
                                )
                                mui.TableCell("Tags", style={"whiteSpace": "nowrap"})
                                mui.TableCell(
                                    "Actions",
                                    style={"width": "20%", "whiteSpace": "nowrap"},
                                )
                        with mui.TableBody():
                            for row in dashboard_items.data:
                                with mui.TableRow():
                                    mui.TableCell(
                                        row["name"], style={"whiteSpace": "nowrap"}
                                    )
                                    mui.TableCell(
                                        row["description"],
                                        style={"whiteSpace": "nowrap"},
                                    )
                                    mui.TableCell(
                                        ", ".join(row["tags"]),
                                        style={"whiteSpace": "nowrap"},
                                    )
                                    with mui.TableCell():
                                        mui.Button("Edit")
                                        mui.Button("Delete")
        else:
            st.write("No dashboard items found.")
    except Exception as e:
        st.error(f"Error displaying dashboard items: {e}")


# Display dashboard layouts with updated table structure
def display_dashboard_layouts():
    try:
        dashboard_layouts = DashboardLayouts()
        dashboard_layouts.load()

        if dashboard_layouts.data:
            with mui.Paper():
                with mui.TableContainer():
                    with mui.Table(stickyHeader=True):
                        with mui.TableHead():
                            with mui.TableRow():
                                mui.TableCell(
                                    "Name",
                                    style={"width": "20%", "whiteSpace": "nowrap"},
                                )
                                mui.TableCell(
                                    "Description", style={"whiteSpace": "nowrap"}
                                )
                                mui.TableCell("Tags", style={"whiteSpace": "nowrap"})
                                mui.TableCell(
                                    "Actions",
                                    style={"width": "20%", "whiteSpace": "nowrap"},
                                )
                        with mui.TableBody():
                            for row in dashboard_layouts.data:
                                with mui.TableRow():
                                    mui.TableCell(
                                        row["name"], style={"whiteSpace": "nowrap"}
                                    )
                                    mui.TableCell(
                                        row["description"],
                                        style={"whiteSpace": "nowrap"},
                                    )
                                    mui.TableCell(
                                        ", ".join(row["tags"]),
                                        style={"whiteSpace": "nowrap"},
                                    )
                                    with mui.TableCell():
                                        mui.Button("Edit")
                                        mui.Button("Delete")
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


def test_data_loading(test_id):
    try:
        # Initialize the DashboardLayouts instance
        test_layouts = DashboardLayouts(id=test_id)

        # Attempt to load data
        test_layouts.load()

        # Check if data is loaded
        if test_layouts.data:
            st.write("Data loaded successfully:", test_layouts.data)
        else:
            st.write("No data found for id:", test_id)

    except Exception as e:
        st.error("Error occurred while loading data:")
        st.exception(e)


def save_layout(layout):
    try:
        page_name = st.session_state["current_page"]
        layouts = DashboardLayouts(id=page_name)
        layouts.load()

        layout_json = json.dumps(layout)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if data exists for the page, update if it does, else insert new record
        if layouts.data:
            layouts.update("layout", layout_json)
            layouts.update("updated_at", current_time)
        else:
            layouts.insert(
                id=page_name,
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
        id = st.session_state["current_page"]

        # Check if the layout is already in the session state
        if (
            "dashboard_layout" in st.session_state
            and st.session_state["dashboard_layout_id"] == id
        ):
            return st.session_state["dashboard_layout"]

        layouts = DashboardLayouts(id=id)
        layouts.load()

        if layouts.data:
            layout_json = layouts.data.get("layout")
            if layout_json:
                layout = json.loads(layout_json)
                st.session_state["dashboard_layout"] = layout
                st.session_state["dashboard_layout_id"] = id
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
    xpaper()
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
