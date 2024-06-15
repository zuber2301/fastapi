from fastapi import FastAPI, HTTPException
from models import Item
import crud
from db import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.Connect

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = await crud.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
