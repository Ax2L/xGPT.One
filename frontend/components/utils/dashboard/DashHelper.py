# components/utils/dash_helper.py
# provide the functions for the dashboard in xdash.py
import streamlit as st
import json
import psycopg2
from components.utils.postgres import xdatastore


def init_connection():
    return xdatastore.init_connection()


# Define a simple update function
def update_field(field_name, value):
    st.session_state[f"edit_item_{field_name}"] = value


ITEM_FIELDS = [
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


DEFAULT_PART_VALUES = {
    "name": "NEW Part",
    "entrypoint": "http://url.with:3000",
    "ssl": False,
    "repository": "https://github.com/Ax2L/xGPT.One",
    "documentation": "Sample documentation",
    "settings_default": json.dumps({"setting1": "value1"}),
    "settings_user": json.dumps({}),
    "using_in_dashboard": False,
    "urls": "http://example.com",
    "files": "file1.py, file2.py",
    "tags": "new, part",
}

DEFAULT_LAYOUT_VALUES = {
    "id": 1,
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
    "username": "admin",
    "description": "New layout description",
    "tags": "New Page",
    "using_item_name_list": json.dumps(["part1", "part2"]),
}


def fetch_dashboard_parts_by_id(TABLE, part_id):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {TABLE} WHERE id = %s"
        cursor.execute(query, (part_id,))
        part = cursor.fetchone()
        conn.close()
        return part
    except Exception as e:
        st.toast(f":red[Error fetching part by ID: {e}]")


def get_dashboard_parts(TABLE):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE}")
        parts = cursor.fetchall()
        conn.close()
        return parts
    except Exception as e:
        st.toast(
            f":red[Error fetching dashboard parts: {e}]",
        )


def insert_new_item():
    conn = psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dashboard_items 
        (name, entrypoint, ssl, repository, documentation, settings_default, settings_user, using_in_dashboard, urls, files, tags) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            DEFAULT_PART_VALUES["name"],
            DEFAULT_PART_VALUES["entrypoint"],
            DEFAULT_PART_VALUES["ssl"],
            DEFAULT_PART_VALUES["repository"],
            DEFAULT_PART_VALUES["documentation"],
            DEFAULT_PART_VALUES["settings_default"],
            DEFAULT_PART_VALUES["settings_user"],
            DEFAULT_PART_VALUES["using_in_dashboard"],
            DEFAULT_PART_VALUES["urls"],
            DEFAULT_PART_VALUES["files"],
            DEFAULT_PART_VALUES["tags"],
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
        (name, layout, username, description, tags, using_item_name_list) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            DEFAULT_LAYOUT_VALUES["name"],
            DEFAULT_LAYOUT_VALUES["layout"],
            DEFAULT_LAYOUT_VALUES["username"],
            DEFAULT_LAYOUT_VALUES["description"],
            DEFAULT_LAYOUT_VALUES["tags"],
            DEFAULT_LAYOUT_VALUES["using_item_name_list"],
        ),
    )
    conn.commit()
    conn.close()


def insert_new_part(TABLE):
    if TABLE == "dashboard_items":
        insert_new_item()
    if TABLE == "dashboard_layouts":
        insert_new_layout()


def check_and_load_or_create_part(TABLE="", partID=None):
    try:
        conn = init_connection()
        cursor = conn.cursor()

        # Check if a part with the given ID exists
        query = f"SELECT * FROM {TABLE} WHERE id = %s"
        cursor.execute(query, (partID,))
        part = cursor.fetchone()

        if part:
            # Part exists, load its data
            st.session_state["edit_part"] = part
            st.toast(
                f":yellow[Part with ID {partID} already exists. Loaded in the editor for editing.]"
            )
        else:
            # Part does not exist, create a new one
            insert_new_part(TABLE)
            cursor.execute(query, (partID,))
            new_part = cursor.fetchone()
            st.session_state["edit_part"] = new_part
            st.toast(":green[New part created and loaded in the editor.]")

        conn.close()
    except Exception as e:
        st.toast(f":red[Error in check_and_load_or_create_part: {e}]")


def delete_dashboard_part(TABLE, partID):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM {TABLE} WHERE id = %s"
        cursor.execute(query, (partID,))
        conn.commit()
        conn.close()
        st.toast(f":green[Part with ID {partID} deleted successfully.]")
    except Exception as e:
        st.toast(f":red[Error deleting part: {e}]")
