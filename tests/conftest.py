"""
Pytest configuration and fixtures for the Mergington High School API tests.

Fixtures provide reusable test setup following the AAA pattern:
- Arrange: Fixtures set up the TestClient and fresh test data
- Act: Tests call endpoints using the client
- Assert: Tests verify responses
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture: Resets the activities dictionary before each test.
    
    This ensures test isolation by resetting the global activities state,
    preventing tests from affecting each other. This autouse fixture runs
    before every test automatically.
    """
    # Reset to initial state
    app_module.activities.clear()
    app_module.activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Team sport with competitive play and skill development",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer": {
            "description": "Outdoor soccer matches and training",
            "schedule": "Tuesdays and Fridays, 3:45 PM - 5:15 PM",
            "max_participants": 22,
            "participants": ["james@mergington.edu", "lucy@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting workshops",
            "schedule": "Mondays and Wednesdays, 4:15 PM - 5:45 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "STEM experiments and scientific research projects",
            "schedule": "Thursdays, 3:45 PM - 5:15 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        }
    })
    yield
    # Cleanup after test (optional, but good practice)
    app_module.activities.clear()


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for testing FastAPI endpoints.
    
    This allows tests to make HTTP requests without running a server.
    The TestClient uses dependency injection to allow mocking if needed.
    """
    return TestClient(app_module.app)


@pytest.fixture
def sample_activities_data():
    """
    Fixture: Provides sample activities data for testing.
    
    This includes various activities with different participant counts
    and max capacity levels to support comprehensive test scenarios.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Team sport with competitive play and skill development",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        }
    }


@pytest.fixture
def test_email_new():
    """Fixture: Provides an email address not yet signed up for any activity."""
    return "test.student@mergington.edu"


@pytest.fixture
def test_email_existing():
    """Fixture: Provides an email address already signed up for Chess Club."""
    return "michael@mergington.edu"
