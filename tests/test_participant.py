"""
Tests for DELETE /activities/{activity_name}/participants endpoint.

Tests student removal/unregistration functionality, including success cases and error scenarios.
Uses AAA (Arrange-Act-Assert) pattern for test clarity.
"""


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_participant_successful(self, client):
        """
        Test successful removal of a participant from activity.
        
        ARRANGE: Use an existing participant in an activity
        ACT: Make DELETE request to remove participant
        ASSERT: Verify status 200 and student removed from participants
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]
        
        # Verify student was actually removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_from_nonexistent_activity(self, client):
        """
        Test removal attempt from non-existent activity.
        
        ARRANGE: Prepare email and invalid activity name
        ACT: Make DELETE request with non-existent activity
        ASSERT: Verify status 404 with error message
        """
        # ARRANGE
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant(self, client):
        """
        Test removal of student not signed up for activity.
        
        ARRANGE: Use activity and email that is not in participants
        ACT: Make DELETE request
        ASSERT: Verify status 400 with error message
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "not.signed.up@mergington.edu"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_remove_missing_email_parameter(self, client):
        """
        Test removal without email query parameter.
        
        ARRANGE: Prepare activity name but no email parameter
        ACT: Make DELETE request without email parameter
        ASSERT: Verify status 422 (validation error)
        """
        # ARRANGE
        activity_name = "Tennis Club"
        
        # ACT
        response = client.delete(f"/activities/{activity_name}/participants")
        
        # ASSERT
        assert response.status_code == 422

    def test_remove_multiple_participants_sequentially(self, client):
        """
        Test removing multiple participants from same activity.
        
        ARRANGE: Activity has multiple participants
        ACT: Remove one participant, verify removal, remove another
        ASSERT: Each participant is removed independently
        """
        # ARRANGE
        activity_name = "Chess Club"
        email1 = "michael@mergington.edu"
        email2 = "daniel@mergington.edu"
        
        # Verify both are present
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
        
        # ACT - Remove first participant
        response1 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email1}
        )
        
        # ASSERT - First removal successful
        assert response1.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 not in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
        
        # ACT - Remove second participant
        response2 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email2}
        )
        
        # ASSERT - Second removal successful
        assert response2.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 not in activities[activity_name]["participants"]
        assert email2 not in activities[activity_name]["participants"]

    def test_remove_then_signup_again(self, client):
        """
        Test that removed student can sign up again for activity.
        
        ARRANGE: Use existing participant
        ACT: Remove participant, then sign them up again
        ASSERT: Participant is back in the activity
        """
        # ARRANGE
        activity_name = "Basketball Team"
        email = "alex@mergington.edu"
        
        # ACT - Remove
        response1 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT - Removed
        assert response1.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]
        
        # ACT - Sign up again
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT - Signed up again
        assert response2.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
