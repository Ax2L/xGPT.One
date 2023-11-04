import streamlit as st

def toggle_slide_css(slide_type="in"):
    """
    Function to toggle the slide CSS in a Streamlit app.
    
    Parameters:
    - slide_type (str): Either "in" or "out" to specify the slide effect.
    """
    # Define the slide-in and slide-out CSS
    slide_in_css = """
    <style>
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    section[data-testid='stSidebar'] {
        animation-name: slideIn;
        animation-timing-function: ease-in;
        animation-duration: 0.5s;
        display: block;
    }
    </style>
    """
    
    slide_out_css = """
    <style>
    @keyframes slideOut {
        from { transform: translateX(0); }
        to { transform: translateX(-100%); }
    }
    section[data-testid='stSidebar'] {
        animation-name: slideOut;
        animation-timing-function: ease-out;
        animation-duration: 0.5s;
        display: none;
    }
    </style>
    """
    
    # Inject the appropriate CSS based on the slide_type
    if slide_type == "in":
        st.markdown(slide_in_css, unsafe_allow_html=True)
    elif slide_type == "out":
        st.markdown(slide_out_css, unsafe_allow_html=True)
    else:
        st.error("Invalid slide type specified!")

# Initialize the session state
if "sidebar_status" not in st.session_state:
    st.session_state.sidebar_status = "out"

# Use session state to control toggle behavior
if st.session_state.sidebar_status == "in":
    toggle_button_text = "Slide Out"
else:
    toggle_button_text = "Slide In"

## Create a MUI Button to control the toggle
#toggle_button_code = f"""
#<div>
#    <button class="MuiButtonBase-root MuiButton-root MuiButton-text" tabindex="0" type="button" 
#        onClick="document.querySelector('.streamlit-button').click();">
#        {toggle_button_text}
#    </button>
#</div>
#"""
#
#st.markdown(toggle_button_code, unsafe_allow_html=True)
#
## React based on button press
#if st.button("Toggle Sidebar"):
#    if st.session_state.sidebar_status == "in":
#        toggle_slide_css("out")
#        st.session_state.sidebar_status = "out"
#    else:
#        toggle_slide_css("in")
#        st.session_state.sidebar_status = "in"
