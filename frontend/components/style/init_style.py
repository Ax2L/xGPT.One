# components/css/1_init_style.py
# ? ------------------ Imports ------------------
import streamlit as st

# First object: Cleanup CSS
cleanup_css = """
<html>
<head>
<style>
:root {
    font-family: Roboto;

}
.title {
    font-size: 34px;
    font-family: "Roboto";
    font-weight: 400;
    width: 360px;
    height: 40px;
}
header[data-testid="stHeader"] {
    display: none !important;
}
/* Cleanup the Header Styles */
section[tabindex="0"] div[data-testid="blockOFF-container"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
}
section[data-testid="stSidebar"] {
    background-color: #262730;
}
</style>
</head>
</html>
"""

# Second object: End of Script Components
end_of_script_components = """
<html>
<head>
<!-- Hypothetical end of script components. Adjust according to your needs. -->
<script>
    // Add your JavaScript here.
    console.log("End of script components loaded.");
</script>
<!-- You can also add other components or tags as needed -->
</head>
</html>
"""


# Streamlit functions to apply the above CSS and JavaScript
def apply_cleanup_css():
    st.markdown(cleanup_css, unsafe_allow_html=True)
    print("successfully initiated css")

def apply_end_of_script_components():
    st.markdown(end_of_script_components, unsafe_allow_html=True)
    print("successfully initiated apply_end_of_script_components")
