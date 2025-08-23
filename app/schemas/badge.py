from pydantic import BaseModel
from typing import Optional

class Badge(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int  # Foreign key to User
    awarded_at: Optional[str] = None
