import os
import streamlit as st

class FileBrowser:
    def __init__(self, root_path=None):
        self.root_path = root_path if root_path is not None else os.getcwd()
        self.current_path = self.root_path
        self.file_selector = st.empty()

    def display(self):
        self.show_path()
        self.show_contents()
        self.handle_navigation()

    def show_path(self):
        st.write(f"Current path: {self.current_path}")

    def show_contents(self):
        # Get all folders and files
        items = os.listdir(self.current_path)
        item_paths = [os.path.join(self.current_path, item) for item in items]
        dirs = [d for d, path in zip(items, item_paths) if os.path.isdir(path)]
        files = [f for f, path in zip(items, item_paths) if os.path.isfile(path)]

        # Display folders
        if dirs:
            folder_button = st.button("Go Up")
            if folder_button:
                # Go up one folder level
                self.current_path = os.path.dirname(self.current_path)

        # Display folders and files
        self.file_selector = st.selectbox("Choose a file", [".."] + dirs + files, format_func=lambda x: x)

    def handle_navigation(self):
        selected = self.file_selector
        if selected == "..":
            self.current_path = os.path.dirname(self.current_path)
        elif os.path.isdir(os.path.join(self.current_path, selected)):
            self.current_path = os.path.join(self.current_path, selected)

def app():
    st.title('Simple File Browser')
    fb = FileBrowser()
    fb.display()

    # Rest of your Streamlit app

app()
