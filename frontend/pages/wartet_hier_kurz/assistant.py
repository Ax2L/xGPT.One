# pages/assistant.py


import streamlit as st
import os
import uuid
import pandas as pd
import openai
from requests.models import ChunkedEncodingError
from streamlit.components import v1
from components.assistant.voice_toolkit import voice_toolkit
from components.assistant.helper import *
import datetime

from components import xlayout
from streamlit_extras.switch_page_button import switch_page
from components import xdatastore_backup as XDatabase

# Set the page name; crucial for various functions
page_name = "assistant"
db = XDatabase()

if "current_page" not in st.session_state:
    st.session_state.current_page = page_name
    switch_page("main")

with open("components/utils/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    
# ⁡⁢⁣⁡⁣⁢⁡⁣⁢⁣===| PAGE NAVIGATION SECTION |================================⁡⁡⁡
# If the current page doesn't match and isn't None, switch to it
current_site = st.session_state['current_page']
if current_site != page_name and current_site is not None:
    switch_page(current_site)


current_site = st.session_state["current_page"]
if current_site != page_name and current_site is not None:
    switch_page(current_site)
    st.write("Current Page is not mine:" + current_site)
else:
    st.write(
        "You clicked on the current page:" + current_site + " your page is:" + page_name
    )

username = st.session_state["username"]

if "openai_key" not in st.session_state:
    st.session_state["openai_key"] = db.db_get_value(
        username, "session_data", "openai_key"
    )

st.session_state["history_chats"] = st.session_state.get("history_chats", [])
st.session_state["current_chat_index"] = st.session_state.get("current_chat_index", 0)
chat_index = st.session_state["current_chat_index"]

if "initial_settings" not in st.session_state:
    st.session_state.update({
        "path": "history_chats_file",
        "delete_dict": {},
        "delete_count": 0,
        "voice_flag": "",
        "user_voice_value": "",
        "error_info": "",
        "current_chat_index": 0,
        "user_input_content": ""
    })

    if os.path.exists("./set.json"):
        with open("./set.json", "r", encoding="utf-8") as f:
            data_set = json.load(f)
        for key, value in data_set.items():
            st.session_state[key] = value

    st.session_state["initial_settings"] = True

if not st.session_state.get("chat_database"):
    initial_chat_entry = {
        "chat_id": 1,
        "username": "admin",
        "start_time": str(datetime.datetime.now()),
        "end_time": None
    }
    xds.save_data(username, "chats", initial_chat_entry)
    
    initial_message_entry = {
        "message_id": 1,
        "chat_id": 1,
        "username": "admin",
        "content": "Initial message",
        "timestamp": str(datetime.datetime.now()),
        "sent_by": "system"
    }
    xds.save_data(username, "messages", initial_message_entry)

current_chat_id = st.session_state



with st.sidebar:
    chat_container = st.container()
    with chat_container:
        chat_index = st.session_state["current_chat_index"]
        if chat_index < 0 or chat_index >= len(st.session_state["history_chats"]):
            chat_index = 0

        if len(st.session_state["history_chats"]) > 0:
            current_chat = st.radio(
                label="Historical chat window",
                format_func=lambda x: x.split("_")[0] if "_" in x else x,
                options=st.session_state["history_chats"],
                label_visibility="collapsed",
                index=chat_index,
                key="current_chat" + st.session_state["history_chats"][chat_index],
            )
        else:
            st.write("No chat history available.")
            current_chat = None

    st.write("---")


# Write data to file
def write_data(new_chat_name=current_chat):
    if "apikey" in st.secrets:
        st.session_state["paras"] = {
            "temperature": st.session_state["temperature" + current_chat],
            "top_p": st.session_state["top_p" + current_chat],
            "presence_penalty": st.session_state["presence_penalty" + current_chat],
            "frequency_penalty": st.session_state["frequency_penalty" + current_chat],
        }
        st.session_state["contexts"] = {
            "context_select": st.session_state["context_select" + current_chat],
            "context_input": st.session_state["context_input" + current_chat],
            "context_level": st.session_state["context_level" + current_chat],
        }
        xds.save_data(
            st.session_state["path"],
            new_chat_name,
            st.session_state["history" + current_chat],
            st.session_state["paras"],
            st.session_state["contexts"],
        )

# Update in the database
def reset_chat_name_fun(chat_name):
    chat_uuid = str(uuid.uuid4())
    new_chat_name = chat_name + "_" + chat_uuid

    if current_chat in st.session_state["history_chats"]:
        current_chat_index = st.session_state["history_chats"].index(current_chat)
    else:
        current_chat_index = len(st.session_state["history_chats"])

    if current_chat_index < len(st.session_state["history_chats"]):
        st.session_state["history_chats"][current_chat_index] = new_chat_name
    else:
        st.session_state["history_chats"].append(new_chat_name)

    st.session_state["current_chat_index"] = current_chat_index

    # Update in the database
    db.db_set_value(
        username, "chats", "chat_name", new_chat_name
    )

    # Transfer session state data
    if current_chat:
        st.session_state["history" + new_chat_name] = st.session_state.get(
            "history" + current_chat, ""
        )
    else:
        st.session_state["history" + new_chat_name] = ""

    for item in [
        "context_select",
        "context_input",
        "context_level",
        *initial_content_all["paras"],
    ]:
        st.session_state[item + chat_name + "value"] = st.session_state.get(
            item + (current_chat if current_chat else "") + "value", ""
        )

    # Remove old chat entry from the database
    delete_query = f"DELETE FROM chats WHERE chat_name = %s"
    with xds.init_connection() as conn:
        xds.run_query(conn, delete_query, (new_chat_name,), return_type="none")


if (
    "set_chat_name" in st.session_state
    and st.session_state["set_chat_name"] is not None
):
    reset_chat_name_fun(chat_name=st.session_state["set_chat_name"])


# Add to the database
def create_chat_fun(username):
    chat_uuid = str(uuid.uuid4())
    chat_name = "New Chat_" + chat_uuid

    st.session_state["history_chats"].insert(0, chat_name)
    st.session_state["current_chat_index"] = 0

    # Add to the database
    insert_query = f"INSERT INTO chats (username, chat_name) VALUES (%s, %s)"
    with xds.init_connection() as conn:
        xds.run_query(conn, insert_query, (username, chat_name), return_type="none")


# Function to delete a chat
def delete_chat_fun(username):
    if len(st.session_state["history_chats"]) == 1:
        chat_uuid = str(uuid.uuid4())
        chat_name = "New Chat_" + chat_uuid
        st.session_state["history_chats"].append(chat_name)

    # Remove from session state
    st.session_state["history_chats"].remove(current_chat)

    # Remove from database
    delete_query = f"DELETE FROM chats WHERE chat_name = %s AND username = %s"
    with xds.init_connection() as conn:
        xds.run_query(conn, delete_query, (current_chat, username), return_type="none")



# Sidebar section
with st.sidebar:
    c1, c2 = st.columns(2)
    create_chat_button = c1.button(
        "New", use_container_width=True, key="create_chat_button"
    )
    if create_chat_button:
        create_chat_fun(st.session_state["username"])
        st.rerun()

    delete_chat_button = c2.button(
        "Delete", use_container_width=True, key="delete_chat_button"
    )
    if delete_chat_button:
        delete_chat_fun()
        st.rerun()

# Sidebar section continued
with st.sidebar:
    if ("set_chat_name" in st.session_state) and st.session_state[
        "set_chat_name"
    ] != "":
        reset_chat_name_fun(chat_name=st.session_state["set_chat_name"])
        st.session_state["set_chat_name"] = ""
        st.rerun()

    st.write("\n")
    st.write("\n")
    st.text_input("Set Chat Name:", key="set_chat_name", placeholder="Click to enter")
    st.selectbox(
        "Select Model:", index=0, options=["gpt-3.5-turbo", "gpt-4"], key="select_model"
    )
    st.write("\n")
    st.caption(
        """
    - Double-click on the page to focus the input box.
    - Ctrl + Enter for quick question submission.
    """
    )

# Load data
if current_chat:
    data = xds.load_data(st.session_state["path"], current_chat)
    if data:
        for key, value in data.items():
            if key == "history":
                st.session_state[key + current_chat] = value
            else:
                for k, v in value.items():
                    st.session_state[k + current_chat + "value"] = st.session_state.get(
                        k + current_chat + "value", v
                    )

    # Ensure the page layout is consistent across different chats, otherwise it will trigger the re-rendering of custom components
    container_show_messages = st.container()
    container_show_messages.write("")
    # Display chat history
    if st.session_state.get("history" + current_chat):
        display_message(current_chat, st.session_state["history" + current_chat])

# Check if there are chats that need to be deleted
if any(st.session_state["delete_dict"].values()):
    for key, value in st.session_state["delete_dict"].items():
        try:
            deleteCount = value.get("deleteCount")
        except AttributeError:
            deleteCount = None
        if deleteCount == st.session_state["delete_count"]:
            delete_keys = key
            st.session_state["delete_count"] = deleteCount + 1
            delete_current_chat, idr = delete_keys.split(">")
            df_history_tem = pd.DataFrame(
                st.session_state["history" + delete_current_chat]
            )
            df_history_tem.drop(
                index=df_history_tem.query("role=='user'").iloc[[int(idr)], :].index,
                inplace=True,
            )
            df_history_tem.drop(
                index=df_history_tem.query("role=='assistant'")
                .iloc[[int(idr)], :]
                .index,
                inplace=True,
            )
            st.session_state["history" + delete_current_chat] = df_history_tem.to_dict(
                "records"
            )
            write_data()
            st.rerun()

if not current_chat:
    current_chat = ""

history_to_check = "history" + current_chat
if history_to_check not in st.session_state:
    st.session_state[history_to_check] = 0


def callback_fun(arg):
    # To prevent errors triggered by fast and consecutive clicks on "New" and "Delete", additional checks are added
    if ("history" + current_chat in st.session_state) and (
        "frequency_penalty" + current_chat in st.session_state
    ):
        write_data()
        st.session_state[arg + current_chat + "value"] = st.session_state[
            arg + current_chat
        ]


def clear_button_callback():
    st.session_state["history" + current_chat] = []
    write_data()


def save_set(arg):
    st.session_state[arg + "_value"] = st.session_state[arg]
    if "apikey" in st.secrets:
        with open("./set.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "open_text_toolkit_value": st.session_state["open_text_toolkit"],
                    "open_voice_toolkit_value": st.session_state["open_voice_toolkit"],
                },
                f,
            )


