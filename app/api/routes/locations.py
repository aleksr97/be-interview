from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_db
from app.models.location import Location
from app.schemas.location import CreateLocationRequest, LocationResponse
from app.services.location_service import LocationService
from app.services.organisation_service import OrganisationService

router = APIRouter()


def get_location_service(session: Session = Depends(get_db)) -> LocationService:
    return LocationService(session=session)


def get_organisation_service(session: Session = Depends(get_db)) -> OrganisationService:
    return OrganisationService(session=session)


@router.post("/create/locations", response_model=Location)
def create_location(
    create_location_request: CreateLocationRequest,
    location_service: LocationService = Depends(get_location_service),
    organisation_service: OrganisationService = Depends(get_organisation_service)
):
    """Check if the organisation exists and create a new location."""
    organisation = organisation_service.get_organisation_by_id(organisation_id=create_location_request.organisation_id)
    return location_service.create_location(location_request=create_location_request)


@router.get("/{organisation_id}/locations", response_model=list[LocationResponse])
def get_organisation_locations(
    organisation_id: int,
    min_longitude: Optional[float] = None,
    max_longitude: Optional[float] = None,
    min_latitude: Optional[float] = None,
    max_latitude: Optional[float] = None,
    location_service: LocationService = Depends(get_location_service),
):
    """Get all locations for an organisation."""
    return location_service.get_locations_by_organisation(
        organisation_id=organisation_id,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
        min_latitude=min_latitude,
        max_latitude=max_latitude
    )
