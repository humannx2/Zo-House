from crewai import Task
from agents import als_agent, caregiving_agent, followup_agent
als_analysis_task = Task(
    description="Analyze the ALS dataset and identify key patterns in disease progression.",
    agent=als_agent,
    expected_output=(
        "A summary of key trends in ALS patient data, including severity levels, "
        "common symptoms, and disease progression patterns."
    )
)

caregiving_task = Task(
    description="Based on dataset insights from the ALS analyst and user-provided patient data, provide caregiving advice in 5 points.",
    agent=caregiving_agent,
    expected_output="Personalized caregiving advice including daily care routines, symptom management, and emergency guidelines."
)

from agents import followup_agent

followup_task = Task(
    description="Ask follow-up questions based on previous caregiving advice and responses.",
    agent=followup_agent,
    expected_output="A structured follow-up question set based on the patient's condition."
) 