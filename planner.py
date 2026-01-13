from datetime import datetime
from llm import ask_llm

def generate_plan(tasks):
    prompt = f"""
    You are a smart AI study planner.

    Tasks:
    {tasks}

    Create a day-wise optimized study plan.
    Consider:
    - Deadlines
    - Priority
    - Avoid burnout
    - Balanced schedule

    Output in a clean daily format.
    """

    return ask_llm(prompt)
