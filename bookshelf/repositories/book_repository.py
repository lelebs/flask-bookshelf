from decimal import Decimal

from sqlalchemy import select

from .base import BaseRepository
from ..models import Book

class BookRepository(BaseRepository[Book]):
    model = Book

    async def get_by_isbn(self, isbn: str) -> Book | None:
        return await self.session.scalar(select(Book).where(Book.isbn == isbn))

    async def find_by_author(self, author_id: int) -> list[Book]:
        stmt = select(Book).where(Book.author_id == author_id).order_by(Book.title)
        return await self.session.scalars(stmt)

    async def query_by_price_range(self, min_range: Decimal, max_range: Decimal):
        stmt = select(Book).order_by(Book.price)
        if min_range: 
            stmt = stmt.where(Book.price > min_range)

        if max_range: 
            stmt = stmt.where(Book.price < max_range)

        return await self.session.scalars(stmt)