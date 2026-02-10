import streamlit as st
import sys, os

sys.path.append(os.getcwd())

from backend.database import init_db
from backend.auth import login_user, register_user, user_exists

st.set_page_config(page_title="Pharma Monitoring", layout="wide")

# Initialize DB
init_db()

# Auto-create demo users on first run
if not user_exists("admin"):
    register_user("admin", "admin123", "Admin")
if not user_exists("operator1"):
    register_user("operator1", "op123", "Operator")
if not user_exists("qa1"):
    register_user("qa1", "qa123", "QA")

# Session state
if "role" not in st.session_state:
    st.session_state.role = None

st.title("🏭 Pharma Manufacturing Monitoring System")

# Login screen
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
