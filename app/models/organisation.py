from app.models.base import Base
from sqlmodel import Field


class Organisation(Base, table=True):
    id: int | None = Field(primary_key=True)
    name: str
