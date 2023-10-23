import json
import psycopg2
import streamlit as st

print("\n Hello World!")

# Database Functions
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def run_query(query, params=None, return_type='all'):
    conn = init_connection()
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
        return None  # To handle database errors
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

class XDatabase:
    def __init__(self):
        self.config = self.load_config("../config/streamlit/db_init_rules.json")
        self.initialize_db()

    def load_config(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def initialize_db(self):
        for table in self.config['tables']:
            self.create_table("admin", table)

    def create_table(self, username, table_config):
        columns = ', '.join([f"{col['column_name']} {col['data_type']} {col.get('constraints', '')}".strip() for col in table_config['columns']])
        create_query = f"CREATE TABLE IF NOT EXISTS {table_config['table_name']} ({columns});"
        run_query(create_query)
        
        if 'initial_data' in table_config:
            for column, value in table_config['initial_data'].items():
                self.db_set_value(username, table_config['table_name'], column, value)

    def db_set_value(self, username, table_name, column_name, value):
        # Check if a record with the given username exists
        select_query = f"SELECT COUNT(*) FROM {table_name} WHERE username = %s;"
        count = run_query(select_query, (username,), return_type='one')[0]

        # If a record exists, update it; otherwise, insert a new record
        if count > 0:
            update_query = f"UPDATE {table_name} SET {column_name} = %s WHERE username = %s;"
            run_query(update_query, (value, username), return_type='none')
        else:
            insert_query = f"INSERT INTO {table_name} (username, {column_name}) VALUES (%s, %s);"
            run_query(insert_query, (username, value), return_type='none')


    def db_get_value(self, username, table_name, column_name):
        select_query = f"""
        SELECT {column_name} FROM {table_name} WHERE username = %s;
        """
        result = run_query(select_query, (username,), return_type='one')
        return result[0] if result else None


#?------------------?#
#?  TEST FUNCTIONS  ?#
#?------------------?#
def test_db_functions():
    # Initialize instance of XDatabase class
    db_instance = XDatabase()
    
    # Test initialize_db function
    try:
        db_instance.initialize_db()
        initialize_db_status = "initialize_db: Success"
    except Exception as e:
        initialize_db_status = f"initialize_db: Failed - {str(e)}"
    
    # Test create_table function
    test_table_config = {
        "table_name": "test_table",
        "columns": [{"column_name": "id", "data_type": "serial primary key"},
                    {"column_name": "data", "data_type": "text"}]
    }
    try:
        db_instance.create_table("admin", test_table_config)
        create_table_status = "create_table: Success"
    except Exception as e:
        create_table_status = f"create_table: Failed - {str(e)}"
    
    # Test db_set_value function
    try:
        db_instance.db_set_value("admin", "test_table", "data", "Test value")
        db_set_value_status = "db_set_value: Success"
    except Exception as e:
        db_set_value_status = f"db_set_value: Failed - {str(e)}"
    
    # Test db_get_value function
    try:
        value = db_instance.db_get_value("admin", "test_table", "data")
        if value == "Test value":
            db_get_value_status = "db_get_value: Success"
        else:
            db_get_value_status = f"db_get_value: Failed - Incorrect value retrieved"
    except Exception as e:
        db_get_value_status = f"db_get_value: Failed - {str(e)}"
    
    # Test delete function (You didn't provide a delete function in your code, so this is a placeholder)
    # If you have a delete function, replace the content of this try-except block with the test for it
    try:
        # db_instance.delete_function()  # Replace with your delete function if you have one
        delete_function_status = "delete_function: Placeholder (Replace with test for your delete function)"
    except Exception as e:
        delete_function_status = f"delete_function: Failed - {str(e)}"

    # Return the test results
    return [
        initialize_db_status,
        create_table_status,
        db_set_value_status,
        db_get_value_status,
        delete_function_status
    ]


#? To run the test, simply call:
# test_results = test_db_functions()
# for result in test_results:
#     print(result)



# Streamlit UI Functions
def display_database_status():
    try:
        # Check if you can connect to the database
        conn = init_connection()
        if conn:
            with st.expander("Database Connection Status: Connected"):
                st.write("Successfully connected to the database!")
        else:
            with st.expander("Database Connection Status: Failed"):
                st.write("Failed to connect to the database.")
    except:
        with st.expander("Database Connection Status: Failed"):
            st.write("Failed to connect to the database.")

def check_init_db_in_session_data():
    query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'session_data');"
    exists = run_query(query, return_type='one')[0]
    if exists:
        st.write("'session_data' table exists in the database.")
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'session_data';"
        columns = [col[0] for col in run_query(query)]
        if "init_db" in columns:
            st.write("'init_db' column exists in 'session_data' table.")
        else:
            st.write("'init_db' column does not exist in 'session_data' table. Consider database initialization.")
    else:
        st.write("'session_data' table does not exist in the database. Consider database initialization.")

def handle_initialize_db():
    db_instance = XDatabase()
    errors = []
    try:
        db_instance.initialize_db()
        st.write("Database initialized successfully!")
    except Exception as e:
        errors.append(str(e))
    
    if errors:
        st.write("Errors occurred during initialization:")
        for err in errors:
            st.write(f"- {err}")

# Main Streamlit UI
if st.__name__ == '__main__':
    display_database_status()
    check_init_db_in_session_data()
    
    if st.button("Initialize Database"):
        handle_initialize_db()

