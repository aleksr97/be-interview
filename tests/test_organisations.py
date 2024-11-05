from fastapi import status

from app.db import get_database_session
from app.models.organisation import Organisation


class TestOrganisationEndpoints:

    def test_organisations_do_not_exist(self, test_client):
        """Test that no organisations exist in the database."""
        with get_database_session() as database_session:
            organisations_before = database_session.query(Organisation).all()
            database_session.expunge_all()
        assert len(organisations_before) == 0

    def test_create_organisation(self, test_client):
        """Test creating a new organisation."""
        organisation_request = {"name": "New Organisation"}
        response = test_client.post(
            "/api/organisations/create",
            json=organisation_request,
            headers={"Content-Type": "application/json"}
        )
        with get_database_session() as database_session:
            organisations_after = database_session.query(Organisation).all()
            database_session.expunge_all()
        assert len(organisations_after) == 1
        assert organisations_after[0].name == organisation_request["name"]
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == organisation_request["name"]

    def test_get_organisations(self, test_client, add_organisation):
        """Test retrieving all organisations."""
        response = test_client.get("/api/organisations")
        organisations = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(organisations) == 1
        assert organisations[0]["name"] == add_organisation.name

    def test_get_organisation_by_id(self, test_client, add_organisation):
        """Test retrieving an organisation by id."""
        response = test_client.get(f"/api/organisations/{add_organisation.id}")
        organisation = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert organisation["name"] == add_organisation.name

    def test_get_organisation_by_invalid_id(self, test_client):
        """Test retrieving an organisation by invalid id."""
        response = test_client.get("/api/organisations/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
