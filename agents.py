from crewai import Agent,LLM
from tools import csv_tool
from dotenv import load_dotenv
import os
load_dotenv()

# api_key = os.environ.get("GROQ_API_KEY")
# llm = LLM(model="groq/llama3-8b-8192", temperature=0.7, api_key=api_key)

api_key = os.environ.get("OPENAI_API_KEY")
llm = LLM(model="gpt-4o-mini", temperature=0.7, api_key=api_key)

# Define the AI Agent
als_agent = Agent(
    role="ALS Data Analyst",

    goal="Analyze and extract insights from the ALS dataset to help caregivers",
    tools=[csv_tool],
    backstory=(
        "A data expert specializing in ALS research, dedicated to extracting "
        "useful information for patient care and medical research."
    ),
    verbose=True,
    llm=llm
)

caregiving_agent = Agent(
    role="Caregiver Assistant",
    goal="Provide tailored caregiving advice for ALS patients based onthe following symptoms {data} and dataset insights provided by the ALS analyst",
    backstory=("A virtual caregiver assistant that helps family members and healthcare professionals "
              "by providing personalized caregiving recommendations based on patient data."),
    verbose=True,
    llm=llm
)

followup_agent = Agent(
    role="Follow-Up Assistant",
    goal="Ask the patient or caregiver follow-up questions based on previous responses.",
    backstory="A dedicated assistant designed to check on ALS patients regularly and collect additional caregiving data.",
    verbose=True,
    llm=llm
)




