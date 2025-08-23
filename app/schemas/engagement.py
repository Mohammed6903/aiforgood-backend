from pydantic import BaseModel
from typing import Optional

class Engagement(BaseModel):
    id: int
    user_id: int  # Foreign key to User
    engagement_score: float
    last_active: Optional[str] = None
    activity_log: Optional[list] = []
