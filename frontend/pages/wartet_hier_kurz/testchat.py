import os
import weaviate
import openai
from pydantic import BaseModel
import streamlit as st

DEFAULT_ASSISTANT_PROMPT = "How can I help you?"
GENERATE_PROMPT = "Act as an experienced and helpful Python and developer, please suggest code from the following response or content: {content}"

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
page_name = "testchat"
page_navi_number = 81
page_navi_category = "tests"

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


class Document(BaseModel):
    content: str

class QueryResult(BaseModel):
    document: Document

class ChatApp:

    def __init__(self):
        self.client = None
        self.get_env_variables()
        self.client = self.get_client()

    def get_env_variable(self, var_name):
        var_value = os.getenv(var_name)
        return var_value

    def get_env_variables(self):
        with st.sidebar:
            self.OPENAI_API_KEY = self.get_env_variable("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")
            self.WEAVIATE_HOST = self.get_env_variable("WEAVIATE_HOST") or st.text_input("Weaviate Host")

        if not self.OPENAI_API_KEY or not self.WEAVIATE_HOST:
            st.info("Please add your OpenAI API Key and Weaviate Host to continue.")
            st.stop()

        openai.api_key = self.OPENAI_API_KEY

    def get_client(self):
        try:
            client = weaviate.Client(
                url=self.WEAVIATE_HOST,
                additional_headers={"X-OpenAI-Api-Key": self.OPENAI_API_KEY},
            )
        except Exception as e:
            st.error(f"Error occurred while creating the Weaviate client: {str(e)}")
            st.stop()

        return client

    def client_query(self, question: str):
        generatePrompt = GENERATE_PROMPT
        nearText = {"concepts": [f"{question}"]}

        with st.spinner("Waiting for the response..."):
            try:
                response = (
                    self.client.query
                    .get("Document", ["content"])
                    .with_generate(single_prompt=generatePrompt)
                    .with_near_text(nearText)
                    .with_limit(3)
                    .do()
                )
            except Exception as e:
                st.error(f"Error occurred while querying the Weaviate client: {str(e)}")
                st.stop()

        return response

    def main(self):
        if "messages" not in st.session_state.keys():
            st.session_state["messages"] = []

        st.chat_message("assistant").write(DEFAULT_ASSISTANT_PROMPT)

        if prompt := st.chat_input("Your prompt:"):
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = self.client_query(prompt)

            if response:
                try:
                    for document in response['data']['Get']['Document']:
                        try:
                            generativeOpenAI = document['_additional']['generate']["singleResult"]
                            content = document['content']
                        except KeyError as ke:
                            st.markdown(f"Error: Expected keys not found in the document. {ke}")
                            continue

                        if content:
                            st.session_state.messages.append({"role": "help", "content": "Semantic Search Response:"})
                            st.session_state.messages.append({"role": "assistant", "content": content})

                        if generativeOpenAI:
                            st.session_state.messages.append({"role": "help", "content": "Generative Open AI Response:"})
                            st.session_state.messages.append({"role": "assistant", "content": generativeOpenAI})

                except KeyError as ke:
                    st.markdown(f"Error: Expected keys not found in the response. {ke}")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

if __name__ == "__main__":
    ChatApp().main()
