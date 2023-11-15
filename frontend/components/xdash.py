import streamlit as st
from components.utils import dash_helper as xds
from components.xdatastore import DashboardLayouts, DashboardItems
from streamlit_elements import mui


def compile_edit_item_data():
    # Initialize an empty dictionary to store the compiled data
    compiled_data = {}

    # Iterate over each key in the session state
    for key in st.session_state:
        # Check if the key starts with 'edit_item'
        if key.startswith("edit_item"):
            # Extract the field name from the key
            field_name = key[len("edit_item_") :]
            # Add the field and its value to the compiled data
            compiled_data[field_name] = st.session_state[key]

    return compiled_data


def combine_items_back():
    try:
        # Initialize an empty dictionary to store the compiled data
        itemID = st.session_state["edit_item_id"]
        dashboard_item = DashboardItems(id=itemID)
        dashboard_item.load()  # Load the existing data
        # Iterate over each key in the session state
        for key in [
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
        ]:
            # Add the field and its value to the compiled data
            value = st.session_state[f"edit_item_{key}"]
            if key != "id":  # Skip updating the ID
                dashboard_item.update(key, value)
        st.toast(":green[Database row updated successfully!]")
    except Exception as e:
        st.toast(f":red[Error updating database: {e}]")


# def update_database_row_item_from_session():
#    try:
#        # Compile the data from session state
#        item_update = compile_edit_item_data()
#        print(f"{item_update}")
#        # Assuming you are updating the 'dashboard_items' table
#        dashboard_item = DashboardItems(id=item_update["id"])
#        dashboard_item.load()  # Load the existing data
#
#        # Update each field
#        for key, value in item_update.items():
#            if key != "id":  # Skip updating the ID
#                dashboard_item.update(key, value)
#
#        st.toast(":green[Database row updated successfully!]")
#    except Exception as e:
#        st.toast(f":red[Error updating database: {e}]")


def convert_tuple_to_dict(input_tuple):
    # Define the keys for the dictionary
    keys = xds.ITEM_FIELDS

    # Ensure the length of the tuple and keys match
    if len(input_tuple) != len(keys):
        raise ValueError("The input tuple does not match the expected format.")

    # Create a dictionary from the keys and the tuple elements
    return dict(zip(keys, input_tuple))


# def update_onchange_database_one_item(id, key, event):
#    try:
#        value = event.target.value
#        # Assuming you are updating the 'dashboard_items' table
#        dashboard_item = DashboardItems(id=id)
#        dashboard_item.load()  # Load the existing data
#
#        print(f"im a Value {value}")
#
#        dashboard_item.update(key, value)
#
#        st.success("Database row updated successfully!")
#    except Exception as e:
#        st.error(f"Error updating database: {e}")


def update_database_row_item(item_update):
    try:
        print(f"{item_update}")
        # Assuming you are updating the 'dashboard_items' table
        dashboard_item = DashboardItems(id=item_update["id"])
        dashboard_item.load()  # Load the existing data
        # Update each field
        for key, value in item_update.items():
            if key != "id":  # Skip updating the ID
                dashboard_item.update(key, value)
        st.toast(":green[Database row updated successfully!]")
    except Exception as e:
        st.toast(f":red[Error updating database: {e}]")


def edit_dashboard_part(this_id):
    st.session_state["edit_item_id"] = this_id
    print(f"edit dashboard part {this_id}")
    fetch_part = DashboardItems(id=this_id)
    fetch_part.load()
    if fetch_part.data:
        st.success(f"fetched {fetch_part.data}")
        st.session_state["edit_item"] = fetch_part.data  # Change here
        st.toast(f":green[Data loaded into edit_item]")


