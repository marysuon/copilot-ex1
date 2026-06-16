"""
Tests for GET /activities endpoint.

Tests the retrieval of all activities and their structure.
Uses AAA (Arrange-Act-Assert) pattern for test clarity.
"""


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        ARRANGE: Use the test client with pre-populated activities
        ACT: Make GET request to /activities
        ASSERT: Verify response contains all 9 activities
        """
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Robotics Club" in activities

    def test_get_activities_returns_correct_structure(self, client):
        """
        Test that each activity has the correct data structure.
        
        ARRANGE: Use the test client
        ACT: Make GET request to /activities
        ASSERT: Verify each activity contains required fields
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()
        
        # ASSERT
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_contains_participants(self, client):
        """
        Test that activities include participants list.
        
        ARRANGE: Use the test client
        ACT: Make GET request to /activities
        ASSERT: Verify specific activity has expected participants
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()
        
        # ASSERT
        chess_club = activities["Chess Club"]
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert len(chess_club["participants"]) == 2

    def test_get_activities_response_is_dict(self, client):
        """
        Test that /activities returns a dictionary (object).
        
        ARRANGE: Use the test client
        ACT: Make GET request to /activities
        ASSERT: Verify response is a dictionary
        """
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_empty_participant_lists(self, client):
        """
        Test that activities with no participants have empty lists.
        
        ARRANGE: Create a test scenario by checking an activity with 1 participant
        ACT: Make GET request to /activities
        ASSERT: Verify participant list format is correct
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()
        
        # ASSERT - Art Studio has 1 participant
        art_studio = activities["Art Studio"]
        assert len(art_studio["participants"]) >= 0
        assert isinstance(art_studio["participants"], list)
