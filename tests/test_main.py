"""
Tests for the root endpoint GET /.

All tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the endpoint being tested
- Assert: Verify the response and behavior
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """
        Test: GET / redirects to the frontend static files
        
        Arrange: client fixture is provided
        Act: Make GET request to / with follow_redirects=False to capture redirect
        Assert: Status is 307 (Temporary Redirect) and Location header points to /static/index.html
        """
        # Arrange (implicit via fixtures)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


    def test_root_redirect_location_is_correct(self, client):
        """
        Test: GET / redirect points to correct static file path
        
        Arrange: client fixture is provided
        Act: Make GET request to / and follow redirects
        Assert: Final response is successful (200) and contains HTML content
        """
        # Arrange (implicit via fixtures)
        
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        # The response should contain HTML content from index.html
        assert "text/html" in response.headers.get("content-type", "")
