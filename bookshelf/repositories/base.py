from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..extensions import db

class BaseRepository[T]: 
    model: type[T]

    def __int__(self, session: Session | None = None) -> None:
        self.session = session or db.session

    def get(self, entity_id: int) -> T | None:
        return self.session.get(self.model, entity_id)

    def find_all(self, *, offset: int = 0, limit: int = 20):
        stmt = select(self.model).order_by(self.model.id).offset(offset).limit(limit)
        return list(self.session.scalars(stmt))

    def count(self) -> int:
        return self.session.scalar(select(func.count()).select_from(self.model))

    def add(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        return entity

    def delete(self, entity) -> None:
        self.session.delete(entity)