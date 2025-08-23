import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI for Good"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/aiforgood")

settings = Settings()
