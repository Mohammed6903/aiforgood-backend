from google.adk.agents import Agent
from .tools.fetch_nearby import fetch_nearby_donors, fetch_location_info
from google.adk.tools import google_search

root_agent = Agent(
    name="aiforgood_comprehensive_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Comprehensive AI-powered agent for the AIFORGOOD project. "
        "Features include: AI-powered chatbot with message routing, blood bridge coordination, "
        "emergency blood request system, predictive donor engagement, automated FAQ handling; "
        "and an AI-powered blood management system with volunteer/donor dashboard, real-time analytics, "
        "user & donor management, emergency blood tracking, AI-driven reports, donor gamification, "
        "badges, leaderboards, milestones, rewards, and consistent engagement for donor retention. "
        "Includes tools for fetching nearby donors and location information."
    ),
    instruction=(
        "Act as an AI-powered assistant for blood donation and management. "
        "Latitude and longitude will be provided in most requests, but only use them with the fetch_nearby_donors and fetch_location_info tools when the user explicitly asks for it or agrees to use their location. "
        "Use the fetch_nearby_donors tool to locate donors near a specified location keep in mind that radius is in metres, and fetch_location_info to get location details, only if the user requests or consents. "
        "If no donor is found in the initial search, increase the search radius exponentially (e.g., double the radius each time) until a donor is found. "
        "Handle message routing, coordinate blood bridge, process emergency blood requests, "
        "engage donors predictively, and answer FAQs. "
        "Manage donors and volunteers, provide real-time analytics, track emergencies, "
        "generate AI-driven reports, and facilitate donor gamification with badges, leaderboards, "
        "milestones, rewards, and recognition to ensure consistent engagement and retention."
    ),
    tools=[fetch_nearby_donors, fetch_location_info, google_search],
)