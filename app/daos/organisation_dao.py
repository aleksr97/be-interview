from typing import Optional

from sqlmodel import Session, select
from app.models.organisation import Organisation


class OrganisationDAO:
    def __init__(self, session: Session):
        self.session = session

    def create(self, organisation: Organisation) -> Organisation:
        self.session.add(organisation)
        self.session.commit()
        self.session.refresh(organisation)
        return organisation

    def get_all(self) -> list[Organisation]:
        return list(self.session.exec(select(Organisation)).all())

    def get_by_id(self, organisation_id: int) -> Optional[Organisation]:
        return self.session.get(Organisation, organisation_id)
