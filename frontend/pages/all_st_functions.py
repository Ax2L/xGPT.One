
#**** Default Page block: **********************************************
import streamlit as st
from components import xhelper, header

# Constants 
PAGE_NAME = "all_st_functions" 
# Set Page settings and Icon
st.markdown(
    """
    <head>
        <link rel="icon" href="http://127.0.0.1:8334/data/images/logo/favicon-32x32.png"  type="image/x-icon">
    </head>
    """,
    unsafe_allow_html=True,
)

# &⁡⁣⁣⁢ Functions
def setup_page(page_name):
    """Setup and initialize the page."""
    xhelper.check_logged_in(page_name)
    xhelper.check_current_page(page_name)

def load_custom_css():
    if f"{PAGE_NAME}_css" not in st.session_state:
        """Load custom CSS style."""
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        print(f"css already active on {PAGE_NAME}")

# Build header, forwards back and forwards to main if not logged in.
header.create_menu(PAGE_NAME)

# ⁣⁣⁢>>>| SETUP PAGE |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<⁡
# Check if 'current_page' not in session state, initialize it and redirect to 'main'
setup_page(PAGE_NAME)

# Check for page change again, and execute the respective section if a change occurred.
# xhelper.check_current_page(PAGE_NAME)

#**** Default Page block end **********************************************



import matplotlib.pyplot as plt
import streamlit as st

# Basic Text
st.title("Streamlit Layout Showcase")

# Container
with st.container():
    st.write("This is a container:")
    
    # Two Columns within Container
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("This is column 1")
        st.button("Click me!")

    with col2:
        st.write("This is column 2")
        st.checkbox("Check me!")

    # Spacer / Divider
    st.write("---")  # This creates a horizontal line (divider)

# Another Container
with st.container():
    st.write("This is another container:")
    
    # Three Columns within Container
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("Col 1")
        st.radio("Pick one", ["A", "B"])

    with col2:
        st.write("Col 2")
        st.selectbox("Choose one", ["X", "Y", "Z"])

    with col3:
        st.write("Col 3")
        st.slider("Slide me!", 0, 10)

# Expander
my_expander = st.expander("Click to expand:")
with my_expander:
    st.write("Hidden content!")

# Final Note
st.write("End of layout showcase!")


# Create a figure and axes
fig, ax = plt.subplots()

# Use the ax object for plotting
ax.plot([1, 2, 3], [1, 2, 3])

# Display the figure in Streamlit
st.pyplot(fig)
st.title("Streamlit Components Showcase")

# Displaying text and data components
st.write("## Text Components")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is plain text")
st.markdown("This is **Markdown** formatted text")
st.latex(r'e^{i\pi} + 1 = 0')  # LaTeX

st.write("## Data Components")
st.dataframe({"A": [1, 2, 3], "B": [4, 5, 6]})
st.table({"A": [1, 2, 3], "B": [4, 5, 6]})
st.json({"name": "John", "age": 30, "city": "New York"})

# Displaying media components
st.write("## Media Components")
st.image("https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", caption="Streamlit Logo", use_column_width=True)
st.audio("https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3")
st.video("https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4")

# Displaying chart components
st.write("## Chart Components")
st.line_chart({"data": [1, 5, 2, 6, 2, 1]})
st.area_chart({"data": [1, 5, 2, 6, 2, 1]})
st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})
st.pyplot()  # You can also integrate with Matplotlib
st.vega_lite_chart({"data": {"name": "table"}, "mark": "point"}, {"datasets": {"table": [{"x": 1, "y": 2}, {"x": 2, "y": 4}]}})  # For Vega-Lite charts

# Displaying interactive widgets
st.write("## Interactive Widgets")
st.button("Button")
st.checkbox("Checkbox", value=True)
st.radio("Radio Buttons", options=["Option A", "Option B", "Option C"])
st.selectbox("Select Box", options=["Option A", "Option B", "Option C"])
st.multiselect("Multiselect", options=["Option A", "Option B", "Option C"])
st.slider("Slider", min_value=0, max_value=100, value=50)
st.text_input("Text Input", "Default Value")
st.text_area("Text Area", "Default Value")
st.date_input("Date Input")
st.time_input("Time Input")
st.file_uploader("File Uploader")
st.color_picker("Color Picker")
st.number_input("Number Input", min_value=0, max_value=100, value=50)

st.write("## Layout Components")
# Layout components such as columns, expander and containers
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", caption="Column 1", use_column_width=True)
with col2:
    st.image("https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", caption="Column 2", use_column_width=True)
with col3:
    st.image("https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", caption="Column 3", use_column_width=True)

with st.expander("Expander"):
    st.write("Content inside an expander")

st.write("## Other")
st.progress(75)  # Progress bar with 75% completion
st.spinner("Loading...")  # Spinner component

# To run, save the script as "streamlit_components_showcase.py" and execute:
# $ streamlit run streamlit_components_showcase.py



load_custom_css()