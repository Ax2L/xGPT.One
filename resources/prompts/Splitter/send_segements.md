My following script is too large for one prompt so that's why I want you now check very deeply if the following script has issues, not related to this, and then provide me an updated version of it before I send you the next part, where you will do the same till we are truth the file. DId you understand that?
_____
I currently facing this error when I open my streamlit page below:


# TODO: fix the issue!


*#* Issue:
```

```

*#* Here my Files:

* We use the following one as init db table creation:
```
import json
import streamlit as st
import psycopg2


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
    ON CONFLICT (id) DO UPDATE SET db_version = %s;
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
        return run_query(conn, select_query, (username,), return_type='one')

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

def get_all_chats_from_db() -> list:
    """Fetches all chat records from the chats table."""
    select_query = "SELECT * FROM chats;"
    with init_connection() as conn:
        return run_query(conn, select_query)


def display_session_data():
    """Displays session state data if session_state.show_session_data is True."""
    if st.session_state.get("show_session_data", False):
        st.write(st.session_state)
```

FOLLOW RULES: 
- JUMP DIRECTLY TO THE SECTION THAT I NEED, BUT INCLUDE INDICATORS 
- WHERE TO PLACE THE CODE AS WELL!
- DO NOT WRITE FUNCTIONS OR OTHER OBJECTS THAT DO NOT EXIST, ASK IF YOU DON'T KNOW!
- RULE: KEEP YOUR ANSWER EFFECTIVE AND VERY SHORT!

