# styles.py

#// region [ rgba(50, 15, 100, 0.03)] Imports
import streamlit as st
from os import getenv
import time
#// endregion
#// region [ rgba(50, 15, 100, 0.03)] Imports


#// region [ rgba(250, 215, 100, 0.05)] Styles Setup


#? Placeholder between Logout and the other buttons.
sidebar_logout_placeholder_template =  """
                            button {
                                }
                            """


#? Container where the sidebar Menu buttons.
sidebar_menu_container_styles_template = """
                                    {   
                                    
                                    }
                                    """


#? Style for the buttons only, which in the sidebar. | Merge with Sidebar?
sidebar_button_styles_template = """
                            {


                            }
                            """

#? Logout button in sidebar style #TODO: Is it really needed? 
sidebar_logout_button_styles_template = """
                            nothing {

                            }
                            """


#!ToDo: Split the big block into smaller peaces, and add those as css object below the block.
#* Goal: We can then use less code to achive a clean and superfast design.
#? Frame for content below the Sidebar Menü. | Update carefully!
sidebar_settings_content_container_styles_template = """
                                                    {
                                                    }
                                                    """

logoutButton = """ {
                --tw-bg-colored: 0 10px 15px -3px var(--tw-shadow-color), 0 4px 6px -4px var(--tw-shadow-color);
                --tw-bg-color: #111827;
                --tw-bg: var(--tw-shadow-colored);
                }
                """


hiddenElement = """ {
                }
                """



sidebar_button_tools_template = """
                            {

                            }
                            """

#// endregion

#// region [ rgba(20, 15, 100, 0.05)] Page Settings and Basic Styles

# def apply_page_settings(title):
#     st.set_page_config(
#         page_title="xGPT.One",
#         page_icon="🧊",
#         layout="wide",
#         initial_sidebar_state="auto",
#         menu_items={
#             'Get Help': 'https://github.com/Ax2L/xGPT.One/help',
#             'Report a bug': "https://github.com/Ax2L/xGPT.One/bug",
#             'About': "# Unveil the Universe of AI: Your Own AI-Driven Sidekick at Your Fingertips!"
#         }
#     )


def apply_styles():
    with open('components/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#// endregion



# HTML string
Loader_green_yellow_data = """
<div class="loader">
    <div class="face">
        <div class="circle"></div>
    </div>
    <div class="face">
        <div class="circle"></div>
    </div>
</div>
"""

loading_line_data = """
<span class="loader"></span>
"""

# Function to show loader with custom speed
def Loader_green_yellow():
    return st.markdown(Loader_green_yellow_data, unsafe_allow_html=True)


# Function to show loader with custom speed
def loading_line():
    return st.markdown(loading_line_data, unsafe_allow_html=True)

# Function to show loader with custom speed
def show_loader(spinner_name=loading_line_data):
    return spinner_name


def spinner_custom_line(height, width_percent, duration):
    # Function to get CSS with dynamic values
    def get_css(height, width, duration):
        return f"""
        <style>
            .loader {{
                width: {width};
                height: {height}px;
                display: inline-block;
                position: relative;
                background: rgba(255, 255, 255, 0.15);
                overflow: hidden;
            }}
            .loader::after {{
                content: '';
                width: {width};
                height: {height}px;
                background: #FFF;
                position: absolute;
                top: 0;
                left: 0;
                box-sizing: border-box;
                animation: animloader {duration}s linear infinite;
            }}

            @keyframes animloader {{
                0% {{
                    left: 0;
                    transform: translateX(-100%);
                }}
                100% {{
                    left: 100%;
                    transform: translateX(0%);
                }}
            }}
        </style>
        """

    # HTML string
    html = """
    <span class="loader below_logo"></span>
    """

    # Getting user inputs for customization
    # height = st.number_input("Height of loader (px):", min_value=1, value=4, step=1)
    # width_percent = st.number_input("Width of loader (%):", min_value=1, value=100, step=1)
    # duration = st.number_input("Animation duration (sec):", min_value=0.1, value=0.7, step=0.1)
    # Getting user inputs for customization
    # Forming width string

    # Injecting the CSS and HTML into the Streamlit app

    # Display the custom CSS
    
    ## Function to simulate app loading
    #def simulate_loading(seconds):
    #    time.sleep(seconds)
#
#
    ## Simulate app loading for 5 seconds
    #simulate_loading(5)

    # Injecting the CSS and HTML into the Streamlit app
    st.markdown(get_css(4, 100, 0.7), unsafe_allow_html=True)
    # Wait a bit till the page is ready.
    time.sleep(1)
    # Remove loading spinner after loading is complete
    st.markdown(html, unsafe_allow_html=True)



