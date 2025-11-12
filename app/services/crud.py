from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Type, TypeVar
from pydantic import BaseModel


class CRUD():
    ModelType = TypeVar("ModelType")
    SchemaType = TypeVar("SchemaType", bound=BaseModel)

    @classmethod
    async def add(self, model: Type[ModelType], data: Type[SchemaType], db: AsyncSession):
        params = data.model_dump(exclude_unset=True)
        stmt = insert(model).values(**params)
        result = await db.execute(stmt)
        await db.commit()
        new_id = result.inserted_primary_key[0]
        return new_id

    @classmethod
    async def get(self, model: Type[ModelType], db: AsyncSession, filters: dict = None, order_by=None):
        stmt = select(model)
        if filters:
            stmt = stmt.where(*(getattr(model, key) == value for key, value in filters.items()))  
        if order_by:
            stmt = stmt.order_by(order_by)  
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def read(self, model: Type[ModelType], entry_id: int, db: AsyncSession):
        query = select(model).where(model.id == entry_id)
        result = await db.execute(query)
        entry = result.scalars().first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry

    @classmethod
    async def update(self, model: Type[ModelType], entry_id: int, data: Type[SchemaType], db: AsyncSession):
        params = data.model_dump(exclude_unset=True)
        query = select(model).where(model.id == entry_id)
        result = await db.execute(query)
        entry = result.scalars().first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")

        for key, value in params.items():
            if key != "id" and hasattr(entry, key):
                setattr(entry, key, value)

        await db.commit()
        return True
    
    @classmethod
    async def delete(self, model: Type[ModelType], entry_id: int, db: AsyncSession):
        query = select(model).where(model.id == entry_id)
        result = await db.execute(query)
        entry = result.scalars().first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")

        await db.delete(entry)
        await db.commit()
        return True
