from typing import Optional

from pydantic import BaseModel

from app.schemas.standard_model import StandardModel


class CreateLocationRequest(StandardModel):
    location_name: str
    organisation_id: int
    longitude: float
    latitude: float

    class Config:
        extra = "forbid"


class LocationResponse(BaseModel):
    location_name: str
    longitude: float
    latitude: float

    class Config:
        orm_mode = True
        from_attributes = True


class BoundingBox(BaseModel):
    min_longitude: Optional[float] = None
    min_latitude: Optional[float] = None
    max_longitude: Optional[float] = None
    max_latitude: Optional[float] = None
