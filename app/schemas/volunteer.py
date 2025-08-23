from pydantic import BaseModel
from typing import Optional

class Volunteer(BaseModel):
    id: int
    user_id: int  # Foreign key to User
    joined_at: Optional[str] = None
    activities: Optional[list] = []  # List of volunteer activities