# Display input area for user
area_user_svg = st.empty()
area_user_content = st.empty()
# Display area for assistant's response
area_gpt_svg = st.empty()
area_gpt_content = st.empty()
# Display area for errors
area_error = st.empty()

st.write("\n")
st.header("ChatGPT Assistant")
tap_input, tap_context, tap_model, tab_func = st.tabs(
    ["💬 Chat", "🗒️ Presets", "⚙️ Model", "🛠️ Functions"]
)


with tap_context:
    set_context_list = list(set_context_all.keys())

    # Safely get the index; if the value isn't found, default to 0 (or another default index)
    context_select_index = (
        set_context_list.index(st.session_state.get("value", ""))
        if st.session_state.get("value", "") in set_context_list
        else 0
    )

    st.selectbox(
        label="Select Context",
        options=set_context_list,
        key="context_select" + current_chat,
        index=context_select_index,
        on_change=callback_fun,
        args=("context_select",),
    )
    st.caption(set_context_all[st.session_state["context_select" + current_chat]])
    # Safely get the key value before using it
    key_to_check = "context_input" + current_chat + "value"
    if key_to_check not in st.session_state:
        st.session_state.setdefault(key_to_check, "")
    context_input_value = st.session_state.get(key_to_check, "") 
    st.text_area(
        label="Supplement or Customize Context:",
        key="context_input" + current_chat,
        value=context_input_value,  # Use the safely retrieved value here
        on_change=callback_fun,
        args=("context_input",),
    )



