from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    id: Optional[int] = None
    user_id: int   # since it's required and unique
    medical_history: Optional[str] = None
    blood_group: str
    age: Optional[int] = None
    gender: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        validate_assignment = True
