# 🧪 Pharma Industrial Sensor Monitoring & Alert System

A real-time pharma cleanroom monitoring system inspired by industrial data historian platforms like AVEVA PI and SCADA systems.  
This project simulates industrial sensor data (temperature, humidity, pressure differential, particle count), stores time-series data, visualizes live trends, and generates alerts for GMP threshold violations with role-based login (Operator / QA / Admin).

---

## 🚀 Features

- 📡 Real-time sensor data simulation (pharma cleanroom parameters)
- 📊 Live dashboards with trend charts (Streamlit)
- 🚨 Threshold-based alerts for GMP compliance
- 🔐 Role-based login (Operator / QA / Admin)
- 🗄️ Time-series data storage (SQLite)
- 📁 Modular backend + dashboard architecture
- ☁️ Cloud deployable (Streamlit Cloud)
- 🔁 Auto-deploy after Git push (CI/CD)

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Dashboard:** Streamlit  
- **Libraries:** Pandas, NumPy, Matplotlib  
- **Database:** SQLite  
- **Industrial Concepts (Learning):** PLC, SCADA, OPC, PI System  
- **Tools:** VS Code, GitHub  
- **OS:** Linux / Windows



  # 1. Clone the repository
git clone https://github.com/Kunal-Kamod25/pharma-monitoring-system.git
cd pharma-monitoring-system

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# (Ubuntu users only – if venv error)
sudo apt install python3-venv

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database & create admin user
python3 - << 'EOF'
from backend.database import init_db
from backend.auth import register_user

init_db()
register_user("admin", "admin123", "Admin")
print("Admin user created: admin / admin123")
EOF

# 5. Start sensor simulator (keep running)
python3 backend/sensor_simulator.py

# 6. Open new terminal, activate venv again, start dashboard
source venv/bin/activate
streamlit run dashboard/app.py

