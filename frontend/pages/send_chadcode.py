# ./frontend/pages/send_chat_code.py
# ! Do not modify this section below! >>>
import streamlit as st
from components.utils.init import xinit_page
from components.utils import xhelper

# ^ Constants
PAGE_NAME = "send_chadcode"
# * Initializing the page with required configurations
xinit_page.set_page_config(PAGE_NAME, "wide", "collapsed")

#! <<< Do not modify this section above!

# ? Local modules
from components import xheader
from components.utils.dashboard import DashConfig


# & Functions
def setup_page(page_name):
    """* Setup and initialize the page.
    * Args:
    *   page_name (str): Name of the current page.
    """
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)


def load_custom_css():
    """* Load custom CSS for the page if not already active."""
    if f"{PAGE_NAME}_css" not in st.session_state:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            st.session_state.setdefault("{PAGE_NAME}_css", True)
    else:
        print(f"css already active on {PAGE_NAME}")


# & Page Initialization Process
xheader.init(PAGE_NAME)

# * Setting up the page environment
setup_page(PAGE_NAME)

# ! Content Section


#! Content Area #################################

import streamlit as st
from components.utils.selenium.selenium_helper import (
    get_chrome_driver,
    find_matching_files,
    send_content,
    wait_for_acknowledgment,
    get_chrome_driver,
)


# Main Streamlit page
def main():
    st.title("Chat Automation Interface")

    st.sidebar.header("Configuration")
    directory = st.sidebar.text_input("Directory to search")
    indicators = st.sidebar.text_area("Indicators (comma-separated)")
    acknowledgment_word = st.sidebar.text_input("Acknowledgment Word")

    if st.sidebar.button("Start Session"):
        with st.spinner("Starting Chrome Driver..."):
            # Path to the chromedriver
            chromedriver_path = "./helper/selenium/chromedriver"
            driver = get_chrome_driver(chromedriver_path)
            driver.get("http://yourwebsite.com/chat")

    if st.sidebar.button("Start Sending"):
        if not directory or not indicators or not acknowledgment_word:
            st.sidebar.error("Please fill out all configuration fields.")
            return

        indicators_list = [x.strip() for x in indicators.split(",")]
        matched_files = find_matching_files(directory, indicators_list)
        if not matched_files:
            st.sidebar.warning("No matching files found.")
            return

        # Start the Selenium Chrome WebDriver
        chromedriver_path = "./helper/selenium/chromedriver"
        driver = get_chrome_driver(chromedriver_path)
        try:
            for i, file_path in enumerate(matched_files):
                send_content(driver, file_path)
                st.write(f"Sent content of {file_path}")
                wait_for_acknowledgment(driver, acknowledgment_word)
                st.progress((i + 1) / len(matched_files))
            st.success("All files have been sent and acknowledged.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Make sure to close the browser after the session
        driver.quit()
        st.success("Session ended.")


main()

# * Loading custom CSS at the end
load_custom_css()
