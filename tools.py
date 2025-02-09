from crewai_tools import CSVSearchTool
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
# Initialize the CSVSearchTool
csv_tool = CSVSearchTool(csv="bram.csv", api_key=api_key)

