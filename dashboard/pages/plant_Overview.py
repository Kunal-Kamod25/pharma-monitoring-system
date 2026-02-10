import streamlit as st
import pandas as pd
import sqlite3
import os

db = os.path.join(os.getcwd(), "data", "pharma.db")
conn = sqlite3.connect(db)

st.title("🏭 Plant Overview")

df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 50", conn)
st.dataframe(df)
st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])
