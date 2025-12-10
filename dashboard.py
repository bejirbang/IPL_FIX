# dashboard.py
import streamlit as st
from backend import get_engine
from tabs.tab1.tab1_controller import show_tab1
from tabs.tab2.tab2 import show_tab2
from tabs.tab3.tab3_controller import show_tab3

# PAGE CONFIG
st.set_page_config(
    page_title="Intelligent Product Lifecycle",
    layout="wide",
)

st.title("Intelligent Product Lifecycle Dashboard")

engine = get_engine()

main_tabs = st.tabs([
    "Summary Performance",
    "Lifecycle Analysis",
    "Reporting & Monitoring",
])

with main_tabs[0]:
    show_tab1(engine)   

with main_tabs[1]:
    show_tab2(engine)

with main_tabs[2]:
    show_tab3(engine)