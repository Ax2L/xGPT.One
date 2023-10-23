# 🤖 ChatGPT-Assistant

A ChatGPT assistant built on Streamlit, easy to use, stable connection, supporting the following features:
- Multiple chat windows
- Preservation of chat history
- Predefined chat contexts
- Model parameter adjustment
- Export of conversations to Markdown files
- ChatGPT voice interaction (Recommended for desktop users with the Edge browser)

## 🤩 [Deployed Project](https://pearxuy-gpt.streamlit.app/)
- Use the deployed project directly. You can configure the OpenAI key in the web settings. No chat history will be saved and will only be available for the current session.
- Deploy the project yourself, configure the OpenAI key in Secrets to keep the chat history. Make it a private application to serve as your personal GPT assistant.

### Tips for use:
- Double-clicking on the page will take you directly to the input bar.
- Ctrl + Enter for quick question submission.

# Deployment

## Streamlit Cloud Deployment (Recommended)
Easy and free to deploy. No VPN needed. Make sure to set it as a private application.
Follow the [detailed steps](https://github.com/PierXuY/ChatGPT-Assistant/blob/main/Tutorial.md) provided by [@Hannah11111](https://github.com/Hannah11111).
1. `Fork` this project into your personal Github repository.
2. Register a [Streamlit Cloud account](https://share.streamlit.io/) and connect it to Github.
3. Start the deployment, details can be found in the [official tutorial](https://docs.streamlit.io/streamlit-community-cloud/get-started).
4. Configure the OpenAI key in the application Secrets. The format is shown in the images below:

(Images omitted)

You can also configure this after deployment.

## Local Deployment
VPN needed for local deployment.
1. Create a virtual environment (recommended)
  
2. Clone the project (or download it manually)
  ```bash
  git clone https://github.com/PierXuY/ChatGPT-Assistant.git
  ```

3. Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
  
4. Set the API key
  - Write `apikey = "Your Openai Key"` in the `.streamlit/secrets.toml` file.
  
5. Launch the application
  ```bash
  streamlit run app.py
  ```

# Notes
- Customize the username and SVG avatar in the [custom.py](https://github.com/PierXuY/ChatGPT-Assistant/blob/main/custom.py) file.
- Edit the [set_context.py](https://github.com/PierXuY/ChatGPT-Assistant/blob/main/set_context.py) to add predefined context options, which will automatically synchronize with the application.
- Consider modifying the file read/write logic in [helper.py](https://github.com/PierXuY/ChatGPT-Assistant/blob/main/helper.py) to use a cloud database, to prevent loss of chat history.

# Acknowledgments
- Originally based on the [shan-mx/ChatGPT_Streamlit](https://github.com/shan-mx/ChatGPT_Streamlit) project, thanks.
- Predefined [context functionality](https://github.com/PierXuY/ChatGPT-Assistant/blob/main/set_context.py) is inspired by [binary-husky/chatgpt_academic](https://github.com/binary-husky/chatgpt_academic) and [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts), thanks.
- Voice interaction features are inspired by [talk-to-chatgpt](https://github.com/C-Nedelcu/talk-to-chatgpt) and [Voice Control for ChatGPT](https://chrome.google.com/webstore/detail/voice-control-for-chatgpt/eollffkcakegifhacjnlnegohfdlidhn), thanks.
