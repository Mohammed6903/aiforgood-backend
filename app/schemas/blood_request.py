from pydantic import BaseModel, Optional
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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    matched_donor: Optional[int] = None