default_values = {
    "context_level": 0,
    "temperature": 1.0,
    "top_p": 0.5,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
}

for param in default_values:
    if param + current_chat + "value" not in st.session_state:
        st.session_state[param + current_chat + "value"] = default_values[param]

with tap_model:
    st.markdown("OpenAI API Key (Optional)")
    st.text_input(
        "Your OpenAI API Key", value=db.db_get_value(username, "session_data", "openai_key"), type="password"
    )
    st.caption(
        "This key is only valid on the current webpage and takes precedence over the configurations in Secrets. It is for your own use only and cannot be shared with others. [Obtain from official website](https://platform.openai.com/account/api-keys)"
    )

    st.markdown("Number of Conversations to Include:")
    st.slider(
        "Context Level",
        0,
        10,
        1, #st.session_state["context_level" + current_chat + "value"],
        1,
        on_change=callback_fun,
        key="context_level" + current_chat,
        args=("context_level",),
        help="Indicates the number of historical conversations to include in each session, preset content not counted.",
    )

    st.markdown("Model Parameters:")
    st.slider(
        "Temperature",
        0.0,
        2.0,
        st.session_state["temperature" + current_chat + "value"],
        0.1,
        help="""What sampling temperature between 0 and 2 should be used? Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) make it more focused and deterministic.
            We generally recommend changing either this parameter or the top_p parameter, but not both at the same time.""",
        on_change=callback_fun,
        key="temperature" + current_chat,
        args=("temperature",),
    )
    st.slider(
        "Top P",
        0.1,
        1.0,
        st.session_state["top_p" + current_chat + "value"],
        0.1,
        help="""An alternative to sampling with temperature is called 'nucleus sampling'. In this method, the model considers the predictions of the top_p most probable tokens.
            So when this parameter is 0.1, only tokens that include the top 10% probability mass will be considered. We generally recommend changing either this parameter or the temperature parameter, but not both at the same time.""",
        on_change=callback_fun,
        key="top_p" + current_chat,
        args=("top_p",),
    )

    st.slider(
        "Presence Penalty",
        -2.0,
        2.0,
        st.session_state["presence_penalty" + current_chat + "value"],
        0.1,
        help="""This parameter ranges from -2.0 to 2.0. Positive values penalize new tokens based on whether they appear in the current generated text, thus increasing the likelihood of the model discussing new topics.""",
        on_change=callback_fun,
        key="presence_penalty" + current_chat,
        args=("presence_penalty",),
    )

    st.slider(
        "Frequency Penalty",
        -2.0,
        2.0,
        st.session_state["frequency_penalty" + current_chat + "value"],
        0.1,
        help="""This parameter ranges from -2.0 to 2.0. Positive values penalize new tokens based on their existing frequency in the currently generated text, thus reducing the likelihood of the model directly repeating the same sentences.""",
        on_change=callback_fun,
        key="frequency_penalty" + current_chat,
        args=("frequency_penalty",),
    )

    st.caption(
        "[Official Parameter Description](https://platform.openai.com/docs/api-reference/completions/create)"
    )

