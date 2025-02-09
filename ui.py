import streamlit as st
import requests
import json

# Flask API endpoint
FLASK_API_URL = "http://127.0.0.1:5000/als_caregiver"

# Streamlit UI layout
st.set_page_config(page_title="ALS Caregiver Assistant", layout="centered")

st.title("🩺 ALS Caregiving Advice Assistant")
st.write("Enter patient details below, and receive personalized caregiving recommendations.")

# Form for user input
with st.form("user_input_form"):
    patient_name = st.text_input("Patient Name", placeholder="John Doe")
    age = st.number_input("Age", min_value=18, max_value=120, value=65, step=1)
    symptoms = st.multiselect("Symptoms", 
                              ["Muscle weakness", "Difficulty swallowing", "Fatigue",
                               "Breathing difficulty", "Speech issues", "Loss of coordination"])
    mobility_status = st.selectbox("Mobility Status", ["Can walk independently", 
                                                       "Uses a walker", 
                                                       "Wheelchair-bound", 
                                                       "Completely bedridden"])
    communication_ability = st.selectbox("Communication Ability", ["Normal speech", 
                                                                   "Mild speech difficulty", 
                                                                   "Limited speech", 
                                                                   "Uses a speech device"])
    medications = st.text_input("Medications (comma-separated)", placeholder="Riluzole, Edaravone")
    caregiver_notes = st.text_area("Caregiver Notes", placeholder="Mention any specific caregiving challenges.")

    submit = st.form_submit_button("Get Caregiving Advice")

# Process the form on submission
if submit:
    # Convert user input into JSON format
    user_data = {
        "patient_name": patient_name,
        "age": age,
        "symptoms": symptoms,
        "mobility_status": mobility_status,
        "communication_ability": communication_ability,
        "medications": [med.strip() for med in medications.split(",") if med.strip()],
        "caregiver_notes": caregiver_notes
    }

    st.info("⏳ Processing... Please wait.")

    # Send data to the Flask API
    try:
        response = requests.post(FLASK_API_URL, json=user_data)
        
        if response.status_code == 200:
            caregiving_advice = response.json().get("caregiving_advice", "No advice generated.")
            st.success("✅ Caregiving Advice Generated Successfully!")
            st.write(f"### 🏥 Recommended Care Plan for **{patient_name}**")
            st.write(caregiving_advice)
        else:
            st.error(f"❌ Error: {response.json().get('error', 'Something went wrong!')}")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API Connection Error: {e}")
