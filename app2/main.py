from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from contextlib import asynccontextmanager
from fastapi import crud, models, schemas, database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    
    yield  # Run the application

    # Code to run on shutdown
    await database.engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/items/", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: AsyncSession = Depends(database.get_db)):
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_item(db=db, item=item)

@app.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(database.get_db)):
    updated_item = await crud.update_item(db=db, item_id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}", response_model=schemas.Item)
async def delete_item(item_id: int, db: AsyncSession = Depends(database.get_db)):
    success = await crud.delete_item(db=db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": success}
