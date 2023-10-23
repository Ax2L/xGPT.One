# pages/assistant.py
from components.assistant.helper import *
import hydralit_components as hc
import streamlit as st
import uuid
import pandas as pd
import openai
from requests.models import ChunkedEncodingError
from streamlit.components import v1
from components.assistant.voice_toolkit import voice_toolkit
from components.default import *
from components import default
from PIL import Image

# Load Config
logo = Image.open('images/logo/logo_long.png')

#? ||--------------------------------------------------------------------------------||
#? ||                                  xGPT.Setup                                    ||
#? ||--------------------------------------------------------------------------------||


# Initialize session_state if it doesn't exist
if "authenticator" or "username" or "dev_mode" not in st.session_state:
    #switch_page('main')


# Specific config for this page only:
page_name = "assistant"
page_navi_number = 10

# Install styles, and loader then create Navbar
setup()
setup_navbar(page_navi_number,page_name)

#// endregion

# // region [ rgba(50, 100, 150, 0.05)] Navigation Data and Theme
#? ||++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++||
#? ||                                    # Initiate                                  ||
#? ||++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++||

# Initialize session_state if it doesn't exist
if "openai_key" not in st.session_state:
    st.session_state["openai_key"] = "OpenAI_Key"

try:
    st.session_state["openai_key"] = db_get_value(st.session_state["username"], 'key_openai')
except Exception as e:
    pass
# Custom element style
st.markdown(css_code, unsafe_allow_html=True)

if "initial_settings" not in st.session_state:
    # Historical chat window
    st.session_state["path"] = "history_chats_file"
    st.session_state["history_chats"] = get_history_chats(st.session_state["path"])
    # Initialize ss parameters
    st.session_state["delete_dict"] = {}
    st.session_state["delete_count"] = 0
    st.session_state["voice_flag"] = ""
    st.session_state["user_voice_value"] = ""
    st.session_state["error_info"] = ""
    st.session_state["current_chat_index"] = 0
    st.session_state["user_input_content"] = ""
    # Read global settings
    if os.path.exists("./set.json"):
        with open("./set.json", "r", encoding="utf-8") as f:
            data_set = json.load(f)
        for key, value in data_set.items():
            st.session_state[key] = value
    # Settings complete
    from components.utils.styles import apply_styles
    apply_styles()
    st.session_state["initial_settings"] = True
#// endregion

#// region [ rgba(250, 15, 100, 0.05)] Sidebar Initialization
#? ||--------------------------------------------------------------------------------||
#? ||                                    # Sidebar                                   ||
#? ||--------------------------------------------------------------------------------||
with st.sidebar:
    st.markdown("# 🤖 Chat Window")
    # The purpose of creating a container is to cooperate with the listening operation of custom components
    chat_container = st.container()
    with chat_container:
        current_chat = st.radio(
            label="Historical chat window",
            format_func=lambda x: x.split("_")[0] if "_" in x else x,
            options=st.session_state["history_chats"],
            label_visibility="collapsed",
            index=st.session_state["current_chat_index"],
            key="current_chat"
            + st.session_state["history_chats"][st.session_state["current_chat_index"]],
        )
    st.write("---")
#// endregion
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
        save_data(
            st.session_state["path"],
            new_chat_name,
            st.session_state["history" + current_chat],
            st.session_state["paras"],
            st.session_state["contexts"],
        )


# Function to reset the chat name
def reset_chat_name_fun(chat_name):
    chat_name = chat_name + "_" + str(uuid.uuid4())
    new_name = filename_correction(chat_name)
    current_chat_index = st.session_state["history_chats"].index(current_chat)
    st.session_state["history_chats"][current_chat_index] = new_name
    st.session_state["current_chat_index"] = current_chat_index
    # Write to a new file
    write_data(new_name)
    # Transfer data
    st.session_state["history" + new_name] = st.session_state["history" + current_chat]
    for item in [
        "context_select",
        "context_input",
        "context_level",
        *initial_content_all["paras"],
    ]:
        st.session_state[item + new_name + "value"] = st.session_state[
            item + current_chat + "value"
        ]
    remove_data(st.session_state["path"], current_chat)

#// endregion 

