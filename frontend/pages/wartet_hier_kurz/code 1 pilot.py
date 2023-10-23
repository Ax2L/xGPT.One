import streamlit as st

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
page_name = "code 1 pilot"
page_navi_number = 21
page_navi_category = "coder"

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


import streamlit as st
import psycopg2
        
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from UserAPIKey;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")