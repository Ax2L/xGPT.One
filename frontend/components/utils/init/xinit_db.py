# components/init_db.py

import streamlit as st
import psycopg2
import json
from datetime import datetime


def init_connection():
    return psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )


def create_tables():
    conn = init_connection()
    cursor = conn.cursor()

    user_settings_table = """
        CREATE TABLE user_settings (
            username VARCHAR(255) PRIMARY KEY,
            openai_key VARCHAR(255),
            init_db BOOLEAN,
            dev_mode BOOLEAN,
            notes VARCHAR(255),
            authentication_status BOOLEAN,
            name VARCHAR(255),
            authenticator VARCHAR(255),
            current_page VARCHAR(255),
            initial_main BOOLEAN,
            shared BOOLEAN
        )
    """

    page_settings_table = """
        CREATE TABLE page_settings (
            username VARCHAR(255) PRIMARY KEY,
            menu_active_button VARCHAR(255),
            menu_previous_button VARCHAR(255),
            active_section VARCHAR(255),
            ai_apps_accordion_active VARCHAR(255),
            show_session_data BOOLEAN,
            chat_database JSONB
        )
    """

    chats_table = """
        CREATE TABLE chats (
            chat_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            start_time TEXT,
            end_time TIMESTAMP WITH TIME ZONE,
            chat_name VARCHAR(255)
        )
    """

    messages_table = """
        CREATE TABLE messages (
            message_id SERIAL PRIMARY KEY,
            chat_id INTEGER,
            username VARCHAR(255),
            content TEXT,
            timestamp TEXT,
            sent_by VARCHAR(50)
        )
    """

    history_chats_table = """
        CREATE TABLE history_chats (
            history_chat_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            chat_content TEXT,
            timestamp TEXT
        )
    """
    dashboard_tables = """
        CREATE TABLE IF NOT EXISTS dashboard_items (
            id SERIAL PRIMARY KEY,
            name TEXT,
            entrypoint TEXT,
            ssl BOOLEAN,
            repository TEXT,
            documentation TEXT,
            settings_default TEXT,
            settings_user TEXT,
            using_in_dashboard BOOLEAN,
            urls TEXT,
            files TEXT,
            tags TEXT
        );
        CREATE TABLE IF NOT EXISTS dashboard_layouts (
            id SERIAL PRIMARY KEY,
            name TEXT,
            layout TEXT,
            username TEXT,
            description TEXT,
            tags TEXT,
            using_item_name_list TEXT
        );
    """

    try:
        cursor.execute(user_settings_table)
        cursor.execute(dashboard_tables)
        cursor.execute(page_settings_table)
        cursor.execute(chats_table)
        cursor.execute(messages_table)
        cursor.execute(history_chats_table)
    except Exception as e:
        print(f"Error creating tables: {e}")

    conn.commit()
    cursor.close()
    conn.close()


def insert_initial_data():
    conn = init_connection()
    cursor = conn.cursor()

    # Inserting initial data
    cursor.execute(
        "INSERT INTO user_settings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            "admin",
            "Enter your Key",
            True,
            True,
            "Note it down.",
            False,
            "",
            False,
            "",
            True,
            True,
        ),
    )

    cursor.execute(
        "INSERT INTO page_settings VALUES (%s, %s, %s, %s, %s, %s, %s)",
        ("admin", "apps", "", "", "", False, []),
    )

    cursor.execute(
        "INSERT INTO chats (username, chat_name) VALUES (%s, %s)",
        ("admin", "Sample Chat"),
    )

    cursor.execute(
        "INSERT INTO messages (chat_id, username, content, sent_by) VALUES (%s, %s, %s, %s)",
        (1, "admin", "Sample message content", "admin"),
    )

    cursor.execute(
        "INSERT INTO history_chats (username, chat_content) VALUES (%s, %s)",
        ("admin", "Sample historical chat content"),
    )
    username = st.session_state.get("username", "admin")
    cursor.execute(
        """
        INSERT INTO dashboard_items 
        (name, entrypoint, ssl, repository, documentation, settings_default, settings_user, using_in_dashboard, urls, files, tags) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            f"{username}_item",
            "http://user.url:3000",
            False,
            "",
            "User specific documentation",
            json.dumps({"setting1": "value1"}),
            json.dumps({"setting1": "value1"}),
            False,
            "",
            "",
            "user, custom",
        ),
    )

    # Updated INSERT statement for dashboard_layouts
    default_dashboard_layouts = [
        {
            "name": "Default Page",
            "layout": json.dumps(
                {
                    "widgets": [
                        {
                            "id": 1,
                            "type": "chart",
                            "position": {"x": 0, "y": 0, "w": 4, "h": 3},
                        }
                    ]
                }
            ),
            "username": "admin",
            "description": "Default layout description",
            "tags": "default page template",
            "using_item_name_list": json.dumps(["item1", "item2"]),
        }
    ]
    for layout in default_dashboard_layouts:
        cursor.execute(
            """
            INSERT INTO dashboard_layouts 
            (name, layout, username, description, tags, using_item_name_list) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                layout["name"],
                layout["layout"],
                layout["username"],
                layout["description"],
                layout["tags"],
                layout["using_item_name_list"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()


create_tables()
insert_initial_data()
