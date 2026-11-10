from ..errors import ConflictError, NotFoundError
from ..core.database import AsyncSession
from ..models import Author
from ..repositories.author_repository import AuthorRepository
from sqlalchemy.orm import Session

class AuthorService: 
    def __init__(
        self,
        session: AsyncSession,
        authorRepository: AuthorRepository
    ) -> None:
        self.session = session
        self.authorRepository = authorRepository

    async def get(self, author_id: int, include_books: bool) -> Author | None:
        author = (await self.authorRepository.get_with_books(author_id) if include_books 
                  else await self.authorRepository.get(author_id))

        if author is None:
            raise NotFoundError(f"Author {author_id} not found")
        return author

    async def create(self, *, name: str, email: str) -> Author:
        if await self.authorRepository.get_by_email(email):
            raise ConflictError(f"Email {email} already registered")

        author = await self.authorRepository.add(Author(email = email, name = name))
        self.session.commit()
        return author

    async def delete(self, author_id: int):
        await self.authorRepository.delete(author_id)
        self.session.commit()
        