with tab_func:
    c1, c2 = st.columns(2)
    with c1:
        st.button(
            "Clear Chat History",
            use_container_width=True,
            on_click=clear_button_callback,
        )
    
    history_data = st.session_state.get("history" + current_chat, [])
    if isinstance(history_data, list):
        data = download_chat_history(history_data)
    else:
        st.error(f"Expected a list but got {type(history_data)} for history data.")
        data = None  # Set a default None value or an empty string so the download button doesn't throw an error
    
    with c2:
        if data:  # This ensures the download button is functional only if data is not None
            btn = st.download_button(
                label="Export Chat History",
                data=data,
                file_name=f'{current_chat.split("_")[0]}.md',
                mime="text/markdown",
                use_container_width=True,
            )
    
    st.write("\n")
    st.markdown("Custom Features:")
    c1, c2 = st.columns(2)
    with c1:
        if "open_text_toolkit_value" in st.session_state:
            default = st.session_state["open_text_toolkit_value"]
        else:
            default = True
        st.checkbox(
            "Enable Text Toolkit Below",
            value=default,
            key="open_text_toolkit",
            on_change=save_set,
            args=("open_text_toolkit",),
        )

    with c2:
        if "open_voice_toolkit_value" in st.session_state:
            default = st.session_state["open_voice_toolkit_value"]
        else:
            default = True
        st.checkbox(
            "Enable Voice Input Toolkit",
            value=default,
            key="open_voice_toolkit",
            on_change=save_set,
            args=("open_voice_toolkit",),
        )


