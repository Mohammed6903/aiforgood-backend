from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool

root_agent = Agent(
    name="aiforgood_search_agent",
    model="gemini-2.0-flash-exp",
    description="Agent for AIFORGOOD project to answer questions using Google Search.",
    instruction="Use the Google Search tool to find accurate and relevant answers for the AIFORGOOD project.",
    tools=[google_search],
)

