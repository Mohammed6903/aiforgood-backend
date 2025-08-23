from fastapi import FastAPI
from app.api import chatbot, blood_management

app = FastAPI(title="AI for Good - Blood Management & Chatbot")

# Include routers
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(blood_management.router, prefix="/blood", tags=["Blood Management"])

@app.get("/")
def root():
    return {"message": "Welcome to AI for Good API"}
