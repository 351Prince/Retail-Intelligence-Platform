import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "database/retail.db"

@st.cache_data
def get_data(query="SELECT * FROM sales"):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df
