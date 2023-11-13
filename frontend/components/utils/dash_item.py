import streamlit as st
import json
import psycopg2


def init_connection():
    return psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )


DEFAULT_ITEM_VALUES = {
    "name": "NEW Item",
    "tags": "new, item",
    "using_in_dashboard": "unused so far",
    "settings_default": json.dumps({"setting1": "value1"}),
    "settings_user": json.dumps({}),
    "documentation": "Sample documentation",
    "repository": "https://github.com/Ax2L/xGPT.One",
    "files": "file1.py, file2.py",
    "urls": "http://example.com",
    "ssl": False,
    "entrypoint": "http://url.with:3000",
}


def fetch_dashboard_item_by_id(item_id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dashboard_items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        conn.close()
        return item
    except Exception as e:
        st.toast(f":red[Error fetching item by ID: {e}]")


def edit_dashboard_item(useID):
    print(f"edit dashboard item {useID}")
    fetch_item = fetch_dashboard_item_by_id(useID)
    if fetch_item:
        st.session_state["edit_item"] = fetch_item


def get_dashboard_items():
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dashboard_items")
        items = cursor.fetchall()
        conn.close()
        return items
    except Exception as e:
        st.toast(
            f":red[Error fetching dashboard items: {e}]",
        )


def insert_new_item():
    conn = psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dashboard_items 
        (name, tags, using_in_dashboard, settings_default, settings_user, documentation, repository, files, urls, ssl, entrypoint) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            DEFAULT_ITEM_VALUES["name"],
            DEFAULT_ITEM_VALUES["tags"],
            False,  # Assuming 'using_in_dashboard' is a boolean, replace with the correct boolean value
            DEFAULT_ITEM_VALUES["settings_default"],
            DEFAULT_ITEM_VALUES["settings_user"],
            DEFAULT_ITEM_VALUES["documentation"],
            DEFAULT_ITEM_VALUES["repository"],
            DEFAULT_ITEM_VALUES["files"],
            DEFAULT_ITEM_VALUES["urls"],
            DEFAULT_ITEM_VALUES["ssl"],
            DEFAULT_ITEM_VALUES["entrypoint"],
        ),
    )

    conn.commit()
    conn.close()


def check_and_load_or_create_item(itemID=None):
    try:
        conn = init_connection()
        cursor = conn.cursor()

        # Check if an item with the name "New Item" exists
        cursor.execute("SELECT * FROM dashboard_items WHERE id = %s", (itemID,))
        item = cursor.fetchone()

        if item:
            # Item exists, load its data
            st.session_state["edit_item"] = item
            st.toast(
                f":yellow[Item 'New Item' already exists. Loaded in the editor for editing.]"
            )
        else:
            # Item does not exist, create a new one
            insert_new_item()
            cursor.execute("SELECT * FROM dashboard_items WHERE id = %s", (itemID,))
            new_item = cursor.fetchone()
            st.session_state["edit_item"] = new_item
            st.toast(":green[New item 'New Item' created and loaded in the editor.]")

        conn.close()
    except Exception as e:
        st.toast(f":red[Error in check_and_load_or_create_item: {e}]")


def delete_dashboard_item(id):
    try:
        conn = psycopg2.connect(
            dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dashboard_items WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        st.toast(
            f":green[Item with ID {id} deleted successfully.]",
        )
    except Exception as e:
        st.toast(
            f":red[Error deleting item: {e}]",
        )
