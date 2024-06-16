from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app2 import models, schemas


async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    return result.scalars().first()

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Item).offset(skip).limit(limit))
    return result.scalars().all()

async def create_item(db: AsyncSession, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_item(db: AsyncSession, item_id: int):
    item = await get_item(db, item_id)
    if item:
        await db.delete(item)
        await db.commit()
        return True
    return False

async def update_item(db: AsyncSession, item_id: int, item: schemas.ItemCreate):
    db_item = await get_item(db, item_id)
    if db_item:
        for key, value in item.model_dump().items():
            setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)
        return db_item
    return None
