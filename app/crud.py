from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, utils

async def get_url_by_short_id(db: AsyncSession, short_id: str):
    result = await db.execute(select(models.URL).where(models.URL.short_id == short_id))
    return result.scalars().first()

async def create_url(db: AsyncSession, url: str):
    short_id = None
    for _ in range(5):  # 5 попыток на случай коллизии
        temp_id = utils.create_random_code()
        existing = await get_url_by_short_id(db, temp_id)
        if not existing:
            short_id = temp_id
            break
    
    if not short_id:
        short_id = utils.create_random_code()

    new_url = models.URL(original_url=url, short_id=short_id)
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)
    return new_url

async def update_clicks(db: AsyncSession, db_url: models.URL):
    db_url.clicks += 1
    await db.commit()
    await db.refresh(db_url)
    return db_url