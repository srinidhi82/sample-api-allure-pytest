"""Unit tests for the sample API.

These tests exercise the POST, GET and PUT endpoints exposed by the FastAPI
application defined in `app.main`. The tests use FastAPI's `TestClient`
utility, which wraps the application in a WSGI environment and allows
synchronous HTTP calls. Allure decorators are used to provide metadata
about each test, which will appear in generated reports when using the
allure-pytest plugin.
"""

import allure
from fastapi.testclient import TestClient

from app.main import app


# Create a client that can be used to interact with the FastAPI application.
client = TestClient(app)


@allure.title("Create an item via POST request")
@allure.description("This test verifies that a POST request to create a new item "
                    "returns the correct status code and payload.")
def test_create_item() -> None:
    """Ensure that the POST endpoint successfully creates a new item."""
    payload = {"name": "Widget", "description": "A useful widget"}
    response = client.post("/items/1", json=payload)
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, **payload}


@allure.title("Retrieve an item via GET request")
@allure.description("This test confirms that an existing item can be retrieved via GET.")
def test_read_item() -> None:
    """Ensure that the GET endpoint returns an item previously created."""
    # First create the item
    payload = {"name": "Gadget", "description": "A fancy gadget"}
    client.post("/items/2", json=payload)
    # Then retrieve it
    response = client.get("/items/2")
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == 2
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]


@allure.title("Update an existing item via PUT request")
@allure.description("This test checks that updating an existing item modifies its data.")
def test_update_item() -> None:
    """Ensure that the PUT endpoint updates an existing item."""
    # Create the item first
    original = {"name": "Thing", "description": "Original description"}
    client.post("/items/3", json=original)
    # Update the item
    updated = {"name": "Thing", "description": "Updated description"}
    response = client.put("/items/3", json=updated)
    assert response.status_code == 200
    assert response.json() == {"item_id": 3, **updated}


@allure.title("Handle missing item on GET request")
@allure.description("This test ensures the API returns a 404 status code when trying to "
                    "retrieve a non-existent item.")
def test_read_item_not_found() -> None:
    """Verify that requesting a non-existent item yields a 404 response."""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
