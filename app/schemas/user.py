from pydantic import BaseModel, EmailStr
from typing import Optional, List 
from badge import Badge

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    blood_type: Optional[str] = None
    is_donor: bool = False
    is_volunteer: bool = False
    last_donation_date: Optional[str] = None
    total_donations: int = 0
    badges: Optional[List[Badge]] = []
    leaderboard_rank: Optional[int] = None
    rewards: Optional[List[str]] = []
    engagement_score: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
