import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="PMMS - Predictive Maintenance Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern UI
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E3A8A; }
    .card-metric { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #1E3A8A; }
    .status-normal { color: #10B981; font-weight: bold; }
    .status-warning { color: #F59E0B; font-weight: bold; }
    .status-critical { color: #EF4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/maintenance.png", width=70)
st.sidebar.title("PMMS Navigation")
st.sidebar.markdown("**Predictive Maintenance Management System**")
page = st.sidebar.radio("Go to:", [
    "📊 System Dashboard",
    "🏭 Equipment & Sensors",
    "🤖 AI Prediction & Analytics",
    "📋 Work Orders & Alerts",
    "📅 Project SPM Summary"
])

# Mock Data Generation
@st.cache_data
def load_equipment_data():
    return pd.DataFrame({
        "Equipment ID": ["EQ-101 (Turbine A)", "EQ-102 (Pump B)", "EQ-103 (Compressor C)", "EQ-104 (Generator D)", "EQ-105 (Cooling Tower)"],
        "Facility": ["Energy Sector Unit 1", "Factory Line 2", "Warehouse Hub", "Energy Sector Unit 2", "Factory Line 1"],
        "Status": ["Normal", "Warning", "Normal", "Critical", "Normal"],
        "Operating Hours": [1420, 3100, 890, 4250, 1980],
        "Vibration (mm/s)": [1.2, 4.8, 0.9, 8.5, 1.1],
        "Temp (°C)": [45.2, 78.5, 38.0, 95.4, 41.0],
        "Failure Risk (%)": [5, 62, 3, 91, 8],
        "RUL (Days)": [120, 14, 180, 2, 95]
    })

df_equipment = load_equipment_data()

# ------------------- PAGE 1: DASHBOARD -------------------
if page == "📊 System Dashboard":
    st.info("Prototype Demo: This interactive dashboard operates on simulated IoT sensor data for project demonstration purposes.")
    st.markdown('<p class="main-header">⚙️ Real-Time Equipment Monitoring Dashboard</p>', unsafe_allow_html=True)
    st.write("Continuous IoT sensor monitoring and system status overview across facilities.")

    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Monitored Machines", len(df_equipment), "15 Sensors Active")
    c2.metric("Operational Status", "3 Normal", delta="Healthy", delta_color="normal")
    c3.metric("Requires Inspection", "1 Warning", delta="Needs Review", delta_color="off")
    c4.metric("Critical Alerts", "1 Critical", delta="-1 Action Required", delta_color="inverse")

    st.divider()

    # Overview Layout
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Equipment Health Overview")
        fig_status = px.bar(
            df_equipment,
            x="Equipment ID",
            y="Failure Risk (%)",
            color="Status",
            color_discrete_map={"Normal": "#10B981", "Warning": "#F59E0B", "Critical": "#EF4444"},
            text_auto=True,
            title="Real-time Machine Failure Probability (%)"
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col_right:
        st.subheader("Active Alerts")
        st.error("🚨 **EQ-104 (Generator D)**: Severe vibration & overheating detected. High risk of failure!")
        st.warning("⚠️ **EQ-102 (Pump B)**: Bearing wear pattern identified by AI.")
        st.info("ℹ️ **EQ-101**: Scheduled maintenance completed last week.")

# ------------------- PAGE 2: EQUIPMENT & SENSORS -------------------
elif page == "🏭 Equipment & Sensors":
    st.markdown('<p class="main-header">🏭 Central Equipment Records & Sensor Live Readings</p>', unsafe_allow_html=True)

    selected_eq = st.selectbox("Select Equipment Record:", df_equipment["Equipment ID"])
    eq_info = df_equipment[df_equipment["Equipment ID"] == selected_eq].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.info(f"**Facility:** {eq_info['Facility']}")
    c2.info(f"**Operating Hours:** {eq_info['Operating Hours']} hrs")
    c3.info(f"**Condition Status:** {eq_info['Status']}")

    st.subheader("Sensor Stream Simulation")

    # Generate live telemetry chart simulation
    time_series = pd.date_range(end=datetime.now(), periods=30, freq="min")
    sensor_val = np.random.normal(loc=eq_info["Vibration (mm/s)"], scale=0.3, size=30)
    df_sensor = pd.DataFrame({"Timestamp": time_series, "Vibration (mm/s)": sensor_val})

    fig_sensor = px.line(df_sensor, x="Timestamp", y="Vibration (mm/s)", title=f"Live Vibration Telemetry for {selected_eq}")
    fig_sensor.add_hline(y=5.0, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    st.plotly_chart(fig_sensor, use_container_width=True)

# ------------------- PAGE 3: AI PREDICTION -------------------
elif page == "🤖 AI Prediction & Analytics":
    st.markdown('<p class="main-header">🤖 AI Anomaly Detection & Recommendation Engine</p>', unsafe_allow_html=True)
    st.write("Artificial Intelligence failure predictions and suggested technician intervention steps.")

    st.dataframe(df_equipment[["Equipment ID", "Status", "Failure Risk (%)", "RUL (Days)"]], use_container_width=True)

    st.subheader("Detailed Diagnostic & Recommended Action")
    eq_target = st.selectbox("Select Machine for Diagnostic:", df_equipment["Equipment ID"], index=3)

    if eq_target == "EQ-104 (Generator D)":
        st.markdown("""
        <div style="background-color: #FEE2E2; padding: 15px; border-radius: 8px; border-left: 5px solid #EF4444;">
            <h4 style="color: #991B1B; margin: 0;">Predicted Failure Mode: Bearing Seizure & Overheating</h4>
            <p style="color: #7F1D1D;"><b>Failure Probability:</b> 91% | <b>Estimated RUL:</b> 2 Days</p>
            <hr>
            <h5>Suggested Technician Actions:</h5>
            <ul>
                <li>Inspect rotor bearings for physical surface fatigue.</li>
                <li>Verify coolant oil pressure levels and oil filter cleanliness.</li>
                <li>Consider immediate scheduled shutdown before catastrophic failure.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("Machine is operating within baseline parameters. No critical intervention required.")

# ------------------- PAGE 4: WORK ORDERS -------------------
elif page == "📋 Work Orders & Alerts":
    st.markdown('<p class="main-header">📋 Maintenance Work Orders & Notification Log</p>', unsafe_allow_html=True)

    wo_data = pd.DataFrame({
        "WO ID": ["WO-2026-001", "WO-2026-002", "WO-2026-003"],
        "Equipment": ["EQ-104 (Generator D)", "EQ-102 (Pump B)", "EQ-101 (Turbine A)"],
        "Priority": ["Urgent (Critical)", "Medium", "Low"],
        "Assigned Technician": ["Unassigned", "Technician Team A", "Technician Team B"],
        "Status": ["Open", "In Progress", "Completed"]
    })

    st.table(wo_data)

    st.subheader("Create New Work Order")
    with st.form("new_wo_form"):
        f_eq = st.selectbox("Equipment", df_equipment["Equipment ID"])
        f_prio = st.selectbox("Priority", ["Low", "Medium", "Urgent"])
        f_desc = st.text_area("Maintenance Task Description")
        submitted = st.form_submit_button("Generate Work Order")
        if submitted:
            st.success(f"Work order generated successfully for {f_eq}!")

# ------------------- PAGE 5: SPM SUMMARY -------------------
elif page == "📅 Project SPM Summary":
    st.markdown('<p class="main-header">📌 Software Project Management (SPM) Execution Baseline</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Project Duration", "19 Weeks", "Critical Path Baseline")
    c2.metric("Total Estimated Effort", "141 Person-Days", "3 Team Members")
    c3.metric("Project Budget", "SAR 42,050.53", "Includes Contingency")

    st.subheader("Critical Path Method (CPM) Summary")
    st.info("**Critical Paths:** A → C → G → H → I → J → K → L → M (or via B & Dummy Activity)")
    st.write("Activities **D (Database)** and **E (Dashboard)** have 9 weeks of Total Float, while **F (Sensor API)** has 7 weeks.")
