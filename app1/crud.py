from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app1 import models, schemas

async def get_item(db: Session, item_id: int):
    return await db.get(models.Item, item_id)

async def get_item(db: Session, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Item).offset(skip).limit(limit))
    return result.scalars().all()

async def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = await db.get(models.Item, item_id)
    if not db_item:
        return None
    for key, value in item.dict().items():
        setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)
        return db_item()

