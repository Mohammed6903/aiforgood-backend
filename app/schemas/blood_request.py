from pydantic import BaseModel, Optional

class BloodRequest(BaseModel):
    id: int
    requester_id: int
    blood_type: str
    status: str
    requested_at: Optional[str] = None
    fulfilled_at: Optional[str] = None
