import streamlit as st
import json
import psycopg2


def init_connection():
    return psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )


DEFAULT_LAYOUT_VALUES = {
    "name": "New Page",
    "layout": json.dumps(
        {
            "widgets": [
                {
                    "id": 1,
                    "type": "chart",
                    "position": {"x": 0, "y": 0, "w": 4, "h": 3},
                },
            ]
        }
    ),
    "tags": "New Page",
    "username": "admin",
    "description": "New layout description",
    "using_item_name_list": json.dumps(["item1", "item2"]),
}


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


def edit_dashboard_layout(useID):
    layout = fetch_dashboard_layout_by_id(useID)
    if layout:
        st.session_state["edit_layout"] = layout


def get_dashboard_layouts():
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dashboard_layouts")
        layouts = cursor.fetchall()
        conn.close()
        return layouts
    except Exception as e:
        st.toast(
            f":red[Error fetching dashboard layouts: {e}]",
        )


def insert_new_layout():
    conn = psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dashboard_layouts 
        (name, layout, tags, username, description, using_item_name_list) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            DEFAULT_LAYOUT_VALUES["name"],
            DEFAULT_LAYOUT_VALUES["layout"],
            DEFAULT_LAYOUT_VALUES["tags"],
            DEFAULT_LAYOUT_VALUES["username"],
            DEFAULT_LAYOUT_VALUES["description"],
            DEFAULT_LAYOUT_VALUES["using_item_name_list"],
        ),
    )
    conn.commit()
    conn.close()


def check_and_load_or_create_layouts(layoutID):
    try:
        conn = init_connection()
        cursor = conn.cursor()

        # Check if a layout with the name "New Layout" exists
        cursor.execute("SELECT * FROM dashboard_layouts WHERE id = %s", (layoutID,))
        layout = cursor.fetchone()

        if layout:
            # Layout exists, load its data
            st.session_state["edit_layout"] = layout
            st.toast(
                f":green[Item 'New Layout' already exists. Loaded in the editor for editing.]"
            )
        else:
            # Layout does not exist, create a new one
            insert_new_layout()
            cursor.execute("SELECT * FROM dashboard_layouts WHERE id = %s", (layoutID,))
            new_layout = cursor.fetchone()
            st.session_state["edit_layout"] = new_layout
            st.toast(
                ":green[New layout 'New Layout' created and loaded in the editor.]"
            )

        conn.close()
    except Exception as e:
        st.toast(f":red[Error in check_and_load_or_create_layouts: {e}]")


def delete_dashboard_layout(id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dashboard_layouts WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        st.toast(
            f":green[Layout with ID {id} deleted successfully.]",
        )
    except Exception as e:
        st.toast(
            f":red[Error deleting layout: {e}]",
        )
