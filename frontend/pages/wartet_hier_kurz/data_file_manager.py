import os
import streamlit as st
from pathlib import Path
from st_click_detector import click_detector as did_click
from streamlit_elements import elements, mui, html, lazy, sync
from streamlit_elements import editor
import shutil
import streamlit as st





######## THIS BELOW NOT! ########
from components.utils import sidebar_menu
from PIL import Image

menu = sidebar_menu.sidebar_header_button()

if menu == "settings":
    sidebar_menu.settings_box()

if menu == "datastore":
    sidebar_menu.datastore_box()

if menu == "apps":
    sidebar_menu.settings_box()

if menu == "tools":
    sidebar_menu.settings_box()

if menu == "dashboard":
    sidebar_menu.settings_box()


# Load Config
logo = Image.open('images/logo/xgpt.png')
######### THIS ABOVE NOT! #######


# Function to get the subfolders and files in a directory.
def get_subfolders_and_files(folder_path):
    subfolders = []
    files = []
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                subfolders.append(item)
            else:
                files.append(item)
        return subfolders, files
    except Exception as e:
        st.error(str(e))
        return subfolders, files

# Function to create folder or file.
def create_item(current_path, type):
    new_name = st.text_input(f"Create a new {type}")
    if st.button(f"Create {type}"):
        new_path = os.path.join(current_path, new_name)
        try:
            if type == "Folder":
                os.makedirs(new_path)
            elif type == "File":
                with open(new_path, 'w') as f:
                    pass
            st.success(f"{type} created successfully!")
            return True
        except Exception as e:
            st.error(str(e))
            return False
    return False

# Main navigation and UI flow
def file_folder_navigator(current_path):
    subfolders, files = get_subfolders_and_files(current_path)

    # Folders Table
    st.write("### Folders")
    selected_folders = st.multiselect("Select to Delete", options=subfolders)
    if st.button("Delete Selected Folders"):
        for folder in selected_folders:
            try:
                shutil.rmtree(os.path.join(current_path, folder))
                st.success(f"Deleted: {folder}")
            except Exception as e:
                st.error(str(e))

    for folder in subfolders:
        col1, col2 = st.columns([4, 1])
        if col1.button(folder):
            st.session_state["current_path"] = os.path.join(current_path, folder)

    should_refresh = create_item(current_path, "Folder")

    # Files Table
    st.write("### Files")
    selected_files = st.multiselect("Select to Delete (Files)", options=files, key='files')
    if st.button("Delete Selected Files"):
        for file in selected_files:
            try:
                os.remove(os.path.join(current_path, file))
                st.success(f"Deleted: {file}")
            except Exception as e:
                st.error(str(e))

    for file in files:
        col1, col2 = st.columns([4, 3])
        col1.write(file)
        if col2.button(f"{file}"):
            with open(os.path.join(current_path, file), 'r') as f:
                st.text_area("File Content", f.read())

    should_refresh = create_item(current_path, "File") or should_refresh

    # Refresh if needed
    if should_refresh:
        st.experimental_rerun()

# Streamlit UI
st.title("Simple File Manager")

# Session state initialization
if "current_path" not in st.session_state:
    st.session_state["current_path"] = os.getcwd()

# Displaying and allowing the user to change the current path.
current_path = st.text_input("Current Path:", st.session_state["current_path"])
if Path(current_path).exists():
    st.session_state["current_path"] = current_path
else:
    st.error("Path does not exist!")

# Upload File
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    with open(os.path.join(st.session_state["current_path"], uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} has been uploaded.")

# File/Folder navigator UI and actions.
file_folder_navigator(st.session_state["current_path"])


with elements("monaco_editors"):

    # Streamlit Elements embeds Monaco code and diff editor that powers Visual Studio Code.
    # You can configure editor's behavior and features with the 'options' parameter.
    #
    # Streamlit Elements uses an unofficial React implementation (GitHub links below for
    # documentation).

    if "content" not in st.session_state:
        st.session_state.content = "Default value"

    mui.Typography("Content: ", st.session_state.content)

    def update_content(value):
        st.session_state.content = value

    editor.Monaco(
        height=300,
        defaultValue=st.session_state.content,
        onChange=lazy(update_content)
    )

    mui.Button("Update content", onClick=sync())

    editor.MonacoDiff(
        original="Happy Streamlit-ing!",
        modified="Happy Streamlit-in' with Elements!",
        height=300,
    )








#* Add custom CSS Style
with open('components/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
