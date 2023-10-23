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

# Default
username = "admin"

# Check for provided Values
if "username" in st.session_state:
    username = st.session_state['username']

def fetch_as_dict(cursor, query, params=None):
    """Fetch a single record from a query and return it as a dictionary."""
    cursor.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None

class DatabaseModel:
    TABLE_NAME = None

    def __init__(self, **identifiers):
        self.conn = init_connection()
        self.identifiers = identifiers
        self.data = {}

    def load(self):
        if self.TABLE_NAME:
            where_clause = ' AND '.join([f"{k} = %s" for k in self.identifiers.keys()])
            query = f"SELECT * FROM {self.TABLE_NAME} WHERE {where_clause}"
            cursor = self.conn.cursor()
            self.data = fetch_as_dict(cursor, query, tuple(self.identifiers.values()))
            cursor.close()

    def update(self, column, value):
        cursor = self.conn.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in self.identifiers.keys()])
        
        # Check if the value is an empty string and set it to None
        if value == "":
            value = None    

        cursor.execute(f"UPDATE {self.TABLE_NAME} SET {column} = %s WHERE {where_clause}",
                       (value, *self.identifiers.values()))
        self.conn.commit()
        cursor.close()

    def delete(self):
        cursor = self.conn.cursor()
        where_clause = ' AND '.join([f"{k} = %s" for k in self.identifiers.keys()])
        cursor.execute(f"DELETE FROM {self.TABLE_NAME} WHERE {where_clause}", tuple(self.identifiers.values()))
        self.conn.commit()
        cursor.close()
    
    def monitor(self, key):
        """Monitor a specific session state key and synchronize its value with the data object."""
        try:
            # Initialize session state key from data object
            if key not in st.session_state:
                st.session_state[key] = self.data.get(key, None)
            
            # Update data object if session state differs from it
            if st.session_state[key] != self.data.get(key):
                self.update(key, st.session_state[key])

        except Exception as e:
            # Handle exceptions (e.g., if data is None or "")
            pass

class UserSettings(DatabaseModel): 
    TABLE_NAME = "user_settings"

class ColorSettings(DatabaseModel):
    TABLE_NAME = "color_settings"

class PageSettings(DatabaseModel):
    TABLE_NAME = "page_settings"

class Chats(DatabaseModel):
    TABLE_NAME = "chats"

class Messages(DatabaseModel):
    TABLE_NAME = "messages"

class HistoryChats(DatabaseModel):
    TABLE_NAME = "history_chats"
































# def initialize_datastore():
#     """Initialize and monitor the session states for the data objects."""
#     user = UserSettings(username="admin")
#     user.load()
#     user.monitor("dev_mode")
#     user.monitor("openai_key")
# 
#     page_config = PageSettings(username="admin")
#     page_config.load()
#     page_config.monitor("show_session_data")
# 
# # Usage:
# 
# # Initialization (only done once)
# if "initialized" not in st.session_state:
#     user = UserSettings(username="admin")
#     user.load()
#     
#     # Initialize session state from data object
#     st.session_state["dev_mode"] = user.data.get("dev_mode", False)
#     st.session_state["openai_key"] = user.data.get("openai_key", None)
#     
#     st.session_state["initialized"] = True















# # UI and Interaction
# st.title("Datastore Test")
# 
# if st.checkbox("Dev Mode", value=st.session_state["dev_mode"]):
#     st.session_state["dev_mode"] = True
# else:
#     st.session_state["dev_mode"] = False
# 
# openai_key = st.text_input("OpenAI Key", value=st.session_state["openai_key"])
# st.session_state["openai_key"] = openai_key
# 
# # Update Database on Interaction
# user = UserSettings(username="admin")
# user.update("dev_mode", st.session_state["dev_mode"])
# user.update("openai_key", st.session_state["openai_key"])
# 
# st.write("Session state values:")
# st.write(st.session_state)



# Rest of your Streamlit app logic...

#//""""""""
#//#! Multi version for keep data updated, and monitored | disabled because: no need for that many comlexity.
#//#====================#
#//#*__Dictionary_structure_organizing_setting_keys_according_to_their_table
#//#?| SETTINGS_BY_TABLE = {
#//#?|     "user": ["dev_mode", "openai_key"],
#//#?|     "page_config": ["show_session_data"]
#//#?|     # ... add more tables and their associated keys as needed
#//#?| }
#//
#//def init_or_update_data(data_objects, default_values=None, settings_tables={}):
#//    """
#//    Initialize or update st.session_state and data objects.
#//    
#//    :param data_objects: Dictionary of data objects (tables) e.g., {"user": user, "page_config": page_config}.
#//    :param default_values: Dictionary of default values for each table and its keys.
#//    :param settings_tables: Dictionary structure organizing setting keys according to their table.
#//    """
#//    if default_values is None:
#//        default_values = {table: {key: None for key in keys} for table, keys in settings_tables.items()}
#//    
#//    for table, keys in settings_tables.items():
#//        data_object = data_objects.get(table)
#//        
#//        # Ensure the data_object for the table exists
#//        if not data_object:
#//            raise ValueError(f"No data object provided for table: {table}")
#//
#//        for key in keys:
#//            # Initialize session state from data object or defaults
#//            if key not in st.session_state:
#//                st.session_state[key] = data_object.data.get(key, default_values[table][key])
#//            
#//            # If the key doesn't exist in data object's data, initialize it
#//            if key not in data_object.data:
#//                data_object.update(key, default_values[table][key])
#//
#//            # At the end, update data object if there's any change
#//            if st.session_state[key] != data_object.data.get(key):
#//                data_object.update(key, st.session_state[key])
#//
#//#*__Call_the_function_with_your_data_objects
#//#?| user = UserSettings(username="admin")
#//#?| user.load()
#//#?| page_config = PageSettings(username="admin")
#//#?| page_config.load()
#//#?| init_or_update_data(data_objects={"user_session": user, "page_config": page_config})
#//""""""""