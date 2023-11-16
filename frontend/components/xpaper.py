import streamlit as st
from streamlit_elements import mui
from components.utilsnents.utils.postgres.xdatastore import (
    DashboardLayouts,
    DashboardItems,
)


def display_edit_item_form():
    try:
        item = st.session_state["edit_item"]
        st.write(f"Current item data: {item}")

        fields = [
            "id",
            "name",
            "tags",
            "using_in_dashboard",
            "settings_default",
            "settings_user",
            "documentation",
            "repository",
            "files",
            "urls",
            "ssl",
            "entrypoint",
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
    items = get_dashboard_items()
    layouts = get_dashboard_layouts()

    def create_item_buttons(item_id):
        return [
            mui.Button("Edit", onClick=lambda: edit_dashboard_item(item_id)),
            mui.Button("Delete", onClick=lambda: delete_dashboard_item(item_id)),
        ]

    def create_layout_buttons(layout_id):
        return [
            mui.Button("Edit", onClick=lambda: edit_dashboard_layout(layout_id)),
            mui.Button("Delete", onClick=lambda: delete_dashboard_layout(layout_id)),
        ]

    with mui.Paper():
        mui.Typography("Dashboard Items", variant="h6")
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("ID", style={"fontWeight": "bold"})
                        mui.TableCell("Name", style={"fontWeight": "bold"})
                        mui.TableCell("Documentation", style={"fontWeight": "bold"})
                        mui.TableCell("Tags", style={"fontWeight": "bold"})
                        mui.TableCell("Actions", style={"fontWeight": "bold"})

                with mui.TableBody():
                    if items:
                        for item in items:
                            with mui.TableRow():
                                mui.TableCell(item[3], noWrap=True)
                                mui.TableCell(item[0], noWrap=True)
                                mui.TableCell(item[1], noWrap=True)
                                mui.TableCell(item[2], noWrap=True)
                                with mui.TableCell():
                                    for button in create_item_buttons(item[3]):
                                        button
                    else:
                        st.error("Failed to load dashboard items.")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Item",
                variant="contained",
                color="primary",
                onClick=check_and_load_or_create_item(),
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
                    if layouts:
                        for layout in layouts:
                            with mui.TableRow():
                                mui.TableCell(layout[3], noWrap=True)
                                mui.TableCell(layout[0], noWrap=True)
                                mui.TableCell(layout[1], noWrap=True)
                                mui.TableCell(layout[2], noWrap=True)
                                with mui.TableCell():
                                    for button in create_layout_buttons(layout[3]):
                                        button
                    else:
                        st.error("Failed to load dashboard layouts.")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Layout",
                variant="contained",
                color="primary",
                onClick=check_and_load_or_create_layouts,
            )


# ?##########################################################################
