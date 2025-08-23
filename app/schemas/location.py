from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class LocationBase(BaseModel):
    name: Optional[str] = None
    # coords: unsupported geometry type, consider storing as WKT string or GeoJSON
    coords: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    createdAt: datetime

    # Relations: use List[int] for related IDs, or List[Donor], etc. if you have those models
    donors: Optional[List[int]] = []
    donations: Optional[List[int]] = []
    bloodRequests: Optional[List[int]] = []

    class Config:
        orm_mode = True