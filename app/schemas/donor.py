from typing import List, Optional
from pydantic import BaseModel
from donation import Donation

class Donor(BaseModel):
    id: int
    user_id: int
    blood_type: str
    last_donation_date: Optional[str] = None
    total_donations: int = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    donations: Optional[List['Donation']] = []