# Function to create a new chat
def create_chat_fun():
    st.session_state["history_chats"] = [
        "New Chat_" + str(uuid.uuid4())
    ] + st.session_state["history_chats"]
    st.session_state["current_chat_index"] = 0


# Function to delete a chat
def delete_chat_fun():
    if len(st.session_state["history_chats"]) == 1:
        chat_init = "New Chat_" + str(uuid.uuid4())
        st.session_state["history_chats"].append(chat_init)
    pre_chat_index = st.session_state["history_chats"].index(current_chat)
    if pre_chat_index > 0:
        st.session_state["current_chat_index"] = (
            st.session_state["history_chats"].index(current_chat) - 1
        )
    else:
        st.session_state["current_chat_index"] = 0
    st.session_state["history_chats"].remove(current_chat)
    remove_data(st.session_state["path"], current_chat)


# Sidebar section
with st.sidebar:
    c1, c2 = st.columns(2)
    create_chat_button = c1.button(
        "New", use_container_width=True, key="create_chat_button"
    )
    if create_chat_button:
        create_chat_fun()
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
        reset_chat_name_fun(st.session_state["set_chat_name"])
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
    st.markdown(
        '<a href="https://github.com/PierXuY/ChatGPT-Assistant" target="_blank" rel="ChatGPT-Assistant">'
        '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=ChatGPT Assistant" alt="GitHub">'
        "</a>",
        unsafe_allow_html=True,
    )

# TODO PART
# Load data
if "history" + current_chat not in st.session_state:
    for key, value in load_data(st.session_state["path"], current_chat).items():
        if key == "history":
            st.session_state[key + current_chat] = value
        else:
            for k, v in value.items():
                st.session_state[k + current_chat + "value"] = v

# Ensure the page layout is consistent across different chats, otherwise it will trigger the re-rendering of custom components
container_show_messages = st.container()
container_show_messages.write("")
# Display chat history
with container_show_messages:
    if st.session_state["history" + current_chat]:
        show_messages(current_chat, st.session_state["history" + current_chat])

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
    context_select_index = set_context_list.index(
        st.session_state["context_select" + current_chat + "value"]
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

    st.text_area(
        label="Supplement or Customize Context:",
        key="context_input" + current_chat,
        value=st.session_state["context_input" + current_chat + "value"],
        on_change=callback_fun,
        args=("context_input",),
    )

with tap_model:
    st.markdown("OpenAI API Key (Optional)")
    st.text_input("Your OpenAI API Key", value=st.session_state.openai_key, type="password")  # Display the current key from session state
    st.caption(
        "This key is only valid on the current webpage and takes precedence over the configurations in Secrets. It is for your own use only and cannot be shared with others. [Obtain from official website](https://platform.openai.com/account/api-keys)"
    )

    st.markdown("Number of Conversations to Include:")
    st.slider(
        "Context Level",
        0,
        10,
        st.session_state["context_level" + current_chat + "value"],
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
    with c2:
        btn = st.download_button(
            label="Export Chat History",
            data=download_history(st.session_state["history" + current_chat]),
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

# TODO PART 3
# Create a Streamlit form to input text or use voice recognition
with tap_input:
    # Callback function triggered when the form is submitted
    def input_callback():
        if st.session_state["user_input_area"] != "":
            # Change the window name
            user_input_content = st.session_state["user_input_area"]
            df_history = pd.DataFrame(st.session_state["history" + current_chat])
            if df_history.empty or len(df_history.query('role!="system"')) == 0:
                new_name = extract_chars(user_input_content, 18)
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
    show_each_message(
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
            if apikey := st.session_state.get("openai_key", None):  # Use the 'openai_key' from the session state
                openai.api_key = apikey
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
                show_each_message(
                    st.session_state["pre_user_input_content"],
                    "user",
                    "tem",
                    [area_user_svg.markdown, area_user_content.markdown],
                )
                show_each_message(
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
        write_data()

    # Handle corner cases when the user clicks 'stop' on the web page
    if current_chat + "report" in st.session_state:
        st.session_state.pop(current_chat + "report")
    if "r" in st.session_state:
        st.session_state.pop("r")
        st.rerun()

# Add event listener
v1.html(js_code, height=0)
