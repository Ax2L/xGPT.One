import streamlit as st
from components.utils import dash_helper as xds
from components.utils.postgres.xdatastore import DashboardLayouts, DashboardItems
from streamlit_elements import elements, mui

# Attributes
allowed_pages = ["apps", "dashboard_layouts_editor", "dashboard_items_editor"]
dashboard_names = ["Dashboard 1", "Dashboard 2", "Dashboard 3"]


def create_grid_settings():
    grid_settings = {
        "width": 1200,  # Default width
        "autoSize": True,
        "cols": 12,
        "draggableCancel": "",
        "draggableHandle": "",
        "compactType": "vertical",
        "layout": None,
        "margin": [10, 10],
        "containerPadding": [10, 10],
        "rowHeight": 150,
        "droppingItem": {"i": "newItem", "w": 2, "h": 2},
        "isDraggable": True,
        "isResizable": True,
        "isBounded": False,
        "useCSSTransforms": True,
        "transformScale": 1,
        "allowOverlap": False,
        "preventCollision": False,
        "isDroppable": False,
        "resizeHandles": ["se"],
        "resizeHandle": None,
        "onLayoutChange": None,
        "onDragStart": None,
        "onDrag": None,
        "onDragStop": None,
        "onResizeStart": None,
        "onResize": None,
        "onResizeStop": None,
        "onDrop": None,
        "onDropDragOver": None,
        "innerRef": None,
    }
    return grid_settings


def update_edit_item(item_id):
    """Updates the session state with the selected item number for editing."""
    try:
        item_nr = st.session_state[f"item_count_id_{item_id}"]
        item_nr_int = int(item_nr)  # Convert to integer
        st.session_state["item_nr"] = item_nr_int
        # st.info(f"Selected item number for editing: {item_nr_int}")
    except ValueError:
        st.error("Invalid item number. It must be an integer.")


