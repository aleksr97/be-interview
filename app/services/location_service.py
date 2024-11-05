from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.daos.location_dao import LocationDAO
from app.models.location import Location
from app.schemas.location import BoundingBox, CreateLocationRequest, LocationResponse


class LocationService:
    def __init__(self, session: Session):
        self.location_dao = LocationDAO(session=session)

    def get_locations_by_organisation(
        self,
        organisation_id: int,
        min_longitude: Optional[float] = None,
        max_longitude: Optional[float] = None,
        min_latitude: Optional[float] = None,
        max_latitude: Optional[float] = None
    ) -> list[LocationResponse]:
        bounding_box = None
        if any([min_longitude, max_longitude, min_latitude, max_latitude]):
            bounding_box = BoundingBox(
                min_longitude=min_longitude,
                max_longitude=max_longitude,
                min_latitude=min_latitude,
                max_latitude=max_latitude,
            )
        locations = self.location_dao.get_by_organisation(organisation_id=organisation_id, bounding_box=bounding_box)
        return [LocationResponse(
            location_name=location.location_name,
            longitude=location.longitude,
            latitude=location.latitude
        ) for location in locations]

    def create_location(self, location_request: CreateLocationRequest) -> Optional[Location]:
        """Check if the location already exists, if not create a new location."""
        if self.location_dao.get_by_name(
                organisation_id=location_request.organisation_id,
                location_name=location_request.location_name
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Location already exists")

        new_location = Location(
            organisation_id=location_request.organisation_id,
            location_name=location_request.location_name,
            longitude=location_request.longitude,
            latitude=location_request.latitude
        )
        return self.location_dao.create(location=new_location)
