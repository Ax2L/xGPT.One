import streamlit as st
from streamlit_elements import mui
from components.xdatastore import DashboardLayouts, DashboardItems
import psycopg2
from components.utils.dash_helper import *
import datetime


def display_edit_item_form():
    try:
        item = st.session_state["edit_item"]
        st.write(f"Current item data: {item}")

        fields = [
            "id",
            "name",
            "entrypoint",
            "ssl",
            "repository",
            "documentation",
            "settings_default",
            "settings_user",
            "using_in_dashboard",
            "urls",
            "files",
            "tags",
        ]

        item_dict = dict(zip(fields, item))

        # Convert datetime objects to strings for JSON serialization
        for field in fields:
            if isinstance(item_dict[field], datetime.datetime):
                item_dict[field] = item_dict[field].strftime("%Y-%m-%dT%H:%M:%S")

        for field in fields[1:]:
            if field in ["ssl", "using_in_dashboard"]:
                item_dict[field] = st.checkbox(
                    field.upper(), item_dict.get(field, False)
                )
            else:
                item_dict[field] = st.text_input(
                    field.capitalize().replace("_", " "), item_dict.get(field, "")
                )

        if st.button("Save"):
            # Convert back string representations of datetime objects to datetime
            for field in fields:
                if isinstance(item_dict[field], str):
                    try:
                        item_dict[field] = datetime.datetime.fromisoformat(
                            item_dict[field]
                        )
                    except ValueError:
                        pass  # It's not a datetime string, do nothing

            update_database_row_item(item_dict)
            st.success("Item updated successfully!")
    except Exception as e:
        st.error(f"Error: {e}")


def update_database_row_item(item_dict):
    try:
        # Assuming you are updating the 'dashboard_items' table
        dashboard_item = DashboardItems(id=item_dict["id"])
        dashboard_item.load()  # Load the existing data

        # Update each field
        for key, value in item_dict.items():
            if key != "id":  # Skip updating the ID
                dashboard_item.update(key, value)

        st.success("Database row updated successfully!")
    except Exception as e:
        st.error(f"Error updating database: {e}")


## Example usage in your Streamlit app
# if "edit_item" in st.session_state:
#    display_edit_item_form()


def xpaper():
    items = get_dashboard_parts("dashboard_items")
    layouts = get_dashboard_parts("dashboard_layouts")

    def create_item_buttons(item_id):
        return [
            mui.Button(
                "Edit", onClick=lambda: edit_dashboard_part("dashboard_items", item_id)
            ),
            mui.Button(
                "Delete",
                onClick=lambda: delete_dashboard_part("dashboard_items", item_id),
            ),
        ]

    def create_layout_buttons(layout_id):
        return [
            mui.Button(
                "Edit",
                onClick=lambda: edit_dashboard_part("dashboard_layouts", layout_id),
            ),
            mui.Button(
                "Delete",
                onClick=lambda: delete_dashboard_part("dashboard_layouts", layout_id),
            ),
        ]

    # & ITEMS
    with mui.Paper():
        mui.Typography("Dashboard Items", variant="h6")
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("ID", style={"fontWeight": "bold"})
                        mui.TableCell("Name", style={"fontWeight": "bold"})
                        mui.TableCell("Entrypoint", style={"fontWeight": "bold"})
                        mui.TableCell("SSL", style={"fontWeight": "bold"})
                        mui.TableCell("Repository", style={"fontWeight": "bold"})
                        # mui.TableCell("Documentation", style={"fontWeight": "bold"})
                        # mui.TableCell("Default Settings", style={"fontWeight": "bold"})
                        # mui.TableCell("User Settings", style={"fontWeight": "bold"})
                        # mui.TableCell("Using in ...", style={"fontWeight": "bold"})
                        # mui.TableCell("URLs", style={"fontWeight": "bold"})
                        # mui.TableCell("Files", style={"fontWeight": "bold"})
                        # mui.TableCell("Tags", style={"fontWeight": "bold"})
                        mui.TableCell("Actions", style={"fontWeight": "bold"})
                with mui.TableBody():
                    if items:
                        for item in items:
                            with mui.TableRow():
                                for i in range(5):
                                    mui.TableCell(item[i], noWrap=True)
                                with mui.TableCell():
                                    for button in create_item_buttons(item[0]):
                                        button
                    else:
                        st.error("Failed to load dashboard items.")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Item",
                variant="contained",
                color="primary",
                onClick=check_and_load_or_create_part("dashboard_items"),
            )

        # & LAYOUTS
    with mui.Paper():
        mui.Typography("Dashboard Layouts", variant="h6", sx={"marginTop": 4})
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("ID", style={"fontWeight": "bold"})
                        mui.TableCell("Name", style={"fontWeight": "bold"})
                        # mui.TableCell("Layout", style={"fontWeight": "bold"})
                        # mui.TableCell("Username", style={"fontWeight": "bold"})
                        mui.TableCell("Description", style={"fontWeight": "bold"})
                        mui.TableCell("Tags", style={"fontWeight": "bold"})
                        mui.TableCell("Items", style={"fontWeight": "bold"})
                        mui.TableCell("Actions", style={"fontWeight": "bold"})

                with mui.TableBody():
                    if layouts:
                        for layout in layouts:
                            with mui.TableRow():
                                mui.TableCell(layout[0], noWrap=True)
                                mui.TableCell(layout[1], noWrap=True)
                                # mui.TableCell(layout[2], noWrap=True)
                                # mui.TableCell(layout[3], noWrap=True)
                                mui.TableCell(layout[4], noWrap=True)
                                mui.TableCell(layout[5], noWrap=True)
                                mui.TableCell(layout[6], noWrap=True)
                                with mui.TableCell():
                                    for button in create_layout_buttons(layout[0]):
                                        button
                    else:
                        st.error("Failed to load dashboard layouts.")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Layout",
                variant="contained",
                color="primary",
                onClick=check_and_load_or_create_part("dashboard_items"),
            )
