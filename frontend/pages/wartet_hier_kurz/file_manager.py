import streamlit as st
import os
import glob
import subprocess

# // region [ rgba(50, 100, 110, 0.2)] Navigation Data and Theme
#? ||--------------------------------------------------------------------------------||
#? ||                                    # NavBar                                    ||
#? ||--------------------------------------------------------------------------------||
from components.utils.navbar import NavBar
from streamlit_extras.#switch_page_button import #switch_page
# Background
from components.default import set_png_as_page_bg
set_png_as_page_bg('images/blue_dark_bg.png')

# Specific config for this page only:
page_name = "file_manager"
page_navi_number = 61
page_navi_category = "all_mls"

# Build Navi 
navbar = NavBar()
navi = navbar.build_navbar(page_navi_number)


try:
    if navi == page_name or page_navi_category:
        # st.text("current Page selected")
        do = "nothing"
    else:
        # st.text("You selected: "+ navi)
        #switch_page(navi)
except Exception as e:
    st.error(e)
#// endregion


def list_files(directory, extensions, search_filter="", max_display=10):
    all_files = []
    for ext in extensions:
        all_files.extend(glob.glob(f"{directory}/**/*{ext}", recursive=True))

    filtered_files = [os.path.relpath(f, start="database/resources") for f in all_files if search_filter.lower() in f.lower()]
    filtered_files = filtered_files[:max_display]

    if filtered_files:
        st.table(filtered_files)
    else:
        st.write("No matching files found.")

def refresh_script():
    try:
        subprocess.run(["python", "database/langchain_repo.py"])
        st.success("Script executed successfully.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Define directories and extensions
IMPORT_DIR = os.path.join(os.getcwd(), "database/resources/import")
LANGCHAIN_REPO_DIR = os.path.join(os.getcwd(), "database/resources/langchain-repo")
XGPT_REPO_DIR = os.path.join(os.getcwd(), "database/resources/xGPT-Repo")
EXTENSIONS = [".py", ".ipynb", ".md", ".mdx"]

# Create directories if they don't exist
for directory in [IMPORT_DIR, LANGCHAIN_REPO_DIR, XGPT_REPO_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Streamlit app title
st.title("File Management")

# Import Section
with st.expander("Import"):
    list_files(IMPORT_DIR, EXTENSIONS, max_display=10)
    uploaded_files = st.file_uploader("Choose files to upload to Import", accept_multiple_files=True)
    if st.button("Upload Files to Import"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                filepath = os.path.join(IMPORT_DIR, uploaded_file.name)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File {uploaded_file.name} is uploaded successfully.")
            list_files(IMPORT_DIR, EXTENSIONS, max_display=10)

# Langchain Repo Section
with st.expander("Langchain Repo"):
    langchain_search = st.text_input("Search files in Langchain Repo")
    if st.button("Refresh Langchain Repo"):
        refresh_script()
    list_files(LANGCHAIN_REPO_DIR, EXTENSIONS, search_filter=langchain_search, max_display=10)

# xGPT-Repo Section
with st.expander("xGPT-Repo"):
    xgpt_search = st.text_input("Search files in xGPT-Repo")
    list_files(XGPT_REPO_DIR, EXTENSIONS, search_filter=xgpt_search, max_display=10)

# Display iframe embedding localhost:8082
st.components.v1.html('<iframe src="http://localhost:8082/" width="800" height="600"></iframe>', width=820, height=620)