# Create a Streamlit form to input text or use voice recognition
with tap_input:
    # Callback function triggered when the form is submitted
    def input_callback():
        if st.session_state["user_input_area"] != "":
            # Change the window name
            user_input_content = st.session_state["user_input_area"]
            data = st.session_state.get("history" + current_chat)
            print(type(data), data)
            if data and isinstance(data, list) and all(isinstance(item, dict) for item in data):
                df_history = pd.DataFrame(data)
            else:
                st.error("Invalid data format!")
            df_history = pd.DataFrame(data)
            if df_history.empty or len(df_history.query('role!="system"')) == 0:
                new_name = extract_characters(user_input_content, 18)
                reset_chat_name_fun(new_name)

    # Create a form
    with st.form("input_form", clear_on_submit=True):
        user_input = st.text_area(
            "**Input:**",
            key="user_input_area",
            help="The content will be displayed in Markdown format on the page. It's recommended to follow the related language specification, which also helps GPT to read it correctly. For example:"
            "\n- Code blocks should be written within three backticks, and the language type should be indicated."
            "\n- Content that starts with an English colon or regular expressions, etc., should be written in a single backtick.",
            value=st.session_state["user_voice_value"],
        )
        submitted = st.form_submit_button(
            "Confirm Submission", use_container_width=True, on_click=input_callback
        )
    if submitted:
        st.session_state["user_input_content"] = user_input
        st.session_state["user_voice_value"] = ""
        st.rerun()

    # Voice input feature
    if (
        "open_voice_toolkit_value" not in st.session_state
        or st.session_state["open_voice_toolkit_value"]
    ):
        voice_result = voice_toolkit()
        # voice_result will store the last result
        if (
            voice_result and voice_result["voice_result"]["flag"] == "interim"
        ) or st.session_state["voice_flag"] == "interim":
            st.session_state["voice_flag"] = "interim"
            st.session_state["user_voice_value"] = voice_result["voice_result"]["value"]
            if voice_result["voice_result"]["flag"] == "final":
                st.session_state["voice_flag"] = "final"
                st.rerun()


# Function to get model input
def get_model_input():
    context_level = st.session_state["context_level" + current_chat]
    history = get_history_input(
        st.session_state["history" + current_chat], context_level
    ) + [{"role": "user", "content": st.session_state["pre_user_input_content"]}]
    for ctx in [
        st.session_state["context_input" + current_chat],
        set_context_all[st.session_state["context_select" + current_chat]],
    ]:
        if ctx != "":
            history = [{"role": "system", "content": ctx}] + history
    # Model parameters
    paras = {
        "temperature": st.session_state["temperature" + current_chat],
        "top_p": st.session_state["top_p" + current_chat],
        "presence_penalty": st.session_state["presence_penalty" + current_chat],
        "frequency_penalty": st.session_state["frequency_penalty" + current_chat],
    }
    return history, paras


