from fastapi import FastAPI
from app.api import chatbot, blood_management, auth

app = FastAPI(title="AI for Good - Blood Management & Chatbot")

# Include routers
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(blood_management.router, prefix="/blood", tags=["Blood Management"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Welcome to AI for Good API"}
