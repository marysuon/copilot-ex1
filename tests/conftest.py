"""
Shared test fixtures and configuration for the FastAPI app tests.

Provides:
- TestClient instance connected to the app
- Fixture to reset activity state between tests
- Sample test data
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making HTTP requests to the app.
    
    This fixture resets the activities state before each test to ensure
    test isolation and prevent state leakage between tests.
    """
    # Reset activities to initial state before each test
    activities.clear()
    activities.update({
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
        "Basketball Team": {
            "description": "Competitive basketball team for intercollegiate tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["jasmine@mergington.edu", "ryan@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["maya@mergington.edu"]
        },
        "Music Band": {
            "description": "Play in the school band and perform at concerts",
            "schedule": "Mondays, 4:30 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "noah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in debate tournaments and develop argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for STEM competitions",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["ethan@mergington.edu", "zoe@mergington.edu"]
        }
    })
    
    return TestClient(app)
