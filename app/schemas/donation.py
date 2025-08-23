from typing import Optional
from pydantic import BaseModel

class Donation(BaseModel):
    id: int
    donor_id: int
    date: str
    blood_type: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None