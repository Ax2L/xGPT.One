import streamlit as st
import psycopg2

def init_connection():
    return psycopg2.connect(            
        dbname="xgpt",
        user="xgpt",
        password="xgpt",
        host="localhost",
        port="5435"
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

    color_settings_table = """
        CREATE TABLE color_settings (
            username VARCHAR(255) PRIMARY KEY,
            color_active_settings_button VARCHAR(7),
            color_active_help_button VARCHAR(7),
            color_active_datastore_button VARCHAR(7),
            color_active_tools_button VARCHAR(7),
            color_active_dashboard_button VARCHAR(7),
            color_active_apps_button VARCHAR(7),
            color_active_mlearning_button VARCHAR(7),
            color_active_upload_button VARCHAR(7),
            button_color_settings VARCHAR(7),
            button_color_help VARCHAR(7),
            button_color_datastore VARCHAR(7),
            button_color_tools VARCHAR(7),
            button_color_dashboard VARCHAR(7),
            button_color_apps VARCHAR(7),
            button_color_mlearning VARCHAR(7),
            button_color_upload VARCHAR(7)
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

    try:
        cursor.execute(user_settings_table)
    except Exception as e:
        print(f"Error: {e}")
    
    cursor.execute(color_settings_table)
    cursor.execute(page_settings_table)
    cursor.execute(chats_table)
    cursor.execute(messages_table)
    cursor.execute(history_chats_table)

    conn.commit()
    cursor.close()
    conn.close()

def insert_initial_data():
    conn = init_connection()
    cursor = conn.cursor()

    # Inserting initial data
    cursor.execute("INSERT INTO user_settings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    ('admin', 'Enter your Key', True, True, 'Note it down.', False, '', False, '', True, True))

    cursor.execute("INSERT INTO color_settings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    ('admin', '#1E1E1E', '#1E1E1E', '#1E1E1E', '#1E1E1E', '#1E1E1E', '#4F378B', '#1E1E1E', '#1E1E1E', 
                    '#4F378B', '#4F378B', '#4F378B', '#4F378B', '#4F378B', '#4F378B', '#4F378B', '#4F378B'))

    cursor.execute("INSERT INTO page_settings VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    ('admin', 'apps', '', '', '', False, []))

    cursor.execute("INSERT INTO chats (username, chat_name) VALUES (%s, %s)",
                    ('admin', 'Sample Chat'))

    cursor.execute("INSERT INTO messages (chat_id, username, content, sent_by) VALUES (%s, %s, %s, %s)",
                    (1, 'admin', 'Sample message content', 'admin'))

    cursor.execute("INSERT INTO history_chats (username, chat_content) VALUES (%s, %s)",
                    ('admin', 'Sample historical chat content'))

    conn.commit()
    cursor.close()
    conn.close()



create_tables()
insert_initial_data()

