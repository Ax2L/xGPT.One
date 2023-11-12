# components/xdatastore.py

import streamlit as st
import psycopg2


def init_connection():
    return psycopg2.connect(
        dbname="xgpt", user="xgpt", password="xgpt", host="localhost", port="5435"
    )


# Default
username = "admin"

# Check for provided Values
if "username" in st.session_state:
    username = st.session_state["username"]


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
        self.ensure_table_exists()

    def ensure_table_exists(self):
        if self.TABLE_NAME:
            cursor = self.conn.cursor()
            cursor.execute(
                f"""
                SELECT EXISTS (
                    SELECT FROM 
                        pg_tables
                    WHERE 
                        schemaname = 'public' AND 
                        tablename  = '{self.TABLE_NAME}'
                );
            """
            )
            if not cursor.fetchone()[0]:
                self.create_table(cursor)
            cursor.close()

    def create_table(self, cursor):
        # Override this method in subclasses to define table creation logic
        pass

    def load(self):
        if self.TABLE_NAME:
            query = f"SELECT * FROM {self.TABLE_NAME}"
            if self.identifiers:
                where_clause = " AND ".join(
                    [f"{k} = %s" for k in self.identifiers.keys()]
                )
                query += f" WHERE {where_clause}"
                cursor = self.conn.cursor()
                self.data = fetch_as_dict(
                    cursor, query, tuple(self.identifiers.values())
                )
            else:
                cursor = self.conn.cursor()
                cursor.execute(query)
                self.data = (
                    cursor.fetchall()
                )  # or fetchone(), depending on your requirement
            cursor.close()

    # def load(self): # OLD
    #    if self.TABLE_NAME:
    #        where_clause = " AND ".join([f"{k} = %s" for k in self.identifiers.keys()])
    #        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {where_clause}"
    #        cursor = self.conn.cursor()
    #        self.data = fetch_as_dict(cursor, query, tuple(self.identifiers.values()))
    #        cursor.close()

    def update(self, column, value):
        cursor = self.conn.cursor()
        where_clause = " AND ".join([f"{k} = %s" for k in self.identifiers.keys()])

        # Check if the value is an empty string and set it to None
        if value == "":
            value = None

        cursor.execute(
            f"UPDATE {self.TABLE_NAME} SET {column} = %s WHERE {where_clause}",
            (value, *self.identifiers.values()),
        )
        self.conn.commit()
        cursor.close()

    def delete(self):
        cursor = self.conn.cursor()
        where_clause = " AND ".join([f"{k} = %s" for k in self.identifiers.keys()])
        cursor.execute(
            f"DELETE FROM {self.TABLE_NAME} WHERE {where_clause}",
            tuple(self.identifiers.values()),
        )
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


class DashboardLayouts(DatabaseModel):
    TABLE_NAME = "dashboard_layouts"

    def insert(self, **data):
        cursor = self.conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        cursor.close()

    def get_column_names(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dashboard_layouts LIMIT 0")
        return [desc[0] for desc in cursor.description]


class DashboardItems(DatabaseModel):
    TABLE_NAME = "dashboard_items"

    def insert(self, **data):
        cursor = self.conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        cursor.close()

    def get_column_names(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dashboard_items LIMIT 0")
        return [desc[0] for desc in cursor.description]


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
