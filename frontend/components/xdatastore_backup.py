import json
import streamlit as st
import psycopg2




print("\n Hello World!")

#? What you need for a new Value:
#* add_column('last_login', 'TIMESTAMP') # VARCHAR(255), BOOLEAN, etc...
#* db_set_value('admin', 'last_login', new_last_login_datetime)
#
#? What you need to read any value:
#* db_get_value('admin', 'last_login') # (username, parameter)


# Database Functions

def init_connection():
    """Initialize a connection to the database."""
    return psycopg2.connect(**st.secrets["postgres"])


def run_query(conn, query, params=None, return_type='all'):
    """Run a database query and return the results based on the specified return type."""
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            
            if return_type == 'all':
                return cur.fetchall()
            elif return_type == 'one':
                return cur.fetchone()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def create_metadata_table(db_version):
    """Create the metadata table and insert the current db_version."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS metadata (
        id SERIAL PRIMARY KEY,
        db_version VARCHAR(255)
    );
    """
    
    insert_version_query = """
    INSERT INTO metadata(db_version)
    VALUES (%s)
    ON CONFLICT (username, chat_name) DO UPDATE SET data = %s;
    """
    
    with init_connection() as conn:
        run_query(conn, create_table_query, return_type='none')
        run_query(conn, insert_version_query, (db_version, db_version), return_type='none')

def load_db_rules_from_json(filename='../config/streamlit/db_init_rules.json'):
    """Load the database initialization rules from a JSON file."""
    with open(filename, 'r') as file:   
        return json.load(file)
def handle_missing_tables(db_rules):
    """Check and add any missing tables based on the JSON rules."""
    existing_tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    
    with init_connection() as conn:
        existing_tables = run_query(conn, existing_tables_query, return_type='all')
        existing_table_names = {table[0] for table in existing_tables}
        desired_table_names = {table["table_name"] for table in db_rules["tables"]}
        
        missing_tables = desired_table_names - existing_table_names
        for table in db_rules["tables"]:
            if table["table_name"] in missing_tables:
                columns = table["columns"]
                columns_sql_list = [f"{col['column_name']} {col['data_type']} {col.get('constraints', '')}" for col in columns]
                columns_sql = ', '.join(columns_sql_list)
                create_table_query = f"CREATE TABLE {table['table_name']} ({columns_sql});"
                run_query(conn, create_table_query, return_type='none')

def ensure_table_exists(table_name, columns):
    """Ensure that the table exists and create it if not."""
    columns_sql_list = [f"{col['column_name']} {col['data_type']} {col.get('constraints', '')}" for col in columns]
    columns_sql = ', '.join(columns_sql_list)
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
    
    with init_connection() as conn:
        run_query(conn, create_table_query, return_type='none')

def ensure_column_exists(table_name, column_name, data_type):
    """Ensure that the column exists in the table and create it if not."""
    alter_query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {data_type};"
    
    with init_connection() as conn:
        run_query(conn, alter_query, return_type='none')


def db_init_from_json():
    """Initialize the database based on JSON rules."""
    db_rules = load_db_rules_from_json()
    
    # Ensure all tables exist
    handle_missing_tables(db_rules)

    with init_connection() as conn:
        for table in db_rules["tables"]:
            table_name = table["table_name"]
            columns = table["columns"]

            # Ensure all columns exist
            handle_missing_columns(table_name, columns)

            # Construct SQL for column creation
            columns_sql_list = [f"{col['column_name']} {col['data_type']} {col.get('constraints', '')}" for col in columns]
            columns_sql = ', '.join(columns_sql_list)

            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
            run_query(conn, create_table_query)

            if table_name in db_rules['initial_data']:
                column_names = [col['column_name'] for col in columns]
                placeholders = ', '.join(['%s' for _ in column_names])
                initial_data_values = tuple(db_rules["initial_data"][table_name][col_name] for col_name in column_names if col_name in db_rules["initial_data"][table_name])

                insert_init_data_query = f"INSERT INTO {table_name}({', '.join(column_names)}) VALUES ({placeholders}) ON CONFLICT ({column_names[0]}) DO NOTHING;"
                run_query(conn, insert_init_data_query, initial_data_values)

