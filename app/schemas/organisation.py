from app.schemas.standard_model import StandardModel


class CreateOrganisationRequest(StandardModel):
    name: str
