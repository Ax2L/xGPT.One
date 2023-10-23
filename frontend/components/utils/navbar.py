# components/utils/navbar.py

# // region [ rgba(0, 100, 250, 0.05)] Imports and Constants
import streamlit as st
import hydralit_components as hc


# // region [ rgba(50, 200, 10, 0.05)] Navigation Data and Theme

class NavBar:
    def __init__(self):
        
        # Menu data with appropriate icons
        self.menu_data = [
            {"id": "assistant", "icon": "fas fa-robot", "label": "Assistant"},
            {"id": "coder", "icon": "fas fa-code", "label": "Coder", 'submenu':[{"id": "code 1 pilot", "icon": "fas fa-code", "label": "Code Pilot"}, {"id": "demogpt", "icon": "fas fa-code", "label": "demogpt"}]},
            {"id": "tools", "icon": "fas fa-wrench", "label": "Tools",'submenu':[{"id": "writer", "icon": "fas fa-pencil-alt", "label": "Writer"}]},
            {"id": "all_llms", "icon": "fas fa-chart-line", "label": "LLMs",'submenu':[{"id": "llms", "icon": "fas fa-chart-line", "label": "First LLMs"}]},
            {"id": "database", "icon": "fas fa-database", "label": "Database",'submenu':[{"id": "attu", "icon":  "fas fa-book-reader", "label": "Milvus Dashboard"}]},
            {"id": "all_mls", "icon": "fas fa-book-reader", "label": "Machine Learning",'submenu':[{"id": "file_manager", "icon":  "fas fa-book-reader", "label": "File Manager"}]},
            {"id": "knowledge", "icon": "fas fa-book-reader", "label": "Knowledge Base",'submenu':[{"id": "wiki_0_research_assistant", "icon":  "fas fa-book-reader", "label": "Research Assistant"},{"id": "wiki_2_semantic_search", "icon":  "fas fa-book-reader", "label": "Semantic Search"}]},
            {"id": "tests", "icon": "fas fa-ellipsis-h", "label": "Tests",'submenu':[{"id": "testchat", "icon": "fas fa-pencil-alt", "label": "Test Chat"}]},
        ]

        self.override_theme = {
            "txc_inactive": "#EBEBF5",
            "menu_background": "#1a202c",
            "txc_active": "#644C8F",
            #"option_active": "white",
        }

    def build_navbar(self, number):
        # Build NavBar and drop directly as first.
        menu_id = hc.nav_bar(
            menu_definition=self.menu_data,
            override_theme=self.override_theme,
            home_name="Home",
            login_name="Logout",
            hide_streamlit_markers=True,
            sticky_nav=True,
            sticky_mode="pinned",
            first_select=number
        )
        return menu_id

