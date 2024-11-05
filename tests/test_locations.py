from fastapi import status
from starlette.testclient import TestClient

from app.db import get_database_session
from app.models.organisation import Organisation
from app.models.location import Location


class TestLocationEndpoints:

    def test_locations_do_not_exist(self, test_client: TestClient):
        """
        Test that no locations exist in the database.
        """
        with get_database_session() as database_session:
            organisations_before = database_session.query(Location).all()
            database_session.expunge_all()
        assert len(organisations_before) == 0

    def test_get_locations_by_organisation(self, test_client: TestClient, add_location: Location):
        """
        Test retrieving all locations for an organisation by id.
        """
        response = test_client.get(
            f"/api/organisations/{add_location.organisation_id}/locations")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        print(response.json())
        assert response.json()[0]["location_name"] == add_location.location_name

    def test_get_locations_by_organisation_with_partial_bounding_box(
        self,
        test_client: TestClient,
        add_three_locations: list[Location]
    ):
        """
        Test retrieving all locations that are within a bounding box for an organisation by id.
        The test should work also with only one boundary set.
        """
        response = test_client.get(
            f"/api/organisations/{add_three_locations[0].organisation_id}/locations",
            params={
                "min_longitude": add_three_locations[0].longitude - 1,
                "max_longitude": add_three_locations[0].longitude + 1,
            })
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_get_locations_by_organisation_with_full_bounding_box(
        self,
        test_client: TestClient,
        add_three_locations: list[Location]
    ):
        """
        Test retrieving all locations that are within a bounding box for an organisation by id.
        """
        response = test_client.get(
            f"/api/organisations/{add_three_locations[0].organisation_id}/locations",
            params={
                "min_longitude": add_three_locations[0].longitude - 1,
                "max_longitude": add_three_locations[1].longitude + 1,
                "min_latitude": add_three_locations[0].latitude - 1,
                "max_latitude": add_three_locations[1].latitude + 1
            })
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_create_location(self, test_client, add_organisation: Organisation):
        """
        Test creating a new location.
        """
        location_request = {
            "locationName": "New Location",
            "organisationId": 1,
            "longitude": 0.0,
            "latitude": 0.0
        }
        response = test_client.post(
            "/api/organisations/create/locations",
            json=location_request,
            headers={"Content-Type": "application/json"}
        )
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["organisation_id"] == location_request["organisationId"]

    def test_create_duplicate_location(self, test_client, add_location: Location):
        """
        Creating the same location twice should fail.
        """
        location_request = {
            "locationName": add_location.location_name,
            "organisationId": add_location.organisation_id,
            "longitude": add_location.longitude,
            "latitude": add_location.latitude
        }
        response = test_client.post(
            "/api/organisations/create/locations",
            json=location_request,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == status.HTTP_409_CONFLICT
