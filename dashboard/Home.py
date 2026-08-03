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
import streamlit as st

st.title("🏪 Retail Intelligence Platform")

st.markdown("""
## Welcome 👋

Ye ek **End-to-End Retail Intelligence Platform** hai.

### Modules
- 📊 Executive Dashboard
- 💰 Sales Analytics
- 👥 Customer Analytics
- 📦 Inventory Analytics
- 🗄️ SQL Insights

👈 Sidebar se kisi bhi module par click karo.
""")
