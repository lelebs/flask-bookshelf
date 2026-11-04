from pydantic import BaseModel, ConfigDict, Field
from .book import BookOut

class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=255)

class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str

class AuthorDetailOut(AuthorOut):          # inheritance between DTOs
    books: list[BookOut] = []
    