def get_history_chats(username: str) -> list:
    select_query = f"SELECT chat_name FROM chats WHERE username = %s;"
    with init_connection() as conn:
        return [chat[0] for chat in run_query(conn, select_query, (username,))]

def load_data(username: str, chat_name: str) -> dict:
    select_query = f"SELECT data FROM chats WHERE username = %s AND chat_name = %s;"
    with init_connection() as conn:
        result = run_query(conn, select_query, (username, chat_name))
        return result[0] if result else None

def save_data(username: str, chat_name: str, data: dict):
    # Ensure table and columns exist
    chats_columns = [
        {"column_name": "username", "data_type": "VARCHAR(255)"},
        {"column_name": "chat_name", "data_type": "VARCHAR(255)"},
        {"column_name": "data", "data_type": "JSONB"}
    ]
    ensure_table_exists("chats", chats_columns)
    
    upsert_query = """
    INSERT INTO chats(username, chat_name, data)
    VALUES (%s, %s, %s)
    ON CONFLICT (username, chat_name) DO UPDATE SET data = %s;
    """
    with init_connection() as conn:
        run_query(conn, upsert_query, (username, chat_name, json.dumps(data), json.dumps(data)))


def remove_data(username: str, chat_name: str):
    delete_query = "DELETE FROM chats WHERE username = %s AND chat_name = %s;"
    with init_connection() as conn:
        run_query(conn, delete_query, (username, chat_name))


#def load_db_rules_from_json(filename='../config/streamlit/db_init_rules.json'):
#    """Load the database initialization rules from a JSON file."""
#    with open(filename, 'r') as file:   
#        return json.load(file)

#def db_init_from_json():
#    """Initialize the database based on JSON rules."""
#    db_rules = load_db_rules_from_json()
#    
#    # Process multiple tables
#    for table in db_rules["tables"]:
#        table_name = table["table_name"]
#        columns = table["columns"]
#        
#        # Construct SQL for column creation
#        columns_sql_list = [f"{col['column_name']} {col['data_type']} {col.get('constraints', '')}" for col in columns]
#        columns_sql = ', '.join(columns_sql_list)
#        
#        create_table_query = f"""
#        CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});
#        """
#        
#        with init_connection() as conn:
#            run_query(conn, create_table_query, return_type='none')
#            
#            # Check if initial data for this table exists in the JSON file
#            if table_name in db_rules['tables'][2]:
#                column_names = [col['column_name'] for col in columns]
#                placeholders = ', '.join(['%s' for _ in column_names])
#                initial_data_values = tuple(db_rules["initial_data"][table_name][col_name] for col_name in column_names if col_name in db_rules["initial_data"][table_name])
#                
#                insert_init_data_query = f"""
#                INSERT INTO {table_name}({', '.join(column_names)})
#                VALUES ({placeholders})
#                ON CONFLICT ({column_names[0]}) DO NOTHING;
#                """
#                
#                run_query(conn, insert_init_data_query, initial_data_values, return_type='none')


def handle_missing_columns(table_name, columns):
    """Check and add any missing columns based on the JSON rules."""
    existing_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';"
    
    with init_connection() as conn:
        existing_columns = run_query(conn, existing_columns_query, return_type='all')
        existing_column_names = {column[0] for column in existing_columns}
        desired_column_names = {column[0] for column in columns}
        
        missing_columns = desired_column_names - existing_column_names
        for missing_column in missing_columns:
            column_info = next(col for col in columns if col[0] == missing_column)
            add_column(column_info[0], column_info[1])


def add_column(column_name, data_type):
    """Add a new column to the session_data table."""
    alter_query = f"ALTER TABLE session_data ADD COLUMN IF NOT EXISTS {column_name} {data_type};"
    
    with init_connection() as conn:
        run_query(conn, alter_query, return_type='none')


