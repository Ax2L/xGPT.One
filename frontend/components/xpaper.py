import streamlit as st
from streamlit_elements import elements, mui, dashboard, html
from components.xdatastore import DashboardLayouts, DashboardItems
import json
from datetime import datetime
import psycopg2

# ?##########################################################################
# Default values for new items and layouts
DEFAULT_ITEM_VALUES = {
    "layout": "sample_layout",
    "username": "admin",
    "page_name": "New Page",
    "description": "Sample item description",
    "notes": "Sample notes",
    "issues": "None",
    "name": "NEW Item",
    "version": "1.0",
    "tags": "new, item",
    "using_in_dashboard": "unused so far",
    "settings_default": json.dumps({"setting1": "value1"}),
    "settings_user": json.dumps({}),
    "documentation": "Sample documentation",
    "repository": "https://github.com/Ax2L/xGPT.One",
    "files": "file1.py, file2.py",
    "urls": "http://example.com",
    "ssl": False,
    "entrypoint": "http://url.with:3000",
    "item_list": json.dumps(["item1", "item2"]),
}


DEFAULT_LAYOUT_VALUES = {
    # "id": "new_page_1.0",
    "layout": json.dumps(
        {
            "widgets": [
                {
                    "id": 1,
                    "type": "chart",
                    "position": {"x": 0, "y": 0, "w": 4, "h": 3},
                }
            ]
        }
    ),
    "username": "admin",
    "page_name": "New Page",
    "description": "New layout description",
    "notes": "Sample notes",
    "issues": "None",
    "name": "New Layout",
    "version": "1.0",
    "tags": "new, layout",
    "settings_default": json.dumps({"setting1": "value1"}),
    "settings_user": json.dumps({}),
    "documentation": "New layout documentation",
    "repository": "https://github.com/Ax2L/xGPT.One",
    "files": "layout1.py, layout2.py",
    "urls": "http://example.com",
    "ssl": False,
    "entrypoint": "http://url.with:3000",
    "using_item_name_list": json.dumps(["item1", "item2"]),
}


def fetch_dashboard_item_by_id(item_id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dashboard_items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        conn.close()
        return item
    except Exception as e:
        st.toast(f":red[Error fetching item by ID: {e}]")


def fetch_dashboard_layout_by_id(layout_id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dashboard_layouts WHERE id = %s", (layout_id,))
        layout = cursor.fetchone()
        conn.close()
        return layout
    except Exception as e:
        st.toast(f":red[Error fetching layout by ID: {e}]")


def edit_dashboard_item(item_id):
    item = fetch_dashboard_item_by_id(item_id)
    if item:
        st.session_state["edit_item"] = None
        st.session_state["edit_item"] = item


def edit_dashboard_layout(layout_id):
    layout = fetch_dashboard_layout_by_id(layout_id)
    if layout:
        st.session_state["edit_layout"] = None
        st.session_state["edit_layout"] = layout


def get_dashboard_items():
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, tags, id FROM dashboard_items")
        items = cursor.fetchall()
        conn.close()
        return items
    except Exception as e:
        st.toast(
            f":red[Error fetching dashboard items: {e}]",
        )


def get_dashboard_layouts():
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, tags, id FROM dashboard_layouts")
        layouts = cursor.fetchall()
        conn.close()
        return layouts
    except Exception as e:
        st.toast(
            f":red[Error fetching dashboard layouts: {e}]",
        )


def insert_new_item():
    conn = psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dashboard_items 
        (layout, username, page_name, description, notes, issues, name, version, tags, using_in_dashboard, settings_default, settings_user, documentation, repository, files, urls, ssl, entrypoint, item_list) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            DEFAULT_ITEM_VALUES["layout"],
            DEFAULT_ITEM_VALUES["username"],
            DEFAULT_ITEM_VALUES["page_name"],
            DEFAULT_ITEM_VALUES["description"],
            DEFAULT_ITEM_VALUES["notes"],
            DEFAULT_ITEM_VALUES["issues"],
            DEFAULT_ITEM_VALUES["name"],
            DEFAULT_ITEM_VALUES["version"],
            DEFAULT_ITEM_VALUES["tags"],
            DEFAULT_ITEM_VALUES["using_in_dashboard"],
            DEFAULT_ITEM_VALUES["settings_default"],
            DEFAULT_ITEM_VALUES["settings_user"],
            DEFAULT_ITEM_VALUES["documentation"],
            DEFAULT_ITEM_VALUES["repository"],
            DEFAULT_ITEM_VALUES["files"],
            DEFAULT_ITEM_VALUES["urls"],
            DEFAULT_ITEM_VALUES["ssl"],
            DEFAULT_ITEM_VALUES["entrypoint"],
            DEFAULT_ITEM_VALUES["item_list"],
        ),
    )
    conn.commit()
    conn.close()


