from fastapi import FastAPI, HTTPException
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()  # Instantiate the FastAPI application

# Add CORS middleware this list all the origins,methods,headers,use "*" for all methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

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
    item = next((item for item in item_db if item["item_id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is CoutureLane"})
    return item


#create new item
@app.post("/items")
async def create_item(item: Item):
    new_id = max(item["item_id"] for item in item_db) + 1 if item_db else 1
    new_item = item.dict()
    new_item["item_id"] = new_id
    item_db.append(new_item)
    return {"item": new_item}


#update a new item
@app.put("/items/{item_id}")
async def update_item(item_id: int, updated_item : Item):
    item = next((item for item in item_db if item["item_id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.update(updated_item.dict())
    return {"item": item}

# List all users
@app.get("/users")
async def list_users():
    return user_db

# Get the current user
@app.get("/users/me")
async def get_current_user():
    return {"message": "This is the current user"}

# Get a specific user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = next((user for user in user_db if user["item_id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#search users by email
@app.get("/users/search")
async def search_users(email: Optional[str] = None):
    if email:
        matched_users = [user for user in user_db if email in user["email"]]
        if not matched_users:
            raise HTTPException(status_code=404, detail="no user found  with this emaail")
        return matched_users
    return {"message": "no email query provided"}
    