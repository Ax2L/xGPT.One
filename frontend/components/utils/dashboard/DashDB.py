import streamlit as st
from components.utils.postgres.xdatastore import DashboardLayouts, DashboardItems


def dashboard_items_state_from_db():
    dashboard_items = DashboardItems()
    dashboard_items.load()  # Load the existing data
    st.session_state["all_items"] = dashboard_items.data
    print("Loading items from database...")


def dashboard_layouts_state_from_db():
    dashboard_layouts = DashboardLayouts()
    dashboard_layouts.load()  # Load the existing data
    st.session_state["all_layouts"] = dashboard_layouts.data
    print("Loading layouts from database...")
