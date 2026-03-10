from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import models, schemas, crud, database

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Инициализация базы данных...")
    await database.create_db_and_tables()
    yield
    print("Приложение остановлено.")

app = FastAPI(
    title="URL Shortener API",
    lifespan=lifespan
)

@app.post("/shorten", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(url_in: schemas.URLCreate, db: AsyncSession = Depends(database.get_db)):
    """Принимает длинную ссылку и возвращает короткий ID"""
    # Добавляем await для асинхронного CRUD
    return await crud.create_url(db, url=str(url_in.url))


@app.get("/{short_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_original(short_id: str, db: AsyncSession = Depends(database.get_db)):
    """Редирект на оригинальную ссылку с обновлением счетчика"""
    db_url = await crud.get_url_by_short_id(db, short_id)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ссылка не найдена"
        )
    
    await crud.update_clicks(db, db_url)
    return RedirectResponse(url=db_url.original_url)


@app.get("/stats/{short_id}", response_model=schemas.URLStats)
async def get_url_stats(short_id: str, db: AsyncSession = Depends(database.get_db)):
    """Возвращает статистику по ссылке"""
    db_url = await crud.get_url_by_short_id(db, short_id)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ссылка не найдена"
        )
    return db_url

@app.get("/", tags=["Root"])
async def root():
    """Корневой эндпоинт."""
    return {"message": "Это проект URL Shortener API. Документация доступна по адресу /docs"}