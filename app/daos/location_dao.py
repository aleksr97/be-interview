from typing import Optional

from sqlmodel import Session, select
from app.models.location import Location
from app.schemas.location import BoundingBox


class LocationDAO:
    def __init__(self, session: Session):
        self.session = session

    def create(self, location: Location) -> Location:
        self.session.add(location)
        self.session.commit()
        self.session.refresh(location)
        return location

    def get_by_organisation(
        self,
        organisation_id: int,
        bounding_box: Optional[BoundingBox] = None
    ) -> list[Location]:
        query = select(Location).where(Location.organisation_id == organisation_id)

        if bounding_box:
            if bounding_box.min_longitude:
                query = query.where(Location.longitude >= bounding_box.min_longitude)
            if bounding_box.max_longitude:
                query = query.where(Location.longitude <= bounding_box.max_longitude)
            if bounding_box.min_latitude:
                query = query.where(Location.latitude >= bounding_box.min_latitude)
            if bounding_box.max_latitude:
                query = query.where(Location.latitude <= bounding_box.max_latitude)

        locations = list(self.session.exec(query).all())
        return locations

    def get_by_name(self, organisation_id: int, location_name: str) -> Optional[Location]:
        query = select(Location).where(
            Location.organisation_id == organisation_id,
            Location.location_name == location_name
        )
        result = self.session.exec(query).first()
        return result
