from .base import BaseRepository
from ..models import Author
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class AuthorRepository(BaseRepository[Author]):
    model = Author

    def get_by_email(self, email: str) -> Author | None:
        return self.session.scalar(select(Author).where(Author.email == email).order_by(Author.name))

    def get_with_books(self, author_id) -> Author | None:
        stmt = select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
        return self.session.scalar(stmt)