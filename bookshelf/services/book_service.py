from decimal import Decimal
from ..errors import BusinessRuleError, ConflictError, NotFoundError

from ..extensions import db
from ..models import Book
from sqlalchemy.orm import Session
from ..repositories.author_repository import AuthorRepository
from ..repositories.book_repository import BookRepository

class BookService:

    def __init__(
        self,
        session: Session | None = None,
        booksRepository: BookRepository | None = None,
        authorsRepository: AuthorRepository | None = None
    ) -> None:
        self.session = session or db.session
        self.booksRepository = booksRepository or BookRepository(self.session)
        self.authorsRepository = authorsRepository or AuthorRepository(self.session)


    def get(self, book_id: int) -> Book:
        book = self.booksRepository.get(book_id)
        if book is None: 
            raise NotFoundError(f"Book {book_id} not found")

        return book

    def list_page(self, page: int, size: int) -> tuple[list[Book], int]:
        books = self.booksRepository.find_all(offset=(page - 1), limit = size)
        return books, self.booksRepository.count()

    def create(self, *, title: str, isbn: str, price: Decimal, author_id: int, published_year: int | None = None):
        if self.authorsRepository.get(author_id) is None:
            raise NotFoundError(f"Author {author_id} not found")

        if self.booksRepository.get_by_isbn(isbn):
            raise ConflictError(f"ISBN {isbn} is already registered")

        book = self.booksRepository.add(
            Book(title = title, isbn = isbn, price = price, author_id = author_id, published_year = published_year)
        )

        self.session.commit()
        return book

    def delete(self, book_id: int):
        self.booksRepository.delete(self.get(book_id))
        self.session.commit()

    def update(self, book_id: int, **changes) -> Book:
        book = self.get(book_id)
        if book is None:
            raise NotFoundError(f"Book {book_id} not found")
        new_isbn = changes.get("isbn")

        if new_isbn and new_isbn != book.isbn and self.booksRepository.get_by_isbn(new_isbn):
            raise ConflictError(f"ISBN {new_isbn} already registered")

        new_author = changes.get("author_id")
        if new_author and self.authorsRepository.get(new_author) is None:
            raise NotFoundError(f"Author {new_author} not found")
        
        for field, value in changes.items():
            setattr(book, field, value)

        self.session.commit()
        return book

    def apply_discount(self, book_id: int, percentage: int) -> Book:
        book = self.get(book_id)
        try:
            book.apply_discount(percentage)
        except ValueError as exc:
            raise BusinessRuleError(str(exc)) from exc

        self.session.commit()
        return book

    def query_by_price_range(self, min_range: Decimal, max_range: Decimal):
        return self.booksRepository.query_by_price_range(min_range, max_range)