def insert_new_layout():
    conn = psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dashboard_layouts 
        (layout, username, page_name, description, notes, issues, name, version, tags, settings_default, settings_user, documentation, repository, files, urls, ssl, entrypoint, using_item_name_list) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            # DEFAULT_LAYOUT_VALUES["id"],
            DEFAULT_LAYOUT_VALUES["layout"],
            DEFAULT_LAYOUT_VALUES["username"],
            DEFAULT_LAYOUT_VALUES["page_name"],
            DEFAULT_LAYOUT_VALUES["description"],
            DEFAULT_LAYOUT_VALUES["notes"],
            DEFAULT_LAYOUT_VALUES["issues"],
            DEFAULT_LAYOUT_VALUES["name"],
            DEFAULT_LAYOUT_VALUES["version"],
            DEFAULT_LAYOUT_VALUES["tags"],
            DEFAULT_LAYOUT_VALUES["settings_default"],
            DEFAULT_LAYOUT_VALUES["settings_user"],
            DEFAULT_LAYOUT_VALUES["documentation"],
            DEFAULT_LAYOUT_VALUES["repository"],
            DEFAULT_LAYOUT_VALUES["files"],
            DEFAULT_LAYOUT_VALUES["urls"],
            DEFAULT_LAYOUT_VALUES["ssl"],
            DEFAULT_LAYOUT_VALUES["entrypoint"],
            DEFAULT_LAYOUT_VALUES["using_item_name_list"],
        ),
    )
    conn.commit()
    conn.close()


def check_and_load_or_create_item():
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()

        # Check if an item with the name "New Item" exists
        cursor.execute("SELECT * FROM dashboard_items WHERE name = 'New Item'")
        item = cursor.fetchone()

        if item:
            # Item exists, load its data
            st.session_state["edit_item"] = item

            st.toast(
                f":yellow[Item 'New Item' already exists. Loaded in the editor for editing.]",
            )
        else:
            # Item does not exist, create a new one
            insert_new_item()
            cursor.execute("SELECT * FROM dashboard_items WHERE name = 'New Item'")
            new_item = cursor.fetchone()
            st.session_state["edit_item"] = new_item
            st.toast(":green[New item 'New Item' created and loaded in the editor.]")

        conn.close()
    except Exception as e:
        st.toast(
            f":red[Error in check_and_load_or_create_item: {e}]",
        )


def check_and_load_or_create_layouts():
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()

        # Check if an layout with the name "New Layout" exists
        cursor.execute("SELECT * FROM dashboard_layouts WHERE name = 'New Layout'")
        layout = cursor.fetchone()

        if layout:
            # Layout exists, load its data
            st.session_state["edit_layout"] = layout
            st.toast(
                f":green[Item 'New Layout' already exists. Loaded in the editor for editing.]",
            )
        else:
            # Layout does not exist, create a new one
            insert_new_layout()
            cursor.execute("SELECT * FROM dashboard_layouts WHERE name = 'New Layout'")
            new_layout = cursor.fetchone()
            st.session_state["edit_layout"] = new_layout
            st.toast(
                ":green[New layout 'New Layout' created and loaded in the editor.]"
            )

        conn.close()
    except Exception as e:
        st.toast(
            f":red[Error in check_and_load_or_create_layouts: {e}]",
        )


