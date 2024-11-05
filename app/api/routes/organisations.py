from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_db
from app.models.organisation import Organisation
from app.schemas.organisation import CreateOrganisationRequest
from app.services.organisation_service import OrganisationService

router = APIRouter()


def get_organisation_service(session: Session = Depends(get_db)) -> OrganisationService:
    return OrganisationService(session=session)


@router.post("/create", response_model=Organisation)
def create_organisation(
    create_organisation_request: CreateOrganisationRequest,
    organisation_service: OrganisationService = Depends(get_organisation_service)
):
    """Create an organisation."""
    return organisation_service.create_organisation(organisation_request=create_organisation_request)


@router.get("/", response_model=list[Organisation])
def get_organisations(organisation_service: OrganisationService = Depends(get_organisation_service)):
    """Get all organisations."""
    return organisation_service.get_all_organisations()


@router.get("/{organisation_id}", response_model=Organisation)
def get_organisation(
    organisation_id: int,
    organisation_service: OrganisationService = Depends(get_organisation_service)
):
    """Get an organisation by id."""
    return organisation_service.get_organisation_by_id(organisation_id=organisation_id)
