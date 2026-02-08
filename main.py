from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str
    origin: str

teas: List[Tea] = []

@app.get("/")
def home_Page():
    return {"message": "Welcome to the home page"}

@app.get("/get_all_item")
def get_all_item():
    return teas

@app.post("/add_items")
def add_tea(tea:Tea):
    teas.append(tea)
    return tea

@app.delete("/remove_item{item_id}")
def delete_item(item_id:int):
    for index, value in enumerate(teas):
        if item_id == value.id:
            deleted = teas.pop(index)
            return deleted
    return {"message": "unable to find the item"}

@app.put("/update_item")
def update_item(item_id:int,item:Tea):
    for index, value in enumerate(teas):
        if item_id == value.id:
            teas[index] = item
    return item

    