def display_edit_item_form(this_id):
    if "edit_item_id" != this_id:
        try:
            st.session_state["edit_item_id"] = this_id
            fetch_part = DashboardItems(id=this_id)
            fetch_part.load()  #
            item = fetch_part.data
            st.toast(f"fetched {item}")
        except Exception as e:
            st.error(f"Error loading data from Database: {e}")
    else:
        try:
            item = fetch_part.data
            st.success(f"no need to load {fetch_part.data}")

            #    # Check if 'edit_item' is in session state and is a dictionary
            #        st.session_state["edit_item_id"] = item["id"]
            #        st.session_state["edit_item_name"] = item["name"]
            #        st.session_state["edit_item_entrypoint"] = item["entrypoint"]
            #        st.session_state["edit_item_ssl"] = item["ssl"]
            #        st.session_state["edit_item_repository"] = item["repository"]
            #        st.session_state["edit_item_documentation"] = item["documentation"]
            #        st.session_state["edit_item_settings_default"] = item["settings_default"]
            #        st.session_state["edit_item_settings_user"] = item["settings_user"]
            #        st.session_state["edit_item_using_in_dashboard"] = item[
            #            "using_in_dashboard"
            #        ]
            #        st.session_state["edit_item_urls"] = item["urls"]
            #        st.session_state["edit_item_files"] = item["files"]
            #        st.session_state["edit_item_tags"] = item["tags"]
            #    else:
            #        st.error("No item data to edit.")
            #        return
            #
            def handleItemChange(event):
                print(f"i do {event.target.label}")
                st.session_state[
                    event.target.label.replace(" ", "_").lower()
                ] = event.target.value
                print(
                    f"{st.session_state[event.target.label.replace(' ', '_').lower()]}"
                )

            # Hardcoded input fields with onChange logic using lambda
            mui.TextField(
                label="ID",
                defaultValue=st.session_state["edit_item_id"],
                disabled=True,
            )
            # mui.TextField(
            #    label="Name",
            #    defaultValue=st.session_state["edit_item_name"],
            #    onChange=lambda value: update_onchange_database_one_item(
            #        item["id"], "name", value
            #    ),
            # )
            mui.TextField(
                label="Name",
                defaultValue=st.session_state["name"],
                onChange=handleItemChange
                # onChange=lambda value: xds.update_field("name", value),
            )
            mui.TextField(
                label="Entrypoint",
                defaultValue=st.session_state["edit_item_entrypoint"],
                # onChange=lambda value: xds.update_field("entrypoint", value),
            )
            mui.Checkbox(
                label="SSL",
                defaultChecked=st.session_state["edit_item_ssl"],
                # onChange=lambda value: xds.update_field("ssl", value),
            )
            mui.TextField(
                label="Repository",
                defaultValue=st.session_state["edit_item_repository"],
                # onChange=lambda value: xds.update_field("repository", value),
            )
            mui.TextField(
                label="Documentation",
                defaultValue=st.session_state["edit_item_documentation"],
                # onChange=lambda value: xds.update_field("documentation", value),
            )
            mui.TextField(
                label="Default Settings",
                defaultValue=st.session_state["edit_item_settings_default"],
                # onChange=lambda value: xds.update_field("settings_default", value),
            )
            mui.TextField(
                label="User Settings",
                defaultValue=st.session_state["edit_item_settings_user"],
                # onChange=lambda value: xds.update_field("settings_user", value),
            )
            mui.TextField(
                label="Using in Dashboard",
                defaultValue=st.session_state["edit_item_using_in_dashboard"],
                # onChange=lambda value: xds.update_field("using_in_dashboard", value),
            )
            mui.TextField(
                label="URLs",
                defaultValue=st.session_state["edit_item_urls"],
                # onChange=lambda value: xds.update_field("urls", value),
            )
            mui.TextField(
                label="Files",
                defaultValue=st.session_state["edit_item_files"],
                # onChange=lambda value: xds.update_field("files", value),
            )
            mui.TextField(
                label="Tags",
                defaultValue=st.session_state["edit_item_tags"],
                # onChange=lambda value: xds.update_field("tags", value),
            )
            mui.Button(
                "Save",
                # onclick=lambda: update_database_row_item_from_session()
                onClick=(lambda: (lambda: combine_items_back()))(),
            ),
        except Exception as e:
            st.error(f"Error: {e}")


# & ITEM LIST
def dash_item_list():
    item_elements = []
    items = xds.get_dashboard_parts("dashboard_items")
    for item in items:
        item_id = item[0]
        item_elements.append(
            mui.TableRow(
                mui.TableCell(item[0], noWrap=True),
                mui.TableCell(item[1], noWrap=True),
                mui.TableCell(item[2], noWrap=True),
                mui.TableCell(item[3], noWrap=True),
                mui.TableCell(item[4], noWrap=True),
                mui.TableCell(
                    mui.Button(
                        "Edit",
                        # Corrected lambda function for Edit button
                        onClick=(
                            lambda this_id=item[0]: (
                                lambda: display_edit_item_form(this_id)
                            )
                        )(),
                    ),
                    mui.Button(
                        "Delete",
                        # Corrected lambda function for Delete button
                        onClick=(
                            lambda item_id=item_id: (
                                lambda: xds.delete_dashboard_part(
                                    "dashboard_items", item_id
                                )
                            )
                        )(),
                    ),
                ),
            )
        )
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
                        mui.TableCell("Actions", style={"fontWeight": "bold"})
                if items:
                    mui.TableBody(*item_elements)
                else:
                    st.error("Failed to load dashboard items.")
        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Item",
                variant="contained",
                color="primary",
                onClick=lambda: xds.check_and_load_or_create_part("dashboard_items"),
            )


# & LAYOUTS
def dash_layout_list():
    layouts = xds.get_dashboard_parts("dashboard_layouts")
    with mui.Paper():
        mui.Typography("Dashboard Layouts", variant="h6", sx={"marginTop": 4})
        with mui.TableContainer():
            with mui.Table(stickyHeader=True):
                with mui.TableHead():
                    with mui.TableRow():
                        mui.TableCell("ID", style={"fontWeight": "bold"})
                        mui.TableCell("Name", style={"fontWeight": "bold"})
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
                                mui.TableCell(layout[4], noWrap=True)
                                mui.TableCell(layout[5], noWrap=True)
                                mui.TableCell(layout[6], noWrap=True)
                                with mui.TableCell():
                                    mui.Button(
                                        "Edit",
                                        onClick=lambda: edit_dashboard_part(layout[0]),
                                    ),
                                    mui.Button(
                                        "Delete",
                                        onClick=lambda: xds.delete_dashboard_part(
                                            "dashboard_layouts", layout[0]
                                        ),
                                    ),
                    else:
                        st.error("Failed to load dashboard layouts.")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Layout",
                variant="contained",
                color="primary",
                onClick=lambda: xds.check_and_load_or_create_part("dashboard_items"),
            )


def configure_dash_items(page):
    if page == "apps":
        dash_item_list()
    # if "edit_item_id" in st.session_state:
    #    display_edit_item_form()