def update_dashboard_item_in_db():
    try:
        # Retrieve the item number from the session state
        item_nr = st.session_state["item_nr"]

        # Retrieve the updated data for the specific item from the session state
        updated_data = st.session_state.all_items[item_nr]
        item_id = st.session_state.all_items[item_nr][0]
        print(f"updated_data: {updated_data}")
        print(f"item_id: {item_id}")
        # Create an instance of DashboardItems with the specific item ID
        dashboard_item = DashboardItems(
            id=item_id
        )  # Assuming the first element is the ID
        dashboard_item.load()  # Load the existing data
        print(f"old dashboard_item: {dashboard_item.data}")
        # Update each field in the database
        field_names = [
            # "id",
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
        for i, field in enumerate(field_names, start=1):  # Start from 1 as 0 is the ID
            # Update the field in the database
            dashboard_item.update(field, updated_data[i])

        st.success("Dashboard item updated successfully in the database.")
    except Exception as e:
        st.error(f"Error updating dashboard item in database: {e}")


def handleItemChange(event, field_name):
    # Retrieve the item number from the session state
    item_nr = st.session_state["item_nr"]

    # Convert the tuple to a list to allow modification
    item_data = list(st.session_state.all_items[item_nr])

    # Define a mapping of field names to their corresponding indices in item_data
    field_indices = {
        "name": 1,
        "entrypoint": 2,
        "ssl": 3,
        "repository": 4,
        "documentation": 5,
        "settings_default": 6,
        "settings_user": 7,
        "using_in_dashboard": 8,
        "urls": 9,
        "files": 10,
        "tags": 11,
    }

    # Update the specific field of the item in the list
    if field_name in field_indices:
        item_data[field_indices[field_name]] = event.target.value

        # Update the session state with the modified list
        st.session_state.all_items[item_nr] = item_data

        # For debugging purposes
        print(f"Updated {field_name} for item {item_nr} to {event.target.value}")
    else:
        print(f"Field name '{field_name}' is not recognized.")


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


# & ITEM LIST
def dash_item_list():
    count = 0
    items = st.session_state["all_items"]
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

                with mui.TableBody():
                    if items:
                        for item in items:
                            item_nr = count
                            item_id = st.session_state.all_items[item_nr][0]
                            st.session_state[f"item_count_id_{item_id}"] = item_nr
                            count += 1
                            # st.info(f"item_nr111: {item_nr}")
                            # #st.info(f"items: {st.session_state.all_items[item_nr]}")
                            with mui.TableRow():
                                mui.TableCell(
                                    st.session_state.all_items[item_nr][0], noWrap=True
                                ),
                                mui.TableCell(
                                    st.session_state.all_items[item_nr][1], noWrap=True
                                ),
                                mui.TableCell(
                                    st.session_state.all_items[item_nr][2], noWrap=True
                                ),
                                mui.TableCell(
                                    st.session_state.all_items[item_nr][3], noWrap=True
                                ),
                                mui.TableCell(
                                    st.session_state.all_items[item_nr][4], noWrap=True
                                ),
                                with mui.TableCell():
                                    mui.Button(
                                        "Edit",
                                        # Corrected lambda function for Delete button
                                        onClick=(
                                            lambda item_id=st.session_state.all_items[
                                                item_nr
                                            ][0]: (lambda: update_edit_item(item_id))
                                        )(),
                                    ),
                                    mui.Button(
                                        "Delete",
                                        # Corrected lambda function for Delete button
                                        onClick=(
                                            lambda item_id=st.session_state.all_items[
                                                item_nr
                                            ][0]: (
                                                lambda: xds.delete_dashboard_part(
                                                    "dashboard_items", item_id
                                                )
                                            )
                                        )(),
                                    ),
                    else:
                        st.error("Failed to load dashboard items.")
                with mui.Box(sx={"marginTop": 2}):
                    mui.Button(
                        "Add Item",
                        variant="contained",
                        color="primary",
                        onClick=lambda: xds.insert_new_part("dashboard_items"),
                    )


# & LAYOUTS
def update_edit_layout(layout_id):
    """Updates the session state with the selected layout number for editing."""
    if f"layout_count_id_{layout_id}" in st.session_state:
        layout_nr = st.session_state[f"layout_count_id_{layout_id}"]
        try:
            layout_nr_int = int(layout_nr)
            st.session_state["layout_nr"] = layout_nr_int
        except ValueError:
            st.error("Invalid layout number. It must be an integer.")
    else:
        st.error("Layout ID not found in session state.")


def update_dashboard_layout_in_db():
    try:
        layout_nr = st.session_state["layout_nr"]
        updated_data = st.session_state.all_layouts[layout_nr]
        layout_id = st.session_state.all_layouts[layout_nr][0]

        dashboard_layout = DashboardLayouts(id=layout_id)
        dashboard_layout.load()

        field_names = ["name", "description", "tags", "items"]
        for i, field in enumerate(field_names, start=1):
            dashboard_layout.update(field, updated_data[i])

        st.success("Dashboard layout updated successfully in the database.")
    except Exception as e:
        st.error(f"Error updating dashboard layout in database: {e}")


def handleLayoutChange(event, field_name):
    layout_nr = st.session_state["layout_nr"]
    layout_data = list(st.session_state.all_layouts[layout_nr])

    field_indices = {"name": 1, "description": 2, "tags": 3, "items": 4}

    if field_name in field_indices:
        layout_data[field_indices[field_name]] = event.target.value
        st.session_state.all_layouts[layout_nr] = layout_data
    else:
        print(f"Field name '{field_name}' is not recognized.")


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


def dash_layout_list():
    layouts = st.session_state["all_layouts"]
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
                            layout_id = layout[0]
                            if f"layout_count_id_{layout_id}" not in st.session_state:
                                st.session_state[
                                    f"layout_count_id_{layout_id}"
                                ] = layout_id

                            with mui.TableRow():
                                mui.TableCell(layout[0])  # ID
                                mui.TableCell(layout[1])  # Name
                                mui.TableCell(layout[4])  # Description
                                mui.TableCell(layout[5])  # Tags
                                mui.TableCell(layout[6])  # Items
                                with mui.TableCell():
                                    mui.Button(
                                        "Edit",
                                        onClick=lambda layout_id=layout[
                                            0
                                        ]: update_edit_layout(layout_id),
                                    ),
                                    mui.Button(
                                        "Delete",
                                        onClick=lambda layout_id=layout[
                                            0
                                        ]: xds.delete_dashboard_part(
                                            "dashboard_layouts", layout_id
                                        ),
                                    ),
                    else:
                        with mui.TableRow():
                            with mui.TableCell(colSpan=6):
                                mui.Typography("No layouts available.")

        with mui.Box(sx={"marginTop": 2}):
            mui.Button(
                "Add Layout",
                variant="contained",
                color="primary",
                onClick=lambda: xds.insert_new_part("dashboard_layouts"),
            )


def dashboard_items_state_from_db():
    dashboard_items = DashboardItems()
    dashboard_items.load()  # Load the existing data
    st.session_state["all_items"] = dashboard_items.data
    print("Loading items from database...")


def dashboard_layouts_state_from_db():
    dashboard_layouts = DashboardLayouts()
    dashboard_layouts.load()  # Load the existing data
    st.session_state["all_layouts"] = dashboard_layouts.data
    print("Loading layouts from database...")


# def dashboad_item_state_for_editor():
#    edit_item_id = st.session_state.get("edit_item_id")
#    if edit_item_id is not None:
#        dashboard_item_solo = DashboardItems(id=edit_item_id)
#        dashboard_item_solo.load()
#        st.session_state["edit_item"] = dashboard_item_solo.data
#        print(f"Loaded item for editing: {dashboard_item_solo.data}")
#    else:
#        st.error("Failed to load edit item, because there is no edit item id.")


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


#! Test #################################


def load_dashboard(selected_dashboard):
    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.
    loaded_layout = DashboardLayouts(id=selected_dashboard)
    loaded_layout.load()  # Load the existing data
    st.session_state["loaded_layout"] = loaded_layout.data
    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("  ", 0, 0, 2, 2),
        # dashboard.Item(
        #    "second_item",
        #    2,
        #    0,
        #    2,
        #    2,
        # ),
        # dashboard.Item(
        #    "third_item",
        #    4,
        #    0,
        #    2,
        #    2,
        # ),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.
    # If you want to retrieve updated layout values as the user move or resize dashboard items,
    # you can pass a callback to the onLayoutChange event parameter.

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")
        # mui.Paper("Second item (cannot drag)", key="second_item")
        # mui.Paper("Third item (cannot resize)", key="third_item")


def dashboard_test(page):
    if page in allowed_pages:
        selected_dashboard = mui.Autocomplete(
            options=dashboard_names,
            label="Select a Dashboard",
            onChange=lambda e, value: st.session_state.update(
                {"selected_dashboard": value}
            ),
        )
        if "selected_dashboard" in st.session_state:
            # Load and display the selected dashboard
            load_dashboard(st.session_state["selected_dashboard"])


#! Test #################################
