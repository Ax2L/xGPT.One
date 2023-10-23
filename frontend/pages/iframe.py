import streamlit as st
import streamlit.components.v1 as components


# st.set_page_config(layout='wide')

link1 = "http://127.0.0.1:8181"
components.iframe(link1, height=800, width=800)
components.html('<iframe  src="http://localhost:8181/" width="800" height="600"></iframe>', width=820, height=620)