import streamlit as st
from components.utils.postgres.xdatastore import DashboardLayouts, DashboardItems


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
