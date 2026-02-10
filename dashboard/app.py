import streamlit as st
import sys, os
import pandas as pd
import random
from datetime import datetime

sys.path.append(os.getcwd())

from backend.database import init_db, get_connection
from backend.auth import login_user, register_user, user_exists

st.set_page_config(page_title="Pharma Monitoring", layout="wide")

# -------------------- Initialize DB & Users --------------------
init_db()

# Auto-create demo users if they don't exist
demo_users = [
    ("admin", "admin123", "Admin"),
    ("operator1", "op123", "Operator"),
    ("qa1", "qa123", "QA")
]

for username, password, role in demo_users:
    if not user_exists(username):
        register_user(username, password, role)

# -------------------- Session State --------------------
if "role" not in st.session_state:
    st.session_state.role = None

st.title("🏭 Pharma Manufacturing Monitoring System")

# -------------------- Login Screen --------------------
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

# -------------------- Live Dashboards --------------------
else:
    st.success(f"Logged in as: {st.session_state.role}")

    # Sidebar menu based on role
    if st.session_state.role == "Admin":
        menu = st.sidebar.selectbox("Admin Menu", ["Live Sensors", "Alerts", "Trends", "Manage Users"])
    elif st.session_state.role == "Operator":
        menu = st.sidebar.selectbox("Operator Menu", ["Live Sensors", "Alerts"])
    elif st.session_state.role == "QA":
        menu = st.sidebar.selectbox("QA Menu", ["Alerts", "Trends"])
    else:
        menu = None

    conn = get_connection()
    cur = conn.cursor()

    # -------------------- Simulate Live Sensor Data --------------------
    def simulate_sensor_data():
        timestamp = datetime.now().isoformat()
        temperature = round(random.uniform(18, 26), 2)
        humidity = round(random.uniform(35, 65), 2)
        pressure_diff = round(random.uniform(5, 20), 2)
        particle_count = random.randint(300, 5000)

        cur.execute("""
            INSERT INTO sensor_data (timestamp, temperature, humidity, pressure_diff, particle_count)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, temperature, humidity, pressure_diff, particle_count))
        conn.commit()

    # Run simulation on each app load
    simulate_sensor_data()

    # -------------------- Live Sensors --------------------
    if menu == "Live Sensors":
        st.subheader("📊 Live Sensor Data")
        df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 20", conn)
        if not df.empty:
            st.dataframe(df)
            st.line_chart(df.set_index("timestamp")[["temperature", "humidity", "pressure_diff", "particle_count"]])
        else:
            st.info("No sensor data available yet.")

    # -------------------- Alerts --------------------
    elif menu == "Alerts":
        st.subheader("🚨 Alerts Dashboard")
        # Generate alert if any parameter crosses threshold
        df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1", conn)
        if not df.empty:
            latest = df.iloc[0]
            alerts = []
            if latest["temperature"] > 25:
                alerts.append(("High Temperature", "High"))
            if latest["humidity"] < 40:
                alerts.append(("Low Humidity", "Medium"))
            if latest["particle_count"] > 4000:
                alerts.append(("High Particle Count", "High"))

            for msg, sev in alerts:
                cur.execute("""
                    INSERT INTO alerts (timestamp, message, severity) VALUES (?, ?, ?)
                """, (latest["timestamp"], msg, sev))
                conn.commit()

        alerts_df = pd.read_sql("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 20", conn)
        if not alerts_df.empty:
            st.table(alerts_df)
        else:
            st.info("No alerts yet.")

    # -------------------- Trends --------------------
    elif menu == "Trends":
        st.subheader("📈 Trend Analysis")
        df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp ASC", conn)
        if not df.empty:
            st.line_chart(df.set_index("timestamp")[["temperature", "humidity", "pressure_diff", "particle_count"]])
        else:
            st.info("No sensor data yet for trends.")

    # -------------------- User Management (Admin Only) --------------------
    elif menu == "Manage Users" and st.session_state.role == "Admin":
        st.subheader("👤 Manage Users")
        df = pd.read_sql("SELECT id, username, role FROM users", conn)
        st.table(df)

        st.markdown("### Add New User")
        new_username = st.text_input("Username", key="new_user")
        new_password = st.text_input("Password", type="password", key="new_pass")
        new_role = st.selectbox("Role", ["Admin", "Operator", "QA"], key="new_role")
        if st.button("Add User"):
            if new_username and new_password:
                if not user_exists(new_username):
                    register_user(new_username, new_password, new_role)
                    st.success(f"User {new_username} added as {new_role}")
                else:
                    st.error("Username already exists")

    conn.close()
