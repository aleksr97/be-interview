from http.client import HTTPException
from typing import Optional
from fastapi import HTTPException, status
from sqlmodel import Session
from app.daos.organisation_dao import OrganisationDAO
from app.models.organisation import Organisation
from app.schemas.organisation import CreateOrganisationRequest


class OrganisationService:
    def __init__(self, session: Session):
        self.organisation_dao = OrganisationDAO(session=session)

    def get_organisation_by_id(self, organisation_id: int) -> Optional[Organisation]:
        organisation = self.organisation_dao.get_by_id(organisation_id=organisation_id)
        if not organisation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
        return organisation

    def get_all_organisations(self) -> list[Organisation]:
        return self.organisation_dao.get_all()

    def create_organisation(self, organisation_request: CreateOrganisationRequest) -> Organisation:
        new_organisation = Organisation(name=organisation_request.name)
        return self.organisation_dao.create(organisation=new_organisation)
