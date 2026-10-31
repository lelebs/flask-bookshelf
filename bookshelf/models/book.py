from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from .base import TimestampMixin
from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .author import Author

class Book(TimestampMixin, db.Model): 
    __table_name__= "books"
    __table_args__ = (CheckConstraint("price >= 0", name="ck_books_price_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    isbn: Mapped[str] = mapped_column(String(13), unique=True, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    published_year: Mapped[int | None]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), index=True)
    genre: Mapped[str] = mapped_column(String(50))

    author: Mapped[Author] = relationship(back_populates="books")

    def apply_discount(self, percentage: int) -> None:
        if not 0 < percentage <=50:
            raise ValueError("Discount must be between 1 and 50 percentage")
        self.price = (self.price * (100 - percentage) / 100).quantize(Decimal("0.01"))
