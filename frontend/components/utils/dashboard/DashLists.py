import streamlit as st
from streamlit_elements import mui
from components.utils.dashboard.DashUtils import (
    update_edit_item,
    update_edit_layout,
)
from components.utils.dashboard.DashHelper import delete_dashboard_part, insert_new_part


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
                                                lambda: delete_dashboard_part(
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
                        onClick=lambda: insert_new_part("dashboard_items"),
                    )


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
                                        ]: delete_dashboard_part(
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
                onClick=lambda: insert_new_part("dashboard_layouts"),
            )
