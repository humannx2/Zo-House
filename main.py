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
from tasks import als_analysis_task, caregiving_task
from agents import als_agent, caregiving_agent
from tools import csv_tool

# Create the Crew with both agents
als_caregiver_crew = Crew(
    agents=[als_agent, caregiving_agent],
    tasks=[als_analysis_task, caregiving_task],
    verbose=True
)

user_data = {
        "patient_name": "John Doe",
        "age": 65,
        "symptoms": ["Difficulty swallowing", "Muscle weakness", "Fatigue"],
        "mobility_status": "Wheelchair-bound",
        "communication_ability": "Limited speech",
        "medications": ["Riluzole"],
        "caregiver_notes": "Struggles with daily activities, needs assistance with feeding."
    }

als_caregiver_crew.kickoff(inputs={"data":user_data})
