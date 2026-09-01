"""
Integration tests for activity endpoints: GET /activities, POST /activities/{activity_name}/signup, 
and DELETE /activities/{activity_name}/signup.

All tests follow the AAA (Arrange-Act-Assert) pattern for clarity:
- Arrange: Set up test data and preconditions using fixtures
- Act: Execute the endpoint being tested
- Assert: Verify the response status, data, and side effects
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test: GET /activities returns all available activities
        
        Arrange: client fixture is provided
        Act: Make GET request to /activities
        Assert: Status is 200 and response contains all activities
        """
        # Arrange (implicit via fixtures)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9  # All 9 activities from app.py
        assert "Chess Club" in data
        assert "Programming Class" in data


    def test_get_activities_returns_activity_details(self, client):
        """
        Test: GET /activities returns complete activity details
        
        Arrange: client fixture is provided
        Act: Make GET request to /activities
        Assert: Response contains all required fields per activity
        """
        # Arrange (implicit via fixtures)
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        for activity_name, activity in data.items():
            assert all(field in activity for field in required_fields), \
                f"Activity {activity_name} missing required fields"


class TestPostSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_happy_path(self, client, test_email_new):
        """
        Test: Student can successfully sign up for an activity
        
        Arrange: New test email (not already signed up)
        Act: POST to signup endpoint with activity name and email
        Assert: Status is 200, success message returned, student in participants
        """
        # Arrange
        activity_name = "Chess Club"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_new}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify student was added
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        assert updated_count == initial_count + 1


    def test_signup_nonexistent_activity_returns_404(self, client, test_email_new):
        """
        Test: Signup fails with 404 when activity doesn't exist
        
        Arrange: Nonexistent activity name
        Act: POST to signup endpoint with invalid activity name
        Assert: Status is 404 and error detail indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_new}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


    def test_signup_duplicate_student_returns_400(self, client, test_email_existing):
        """
        Test: Signup fails with 400 when student already signed up
        
        Arrange: Email already in participants list for Chess Club
        Act: POST to signup endpoint with duplicate email
        Assert: Status is 400 and error indicates duplicate signup
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_existing}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


    def test_signup_multiple_activities_same_student(self, client, test_email_new):
        """
        Test: Student can sign up for multiple different activities
        
        Arrange: New test email
        Act: POST to signup for two different activities
        Assert: Both signups succeed with 200 status
        """
        # Arrange
        activities = ["Chess Club", "Programming Class"]
        
        # Act & Assert
        for activity_name in activities:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": test_email_new}
            )
            assert response.status_code == 200


class TestDeleteSignup:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_delete_signup_happy_path(self, client, test_email_existing):
        """
        Test: Student can successfully unregister from an activity
        
        Arrange: Email already in participants list for Chess Club
        Act: DELETE from signup endpoint with activity name and email
        Assert: Status is 200, success message returned, student removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_existing}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify student was removed
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        assert updated_count == initial_count - 1


    def test_delete_from_nonexistent_activity_returns_404(self, client, test_email_new):
        """
        Test: Delete fails with 404 when activity doesn't exist
        
        Arrange: Nonexistent activity name
        Act: DELETE from signup endpoint with invalid activity name
        Assert: Status is 404 and error detail indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_new}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


    def test_delete_not_signed_up_student_returns_400(self, client, test_email_new):
        """
        Test: Delete fails with 400 when student not signed up for activity
        
        Arrange: Email not in any participants list
        Act: DELETE from signup endpoint with non-participant email
        Assert: Status is 400 and error indicates student not signed up
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_new}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]


    def test_delete_then_resign_up_happy_path(self, client, test_email_existing):
        """
        Test: Student can unregister and then re-register for same activity
        
        Arrange: Email in Chess Club participants
        Act: DELETE then POST signup for same activity
        Assert: Both operations succeed with 200 status
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act - Delete
        response_delete = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_existing}
        )
        assert response_delete.status_code == 200
        
        # Act - Re-signup
        response_signup = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email_existing}
        )
        
        # Assert
        assert response_signup.status_code == 200
