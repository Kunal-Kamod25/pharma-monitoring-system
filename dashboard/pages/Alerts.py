import streamlit as st
import pandas as pd
import sqlite3
import os

db = os.path.join(os.getcwd(), "data", "pharma.db")
conn = sqlite3.connect(db)

st.title("🚨 Alerts")
alerts = pd.read_sql("SELECT * FROM alerts ORDER BY timestamp DESC", conn)
st.dataframe(alerts)
