import streamlit as st
from datetime import datetime
from components.postgres import *


# Streamlit UI
st.title("Counter App with Database")

# Retrieve and display email
email = db_get_value('admin', 'email')
email_display = email if email is not None else "No email found in database"
st.write(f"Email: {email_display}")

# Retrieve and display last login
last_login = db_get_value('admin', 'last_login')
last_login_display = last_login.strftime('%Y-%m-%d %H:%M:%S') if last_login is not None else "No last login found in database"
st.write(f"Last Login: {last_login_display}")

# Adding and updating last login via UI
new_last_login = st.date_input("New Last Login", value=None)

if st.button("Update Last Login") and new_last_login is not None:
    # Ensure last_login column exists
    add_column('last_login', 'TIMESTAMP')
    
    # Convert new_last_login to datetime because psycopg2 requires a datetime object, not a date object
    new_last_login_datetime = datetime.combine(new_last_login, datetime.min.time())
    
    # Update last login
    db_set_value('admin', 'last_login', new_last_login_datetime)
    st.success("Last login updated successfully!")
    

# TODO: What you need for a new Value:
# add_column('last_login', 'TIMESTAMP') # VARCHAR(255), BOOLEAN, etc...
# db_set_value('admin', 'last_login', new_last_login_datetime)
#
# TODO: What you need to read any value:
# db_get_value('admin', 'last_login') # (username, parameter)
