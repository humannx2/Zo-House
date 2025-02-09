# import requests
# import json
# # from reclaim_protocol import ReclaimClient
# import os

# api_id = os.getenv("APP_ID")
# api_secret = os.getenv("APP_SECRET")
# ALS_DATA_URL = "https://dataportal.answerals.org/api/v1/datasets"


# # Function to get OAuth Token from Reclaim API
# def get_reclaim_token():
#     auth_url = "https://api.reclaimprotocol.org/oauth/token"
#     payload = {
#         "grant_type": "client_credentials",
#         "client_id": api_id,
#         "client_secret": api_secret
#     }
    
#     response = requests.post(auth_url, data=payload)
#     try:
#         token_data = response.json()  # Convert response to JSON
#     except requests.exceptions.JSONDecodeError:
#         print("❌ Error: Unable to decode JSON. Check API response.")
#         print("Response Text:", response.text)
#         return None

    
#     if "access_token" in token_data:
#         return token_data["access_token"]
#     else:
#         raise Exception("Failed to retrieve access token")

# def fetch_als_data():
#     token = get_reclaim_token()
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Accept": "application/json"
#     }
    
#     response = requests.get(ALS_DATA_URL, headers=headers)

#     if response.status_code == 200:
#         als_data = response.json()
#         print("✅ Successfully retrieved ALS data:", als_data)
#     else:
#         print(f"❌ Failed to fetch data. Status Code: {response.status_code}")

# # Execute
# fetch_als_data()



from crewai import Crew
from tasks import als_analysis_task, caregiving_task, followup_task
from agents import als_agent, caregiving_agent, followup_agent
from tools import csv_tool
import schedule
import time
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

scheduled_followups = {}

@app.route('/als_caregiver', methods=['POST'])
def als_caregiver():
    try:
        # Get user data from request
        user_data = request.json

        if not user_data:
            return jsonify({"error": "No data provided"}), 400

        # Run CrewAI agents with user input
        result = als_caregiver_crew.kickoff(inputs={"data": user_data})
        result=result.raw
        patient_id = user_data.get("patient_name", "unknown")
        if patient_id not in scheduled_followups:
            schedule_followups(patient_id)

        return jsonify({
            "caregiving_advice": caregiving_plan,
            "message": f"Follow-ups have been scheduled every 10 minutes for {patient_id}."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

als_caregiver_crew = Crew(
    agents=[als_agent, caregiving_agent],
    tasks=[als_analysis_task, caregiving_task],
    verbose=True
)



def schedule_followups(patient_id):
    """Schedule follow-up questions for a specific patient."""
    if patient_id in scheduled_followups:
        return

    def run_followup():
        result = followup_crew.kickoff()
        print(f"💬 Follow-up question for {patient_id}: {result.raw}")

    # Schedule the follow-up task every 10 minutes
    schedule.every(10).minutes.do(run_followup)
    scheduled_followups[patient_id] = True
    print(f"✅ Follow-ups scheduled for {patient_id}.")

# Function to continuously check and run scheduled tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in a separate thread
threading.Thread(target=run_scheduler, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)

# user_data = {
#         "patient_name": "John Doe",
#         "age": 65,
#         "symptoms": ["Difficulty swallowing", "Muscle weakness", "Fatigue"],
#         "mobility_status": "Wheelchair-bound",
#         "communication_ability": "Limited speech",
#         "medications": ["Riluzole"],
#         "caregiver_notes": "Struggles with daily activities, needs assistance with feeding."
#     }

# als_caregiver_crew.kickoff(inputs={"data":user_data})


