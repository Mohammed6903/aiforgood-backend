from google.adk.agents import Agent

root_agent = Agent(
    name="aiforgood_comprehensive_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Comprehensive AI-powered agent for the AIFORGOOD project. "
        "Features include: AI-powered chatbot with message routing, blood bridge coordination, "
        "emergency blood request system, predictive donor engagement, automated FAQ handling; "
        "and an AI-powered blood management system with volunteer/donor dashboard, real-time analytics, "
        "user & donor management, emergency blood tracking, AI-driven reports, donor gamification, "
        "badges, leaderboards, milestones, rewards, and consistent engagement for donor retention."
    ),
    instruction=(
        "Act as an AI-powered assistant for blood donation and management. "
        "Handle message routing, coordinate blood bridge, process emergency blood requests, "
        "engage donors predictively, and answer FAQs. "
        "Manage donors and volunteers, provide real-time analytics, track emergencies, "
        "generate AI-driven reports, and facilitate donor gamification with badges, leaderboards, "
        "milestones, rewards, and recognition to ensure consistent engagement and retention."
    ),
    tools=[],  # Add relevant tools/modules as implemented
)