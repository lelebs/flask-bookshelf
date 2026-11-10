from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_session
from ..services.author_service import AuthorService
from ..services.book_service import BookService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_book_service(session: SessionDep):
    return BookService(session)

def get_author_service(session: SessionDep):
    return AuthorService(session)

BookServiceDep = Annotated[BookService, Depends(get_book_service)]
AuthorServiceDep = Annotated[AuthorService, Depends(get_author_service)]
