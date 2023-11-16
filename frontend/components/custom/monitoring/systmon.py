# components.monitoring.systmon.py
import streamlit as st
import psutil

class OneSystMon:
    @staticmethod
    def display_metrics():
        st.title("System Metrics Dashboard")

        st.subheader("CPU Info")
        st.write("CPU Usage:", psutil.cpu_percent(), "%")
        st.write("Total Physical Cores:", psutil.cpu_count(logical=False))
        st.write("Total Logical Cores:", psutil.cpu_count(logical=True))
        
        st.subheader("RAM Info")
        memory_info = psutil.virtual_memory()
        st.write("Total Memory:", memory_info.total)
        st.write("Available Memory:", memory_info.available)
        st.write("Used Memory:", memory_info.used)
        st.write("Memory Percentage:", memory_info.percent)
        
        st.subheader("Disk Info")
        disk_info = psutil.disk_usage('/')
        st.write("Total Disk Space:", disk_info.total)
        st.write("Used Disk Space:", disk_info.used)
        st.write("Free Disk Space:", disk_info.free)
        st.write("Disk Usage Percentage:", disk_info.percent)
