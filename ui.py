# import streamlit as st
# import requests
# import json

# # Flask API endpoint
# FLASK_API_URL = "http://127.0.0.1:5000/als_caregiver"

# # Streamlit UI layout
# st.set_page_config(page_title="ALS Caregiver Assistant", layout="centered")

# st.title("🩺 ALS Caregiving Advice Assistant")
# st.write("Enter patient details below, and receive personalized caregiving recommendations.")

# # Form for user input
# with st.form("user_input_form"):
#     patient_name = st.text_input("Patient Name", placeholder="John Doe")
#     age = st.number_input("Age", min_value=18, max_value=120, value=65, step=1)
#     symptoms = st.multiselect("Symptoms", 
#                               ["Muscle weakness", "Difficulty swallowing", "Fatigue",
#                                "Breathing difficulty", "Speech issues", "Loss of coordination"])
#     mobility_status = st.selectbox("Mobility Status", ["Can walk independently", 
#                                                        "Uses a walker", 
#                                                        "Wheelchair-bound", 
#                                                        "Completely bedridden"])
#     communication_ability = st.selectbox("Communication Ability", ["Normal speech", 
#                                                                    "Mild speech difficulty", 
#                                                                    "Limited speech", 
#                                                                    "Uses a speech device"])
#     medications = st.text_input("Medications (comma-separated)", placeholder="Riluzole, Edaravone")
#     caregiver_notes = st.text_area("Caregiver Notes", placeholder="Mention any specific caregiving challenges.")

#     submit = st.form_submit_button("Get Caregiving Advice")

# # Process the form on submission
# if submit:
#     # Convert user input into JSON format
#     user_data = {
#         "patient_name": patient_name,
#         "age": age,
#         "symptoms": symptoms,
#         "mobility_status": mobility_status,
#         "communication_ability": communication_ability,
#         "medications": [med.strip() for med in medications.split(",") if med.strip()],
#         "caregiver_notes": caregiver_notes
#     }

#     st.info("⏳ Processing... Please wait.")

#     # Send data to the Flask API
#     try:
#         response = requests.post(FLASK_API_URL, json=user_data)
        
#         if response.status_code == 200:
#             caregiving_advice = response.json().get("caregiving_advice", "No advice generated.")
#             st.success("✅ Caregiving Advice Generated Successfully!")
#             st.write(f"### 🏥 Recommended Care Plan for **{patient_name}**")
#             st.write(caregiving_advice)
#         else:
#             st.error(f"❌ Error: {response.json().get('error', 'Something went wrong!')}")

#     except requests.exceptions.RequestException as e:
#         st.error(f"⚠️ API Connection Error: {e}")


import streamlit as st
import requests
import json
import time
from streamlit_chat import message

# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/als_caregiver"

st.set_page_config(page_title="ALS Caregiver Assistant", layout="centered")

st.title("🩺 ALS Caregiving Advice Assistant")
st.write("Enter patient details below to receive caregiving recommendations.")

# Session state for tracking caregiving advice and follow-up chat
if "caregiving_plan" not in st.session_state:
    st.session_state.caregiving_plan = None
if "followup_chat" not in st.session_state:
    st.session_state.followup_chat = []
if "followup_active" not in st.session_state:
    st.session_state.followup_active = False

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

# Process form submission
if submit:
    user_data = {
        "patient_name": patient_name,
        "age": age,
        "symptoms": symptoms,
        "mobility_status": mobility_status,
        "communication_ability": communication_ability,
        "medications": [med.strip() for med in medications.split(",") if med.strip()],
        "caregiver_notes": caregiver_notes
    }

    st.info("⏳ Processing caregiving advice... Please wait.")
    
    try:
        response = requests.post(FLASK_API_URL, json=user_data)

        if response.status_code == 200:
            response_data = response.json()
            caregiving_advice = response_data.get("caregiving_advice", "No advice generated.")
            followup_question = response_data.get("followup_question", None)

            st.success("✅ Caregiving Plan Generated!")
            st.session_state.caregiving_plan = caregiving_advice

            # Display caregiving advice
            st.write(f"### 🏥 Recommended Care Plan for **{patient_name}**")
            st.write(caregiving_advice)

            # Activate follow-ups
            if followup_question:
                st.session_state.followup_active = True
                chat_id = len(st.session_state.followup_chat) + 1
                st.session_state.followup_chat.append({"id": chat_id, "role": "agent", "content": followup_question})

        else:
            st.error(f"❌ Error: {response.json().get('error', 'Something went wrong!')}")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API Connection Error: {e}")

# Follow-up Chat Window (Only Appears After Follow-Up Starts)
if st.session_state.followup_active:
    st.subheader("💬 Follow-Up Chat")

    # Display chat messages
    for chat in st.session_state.followup_chat:
        if chat["role"] == "agent":
            message(chat["content"], key=f"agent_{chat['id']}", avatar_style="bottts")
        else:
            message(chat["content"], is_user=True, key=f"user_{chat['id']}", avatar_style="thumbs")

    # Input field for user response
    user_response = st.text_input("Your Response:", key="followup_response")

    if st.button("Send Response"):
        if user_response.strip():
            chat_id = len(st.session_state.followup_chat) + 1
            st.session_state.followup_chat.append({"id": chat_id, "role": "user", "content": user_response})
            st.success("✅ Response sent!")

            # Send user response back to the API
            try:
                response = requests.post(FLASK_API_URL, json={"user_response": user_response})
                if response.status_code == 200:
                    st.info("💡 Your response has been recorded!")
                else:
                    st.warning("⚠️ Unable to save response.")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ API Error: {e}")


