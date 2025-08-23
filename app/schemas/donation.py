from typing import Optional
from pydantic import BaseModel
from .location import Location

class Donation(BaseModel):
    id: int
    donor_id: int
    quantity: int
    date: str  # Consider using datetime if you want to match DateTime type
    blood_type: str
    notes: Optional[str] = None
    location_id: Optional[Location] = None
