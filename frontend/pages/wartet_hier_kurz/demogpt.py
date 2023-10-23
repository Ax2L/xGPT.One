import logging
import os
import signal
import sys

import streamlit as st
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
parent_directory = os.path.dirname(current_directory)
grandparent_directory = os.path.dirname(parent_directory)
sys.path.append(grandparent_directory)

from components.demogpt.model import DemoGPT
from components.demogpt.utils import runStreamlit

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
page_name = "demogpt"
page_navi_number = 22
page_navi_category = "coder"

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

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")


def generate_response(txt, title):
    """
    Generate response using the LangChainCoder.

    Args:
        txt (str): The input text.

    Yields:
        dict: A dictionary containing response information.
    """
    for data in agent(txt, title):
        yield data


def initCode():
    if "code" not in st.session_state:
        st.session_state["code"] = ""
        st.session_state.edit_mode = False


# Page title
title = "🧩 DemoGPT"

st.title(title)

initCode()

# Text input

# Initialize the OpenAI API Key from session state or environment variables
openai_api_key = st.session_state.get("openai_key", os.getenv("OPENAI_API_KEY", ""))

# Replace the existing input with session state or environment variable
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=openai_api_key,  # using openai_api_key variable
    type="password",
)

openai_api_base = st.sidebar.text_input(
    "Open AI base URL",
    placeholder="https://api.openai.com/v1",
)

models = (
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
)

model_name = st.sidebar.selectbox("Model", models)

empty_idea = st.empty()
demo_idea = empty_idea.text_area(
    "Enter your LLM-based demo idea", placeholder="Type your demo idea here", height=100
)

empty_title = st.empty()
demo_title = empty_title.text_input(
    "Give a name for your application", placeholder="Title"
)


def progressBar(percentage, bar=None):
    if bar:
        bar.progress(percentage)
    else:
        return st.progress(percentage)


if "pid" not in st.session_state:
    st.session_state["pid"] = -1

if "done" not in st.session_state:
    st.session_state["done"] = False

with st.form("a", clear_on_submit=True):
    submitted = st.form_submit_button("Submit")


def kill():
    if st.session_state["pid"] != -1:
        logging.info(f"Terminating the previous applicaton ...")
        try:
            os.kill(st.session_state["pid"], signal.SIGTERM)
        except Exception as e:
            pass
        st.session_state["pid"] = -1


if submitted:
    st.session_state.messages = []
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key!", icon="⚠️")
    else:
        bar = progressBar(0)
        st.session_state.container = st.container()
        agent = DemoGPT(openai_api_key=openai_api_key, openai_api_base=openai_api_base)  # using openai_api_key variable
        agent.setModel(model_name)
        kill()
        code_empty = st.empty()
        st.session_state.container = st.container()
        for data in generate_response(demo_idea, demo_title):
            done = data.get("done", False)
            message = data.get("message", "")
            st.session_state["message"] = message
            stage = data.get("stage", "stage")
            code = data.get("code", "")
            progressBar(data["percentage"], bar)

            st.session_state["done"] = True

            if done:
                st.session_state.code = code
                break

            st.info(message, icon="🧩")
            st.session_state.messages.append(message)

elif "messages" in st.session_state:
    for message in st.session_state.messages:
        st.info(message, icon="🧩")

if st.session_state.done:
    st.success(st.session_state.message)
    with st.expander("Code", expanded=True):
        code_empty = st.empty()
        if st.session_state.edit_mode:
            new_code = code_empty.text_area("", st.session_state.code, height=500)
            if st.button("Save & Rerun"):
                st.session_state.code = (
                    new_code  # Save the edited code to session state
                )
                st.session_state.edit_mode = False  # Exit edit mode
                code_empty.code(new_code)
                kill()
                st.session_state["pid"] = runStreamlit(
                    new_code, openai_api_key, openai_api_base
                )
                st.rerun()

        else:
            print("st.session_state.code:", st.session_state.code)
            code_empty.code(st.session_state.code)
            if st.button("Edit"):
                st.session_state.edit_mode = True  # Enter edit mode
                st.rerun()
    example_submitted = False
    if submitted:
        st.session_state["pid"] = runStreamlit(code, openai_api_key, openai_api_base)
