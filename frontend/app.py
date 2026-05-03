import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="MedRemind", layout="wide")

# --- 2. UI STYLING (UPDATED FOR VISIBILITY) ---
st.markdown("""
    <style>
    /* Change sidebar background to dark blue/black */
    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* Force all text in the sidebar to be white */
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stRadio div, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] p {
        color: white !important;
    }

    /* Change the color of the radio button text specifically */
    div[data-testid="stRadio"] > label {
        color: white !important;
        font-weight: bold;
    }

    /* Style the dashboard metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Style the buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2563eb;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color: white;'>💙 MedRemind</h2>", unsafe_allow_html=True)
    portal = st.selectbox("Switch Portal", ["Staff Portal", "Doctor Portal", "Admin Portal", "Patient Portal"])
    st.divider()

    if portal == "Staff Portal":
        menu = ["Dashboard", "Patient Monitor", "Record Vitals", "Med Tracking"]
    elif portal == "Doctor Portal":
        menu = ["Dashboard", "My Patients", "Adherence Reports"]
    elif portal == "Admin Portal":
        menu = ["Dashboard", "All Doctors", "All Patients", "All Staff", "All Records"]
    else:
        menu = ["Dashboard", "My Medicines"]

    choice = st.radio("Navigation", menu)
    st.divider()
    st.write(f"👤 **{portal.split(' ')[0]}**")

# --- 4. HEADER ---
st.header(f"{portal} - {choice}")
st.write(f"📅 **{datetime.now().strftime('%A, %B %d, %Y')}**")

# --- 5. DYNAMIC DATA FETCHING ---
try:
    all_logs = requests.get("http://127.0.0.1:8000/logs").json()
    all_vitals = requests.get("http://127.0.0.1:8000/patient-monitor").json()
    db_patients = requests.get("http://127.0.0.1:8000/patients").json()
    db_doctors = requests.get("http://127.0.0.1:8000/users/doctor").json()
    db_staff = requests.get("http://127.0.0.1:8000/users/staff").json()
except:
    all_logs, all_vitals, db_patients, db_doctors, db_staff = [], [], [], [], []

# --- 6. PORTAL LOGIC ---

if portal == "Staff Portal":
    if choice == "Dashboard":
        c1, c2 = st.columns(2)
        c1.metric("TOTAL PATIENTS", len(db_patients))
        c2.metric("VITALS RECORDED", len(all_vitals))
    
    elif choice == "Patient Monitor":
        st.subheader("🖥️ Live Vitals Monitor")
        if all_vitals:
            st.table(pd.DataFrame(all_vitals))
        else:
            st.info("No vitals recorded yet.")

    elif choice == "Med Tracking":
        with st.form("m_form"):
            p_id = st.number_input("Patient ID", min_value=1)
            m_name = st.text_input("Medicine Name")
            stat = st.selectbox("Status", ["Taken", "Missed"])
            if st.form_submit_button("Log"):
                requests.post("http://127.0.0.1:8000/log-medication", json={"patient_id": p_id, "medicine_name": m_name, "status": stat})
                st.success("Logged!")
        st.dataframe(pd.DataFrame(all_logs))

    elif choice == "Record Vitals":
        with st.form("v_form"):
            p_id = st.number_input("Patient ID", min_value=1)
            bp = st.text_input("Blood Pressure")
            hr = st.number_input("Heart Rate", value=72)
            if st.form_submit_button("Save"):
                requests.post("http://127.0.0.1:8000/log-vitals", json={"patient_id": p_id, "blood_pressure": bp, "heart_rate": hr})
                st.success("Saved!")

elif portal == "Doctor Portal":
    if choice == "Dashboard":
        st.subheader("Doctor's Overview")
        st.metric("TOTAL ASSIGNED PATIENTS", len(db_patients))
    
    elif choice == "My Patients":
        st.table(pd.DataFrame(db_patients)[['id', 'full_name', 'age']] if db_patients else "No Patients Found")

    elif choice == "Adherence Reports":
        st.subheader("📋 Patient Adherence History")
        if all_logs:
            st.dataframe(pd.DataFrame(all_logs), use_container_width=True)
        else:
            st.info("No medication logs found.")

elif portal == "Admin Portal":
    if choice == "Dashboard":
        c1, c2 = st.columns(2)
        c1.metric("DOCTORS", len(db_doctors))
        c1.metric("PATIENTS", len(db_patients))
        c2.metric("STAFF", len(db_staff))
        c2.metric("TOTAL LOGS", len(all_logs))
        
    elif choice == "All Doctors":
        st.table(pd.DataFrame(db_doctors)[['id', 'username']] if db_doctors else "No Data")

    elif choice == "All Patients":
        st.table(pd.DataFrame(db_patients)[['id', 'full_name', 'age']] if db_patients else "No Data")

    elif choice == "All Staff":
        st.table(pd.DataFrame(db_staff)[['id', 'username']] if db_staff else "No Data")

    elif choice == "All Records":
        st.subheader("🗄️ Master System Audit")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Medication Records**")
            st.dataframe(pd.DataFrame(all_logs))
        with col2:
            st.write("**Vital Records**")
            st.dataframe(pd.DataFrame(all_vitals))

elif portal == "Patient Portal":
    if choice == "Dashboard":
        st.subheader("My Health Summary")
        try:
            # Assumes viewing data for Patient ID 1
            res = requests.get("http://127.0.0.1:8000/adherence/1").json()
            rate = res.get("rate", 0)
            st.metric("MY ADHERENCE RATE", f"{rate}%")
            st.progress(rate / 100)
            st.write("Keep up the good work!")
        except:
            st.info("Log your first medication to see your score!")

    elif choice == "My Medicines":
        st.subheader("💊 Prescribed Schedule")
        # Filters logs for Patient 1
        my_meds = [l for l in all_logs if l.get('patient_id') == 1]
        if my_meds:
            st.table(pd.DataFrame(my_meds)[['medicine_name', 'status']])
        else:
            st.write("No medicines recorded for you yet.")