"""
Tests for POST /activities/{activity_name}/signup endpoint.

Tests student signup functionality, including success cases and various error scenarios.
Uses AAA (Arrange-Act-Assert) pattern for test clarity.
"""


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """
        Test successful signup for an activity.
        
        ARRANGE: Prepare email and activity name for new signup
        ACT: Make POST request to signup endpoint
        ASSERT: Verify status 200 and student added to participants
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "new.student@mergington.edu"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        
        # Verify student was actually added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """
        Test signup attempt for non-existent activity.
        
        ARRANGE: Prepare email and invalid activity name
        ACT: Make POST request with non-existent activity
        ASSERT: Verify status 404 with error message
        """
        # ARRANGE
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student(self, client):
        """
        Test signup attempt when student is already signed up.
        
        ARRANGE: Use an existing participant in Chess Club
        ACT: Make POST request with same email
        ASSERT: Verify status 400 with error message
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_missing_email_parameter(self, client):
        """
        Test signup without email query parameter.
        
        ARRANGE: Prepare activity name but no email parameter
        ACT: Make POST request without email parameter
        ASSERT: Verify status 422 (validation error)
        """
        # ARRANGE
        activity_name = "Tennis Club"
        
        # ACT
        response = client.post(f"/activities/{activity_name}/signup")
        
        # ASSERT
        assert response.status_code == 422

    def test_signup_multiple_students_same_activity(self, client):
        """
        Test multiple different students signing up for the same activity.
        
        ARRANGE: Prepare two different emails
        ACT: Sign up first student, then second student
        ASSERT: Both are added to participants list
        """
        # ARRANGE
        activity_name = "Art Studio"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # ACT
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_signup_different_activities_same_student(self, client):
        """
        Test same student signing up for different activities.
        
        ARRANGE: Prepare same email and two different activities
        ACT: Sign up for first activity, then second activity
        ASSERT: Student is in participants for both activities
        """
        # ARRANGE
        email = "multi.student@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Tennis Club"
        
        # ACT
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
