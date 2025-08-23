from pydantic import BaseModel, EmailStr
from typing import Optional, List
from badge import Badge

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    city: str
    state: str
    country: str
    role: str  # Donor, Patient, Volunteer, Admin
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    donor: Optional[dict] = None
    volunteer: Optional[dict] = None
    patient: Optional[dict] = None
    badges: Optional[List[Badge]] = []
    leaderboard: Optional[List[dict]] = []
    bloodRequests: Optional[List[dict]] = []
    engagements: Optional[List[dict]] = []

    # Remove fields not present in the schema
