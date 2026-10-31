from ..errors import ConflictError, NotFoundError
from ..models import Author
from ..repositories.author_repository import AuthorRepository
from sqlalchemy.orm import Session

class AuthorService: 
    def __init__(
        self,
        session: Session,
        authorRepository: AuthorRepository | None
    ) -> None:
        self.session = session
        self.authorRepository = authorRepository

    def get(self, author_id: int, include_books: bool) -> Author | None:
        author = (self.authorRepository.get_with_books(author_id) if include_books 
                  else self.authorRepository.get(author_id))

        if author is None:
            raise NotFoundError(f"Author {author_id} not found")
        return author

    def create(self, *, name: str, email: str) -> Author:
        if self.authorRepository.get_by_email(email):
            raise ConflictError(f"Email {email} already registered")

        author = self.authorRepository.add(Author(email = email, name = name))
        self.session.commit()
        return author

    def delete(self, author_id: int):
        self.authorRepository.delete(author_id)
        self.session.commit()
        