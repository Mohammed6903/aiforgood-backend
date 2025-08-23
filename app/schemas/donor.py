from typing import List, Optional
from pydantic import BaseModel
from .donation import Donation
from .location import Location

class Donor(BaseModel):
    id: int
    user_id: int
    blood_type: str
    last_donation_date: Optional[str] = None
    total_donations: int = 0
    location_id: Optional[int] = None
    location: Optional[Location] = None
    donations: Optional[List[Donation]] = []
