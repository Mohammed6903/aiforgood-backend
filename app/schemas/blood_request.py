from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class BloodRequest(BaseModel):
    id: int
    requester_id: int
    blood_type: str
    urgency: str
    status: str
    requested_at: Optional[str] = None
    fulfilled_at: Optional[str] = None
    matched_donor_id: Optional[int] = None
    location_id: Optional[int] = None
