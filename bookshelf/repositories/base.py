from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..extensions import db

class BaseRepository[T]: 
    model: type[T]

    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session or db.session

    async def get(self, entity_id: int) -> T | None:
        return await self.session.get(self.model, entity_id)

    async def find_all(self, *, offset: int = 0, limit: int = 20):
        stmt = select(self.model).order_by(self.model.id).offset(offset).limit(limit)
        return list(await self.session.scalars(stmt))

    async def add(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, entity) -> None:
        await self.session.delete(entity)