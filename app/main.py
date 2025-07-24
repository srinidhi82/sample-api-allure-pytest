"""Sample FastAPI application exposing CRUD endpoints.

This module defines a simple FastAPI application with a few endpoints for
demonstration purposes. It stores items in an in‑memory dictionary so you
don't need any external database to get started. There are three HTTP
methods supported for the `/items/{item_id}` endpoint:

* **POST** – create a new item with the provided identifier and payload.
* **GET** – retrieve an existing item by its identifier.
* **PUT** – update an existing item with new data.

The API can be run using the ASGI server `uvicorn`. See the project README
for detailed instructions on how to start the server.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Instantiate the FastAPI application. When you run uvicorn and specify
# `main:app`, this object will be imported as the application to serve.
app = FastAPI(title="Sample API", version="1.0.0")


class Item(BaseModel):
    """Pydantic model defining the schema for items handled by the API."""

    name: str
    description: str | None = None


# In‑memory store for items. Keys are integers representing the item ID and
# values are dictionaries holding the item data. This is purely for
# demonstration; in a real application you'd likely interact with a
# persistent database.
items: dict[int, dict[str, str | None]] = {}


@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item) -> dict[str, str | None]:
    """Create a new item or overwrite an existing one.

    Args:
        item_id: Numeric identifier for the item.
        item: The payload containing item fields (`name` and optional `description`).

    Returns:
        A dictionary combining the `item_id` with the provided item data.
    """
    # Store the item data in the in‑memory dictionary. If an item with the
    # given ID already exists it will be overwritten.
    items[item_id] = item.dict()
    return {"item_id": item_id, **items[item_id]}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> dict[str, str | None]:
    """Retrieve an item by its identifier.

    If the requested item is not found an HTTP 404 error is raised.

    Args:
        item_id: Numeric identifier for the item to retrieve.

    Returns:
        A dictionary containing the `item_id` and the stored item data.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, **items[item_id]}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item) -> dict[str, str | None]:
    """Update an existing item.

    Args:
        item_id: Numeric identifier for the item.
        item: The payload containing updated item data.

    Returns:
        A dictionary containing the `item_id` and the new item data.

    Raises:
        HTTPException: If the item does not exist.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item.dict()
    return {"item_id": item_id, **items[item_id]}
