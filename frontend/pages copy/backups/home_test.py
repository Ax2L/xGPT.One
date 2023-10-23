# Working Navbar with switch page

#// region [ rgba(0, 100, 250, 0.05)] Imports and Constants
import streamlit as st
from streamlit_extras.#switch_page_button import #switch_page
import hydralit_components as hc
import datetime
#// endregion
#make it look nice from the start
# st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)
page_id = "home"

# specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label':"Left End"},
    {'id':'test','icon':"🐙",'label':"test"},
    {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
    {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
    {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!",'id':"dashboard"}, #can add a tooltip message
    {'icon': "far fa-copy", 'label':"Right End"},
    {'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
]

""" THIS IS HOME """

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

""" LETS SEE WHATS IN y = """
page_id = "home"

navigation = menu_id
st.text(menu_id)

def check_nav_action(m_id,p_id):
    try:
        # Same button as current page:
        if (str(m_id)).lower() == p_id:
            """ You clicked on the Page you currently in. """
            do = "nothing"
        else:
            #switch_page(str(m_id))
    except Exception as e:
        st.error(f"An error occurred: {e}")

check_nav_action(menu_id,page_id)

#if y == 4:
#    #switch_page("home")
#if y == 5:
#    #switch_page("home")
#if y == 6:
#    #switch_page("home")
#if y == 7:
#    #switch_page("home")
#if y == 8:
#    #switch_page("home")


# if x == 1:
#     #switch_page("home")
# if x == 2:
#     #switch_page("assistant")
# if x == 3:
#     #switch_page("test")
# if x == 4:
#     #switch_page("home")
# if x == 5:
#     #switch_page("home")
# if x == 6:
#     #switch_page("home")
# if x == 7:
#     #switch_page("home")
# if x == 8:
#     #switch_page("home")