def db_set_value(username, table, column_name, value):
    """Set a specific value for a user in the table."""
    if not column_name.isidentifier():
        raise ValueError("Invalid column name")
    
    update_query = f"""
    UPDATE {table}
    SET {column_name} = %s
    WHERE username = %s;
    """
    
    with init_connection() as conn:
        run_query(conn, update_query, (value, username), return_type='none')

def db_get_value(username, table, column_name):
    """Retrieve a specific value for a user from the table."""
    if not column_name.isidentifier():
        raise ValueError("Invalid column name")
    
    select_query = f"""
    SELECT {column_name}
    FROM {table}
    WHERE username = %s;
    """
    
    with init_connection() as conn:
        return run_query(conn, select_query, (username), return_type='one')

def load_data(username: str, chat_name: str) -> dict:
    select_query = f"SELECT data FROM chats WHERE username = %s AND chat_name = %s;"
    with init_connection() as conn:
        result = run_query(conn, select_query, (username, chat_name))
        # Ensure the result is in expected format
        if result and isinstance(result[0], dict):
            return result[0]
        else:
            return {}

def save_data(username: str, chat_name: str, data: dict):
    """
    Save the chat data to the database.
    """
    insert_query = """
        INSERT INTO chats (username, chat_name, data) 
        VALUES (%s, %s, %s)
        ON CONFLICT (username, chat_name) DO UPDATE
        SET data = EXCLUDED.data;
    """
    with init_connection() as conn:
        run_query(conn, insert_query, (username, chat_name, json.dumps(data)))


# Streamlit App
def main():
    st.title('Chat App')

    username = st.text_input("Enter your username:", "")
    chat_name = st.text_input("Enter chat name:", "")

    if username and chat_name:
        chat_data = load_data(username, chat_name)
        chat_history = chat_data.get("chat_history", [])

        # Display previous chats
        for message in chat_history:
            st.write(message)

        # Input for new message
        new_message = st.text_input("Type your message:", "")
        if new_message:
            chat_history.append(new_message)
            save_data(username, chat_name, {"chat_history": chat_history})
            st.write(new_message)


def database_manual_input_ui():
    """Main function to handle Streamlit UI and database operations."""
    st.title("Database Management with Streamlit")
    
    # Example of setting a value
    user_input = st.text_input("Enter username:")
    table_input = st.text_input("Enter table name:")
    column_input = st.text_input("Enter column name:")
    value_input = st.text_input("Enter value:")
    
    if st.button("Set Value"):
        db_set_value(user_input, table_input, column_input, value_input)
        st.success(f"Value set successfully for {user_input} in table {table_input}, column {column_input}.")

    # Example of getting a value
    if st.button("Get Value"):
        result = db_get_value(user_input, table_input, column_input)
        st.write(f"Retrieved Value for {user_input} in table {table_input}, column {column_input}: {result}")


# def get_current_db_version():
#     """Retrieve the current version of the database."""
#     select_query = "SELECT db_version FROM metadata LIMIT 1;"
#     
#     with init_connection() as conn:
#         result = run_query(conn, select_query, return_type='one')
#         return result[0] if result else None


# current_version = get_current_db_version()
# desired_version = load_db_rules_from_json()["metadata"]["db_version"]
# 
# if current_version != desired_version:
#     # Proceed with the initialization or migration.
#     db_init_from_json()
# else:
#     # Database is already initialized to the desired state, so skip.
#     pass


def get_all_chats_from_db() -> list:
    """Fetches all chat records from the chats table."""
    select_query = "SELECT * FROM chats;"
    with init_connection() as conn:
        return run_query(conn, select_query)


def display_session_data():
    """Displays session state data if session_state.show_session_data is True."""
    if st.session_state.get("show_session_data", False):
        st.write(st.session_state)
        



print("\n Hello World!")