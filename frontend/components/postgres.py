import psycopg2

# TODO: What you need for a new Value:
# add_column('last_login', 'TIMESTAMP') # VARCHAR(255), BOOLEAN, etc...
# db_set_value('last_login', new_last_login_datetime)
#
# TODO: What you need to read any value:
# db_get_value('last_login') # (parameter)



# Database Functions
def init_connection():
    return psycopg2.connect(            
        dbname="xgpt",
        user="xgpt",
        password="xgpt",
        host="localhost",
        port="5435"
    )

conn = init_connection()
print(conn)


def run_query(conn, query, params=None, return_type='all'):
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
    except Exception as e:
        print(f"Error: {e}")

def db_init():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS session_data (
        username VARCHAR(255) PRIMARY KEY,
        key_openai VARCHAR(255),
        dev_mode BOOLEAN,
        notes VARCHAR(255)
    );
    """
    insert_init_data_query = """
    INSERT INTO session_data(username, key_openai, dev_mode, notes)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (username) DO NOTHING;
    """
    init_data = ('admin', 'Enter your Key', True, 'Note it down.')  # Initial data

    with init_connection() as conn:
        # Create table
        run_query(conn, create_table_query, return_type='none')

        # Insert initial data
        run_query(conn, insert_init_data_query, init_data, return_type='none')


def add_column(column_name, data_type):
    alter_query = f"ALTER TABLE session_data ADD COLUMN IF NOT EXISTS {column_name} {data_type};"
    with init_connection() as conn:
        run_query(conn, alter_query, return_type='none')

def db_set_value(username, table_name, column_name, value):
    # Make sure column name is safe to insert into SQL
    if not column_name.isidentifier():
        raise ValueError("Invalid column name")
    update_query = f"""
    UPDATE {table_name}
    SET {column_name} = %s
    WHERE username = %s;
    """
    with init_connection() as conn:
        run_query(conn, update_query, (value, username), return_type='none')

def db_get_value(username, table_name, column_name):
    select_query = f"""
    SELECT {column_name} FROM {table_name} WHERE username = %s;
    """
    with init_connection() as conn:
        result = run_query(conn, select_query, (username,), return_type='one')
        return result[0] if result else None



username = "admin"
table_name = "session_data"
column_name = "xtest"
value = "this is a test"

check_column = add_column('xtest', 'VARCHAR(255)') 
print("Checking for Column:",check_column)
set = db_set_value(username, table_name, column_name, value)
print("Setting Value:",check_column)


get = db_get_value(username, table_name, column_name)
print("Getting Data from DB:",check_column)


