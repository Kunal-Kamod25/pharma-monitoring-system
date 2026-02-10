import streamlit as st
import sys, os

sys.path.append(os.getcwd())

from backend.database import init_db
from backend.auth import login_user

st.set_page_config(page_title="Pharma Monitoring", layout="wide")
init_db()

if "role" not in st.session_state:
    st.session_state.role = None

st.title("🏭 Pharma Manufacturing Monitoring System")

if not st.session_state.role:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login_user(username, password)
        if role:
            st.session_state.role = role
            st.success(f"Welcome {role}")
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.success(f"Logged in as: {st.session_state.role}")
    st.info("Use sidebar to navigate dashboards")
