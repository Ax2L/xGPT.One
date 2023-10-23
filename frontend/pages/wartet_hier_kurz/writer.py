# Import necessary libraries
import streamlit as st  # For building the web app
import components.documentor.work as work  # Custom module for various tasks
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union  # For type hints

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
page_name = "writer"
page_navi_number = 41
page_navi_category = "tools"

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

# Function for generating documentation based on the code
def doc_code(code_str, chat) -> str:
    spliter = work.get_file_type(st.session_state.file_type)  # Determine the file type
    code_split_ = work.code_splite(code_str, spliter)  # Split the code
    result = ""  # Initialize an empty result string
    results = work.doc_futures_run(code_split_, chat)  # Generate documentation
    for i in results:
        result += i  # Concatenate the documentation strings
    return result

# Function for inserting comments into the code
def code_with_comment(code_str, chat) -> str:
    spliter = work.get_file_type(st.session_state.file_type)  # Determine the file type
    code_split_ = work.code_splite(code_str, spliter)  # Split the code
    result = ""  # Initialize an empty result string
    results = work.comment_future_run(code_split_, chat)  # Generate comments
    for i in results:
        result += i  # Concatenate the comments into the result string
    return result

# Function for Q&A with the code
def qa_with_code(question: str, code_str, chat) -> str:
    spliter = work.get_file_type(st.session_state.file_type)  # Determine the file type
    code_split_ = work.code_splite(code_str, spliter)  # Split the code
    db = work.get_code_embd_save(code_split_)  # Get embeddings for the code
    result = work.qa_with_code_chain(db=db, question=question, chat=chat)  # Perform Q&A
    return result

# Set the title of the web app
st.title(":blue[Analyzing code using GPT 🤖]")

# Initialize session variables if not already present
if 'code' not in st.session_state:
    st.session_state.code = ""
if 'doc_result' not in st.session_state:
    st.session_state.doc_result = ""
if 'comment_result' not in st.session_state:
    st.session_state.comment_result = ""
if 'file_type' not in st.session_state:
    st.session_state.file_type = ""

# Sidebar configuration for chat and model settings
with st.sidebar:
    st.title(":blue[ChatGPT 🤖]")
    openai_api_key = st.text_input("Your OpenAI API Key", value=st.session_state.openai_key, type="password")  # Display the current key from session state
    model_name = st.selectbox(
        'Select Openai Model',
        ('gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k-0613', 'gpt-4', 'gpt-4-0613', 'gpt-4-32k', 'gpt-4-32k-0613')
    )
    temperature = st.slider('Set model temperature', 0.0, 2.0, 0.5)

# Initialize OpenAI key in session state if not present
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ""

# Check for the API key in session state and stop execution if not present
if st.session_state.openai_key:
    openai_api_key = st.session_state.openai_key
    st.session_state.chat = work.load_env(openai_api_key=openai_api_key, model_name=model_name, temperature=temperature)
elif not openai_api_key:  # If API Key is not found in the session state
    st.error("Please enter the OpenAI API Key")
    st.stop()
else:
    st.session_state.chat = work.load_env(openai_api_key=openai_api_key, model_name=model_name, temperature=temperature)


# File upload functionality
uploaded_file = st.file_uploader("Upload a code file", 
                                type=['cpp', 'cc', 'cxx', 'hpp', 'h', 'hxx', 'go', 'java', 'js', 'php', 'proto', 'py', 'rst', 'rb', 'rs', 'scala', 'swift', 'md', 'markdown', 'tex', 'html', 'sol'], 
                                help="Supports all major code files", key="up_file")

# Process the uploaded file
if uploaded_file is not None:
    with st.sidebar:
        st.title(f"{uploaded_file.name} Source Code:")
        code_str = uploaded_file.getvalue().decode("utf-8")
        st.session_state.file_type = uploaded_file.name
        st.session_state.code = code_str
        st.code(code_str, language="python")

    # Button configuration for adding comments and generating documentation
    col1, col2 = st.columns(spec=[0.5, 0.5], gap="large")
    with col1:
        comment_bt = st.button("Insert Comments")
    if comment_bt:
        with st.spinner("Inserting comments..."):
            result = code_with_comment(st.session_state.code, st.session_state.chat)
        st.session_state.comment_result = result
        st.success("Comments inserted successfully")

    with col2:
        doc_code_bt = st.button("Generate Documentation")
    if doc_code_bt:
        with st.spinner("Generating documentation..."):
            result = doc_code(st.session_state.code, st.session_state.chat)
        st.session_state.doc_result = result
        st.success("Documentation generated successfully")

# Display the results
if st.session_state.comment_result != "":
    with st.expander("Comments Result"):
        st.code(st.session_state.comment_result, language="python")
        st.download_button("Download Commented File", data=st.session_state.comment_result, file_name="commented_code.py")

if st.session_state.doc_result != "":
    with st.expander("Documentation Content"):
        st.markdown(st.session_state.doc_result)
        st.download_button("Download Documentation", data=st.session_state.doc_result, file_name="documentation.md")

# Chat functionality for asking questions related to the code
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "ai", "avatar": "🤖", "content": "I am a powerful AI assistant. Please upload your code file, and I will help you understand it better."}]

for msg in st.session_state.messages:
    st.chat_message(name=msg["role"], avatar=msg["avatar"]).markdown(msg["content"])

if st.session_state.code == "":
    st.error("Please upload a code file")
    st.stop()

if prompt := st.chat_input("Ask questions related to the code file", max_chars=4000, key="prompt"):
    st.session_state.messages.append({"role": "human", "avatar": "🧑", "content": prompt})
    with st.chat_message(name="ai", avatar="🤖"):
        with st.spinner("Generating answer..."):
            response = qa_with_code(prompt, st.session_state.code, st.session_state.chat)
        st.session_state.messages.append({"role": "ai", "avatar": "🤖", "content": response})
        st.markdown(response)
