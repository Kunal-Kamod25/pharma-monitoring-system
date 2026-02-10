import streamlit as st
import pandas as pd
import sqlite3
import os

db = os.path.join(os.getcwd(), "data", "pharma.db")
conn = sqlite3.connect(db)

st.title("📋 GMP Compliance (Live Data)")
df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 20", conn)
st.dataframe(df)
