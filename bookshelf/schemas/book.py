from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

def normalize_isbn(value: str) -> str:
    cleaned = value.replace("-", "")
    if len(cleaned) != 13 or not cleaned.isdigit():
        raise ValueError("ISBN Must Contain Exaclty 13 digits")

    return cleaned

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    isbn: str

    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    author_id: int = Field(gt=0)

    published_year: int | None = Field(default=None, ge=1450, le=2200)

    @field_validator("isbn")
    @classmethod
    def _isbn(cls, v: str) -> str:
        return normalize_isbn(v)

class BookUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    isbn: str
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    published_year: int | None = Field(default=None, ge=1450, le=2200)

    @field_validator("isbn")
    @classmethod
    def _isbn(cls, v: str | None):
        return normalize_isbn(v) if v is not None else v

class DiscountIn(BaseModel):
    percent: int = Field(ge=1, le=50)

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # read from ORM object attributes

    id: int
    title: str
    isbn: str
    price: Decimal
    published_year: int | None
    author_id: int