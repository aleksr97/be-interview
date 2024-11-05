from pathlib import Path
from typing import Generator
from unittest.mock import patch
from uuid import uuid4
import alembic.command
import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.db import get_database_session
from app.main import app
from app.models.location import Location
from app.models.organisation import Organisation

_ALEMBIC_INI_PATH = Path(__file__).parent.parent / "alembic.ini"


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def apply_alembic_migrations() -> Generator[None, None, None]:
    # Creates test database per test function
    test_db_file_name = f"test_{uuid4()}.db"
    database_path = Path(test_db_file_name)
    try:
        test_db_url = f"sqlite:///{test_db_file_name}"
        alembic_cfg = alembic.config.Config(_ALEMBIC_INI_PATH)
        alembic_cfg.attributes["sqlalchemy_url"] = test_db_url
        alembic.command.upgrade(alembic_cfg, "head")
        test_engine = create_engine(test_db_url, echo=True)
        with patch("app.db.get_engine") as mock_engine:
            mock_engine.return_value = test_engine
            yield
    finally:
        database_path.unlink(missing_ok=True)


@pytest.fixture
def add_organisation() -> Organisation:
    """Fixture to add an organisation directly to the database."""
    with get_database_session() as session:
        new_organisation = Organisation(name="organisation_a")
        session.add(new_organisation)
        session.commit()
        session.refresh(new_organisation)  # Get the latest state of the object
    return new_organisation


@pytest.fixture
def add_location(add_organisation: Organisation) -> Location:
    """Fixture to add a location directly to the database."""
    with get_database_session() as session:
        new_location = Location(
            location_name="location_a",
            organisation_id=add_organisation.id,
            longitude=50.0,
            latitude=25.0)
        session.add(new_location)
        session.commit()
        session.refresh(new_location)  # Get the latest state of the object
    return new_location


@pytest.fixture
def add_three_locations(add_organisation: Organisation) -> list[Location]:
    """Fixture to add three different locations directly to the database."""
    with get_database_session() as session:
        new_locations = [
            Location(
                location_name="location_a",
                organisation_id=add_organisation.id,
                longitude=10.0,
                latitude=10.0),
            Location(
                location_name="location_b",
                organisation_id=add_organisation.id,
                longitude=20.0,
                latitude=20.0),
            Location(
                location_name="location_c",
                organisation_id=add_organisation.id,
                longitude=30.0,
                latitude=30.0)
        ]
    session.add_all(new_locations)
    session.commit()
    for location in new_locations:
        session.refresh(location)
    return new_locations
