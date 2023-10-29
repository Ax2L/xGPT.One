import json
import os
import re
import uuid
import streamlit as st
import pandas as pd
import copy
import io
from components.assistant.set_context import set_context


# Username
user_name = 'User'
gpt_name = 'ChatGPT'
# Avatar (in SVG format) from https://www.dicebear.com/playground?style=identicon
user_svg = """
<svg></g></svg>
"""
gpt_svg = """
<svg></path></svg>
"""
# Content background
user_background_color = ''
gpt_background_color = 'rgba(225, 230, 235, 0.5)'
# Initial model settings
initial_content_all = {
    "history": [],
    "paras": {
        "temperature": 1.0,
        "top_p": 1.0,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
    },
    "contexts": {
        'context_select': 'not set',
        'context_input': '',
        'context_level': 4
    }
}
# Context
set_context_all = {"not set": ""}
set_context_all.update(set_context)

# Custom CSS and JS
css_code = """
    <style>
    </style>
"""

js_code = """
<script>
</script>
"""


def get_chat_history(path: str) -> list:
    if "openai_key" in st.session_state or "apikey" in st.secrets:  
        if not os.path.exists(path):
            os.makedirs(path)
        files = [f for f in os.listdir(f'./{path}') if f.endswith('.json')]
        files_with_time = [(f, os.stat(f'./{path}/' + f).st_ctime) for f in files]
        sorted_files = sorted(files_with_time, key=lambda x: x[1], reverse=True)
        chat_names = [os.path.splitext(f[0])[0] for f in sorted_files]
        if len(chat_names) == 0:
            chat_names.append('New_Chat_' + str(uuid.uuid4()))
    else:
        chat_names = ['New_Chat_' + str(uuid.uuid4())]
    return chat_names

def load_chat_data(path: str, file_name: str) -> dict:
    try:
        with open(f"./{path}/{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        content = copy.deepcopy(initial_content_all)
        if "openai_key" in st.session_state or "apikey" in st.secrets:  
            with open(f"./{path}/{file_name}.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(content))
        return content

def save_chat_data(path: str, file_name: str, history: list, parameters: dict, contexts: dict, **kwargs):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"./{path}/{file_name}.json", 'w', encoding='utf-8') as f:
        json.dump({"history": history, "parameters": parameters, "contexts": contexts, **kwargs}, f)

def delete_chat_data(path: str, chat_name: str):
    try:
        os.remove(f"./{path}/{chat_name}.json")
    except FileNotFoundError:
        pass
    try:
        st.session_state.pop('history' + chat_name)
        for item in ["context_select", "context_input", "context_level", *initial_content_all['parameters']]:
            st.session_state.pop(item + chat_name + "value")
    except KeyError:
        pass

def display_message(message: str, role: str, idr: str, area=None):
    if area is None:
        area = [st.markdown] * 2
    if role == 'user':
        icon = user_svg
        name = user_name
        background_color = user_background_color
        data_idr = idr + "_user"
        class_name = 'user'
    else:
        icon = gpt_svg
        name = gpt_name
        background_color = gpt_background_color
        data_idr = idr + "_assistant"
        class_name = 'assistant'
    message = correct_url(message)
    area[0](f"\n<div class='avatar'>{icon}<h2>{name}：</h2></div>", unsafe_allow_html=True)
    area[1](
        f"""<div class='content-div {class_name}' data-idr='{data_idr}' style='background-color: {background_color};'>\n\n{message}""",
        unsafe_allow_html=True)


def display_all_messages(current_chat: str, messages: list):
    id_role = 0
    id_assistant = 0
    for each in messages:
        if each["role"] == "user":
            idr = id_role
            id_role += 1
        elif each["role"] == "assistant":
            idr = id_assistant
            id_assistant += 1
        else:
            idr = False
        if idr is not False:
            display_message(each["content"], each["role"], str(idr))
            if "open_text_toolkit_value" not in st.session_state or st.session_state["open_text_toolkit_value"]:
                st.session_state['delete_dict'][current_chat + ">" + str(idr)] = text_toolkit(
                    data_idr=str(idr) + '_' + each["role"])
        if each["role"] == "assistant":
            st.write("---")


def extract_history_input(history: list, level: int) -> list:
    if level != 0 and history:
        df_input = pd.DataFrame(history).query('role!="system"')
        df_input = df_input[-level * 2:]
        res = df_input.to_dict('records')
    else:
        res = []
    return res

def extract_characters(text: str, num: int) -> str:
    char_num = 0
    chars = ''
    for char in text:
        if '\u4e00' <= char <= '\u9fff':  # Chinese characters
            char_num += 2
        else:
            char_num += 1
        chars += char
        if char_num >= num:
            break
    return chars

@st.cache_data(max_entries=20, show_spinner=False)
def download_chat_history(history: list):
    if not isinstance(history, list):
        st.error(f"Expected a list but received {type(history)} for chat history.")
        return  # Exit the function
    
    md_text = ""
    for entry in history:
        if entry["role"] == "user":
            md_text += f"**User**: {entry['content']}\n\n"
        elif entry["role"] == "assistant":
            md_text += f"**Assistant**: {entry['content']}\n\n"
    return md_text

def correct_url(message: str) -> str:
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    for url in urls:
        message = message.replace(url, f'<a href="{url}" target="_blank">{url}</a>')
    return message

def text_toolkit(data_idr: str):
    if st.button('Edit', key=f'edit_{data_idr}'):
        return 'edit', data_idr
    elif st.button('Delete', key=f'delete_{data_idr}'):
        return 'delete', data_idr
    return None

# Placeholder functions for SVGs
def user_svg():
    # Placeholder for user SVG
    return """<svg>...</svg>"""

def gpt_svg():
    # Placeholder for GPT SVG
    return """<svg>...</svg>"""

if __name__ == '__main__':
    # Placeholder for the main execution block
    pass