def delete_dashboard_item(item_id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dashboard_items WHERE id = %s", (item_id,))
        conn.commit()
        conn.close()
        st.toast(
            f":green[Item with ID {item_id} deleted successfully.]",
        )
    except Exception as e:
        st.toast(
            f":red[Error deleting item: {e}]",
        )


def delete_dashboard_layout(layout_id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dashboard_layouts WHERE id = %s", (layout_id,))
        conn.commit()
        conn.close()
        st.toast(
            f":green[Layout with ID {layout_id} deleted successfully.]",
        )
    except Exception as e:
        st.toast(
            f":red[Error deleting layout: {e}]",
        )


def xpaper():
    items = get_dashboard_items()
    layouts = get_dashboard_layouts()

    with mui.Paper():
        mui.Typography("Dashboard Items", variant="h6")
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("ID", style={"fontWeight": "bold"})
                        mui.TableCell("Name", style={"fontWeight": "bold"})
                        mui.TableCell("Description", style={"fontWeight": "bold"})
                        mui.TableCell("Tags", style={"fontWeight": "bold"})
                        mui.TableCell("Actions", style={"fontWeight": "bold"})

                with mui.TableBody():
                    for item in items:
                        item_id = item[3]
                        with mui.TableRow():
                            mui.TableCell(item[3], noWrap=True)
                            mui.TableCell(item[0], noWrap=True)
                            mui.TableCell(item[1], noWrap=True)
                            mui.TableCell(item[2], noWrap=True)
                            with mui.TableCell():
                                mui.Button(
                                    "Edit", onClick=lambda: edit_dashboard_item(item_id)
                                )
                                mui.Button(
                                    "Delete",
                                    onClick=lambda: delete_dashboard_item(item_id),
                                )

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Item",
                variant="contained",
                color="primary",
                onClick=check_and_load_or_create_item,
            )

        mui.Typography("Dashboard Layouts", variant="h6", sx={"marginTop": 4})
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("ID", style={"fontWeight": "bold"})
                        mui.TableCell("Name", style={"fontWeight": "bold"})
                        mui.TableCell("Description", style={"fontWeight": "bold"})
                        mui.TableCell("Tags", style={"fontWeight": "bold"})
                        mui.TableCell("Actions", style={"fontWeight": "bold"})

                with mui.TableBody():
                    for layout in layouts:
                        layout_id = layout[3]
                        with mui.TableRow():
                            mui.TableCell(layout[3], noWrap=True)
                            mui.TableCell(layout[0], noWrap=True)
                            mui.TableCell(layout[1], noWrap=True)
                            mui.TableCell(layout[2], noWrap=True)
                            with mui.TableCell():
                                mui.Button(
                                    "Edit",
                                    onClick=lambda: edit_dashboard_layout(layout_id),
                                )
                                mui.Button(
                                    "Delete",
                                    onClick=lambda: delete_dashboard_layout(layout_id),
                                )

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Layout",
                variant="contained",
                color="primary",
                onClick=check_and_load_or_create_layouts,
            )


# ?##########################################################################


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
        st.error(f":red[Error saving layout: {e}]")
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
        st.toast(
            f":red[Error loading layout: {e}]",
        )


def gen_dashboard(page, item_data):
    """
    Generate a dashboard with dynamic items.

    Args:
    - page (str): The current page name.
    - item_data (dict): A dictionary mapping item keys to their content.
    """
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
        except Exception as e:
            st.toast(
                f":red[Error in gen_dashboard: {e}]",
            )

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
