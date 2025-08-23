from pydantic import BaseModel
from typing import Optional

class LeaderboardEntry(BaseModel):
    id: int
    user_id: int  # Foreign key to User
    rank: int
    score: float
