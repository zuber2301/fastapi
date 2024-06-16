## Create the FastAPI app1lication and include routes

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app1 import crud, models, schemas
from app1.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app1 = FastAPI()

@app1.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return await crud.create_item(db=db, item=item)

@app1.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app1.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app1.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = await crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app1.delete("/items/{item_id}", response_model=bool)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = await crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return success

