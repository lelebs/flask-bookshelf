from sqlalchemy import select

from .base import BaseRepository
from ..models import Book

class BookRepository(BaseRepository[Book]):
    model = Book

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.session.scalar(select(Book).where(Book.isbn == isbn))

    def find_by_author(self, author_id: int) -> list[Book]:
        stmt = select(Book).where(Book.author_id == author_id).order_by(Book.title)
        return self.session.scalars(stmt)