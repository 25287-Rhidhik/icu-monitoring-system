import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import firebase_admin
from firebase_admin import credentials, db

st.set_page_config(layout="wide")

# =========================
# AUTO REFRESH
# =========================
st_autorefresh(interval=1000, key="refresh")

# =========================
# FIREBASE CONNECT
# =========================
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://icu-monitoring-system-bc1c3-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

# =========================
# STYLE
# =========================
st.markdown("""
<style>
body {background-color:#0e1117; color:white;}
.title {text-align:center; font-size:40px; font-weight:bold;}
.card {padding:15px; border-radius:12px; text-align:center; color:white;}
.safe {background:#1f6f4a;}
.warning {background:#8a6d1a;}
.critical {background:#7a1c1c; animation: blink 1s infinite;}
@keyframes blink {50% {opacity:0.4;}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">ICU Monitoring System</div>', unsafe_allow_html=True)

# =========================
# FETCH DATA
# =========================
ref = db.reference("patients")
data = ref.get()

if not data:
    st.warning("Waiting for Firebase data...")
    st.stop()

# =========================
# CONVERT DATA
# =========================
rows = []

for pid, values in data.items():
    rows.append({
        "patient_id": pid,
        "temp": values.get("temp"),
        "hum": values.get("humidity"),
        "status": values.get("status"),
        "prediction": values.get("ai_score")
    })

df = pd.DataFrame(rows)

# CLEAN DATA
df["temp"] = pd.to_numeric(df["temp"], errors="coerce").fillna(0)
df["hum"] = pd.to_numeric(df["hum"], errors="coerce").fillna(0)
df["prediction"] = pd.to_numeric(df["prediction"], errors="coerce").fillna(0)

# =========================
# PATIENT CARDS
# =========================
st.subheader("Patient Overview")

cols = st.columns(len(df))

for i, row in df.iterrows():

    if row["status"] == "CRITICAL":
        cls = "critical"
    elif row["status"] == "WARNING":
        cls = "warning"
    else:
        cls = "safe"

    cols[i].markdown(f"""
    <div class="card {cls}">
        <h3>{row['patient_id']}</h3>
        Temp: {row['temp']:.1f} °C<br>
        Humidity: {row['hum']:.1f} %<br>
        AI Score: {row['prediction']:.2f}<br><br>
        <b>{row['status']}</b>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CREATE FAKE HISTORY (FOR LINES)
# =========================
plot_data = []

for i in range(20):  # 20 points history
    for _, row in df.iterrows():
        plot_data.append({
            "time": pd.Timestamp.now() - pd.Timedelta(seconds=(20 - i)),
            "patient_id": row["patient_id"],
            "temp": row["temp"] + np.random.uniform(-0.2, 0.2),
            "hum": row["hum"] + np.random.uniform(-0.5, 0.5)
        })

df_plot = pd.DataFrame(plot_data)

# =========================
# TEMPERATURE GRAPH
# =========================
st.subheader("Live Temperature (All Patients)")

fig1 = px.line(
    df_plot,
    x="time",
    y="temp",
    color="patient_id",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# HUMIDITY GRAPH
# =========================
st.subheader("Live Humidity (All Patients)")

fig2 = px.line(
    df_plot,
    x="time",
    y="hum",
    color="patient_id",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# SELECT PATIENT
# =========================
selected = st.selectbox("Select Patient", df["patient_id"])

st.subheader(f"{selected} Details")
st.write(df[df["patient_id"] == selected])