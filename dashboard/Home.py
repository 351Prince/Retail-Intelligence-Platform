import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

st.set_page_config(
    page_title="Retail Intelligence Platform",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Retail Intelligence Platform")
st.write("Select a page from the sidebar.")
