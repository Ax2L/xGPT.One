
# Edit and add the following to each Page in frontend/pages 

# // region [ rgba(50, 100, 110, 0.2)] Navigation Data and Theme
#? ||--------------------------------------------------------------------------------||
#? ||                                    # NavBar                                    ||
#? ||--------------------------------------------------------------------------------||
from components.utils.navbar import NavBar
from streamlit_extras.#switch_page_button import #switch_page

# Specific config for this page only:
page_name = "Home"
page_navi_number = 0

# Build Navi 
navbar = NavBar()
navi = navbar.build_navbar(page_navi_number)


try:
    if navi == page_name:
        # st.text("current Page selected")
        do = "nothing"
    else:
        # st.text("You selected: "+ navi)
        #switch_page(navi)
except Exception as e:
    st.error(e)
#// endregion