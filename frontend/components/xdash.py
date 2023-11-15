import streamlit as st
from streamlit_elements import mui
from components.utils import dash_helper as xds
from components.xdatastore import DashboardLayouts, DashboardItems
import datetime


def edit_dashboard_part(TABLE, useID):
    print(f"edit dashboard part {useID}")
    fetch_part = xds.fetch_dashboard_parts_by_id(TABLE, useID)
    if fetch_part:
        st.session_state[f"edit_{TABLE.lower()}"] = fetch_part
        st.toast(
            f":green[Data loaded into edit_{TABLE.lower()} ]",
        )


# & ITEMS EDITOR
def display_edit_item_form():
    try:
        item = st.session_state["edit_dashboard_items"]
        # Define a key for the save button state
        save_button_key = "save_button_state"

        # Initialize the button state to False
        if save_button_key not in st.session_state:
            st.session_state[save_button_key] = False

        fields = xds.ITEM_FIELDS

        item_dict = dict(zip(fields, item))
        with mui.Paper():
            # Convert datetime objects to strings for JSON serialization
            for field in fields:
                if isinstance(item_dict[field], datetime.datetime):
                    item_dict[field] = item_dict[field].strftime("%Y-%m-%dT%H:%M:%S")

            for field in fields[1:]:
                if field in [
                    "ssl",
                    "using_in_dashboard",
                ]:  # Add "using_in_dashboard" here
                    item_dict[field] = mui.FormControlLabel(
                        control=mui.Checkbox(
                            defaultChecked=item_dict.get(field, False)
                        ),
                        label=field.replace("using_in_dashboard", "crrently in use")
                        .capitalize()
                        .upper()
                        .replace("_", " "),
                    )
                else:
                    item_dict[field] = mui.TextField(
                        label=field.capitalize().replace("_", " "),
                        value=item_dict.get(field, ""),
                        variant="outlined",
                        fullWidth=True,
                        margin="normal",
                    )

            # When the button is clicked, it should set the state to True
            def convert_data(item_dict):
                try:
                    print(f"{item_dict}")
                    # Convert back string representations of datetime objects to datetime
                    for field in fields:
                        if isinstance(item_dict[field], str):
                            try:
                                item_dict[field] = datetime.datetime.fromisoformat(
                                    item_dict[field]
                                )
                            except ValueError:
                                pass  # It's not a datetime string, do nothing
                    return item_dict
                except Exception as e:
                    st.toast(f":red[Error converting before updating database: {e}]")



            if mui.Button("Save"):
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
                st.toast(":green[Item updated successfully!]")
    except Exception as e:
        st.toast(f":red[Error: {e}]")


            mui.Button(
                "Save",
                variant="outlined",
                color="primary",
                onClick=lambda item_update=convert_data(item_dict): (
                    lambda: xds.update_database_row_item(item_update)
                )(),
            )
            # After the button is rendered, check if it was clicked
            # if st.session_state[save_button_key]:
            #    # Reset the button state to False
            #    st.session_state[save_button_key] = False
            #    # Convert back string representations of datetime objects to datetime
            #    for field in fields:
            #        if isinstance(item_dict[field], str):
            #            try:
            #                item_dict[field] = datetime.datetime.fromisoformat(
            #                    item_dict[field]
            #                )
            #            except ValueError:
            #                pass  # It's not a datetime string, do nothing

            # update_database_row_item(item_dict)
            # st.toast(":green[Item updated successfully!]")
    except Exception as e:
        st.toast(f":red[Error: {e}]")


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
                            lambda item_id=item_id: (
                                lambda: edit_dashboard_part("dashboard_items", item_id)
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


def configure_dash_items(page):
    if page == "apps":
        dash_item_list()
        if "edit_dashboard_items" in st.session_state and not None:
            display_edit_item_form()


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
                                        onClick=lambda: edit_dashboard_part(
                                            "dashboard_layouts", layout[0]
                                        ),
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
