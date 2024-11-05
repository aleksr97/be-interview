from app.models.organisation import Organisation
from app.models.base import Base
from sqlmodel import Field, Relationship


class Location(Base, table=True):
    id: int | None = Field(primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship()
    location_name: str
    longitude: float
    latitude: float
