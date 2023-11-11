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
    dashboard_layouts_table = """
        CREATE TABLE dashboard_layouts (
            page_id VARCHAR PRIMARY KEY,
            layout TEXT,
            username VARCHAR,
            page_name VARCHAR,
            description TEXT,
            notes TEXT,
            issues TEXT,
            name VARCHAR,
            version VARCHAR,
            tags TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            settings_default JSONB,
            settings_user JSONB,
            documentation TEXT,
            repository TEXT,
            files TEXT,
            urls TEXT,
            ssl BOOLEAN DEFAULT FALSE,
            entrypoint TEXT,
            using_item_name_list JSONB
        )
    """
    chats_table = """
        CREATE TABLE chats (
            chat_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
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
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            sent_by VARCHAR(50)
        )
    """

    history_chats_table = """
        CREATE TABLE history_chats (
            history_chat_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            chat_content TEXT,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """

    dashboard_items_table = """
        CREATE TABLE dashboard_items (
            id SERIAL PRIMARY KEY,
            layout TEXT,
            username VARCHAR(255),
            page_name VARCHAR(255),
            description TEXT,
            notes TEXT,
            issues TEXT,
            name VARCHAR(255),
            version VARCHAR(50),
            tags TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            using_in_dashboard TEXT,
            settings_default JSONB,
            settings_user JSONB,
            documentation TEXT,
            repository TEXT,
            files TEXT,
            urls TEXT,
            ssl BOOLEAN DEFAULT FALSE,
            entrypoint TEXT,
            item_list JSONB
        )
    """

    try:
        cursor.execute(user_settings_table)
        cursor.execute(dashboard_layouts_table)
        cursor.execute(page_settings_table)
        cursor.execute(chats_table)
        cursor.execute(messages_table)
        cursor.execute(history_chats_table)
        cursor.execute(dashboard_items_table)  # Execute the new table creation
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

    initial_layout = {
        "widgets": [
            {"id": 1, "type": "chart", "position": {"x": 0, "y": 0, "w": 4, "h": 3}},
            {"id": 2, "type": "table", "position": {"x": 4, "y": 0, "w": 4, "h": 3}},
            {"id": 3, "type": "table", "position": {"x": 3, "y": 0, "w": 4, "h": 3}},
        ]
    }
    cursor.execute(
        "INSERT INTO dashboard_layouts (page_id, layout, username, page_name, description, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            "default_page",
            json.dumps(initial_layout),
            "admin",
            "Default Page",
            "Default layout description",
            datetime.now(),
            datetime.now(),
        ),
    )

    default_dashboard_items = [
        {
            "layout": "sample_layout",
            "username": "admin",
            "page_name": "Default Page",
            "description": "Sample item description",
            "notes": "Sample notes",
            "issues": "None",
            "name": "Sample Item",
            "version": "1.0",
            "tags": "example, sample",
            "using_in_dashboard": "unused so far",
            "settings_default": json.dumps({"setting1": "value1"}),
            "settings_user": json.dumps({}),
            "documentation": "Sample documentation",
            "repository": "https://github.com/Ax2L/xGPT.One",
            "files": "file1.py, file2.py",
            "urls": "http://example.com",
            "ssl": False,
            "entrypoint": "http://url.with:3000",
            "item_list": json.dumps(["item1", "item2"]),
        }
        # Add more items as needed
    ]

    for item in default_dashboard_items:
        cursor.execute(
            """
            INSERT INTO dashboard_items 
            (layout, username, page_name, description, notes, issues, name, version, tags, using_in_dashboard, settings_default, settings_user, documentation, repository, files, urls, ssl, entrypoint, item_list) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                item["layout"],
                item["username"],
                item["page_name"],
                item["description"],
                item["notes"],
                item["issues"],
                item["name"],
                item["version"],
                item["tags"],
                item["using_in_dashboard"],
                item["settings_default"],
                item["settings_user"],
                item["documentation"],
                item["repository"],
                item["files"],
                item["urls"],
                item["ssl"],
                item["entrypoint"],
                item["item_list"],
            ),
        )

    # Logic to create an entry with the username as part of its ID
    username = st.session_state.get("username", "default")
    cursor.execute(
        """
        INSERT INTO dashboard_items 
        (layout, username, page_name, description, notes, issues, name, version, tags, using_in_dashboard, settings_default, settings_user, documentation, repository, files, urls, ssl, entrypoint, item_list) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            "user_layout",
            username,
            f"{username}'s Page",
            "User specific item description",
            "User notes",
            "User issues",
            f"{username}_item",
            "1.0",
            "user, custom",
            False,
            json.dumps({"setting1": "value1"}),
            json.dumps({}),
            "User specific documentation",
            "",
            "",
            "",
            False,
            "http://user.url:3000",
            json.dumps(["user_item1", "user_item2"]),
        ),
    )

    default_dashboard_layouts = [
        {
            "page_id": "default_page_1.0",
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
            "page_name": "Default Page",
            "description": "Default layout description",
            "notes": "Sample notes",
            "issues": "None",
            "name": "Default Layout",
            "version": "1.0",
            "tags": "default, layout",
            "settings_default": json.dumps({"setting1": "value1"}),
            "settings_user": json.dumps({}),
            "documentation": "Default layout documentation",
            "repository": "https://github.com/Ax2L/xGPT.One",
            "files": "layout1.py, layout2.py",
            "urls": "http://example.com",
            "ssl": False,
            "entrypoint": "http://url.with:3000",
            "using_item_name_list": json.dumps(["item1", "item2"]),
        }
    ]
    for layout in default_dashboard_layouts:
        cursor.execute(
            """
            INSERT INTO dashboard_layouts 
            (page_id, layout, username, page_name, description, notes, issues, name, version, tags, created_at, updated_at, settings_default, settings_user, documentation, repository, files, urls, ssl, entrypoint, using_item_name_list) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                layout["page_id"],
                layout["layout"],
                layout["username"],
                layout["page_name"],
                layout["description"],
                layout["notes"],
                layout["issues"],
                layout["name"],
                layout["version"],
                layout["tags"],
                datetime.now(),
                datetime.now(),
                layout["settings_default"],
                layout["settings_user"],
                layout["documentation"],
                layout["repository"],
                layout["files"],
                layout["urls"],
                layout["ssl"],
                layout["entrypoint"],
                layout["using_item_name_list"],
            ),
        )
    conn.commit()
    cursor.close()
    conn.close()


create_tables()
insert_initial_data()