# Check if the user has provided some input
if st.session_state["user_input_content"] != "":
    # Remove any existing API response from session state
    if "r" in st.session_state:
        st.session_state.pop("r")
        st.session_state[current_chat + "report"] = ""

    # Store the user's input for future reference
    st.session_state["pre_user_input_content"] = st.session_state["user_input_content"]
    st.session_state["user_input_content"] = ""

    # Temporarily display the user's message
    display_all_messages(
        st.session_state["pre_user_input_content"],
        "user",
        "tem",
        [area_user_svg.markdown, area_user_content.markdown],
    )

    # Prepare the model input
    history_need_input, paras_need_input = get_model_input()

    # Make an API call
    with st.spinner("🤔"):
        try:
            # Set OpenAI API key based on session state or secrets
            if "openai_key" in st.session_state:
                openai.api_key = st.session_state["openai_key"]
            elif "apikey_tem" in st.secrets:
                openai.api_key = st.secrets["apikey_tem"]
            else:
                openai.api_key = st.secrets["apikey"]

            # Make the API request
            r = openai.ChatCompletion.create(
                model=st.session_state["select_model"],
                messages=history_need_input,
                stream=True,
                **paras_need_input,
            )
        except (FileNotFoundError, KeyError):
            area_error.error(
                "Missing OpenAI API Key. Please configure the Secrets after copying the project, or temporarily configure it in the model options. See [Project Repository](https://github.com/PierXuY/ChatGPT-Assistant)."
            )
        except openai.error.AuthenticationError:
            area_error.error("Invalid OpenAI API Key.")
        except openai.error.APIConnectionError as e:
            area_error.error(
                f"Connection timeout, please retry. Error: {str(e.args[0])}"
            )
        except openai.error.InvalidRequestError as e:
            area_error.error(f"Invalid request, please retry. Error: {str(e.args[0])}")
        except openai.error.RateLimitError as e:
            area_error.error(f"Rate limit exceeded. Error: {str(e.args[0])}")
        else:
            st.session_state["chat_of_r"] = current_chat
            st.session_state["r"] = r
            st.rerun()

# Check if there's an API response and it corresponds to the current chat
if ("r" in st.session_state) and (current_chat == st.session_state["chat_of_r"]):
    if current_chat + "report" not in st.session_state:
        st.session_state[current_chat + "report"] = ""

    try:
        for e in st.session_state["r"]:
            if "content" in e["choices"][0]["delta"]:
                st.session_state[current_chat + "report"] += e["choices"][0]["delta"][
                    "content"
                ]
                display_all_messages(
                    st.session_state["pre_user_input_content"],
                    "user",
                    "tem",
                    [area_user_svg.markdown, area_user_content.markdown],
                )
                display_all_messages(
                    st.session_state[current_chat + "report"],
                    "assistant",
                    "tem",
                    [area_gpt_svg.markdown, area_gpt_content.markdown],
                )
    except ChunkedEncodingError:
        area_error.error(
            "Poor network conditions, please refresh the page to try again."
        )
    except Exception:
        pass
    else:
        # Save the conversation history
        st.session_state["history" + current_chat].append(
            {"role": "user", "content": st.session_state["pre_user_input_content"]}
        )
        st.session_state["history" + current_chat].append(
            {"role": "assistant", "content": st.session_state[current_chat + "report"]}
        )
        # With this
        try:
            write_data()
        except Exception as e:
            area_error.error(f"Database error: {str(e)}")

    # Handle corner cases when the user clicks 'stop' on the web page
    if current_chat + "report" in st.session_state:
        st.session_state.pop(current_chat + "report")
    if "r" in st.session_state:
        st.session_state.pop("r")
        st.rerun()



# Add event listener
v1.html(js_code, height=0)
