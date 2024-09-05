from fastapi import FastAPI
from enum import Enum
from typing import Optional
app = FastAPI() #instantiate app

#setup route

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/")
async def post():
    return {"message": "hello from the post route"}

@app.put("/")
async def put():
    return{"message":"hey from put route uWu"}

@app.get("/items")
async def list_items():
    return{"message":"list items"}

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    return{"item_id":item_id}
@app.get("/users")
async def list_users():
    return{"message":"list users"}

@app.get("/users/me")
async def get_current_user():
    return{"message":"This is the current user"}

@app.get("/users/{user_id}")
async def get_item(user_id:str):
    return{"user_id":user_id}

class FoodEnum(str, Enum):
    fruits= "fruits"
    vegetables="vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food_name(food_name:FoodEnum):
    if food_name == FoodEnum.vegetables:
        return{"food_name":food_name, "message":"you're healthy"}
    if food_name == FoodEnum.fruits:
        return{"food_name":food_name, "message":"good to eat fruits"}
    return{"food_name":food_name, "message":"I like dairy"}
#query parameters

fake_items_db = [{"item_name":"Shirt"},{"item_name":"Sweatpants"},{"item_name":"Shoes"}]

@app.get("/items")
async def list_items(skip: int= 0,limit:int = 10):
    return fake_items_db[skip: skip+limit]
#make parameters optional

@app.get("/items/{item_id}")
async def get_item(item_id:str,q:Optional[str]= None, short: bool = False):
    item = {"item_id":item_id}
    if q:
        # return {"item_id":item_id,"q":q}
        return item.update({"q":q})
    if not short:
        item.update({"description":"This is the description"})
    return {"item_id":item_id}
