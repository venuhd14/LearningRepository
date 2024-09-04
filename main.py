from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Define a Pydantic model for request bodies
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Endpoint to retrieve an item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Endpoint to create a new item
@app.post("/items/")
def create_item(item: Item):
    return {"item": item}

# Endpoint to update an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item}

# Endpoint to delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item with id {item_id} has been deleted"}

# Endpoint to trigger an error
@app.get("/error")
def error_example():
    raise HTTPException(status_code=404, detail="Item not found")
