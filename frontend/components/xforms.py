import streamlit as st
import json
import datetime
from components.xdatastore import DashboardItems, DashboardLayouts


def display_edit_item_form():
    try:
        item = st.session_state["edit_item"]
        st.write(f"Current item data: {item}")

        # Assuming the tuple structure matches the order of these fields
        fields = [
            "id",
            "layout",
            "username",
            "page_name",
            "description",
            "notes",
            "issues",
            "name",
            "version",
            "tags",
            "settings_default",
            "settings_user",
            "documentation",
            "repository",
            "files",
            "urls",
            "ssl",
            "entrypoint",
            "item_list",
        ]

        # Create a dictionary from the tuple for easier handling
        item_dict = dict(zip(fields, item))

        for field in fields[1:]:  # Skip 'id'
            if field in ["layout", "settings_default", "settings_user", "item_list"]:
                item_dict[field] = st.text_area(
                    field.capitalize().replace("_", " "),
                    json.dumps(item_dict.get(field, "")),
                )
            elif field == "ssl":
                item_dict[field] = st.checkbox(
                    field.upper(), item_dict.get(field, False)
                )
            else:
                # Convert datetime to string for display
                if isinstance(item_dict[field], datetime.datetime):
                    item_dict[field] = item_dict[field].strftime("%Y-%m-%dT%H:%M:%S")
                item_dict[field] = st.text_input(
                    field.capitalize().replace("_", " "), item_dict.get(field, "")
                )

        if st.button("Save"):
            try:
                for json_field in [
                    "layout",
                    "settings_default",
                    "settings_user",
                    "item_list",
                ]:
                    item_dict[json_field] = json.loads(item_dict[json_field])

                # Convert string back to datetime for database update
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
            except json.JSONDecodeError:
                st.error("Invalid JSON in one of the fields.")
                return
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


# Example usage in your Streamlit app
if "edit_item" in st.session_state:
    display_edit_item_form()
