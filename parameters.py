from fastapi import FastAPI, HTTPException
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI()  # Instantiate the FastAPI application

#fake database

item_db = [
    {"item_id": 1001, "item_name": "Shirt", "price": 600, "stock": 2000},
    {"item_id": 1002, "item_name": "Jeans", "price": 1200, "stock": 500},
    {"item_id": 1003, "item_name": "Shorts", "price": 300, "stock": 300},
    {"item_id": 1004, "item_name": "Tshirts", "price": 500, "stock":200},
]

user_db = [
    {"item_id": "1001", "name": "rahul", "email": "rahul@gmail.com"},
    {"item_id": "1002", "name": "chandan", "email": "chandan@gmail.com"},
    {"item_id": "1003", "name": "nitin", "email": "nitin@gmail.com"},
    {"item_id": "1004", "name": "manoj", "email": "manoj@gmail.com"},
]

# Define a model for request body validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to CoutureLane"}

# POST route
@app.post("/")
async def post():
    return {"message": "old money"}

# PUT route
@app.put("/")
async def put():
    return {"message": "hey we are here"}

# List all items
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return item_db[skip: skip + limit]

# Get a specific item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is CoutureLane"})
    return item

# List all users
@app.get("/users")
async def list_users():
    return {"message": "list users"}

# Get the current user
@app.get("/users/me")
async def get_current_user():
    return {"message": "This is the current user"}

# Get a specific user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}

# Enum for food categories
class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

# Get a specific food category
@app.get("/foods/{food_name}")
async def get_food_name(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you're healthy"}
    if food_name == FoodEnum.fruits:
        return {"food_name": food_name, "message": "good to eat fruits"}
    return {"food_name": food_name, "message": "I like dairy"}
