# ! Python libraries
import streamlit as st

# ? Local modules
from components import xinit_page, xheader
from components.utils import xhelper

# & Functions


def setup_page(page_name):
    """* Setup and initialize the page.
    * Args:
    *   page_name (str): Name of the current page.
    """
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)


def load_custom_css():
    """* Load custom CSS for the page if not already active."""
    if f"{PAGE_NAME}_css" not in st.session_state:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            st.session_state.setdefault("{PAGE_NAME}_css", True)
    else:
        print(f"css already active on {PAGE_NAME}")


# ^ Constants
PAGE_NAME = "helper_itemgenui"

# & Page Initialization Process

# ! Do not modify this section
# * Initializing the page with required configurations
xinit_page.set_page_config(PAGE_NAME, "wide", "auto")
xheader.init(PAGE_NAME)

# * Setting up the page environment
setup_page(PAGE_NAME)
# * Loading custom CSS at the end
load_custom_css()

# ! Content Section


import psycopg2
import pandas as pd
import json
from datetime import datetime


# Database connection function
def init_connection():
    return psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )


# Function to add a new item to the database
def add_new_item(data):
    conn = init_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO dashboard_items (name, version, tags, created_at, updated_at, using_in_dashboard, settings_default, settings_user, documentation, repository, files, urls, ssl) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()


# Function to fetch recent items
def fetch_recent_items():
    conn = init_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM dashboard_layouts ORDER BY updated_at DESC LIMIT 10"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Convert JSON fields back to Python objects
    formatted_rows = []
    for row in rows:
        formatted_row = list(row)
        for index in [
            1,
            7,
            8,
            20,
        ]:  # Adjust these indexes based on your table structure
            formatted_row[index] = json.loads(formatted_row[index])
        formatted_rows.append(formatted_row)

    return pd.DataFrame(
        formatted_rows,
        columns=[
            name,
            version,
            tags,
            created_at,
            updated_at,
            using_in_dashboard,
            settings_default,
            settings_user,
            documentation,
            repository,
            files,
            urls,
            ssl,
        ],
    )


# Function to search items
def search_items(search_query):
    conn = init_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM dashboard_items WHERE name ILIKE %s OR tags ILIKE %s"
    cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(
        rows,
        columns=[
            "id",
            "name",
            "version",
            "tags",
            "created_at",
            "updated_at",
            "using_in_dashboard",
            "settings_default",
            "settings_user",
            "documentation",
            "repository",
            "files",
            "urls",
            "ssl",
        ],
    )


# Streamlit UI
st.title("Dashboard Item Management")

# Add New Item Form
with st.form("new_item_form"):
    st.subheader("Add New Item")
    # Add fields for each column in your dashboard_items table
    name = st.text_input("Name")
    version = st.text_input("Version")
    tags = st.text_input("Tags")
    created_at = st.date_input("Created At")
    updated_at = st.date_input("Updated At")
    using_in_dashboard = st.checkbox("Using in Dashboard")
    settings_default = st.text_area("Default Settings")
    settings_user = st.text_area("User Settings")
    documentation = st.text_area("Documentation")
    repository = st.text_input("Repository")
    files = st.text_input("Files")
    urls = st.text_input("URLs")
    ssl = st.checkbox("SSL")

    submit_button = st.form_submit_button("Add Item")
    if submit_button:
        add_new_item(
            (
                name,
                version,
                tags,
                created_at,
                updated_at,
                using_in_dashboard,
                settings_default,
                settings_user,
                documentation,
                repository,
                files,
                urls,
                ssl,
            )
        )
        st.success("Item Added Successfully")

# Display Recent Items
st.subheader("Recent Items")
recent_items = fetch_recent_items()
st.dataframe(recent_items)

# Search and Edit Items
st.subheader("Search and Edit Items")
search_query = st.text_input("Search Items")
if search_query:
    search_results = search_items(search_query)
    st.dataframe(search_results)

    # Select an item to edit
    selected_item_id = st.selectbox("Select Item to Edit", search_results["id"])
    # Add logic to load the selected item into the editor space
    # Add logic to update the item in the database
